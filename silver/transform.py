"""Silver: Bronze tipada + joins fato×meta + gate join_match (Passo 5).

Uso:
  python silver/transform.py
  python silver/transform.py --run_id 20d3623d0430
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.telemetry import finish_run
from quality.config import JOIN_MATCH_THRESHOLD, SILVER_DATASET, SILVER_TABLES
from quality.ops import append_check, ensure_quality_table, load_env_and_client
from quality.rules_bronze import latest_run_id
from quality.rules_silver import measure_join_match, run_desconhecido_counts

OUT = ROOT / "evidence" / "passo_05"
SQL_FILE = ROOT / "sql" / "02_silver.sql"
RUN_ID_RE = re.compile(r"^[0-9a-fA-F]{8,32}$")


def split_statements(sql_text: str) -> list[str]:
    lines = []
    for line in sql_text.splitlines():
        if line.strip().startswith("--"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    return [p.strip() for p in cleaned.split(";") if p.strip()]


def ensure_silver_dataset(bq: bigquery.Client, project_id: str) -> None:
    dataset_ref = bigquery.Dataset(f"{project_id}.{SILVER_DATASET}")
    dataset_ref.location = "US"
    try:
        bq.get_dataset(dataset_ref)
        print(f"[OK] dataset {SILVER_DATASET} ja existe")
    except NotFound:
        bq.create_dataset(dataset_ref, exists_ok=True)
        print(f"[OK] dataset {SILVER_DATASET} criado (US)")


def run_sql_file(
    bq: bigquery.Client,
    project_id: str,
    run_id: str,
) -> list[dict]:
    raw = SQL_FILE.read_text(encoding="utf-8")
    sql = raw.replace("{{project_id}}", project_id).replace("{{run_id}}", run_id)
    statements = split_statements(sql)
    jobs: list[dict] = []
    for i, stmt in enumerate(statements, start=1):
        label = stmt.splitlines()[0][:80] if stmt else f"stmt_{i}"
        print(f"  [{i}/{len(statements)}] {label}...")
        job = bq.query(stmt)
        job.result()
        jobs.append(
            {
                "step": i,
                "job_id": job.job_id,
                "bytes_processed": getattr(job, "total_bytes_processed", None),
            }
        )
        print(f"       job_id={job.job_id}")
    return jobs


def count_rows(bq: bigquery.Client, project_id: str, table: str) -> int:
    sql = f"SELECT COUNT(*) AS n FROM `{project_id}.{SILVER_DATASET}.{table}`"
    return int(next(bq.query(sql).result())["n"])


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def update_readme(
    run_id: str,
    manifest: list[dict],
    matches: list[dict],
    blocking_fails: int,
    job_ids: list[str],
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Passo 5 — Silver (limpar, tipar, juntar)",
        "",
        f"- comando: `python silver/transform.py --run_id {run_id}`",
        f"- run_id_bronze: `{run_id}`",
        f"- dataset: `{SILVER_DATASET}`",
        f"- limiar join_match (blocking): **{JOIN_MATCH_THRESHOLD}**",
        f"- blocking fails: **{blocking_fails}**",
        f"- exit esperado: `0` se blocking fails = 0",
        f"- job_ids (amostra): `{', '.join(job_ids[:3])}{'...' if len(job_ids) > 3 else ''}`",
        "",
        "## Contagens",
        "",
        "| table | rows |",
        "|-------|------|",
    ]
    for r in manifest:
        lines.append(f"| {r['table']} | {r['rows']} |")
    lines.extend(
        [
            "",
            "## join_match",
            "",
            "| entity | taxa_match | threshold | status | linhas_esquerda | linhas_com_par |",
            "|--------|------------|-----------|--------|-----------------|----------------|",
        ]
    )
    for m in matches:
        lines.append(
            f"| {m['entity']} | {m['value']} | {m['threshold']} | {m['status']} | "
            f"{m.get('linhas_esquerda', '')} | {m.get('linhas_com_par', '')} |"
        )
    lines.extend(["", "Snapshots: `manifest_*.csv`, `join_match_*.csv`.", ""])
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Transformacao Silver (Passo 5)")
    parser.add_argument(
        "--run_id",
        default=None,
        help="run_id Bronze (default: ultima por MAX(ingestion_ts))",
    )
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    project_id, bq = load_env_and_client(ROOT)
    ensure_quality_table(bq, project_id)
    ensure_silver_dataset(bq, project_id)

    run_id = args.run_id or latest_run_id(bq, project_id)
    if not RUN_ID_RE.fullmatch(run_id):
        raise SystemExit(f"[ERRO] run_id invalido: {run_id!r}")

    print("=" * 60)
    print(f"SILVER transform | project={project_id} run_id={run_id}")
    print("=" * 60)

    status = "success"
    detail = ""
    rows_out = 0
    bytes_processed = 0
    exit_code = 0

    try:
        if not SQL_FILE.exists():
            raise SystemExit(f"[ERRO] SQL nao encontrado: {SQL_FILE}")

        jobs = run_sql_file(bq, project_id, run_id)
        bytes_processed = sum(int(j["bytes_processed"] or 0) for j in jobs)

        manifest = []
        for table in SILVER_TABLES:
            n = count_rows(bq, project_id, table)
            manifest.append({"table": table, "rows": n, "run_id_bronze": run_id})
            print(f"  rows {table}: {n}")
        rows_out = sum(int(m["rows"]) for m in manifest)

        print("join_match + quality_checks...")
        match_rows: list[dict] = []
        blocking_fails = 0
        for entity in ("municipio_com_meta", "uf_com_meta", "brasil_com_meta"):
            r = measure_join_match(bq, project_id, entity)
            check_status = "fail" if r.value < JOIN_MATCH_THRESHOLD else "pass"
            if r.rule_class == "blocking" and check_status == "fail":
                blocking_fails += 1
            row = append_check(
                bq,
                project_id,
                run_id=run_id,
                layer="silver",
                entity=r.entity,
                rule=r.rule,
                rule_class=r.rule_class,
                status=check_status,
                value=r.value,
                threshold=JOIN_MATCH_THRESHOLD,
                detail=r.detail,
            )
            match_rows.append(
                {
                    **row,
                    "linhas_esquerda": r.linhas_esquerda,
                    "linhas_com_par": r.linhas_com_par,
                }
            )
            flag = "FAIL" if check_status == "fail" else "OK"
            print(
                f"  [{flag}] {entity}.join_match value={r.value:.6f} "
                f"threshold={JOIN_MATCH_THRESHOLD}"
            )

        for r in run_desconhecido_counts(bq, project_id):
            append_check(
                bq,
                project_id,
                run_id=run_id,
                layer="silver",
                entity=r.entity,
                rule=r.rule,
                rule_class=r.rule_class,
                status=r.status,
                value=r.value,
                threshold=r.threshold,
                detail=r.detail,
            )
            print(
                f"  [info] {r.entity}.{r.rule} value={r.value} status={r.status}"
            )

        write_csv(manifest, OUT / f"manifest_{run_id}.csv")
        write_csv(manifest, OUT / "manifest_latest.csv")
        write_csv(match_rows, OUT / f"join_match_{run_id}.csv")
        write_csv(match_rows, OUT / "join_match_latest.csv")
        update_readme(
            run_id,
            manifest,
            match_rows,
            blocking_fails,
            [j["job_id"] for j in jobs],
        )

        print("=" * 60)
        print(f"evidencia: evidence/passo_05/ (run_id={run_id})")
        if blocking_fails:
            status = "failed"
            detail = f"{blocking_fails} join_match bloqueante(s)"
            exit_code = 1
            print(f"[ERRO] {detail} — Silver nao publicavel")
        else:
            print("[OK] Silver OK (exit 0)")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        if code not in (0, None):
            status = "failed"
            detail = detail or str(exc)
            exit_code = code if isinstance(code, int) else 1
        raise
    except Exception as exc:  # noqa: BLE001
        status = "failed"
        detail = str(exc)
        exit_code = 1
        print(f"[ERRO] {exc}")
    finally:
        finish_run(
            bq,
            project_id,
            run_id=run_id,
            etapa="silver",
            started_at=started_at,
            status=status,
            rows_in=rows_out,
            rows_out=rows_out,
            bytes_processed=bytes_processed,
            detail=detail,
        )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
