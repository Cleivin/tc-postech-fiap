"""Prova obrigatoria: dispara regra bloqueante com fixture (duplicata).

Uso:
  python quality/prove_failure.py

Este comando DEVE terminar com exit code != 0.
Nao altera o lake GCS Bronze.
"""
from __future__ import annotations

import csv
import io
import sys
import uuid
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quality.config import BRONZE_DATASET, FIXTURE_TABLE, OPS_DATASET
from quality.ops import append_check, ensure_ops_dataset, ensure_quality_table, load_env_and_client
from quality.rules_bronze import check_duplicate_keys, latest_run_id

OUT = ROOT / "evidence" / "passo_04"


def create_dup_fixture(bq, project_id: str, source_run_id: str) -> str:
    """Cria tabela com 1 linha de uf duplicada (chave natural repetida)."""
    ensure_ops_dataset(bq, project_id)
    fixture = f"{project_id}.{OPS_DATASET}.{FIXTURE_TABLE}"
    sql = f"""
    CREATE OR REPLACE TABLE `{fixture}` AS
    WITH one AS (
      SELECT ano, sigla_uf, serie, rede
      FROM `{project_id}.{BRONZE_DATASET}.uf`
      WHERE run_id = @run_id
      LIMIT 1
    )
    SELECT * FROM one
    UNION ALL
    SELECT * FROM one
    """
    from google.cloud import bigquery

    job = bq.query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("run_id", "STRING", source_run_id)
            ]
        ),
    )
    job.result()
    return fixture


def append_prove_readme(prove_run_id: str, row: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    readme = OUT / "README.md"
    block = [
        "## Prove failure",
        "",
        "- comando: `python quality/prove_failure.py`",
        f"- prove_run_id: `{prove_run_id}`",
        f"- fixture: `{OPS_DATASET}.{FIXTURE_TABLE}` (1 linha de `uf` duplicada)",
        "- regra: `duplicate_keys` (blocking) → **fail**",
        "- lake GCS Bronze: **nao** alterado",
        "- exit esperado: `1`",
        "- arquivos: `prove_failure_stdout.txt`, `prove_failure_checks.csv`",
        "",
        "| run_id | layer | entity | rule | status | value | threshold |",
        "|--------|-------|--------|------|--------|-------|-----------|",
        (
            f"| {row['run_id']} | {row['layer']} | {row['entity']} | {row['rule']} | "
            f"**{row['status']}** | {row['value']} | {row['threshold']} |"
        ),
        "",
    ]
    text = readme.read_text(encoding="utf-8") if readme.exists() else "# Passo 4 — Qualidade da Bronze\n\n"
    marker = "## Prove failure"
    if marker in text:
        text = text[: text.index(marker)] + "\n".join(block)
    else:
        text = text.rstrip() + "\n\n" + "\n".join(block)
    readme.write_text(text, encoding="utf-8")


def main() -> None:
    project_id, bq = load_env_and_client(ROOT)
    ensure_quality_table(bq, project_id)

    buf = io.StringIO()
    prove_run_id = f"prove_{uuid.uuid4().hex[:12]}"

    with redirect_stdout(buf):
        print("=" * 60)
        print(f"QUALITY prove_failure | project={project_id}")
        print(f"prove_run_id={prove_run_id}")
        print("=" * 60)

        source_run = latest_run_id(bq, project_id)
        print(f"fonte Bronze run_id={source_run}")

        fixture = create_dup_fixture(bq, project_id, source_run)
        print(f"fixture criada: {fixture}")

        result = check_duplicate_keys(
            bq,
            project_id,
            entity="uf",
            run_id=source_run,
            table_fqn=f"`{fixture}`",
            filter_run_id=False,
        )
        print(
            f"duplicate_keys value={result.value} status={result.status} "
            f"(esperado: fail com value>=1)"
        )

        if result.status != "fail" or result.value < 1:
            print("[ERRO] prova invalida: regra bloqueante NAO disparou")
            row = append_check(
                bq,
                project_id,
                run_id=prove_run_id,
                layer="fixture",
                entity="uf",
                rule="duplicate_keys",
                rule_class="blocking",
                status="fail",
                value=result.value,
                threshold=result.threshold,
                detail="prova_invalida: regra nao disparou como esperado",
            )
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / "prove_failure_stdout.txt").write_text(buf.getvalue(), encoding="utf-8")
            with (OUT / "prove_failure_checks.csv").open(
                "w", encoding="utf-8-sig", newline=""
            ) as f:
                w = csv.DictWriter(f, fieldnames=list(row.keys()))
                w.writeheader()
                w.writerow(row)
            append_prove_readme(prove_run_id, row)
            sys.exit(1)

        row = append_check(
            bq,
            project_id,
            run_id=prove_run_id,
            layer="fixture",
            entity="uf",
            rule=result.rule,
            rule_class=result.rule_class,
            status=result.status,
            value=result.value,
            threshold=result.threshold,
            detail=f"fixture={FIXTURE_TABLE}; source_run={source_run}; {result.detail}",
        )
        print(f"[OK] falha bloqueante registrada em quality_checks")
        print(f"  run_id={row['run_id']} status={row['status']} value={row['value']}")
        print("Silver/Gold nao publicadas (scripts nao invocados).")
        print("[ERRO] prove_failure concluiu com falha esperada (exit 1)")

    stdout = buf.getvalue()
    print(stdout, end="")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prove_failure_stdout.txt").write_text(stdout, encoding="utf-8")
    with (OUT / "prove_failure_checks.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
    append_prove_readme(prove_run_id, row)

    sys.exit(1)


if __name__ == "__main__":
    main()
