"""Prova Passo 8: duas runs success (append) + uma falha com alerta Pub/Sub.

Uso:
  python ops/prove_observability.py
  python ops/prove_observability.py --run_id 20d3623d0430

Este comando termina com exit code != 0 (falha provocada no final).
"""
from __future__ import annotations

import argparse
import csv
import io
import subprocess
import sys
import time
import uuid
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.telemetry import (
    ensure_alert_topic,
    ensure_pipeline_runs_table,
    finish_run,
    publish_alert,
)
from quality.config import ALERT_TOPIC_ID, OPS_DATASET, PIPELINE_RUNS_TABLE
from quality.ops import load_env_and_client
from quality.rules_bronze import latest_run_id

OUT = ROOT / "evidence" / "passo_08"
SILVER_SCRIPT = ROOT / "silver" / "transform.py"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def run_silver(run_id: str) -> int:
    print(f"[INFO] executando silver/transform.py --run_id {run_id}")
    proc = subprocess.run(
        [sys.executable, str(SILVER_SCRIPT), "--run_id", run_id],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.stderr:
        print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n")
    print(f"[INFO] silver exit={proc.returncode}")
    return proc.returncode


def fetch_runs(
    bq,
    project_id: str,
    *,
    etapa: str,
    status: str,
    limit: int,
    min_rows: int = 0,
    retries: int = 8,
    sleep_s: float = 3.0,
) -> list[dict]:
    """Query com retry — insert_rows_json pode demorar a aparecer no SELECT."""
    from google.cloud import bigquery

    table = f"{project_id}.{OPS_DATASET}.{PIPELINE_RUNS_TABLE}"
    sql = f"""
    SELECT
      run_id, etapa, started_at, finished_at, duration_seconds,
      rows_in, rows_out, status, bytes_processed,
      latency_min_s, latency_max_s, latency_avg_s, detail
    FROM `{table}`
    WHERE etapa = @etapa AND status = @status
    ORDER BY finished_at DESC
    LIMIT @limit
    """
    rows: list[dict] = []
    for attempt in range(1, retries + 1):
        job = bq.query(
            sql,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("etapa", "STRING", etapa),
                    bigquery.ScalarQueryParameter("status", "STRING", status),
                    bigquery.ScalarQueryParameter("limit", "INT64", limit),
                ]
            ),
        )
        rows = []
        for r in job.result():
            d = dict(r)
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
            rows.append(d)
        if min_rows <= 0 or len(rows) >= min_rows:
            return rows
        print(
            f"[INFO] pipeline_runs ainda com {len(rows)}/{min_rows} "
            f"(tentativa {attempt}/{retries}); aguardando streaming buffer..."
        )
        time.sleep(sleep_s)
    return rows


def write_readme(
    *,
    run_id: str,
    success_n: int,
    fail_row: dict,
    alert: dict,
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    text = f"""# Passo 8 — Observabilidade

- comando: `python ops/prove_observability.py --run_id {run_id}`
- tabela: `{OPS_DATASET}.{PIPELINE_RUNS_TABLE}` (sempre **append**)
- topico alerta: `{ALERT_TOPIC_ID}`
- silver run_id usado nas 2 successes: `{run_id}`

## Criterio de pronto

| check | resultado |
|-------|-----------|
| duas runs success (append) | **{success_n}** linhas em `pipeline_runs_two_success.csv` |
| falha registra status=failed | run_id=`{fail_row.get("run_id")}` |
| alerta Pub/Sub | message_id=`{alert.get("message_id")}` |
| exit da prova | `1` (falha provocada) |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `pipeline_runs_two_success.csv` | 2a run nao apagou a 1a |
| `pipeline_runs_failed.csv` | linha failed |
| `alert_publish.txt` | publish no topico de alertas |
| `prove_stdout.txt` | stdout completo |
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prova observabilidade Passo 8")
    parser.add_argument(
        "--run_id",
        default=None,
        help="run_id Bronze/Silver para as duas execucoes success",
    )
    parser.add_argument(
        "--skip-silver",
        action="store_true",
        help="Nao reexecuta silver (usa linhas ja existentes + so prova falha)",
    )
    args = parser.parse_args()

    project_id, bq = load_env_and_client(ROOT)
    ensure_pipeline_runs_table(bq, project_id)
    topic_path = ensure_alert_topic(project_id)

    run_id = args.run_id or latest_run_id(bq, project_id)
    buf = io.StringIO()
    success_rows: list[dict] = []
    fail_row: dict = {}
    alert: dict = {}

    with redirect_stdout(buf):
        print("=" * 60)
        print(f"OPS prove_observability | project={project_id}")
        print(f"silver_run_id={run_id}")
        print(f"alert_topic={topic_path}")
        print("=" * 60)

        if not args.skip_silver:
            rc1 = run_silver(run_id)
            if rc1 != 0:
                print(f"[ERRO] primeira silver falhou exit={rc1}")
                sys.exit(rc1)
            rc2 = run_silver(run_id)
            if rc2 != 0:
                print(f"[ERRO] segunda silver falhou exit={rc2}")
                sys.exit(rc2)
        else:
            print("[INFO] --skip-silver: nao reexecutou transform")

        success_rows = fetch_runs(
            bq,
            project_id,
            etapa="silver",
            status="success",
            limit=2,
            min_rows=2,
        )
        print(f"[OK] success silver rows fetched: {len(success_rows)}")
        for i, r in enumerate(success_rows, 1):
            print(
                f"  #{i} run_id={r['run_id']} finished_at={r['finished_at']} "
                f"duration_s={r['duration_seconds']}"
            )

        if len(success_rows) < 2:
            print(
                "[ERRO] preciso de >= 2 linhas success em pipeline_runs "
                "(rode sem --skip-silver ou execute silver duas vezes)"
            )
            sys.exit(1)

        # Falha provocada: registra failed + publica alerta (nao altera lake).
        fail_run_id = f"prove_fail_{uuid.uuid4().hex[:12]}"
        started = datetime.now(timezone.utc)
        fail_detail = (
            "falha bloqueante simulada (Passo 8): "
            "quality blocking / join_match — Silver/Gold nao publicaveis"
        )
        fail_row, alert_meta = finish_run(
            bq,
            project_id,
            run_id=fail_run_id,
            etapa="silver",
            started_at=started,
            status="failed",
            rows_in=0,
            rows_out=0,
            bytes_processed=0,
            detail=fail_detail,
            publish_on_failure=True,
        )
        alert = alert_meta or publish_alert(
            project_id,
            run_id=fail_run_id,
            etapa="silver",
            detail=fail_detail,
        )

        print(f"[OK] failed row run_id={fail_run_id}")
        print(f"[OK] alert message_id={alert['message_id']}")
        print("[ERRO] prove_observability concluiu com falha esperada (exit 1)")

    stdout = buf.getvalue()
    print(stdout, end="")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prove_stdout.txt").write_text(stdout, encoding="utf-8")
    write_csv(OUT / "pipeline_runs_two_success.csv", success_rows)
    write_csv(OUT / "pipeline_runs_failed.csv", [fail_row])
    (OUT / "alert_publish.txt").write_text(
        "\n".join(
            [
                f"topic={alert['topic']}",
                f"message_id={alert['message_id']}",
                f"payload={alert['payload']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    write_readme(
        run_id=run_id,
        success_n=len(success_rows),
        fail_row=fail_row,
        alert=alert,
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
