"""Gold: produtos analiticos a partir da Silver (Passo 6).

Uso:
  python gold/build.py
  python gold/build.py --run_id 20d3623d0430
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.telemetry import finish_run
from quality.config import GOLD_DATASET, GOLD_TABLES, JOIN_MATCH_ENTITIES, JOIN_MATCH_THRESHOLD
from quality.ops import load_env_and_client
from quality.rules_silver import latest_silver_run_id, measure_join_match

OUT = ROOT / "evidence" / "passo_06"
SQL_FILE = ROOT / "sql" / "03_gold.sql"
RUN_ID_RE = re.compile(r"^[0-9a-fA-F]{8,32}$")

# Conferencia com numeros oficiais do perfil (passo 2).
CONF_CE_TAXA = 85.31
CONF_CE_TOL = 0.05
CONF_BR_TAXA = 59.2
CONF_BR_META = 80.0
CONF_BR_TOL = 0.05


def split_statements(sql_text: str) -> list[str]:
    lines = []
    for line in sql_text.splitlines():
        if line.strip().startswith("--"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    return [p.strip() for p in cleaned.split(";") if p.strip()]


def ensure_gold_dataset(bq: bigquery.Client, project_id: str) -> None:
    dataset_ref = bigquery.Dataset(f"{project_id}.{GOLD_DATASET}")
    dataset_ref.location = "US"
    try:
        bq.get_dataset(dataset_ref)
        print(f"[OK] dataset {GOLD_DATASET} ja existe")
    except NotFound:
        bq.create_dataset(dataset_ref, exists_ok=True)
        print(f"[OK] dataset {GOLD_DATASET} criado (US)")


def gate_silver_join_match(
    bq: bigquery.Client,
    project_id: str,
) -> list[dict]:
    """Re-mede join_match Silver; bloqueia Gold se algum falhar."""
    rows: list[dict] = []
    fails = 0
    for entity in JOIN_MATCH_ENTITIES:
        r = measure_join_match(bq, project_id, entity)
        status = "fail" if r.value < JOIN_MATCH_THRESHOLD else "pass"
        if status == "fail":
            fails += 1
        rows.append(
            {
                "entity": entity,
                "rule": "join_match",
                "status": status,
                "value": r.value,
                "threshold": JOIN_MATCH_THRESHOLD,
                "linhas_esquerda": r.linhas_esquerda,
                "linhas_com_par": r.linhas_com_par,
            }
        )
        flag = "FAIL" if status == "fail" else "OK"
        print(
            f"  [{flag}] silver.{entity}.join_match "
            f"value={r.value:.6f} threshold={JOIN_MATCH_THRESHOLD}"
        )
    if fails:
        raise SystemExit(
            f"[ERRO] {fails} join_match Silver bloqueante(s) — Gold nao publicada"
        )
    return rows


def dry_run_statement(
    bq: bigquery.Client,
    stmt: str,
    step: int,
) -> dict:
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = bq.query(stmt, job_config=job_config)
    bytes_proc = int(job.total_bytes_processed or 0)
    label = stmt.splitlines()[0][:80] if stmt else f"stmt_{step}"
    print(f"  [dry_run {step}] bytes={bytes_proc} | {label}")
    return {
        "step": step,
        "label": label,
        "total_bytes_processed": bytes_proc,
        "dry_run": True,
    }


def run_sql_file(
    bq: bigquery.Client,
    project_id: str,
    run_id: str,
) -> tuple[list[dict], list[dict]]:
    raw = SQL_FILE.read_text(encoding="utf-8")
    sql = raw.replace("{{project_id}}", project_id).replace("{{run_id}}", run_id)
    statements = split_statements(sql)
    dry_rows: list[dict] = []
    jobs: list[dict] = []
    for i, stmt in enumerate(statements, start=1):
        dry_rows.append(dry_run_statement(bq, stmt, i))
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
    return jobs, dry_rows


def export_table_parquet(
    bq: bigquery.Client,
    project_id: str,
    bucket_name: str,
    table: str,
    run_id: str,
    ingestion_date: str,
) -> dict:
    uri_prefix = (
        f"gs://{bucket_name}/gold/{table}/"
        f"ingestion_date={ingestion_date}/run_id={run_id}"
    )
    sql = f"""
EXPORT DATA OPTIONS (
  uri='{uri_prefix}/part-*.parquet',
  format='PARQUET',
  overwrite=true
) AS
SELECT *
FROM `{project_id}.{GOLD_DATASET}.{table}`
"""
    print(f"  export {table} -> {uri_prefix}/")
    job = bq.query(sql)
    job.result()
    return {
        "table": table,
        "uri_prefix": uri_prefix,
        "job_id": job.job_id,
        "bytes_processed": getattr(job, "total_bytes_processed", None),
    }


def count_rows(bq: bigquery.Client, project_id: str, table: str) -> int:
    sql = f"SELECT COUNT(*) AS n FROM `{project_id}.{GOLD_DATASET}.{table}`"
    return int(next(bq.query(sql).result())["n"])


def run_conferencia(bq: bigquery.Client, project_id: str) -> list[dict]:
    """SELECT de conferencia vs numeros oficiais do perfil (passo 2)."""
    rows: list[dict] = []

    sql_ce = f"""
    SELECT sigla_uf, ano, rede, taxa_alfabetizacao
    FROM `{project_id}.{GOLD_DATASET}.indicador_uf`
    WHERE sigla_uf = 'CE' AND ano = 2024 AND rede = '5'
    """
    ce = list(bq.query(sql_ce).result())
    if not ce:
        rows.append(
            {
                "check": "CE_2024_rede5",
                "status": "fail",
                "expected": CONF_CE_TAXA,
                "observed": None,
                "detail": "linha nao encontrada",
            }
        )
    else:
        obs = float(ce[0]["taxa_alfabetizacao"])
        ok = abs(obs - CONF_CE_TAXA) <= CONF_CE_TOL
        rows.append(
            {
                "check": "CE_2024_rede5",
                "status": "pass" if ok else "fail",
                "expected": CONF_CE_TAXA,
                "observed": obs,
                "detail": f"tol={CONF_CE_TOL}",
            }
        )

    sql_br = f"""
    SELECT ano, rede, taxa_alfabetizacao, meta_alfabetizacao_2030, status_meta
    FROM `{project_id}.{GOLD_DATASET}.meta_vs_resultado`
    WHERE nivel_geo = 'brasil' AND ano = 2024
    """
    br = list(bq.query(sql_br).result())
    if not br:
        rows.append(
            {
                "check": "brasil_2024_meta",
                "status": "fail",
                "expected": CONF_BR_TAXA,
                "observed": None,
                "detail": "linha nao encontrada",
            }
        )
    else:
        obs_taxa = float(br[0]["taxa_alfabetizacao"])
        obs_meta = float(br[0]["meta_alfabetizacao_2030"])
        ok = (
            abs(obs_taxa - CONF_BR_TAXA) <= CONF_BR_TOL
            and abs(obs_meta - CONF_BR_META) <= CONF_BR_TOL
        )
        rows.append(
            {
                "check": "brasil_2024_meta",
                "status": "pass" if ok else "fail",
                "expected": CONF_BR_TAXA,
                "observed": obs_taxa,
                "detail": (
                    f"meta_obs={obs_meta} meta_exp={CONF_BR_META} "
                    f"status={br[0]['status_meta']}"
                ),
            }
        )

    for r in rows:
        flag = "OK" if r["status"] == "pass" else "FAIL"
        print(
            f"  [{flag}] {r['check']} expected={r['expected']} "
            f"observed={r['observed']} {r['detail']}"
        )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def update_readme(
    run_id: str,
    bucket_name: str,
    manifest: list[dict],
    dry_rows: list[dict],
    conf_rows: list[dict],
    export_rows: list[dict],
    job_ids: list[str],
    gate_ok: bool,
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    blocking = sum(1 for r in conf_rows if r["status"] == "fail")
    lines = [
        "# Passo 6 — Gold (produto analitico)",
        "",
        f"- comando: `python gold/build.py --run_id {run_id}`",
        f"- run_id_bronze: `{run_id}`",
        f"- dataset: `{GOLD_DATASET}`",
        f"- bucket export: `gs://{bucket_name}/gold/`",
        f"- gate Silver join_match: **pass**" if gate_ok else "- gate Silver: **fail**",
        f"- conferencia fails: **{blocking}**",
        f"- exit esperado: `0` se conferencia fails = 0",
        f"- job_ids (amostra): `{', '.join(job_ids[:3])}{'...' if len(job_ids) > 3 else ''}`",
        "",
        "## Contagens",
        "",
        "| table | rows |",
        "|-------|------|",
    ]
    for m in manifest:
        lines.append(f"| {m['table']} | {m['rows']} |")

    lines.extend(
        [
            "",
            "## dry_run (bytes)",
            "",
            "| step | total_bytes_processed | label |",
            "|------|----------------------|-------|",
        ]
    )
    for d in dry_rows:
        lines.append(
            f"| {d['step']} | {d['total_bytes_processed']} | `{d['label'][:60]}` |"
        )

    lines.extend(
        [
            "",
            "## Conferencia",
            "",
            "| check | status | expected | observed | detail |",
            "|-------|--------|----------|----------|--------|",
        ]
    )
    for c in conf_rows:
        lines.append(
            f"| {c['check']} | {c['status']} | {c['expected']} | "
            f"{c['observed']} | {c['detail']} |"
        )

    lines.extend(
        [
            "",
            "## Export Parquet",
            "",
            "| table | uri_prefix |",
            "|-------|------------|",
        ]
    )
    for e in export_rows:
        lines.append(f"| {e['table']} | `{e['uri_prefix']}/` |")

    lines.extend(
        [
            "",
            "Snapshots: `manifest_*.csv`, `dry_run_bytes.csv`, `conferencia.csv`, `export_*.csv`.",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gold: produtos analiticos (Passo 6)")
    parser.add_argument(
        "--run_id",
        default=None,
        help="run_id Bronze/Silver (default: ultima Silver)",
    )
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    project_id, bq = load_env_and_client(ROOT)
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    if not bucket_name:
        raise SystemExit("[ERRO] GCP_BUCKET_NAME e obrigatorio no .env.")

    ensure_gold_dataset(bq, project_id)

    run_id = args.run_id or latest_silver_run_id(bq, project_id)
    if not RUN_ID_RE.fullmatch(run_id):
        raise SystemExit(f"[ERRO] run_id invalido: {run_id!r}")

    print("=" * 60)
    print(f"GOLD build | project={project_id} run_id={run_id}")
    print("=" * 60)

    status = "success"
    detail = ""
    rows_out = 0
    bytes_processed = 0
    exit_code = 0
    gate_ok = False

    try:
        print("gate Silver join_match...")
        gate_silver_join_match(bq, project_id)
        gate_ok = True

        if not SQL_FILE.exists():
            raise SystemExit(f"[ERRO] SQL nao encontrado: {SQL_FILE}")

        print("dry_run + CREATE TABLE...")
        jobs, dry_rows = run_sql_file(bq, project_id, run_id)
        bytes_processed = sum(int(d.get("total_bytes_processed") or 0) for d in dry_rows)
        bytes_processed += sum(int(j.get("bytes_processed") or 0) for j in jobs)

        ingestion_date = date.today().isoformat()
        print("EXPORT DATA Parquet...")
        export_rows: list[dict] = []
        for table in GOLD_TABLES:
            export_rows.append(
                export_table_parquet(
                    bq, project_id, bucket_name, table, run_id, ingestion_date
                )
            )

        manifest = []
        for table in GOLD_TABLES:
            n = count_rows(bq, project_id, table)
            manifest.append({"table": table, "rows": n, "run_id_bronze": run_id})
            print(f"  rows {table}: {n}")
        rows_out = sum(int(m["rows"]) for m in manifest)

        empty = [m for m in manifest if m["rows"] < 1]
        if empty:
            names = ", ".join(m["table"] for m in empty)
            raise SystemExit(f"[ERRO] tabelas Gold vazias: {names}")

        print("conferencia...")
        conf_rows = run_conferencia(bq, project_id)
        conf_fails = sum(1 for r in conf_rows if r["status"] == "fail")

        write_csv(manifest, OUT / f"manifest_{run_id}.csv")
        write_csv(manifest, OUT / "manifest_latest.csv")
        write_csv(dry_rows, OUT / "dry_run_bytes.csv")
        write_csv(conf_rows, OUT / "conferencia.csv")
        write_csv(export_rows, OUT / f"export_{run_id}.csv")
        write_csv(export_rows, OUT / "export_latest.csv")

        job_ids = [j["job_id"] for j in jobs] + [e["job_id"] for e in export_rows]
        update_readme(
            run_id,
            bucket_name,
            manifest,
            dry_rows,
            conf_rows,
            export_rows,
            job_ids,
            gate_ok,
        )

        print("=" * 60)
        print(f"evidencia: evidence/passo_06/ (run_id={run_id})")
        if conf_fails:
            status = "failed"
            detail = f"{conf_fails} conferencia(s) falharam"
            exit_code = 1
            print(f"[ERRO] {detail}")
        else:
            print("[OK] Gold OK (exit 0)")
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
            etapa="gold",
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
