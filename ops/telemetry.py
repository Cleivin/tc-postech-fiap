"""Telemetria: pipeline_runs (append) + alerta Pub/Sub (Passo 8)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from google.api_core import exceptions as gcp_exceptions
from google.cloud import bigquery, pubsub_v1
from google.cloud.exceptions import NotFound

from quality.config import ALERT_TOPIC_ID, OPS_DATASET, PIPELINE_RUNS_TABLE
from quality.ops import ensure_ops_dataset

VALID_ETAPAS = frozenset({"bronze", "silver", "gold", "stream"})
VALID_STATUS = frozenset({"success", "failed"})


def ensure_pipeline_runs_table(bq: bigquery.Client, project_id: str) -> str:
    ensure_ops_dataset(bq, project_id)
    table_id = f"{project_id}.{OPS_DATASET}.{PIPELINE_RUNS_TABLE}"
    schema = [
        bigquery.SchemaField("run_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("etapa", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("started_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("finished_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("duration_seconds", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("rows_in", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("rows_out", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("bytes_processed", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("latency_min_s", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("latency_max_s", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("latency_avg_s", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("detail", "STRING", mode="NULLABLE"),
    ]
    try:
        bq.get_table(table_id)
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        bq.create_table(table)
        print(f"[OK] tabela {table_id} criada")
    return table_id


def append_pipeline_run(
    bq: bigquery.Client,
    project_id: str,
    *,
    run_id: str,
    etapa: str,
    started_at: datetime,
    finished_at: datetime | None = None,
    rows_in: int | None = None,
    rows_out: int | None = None,
    status: str,
    bytes_processed: int | None = None,
    latency_min_s: float | None = None,
    latency_max_s: float | None = None,
    latency_avg_s: float | None = None,
    detail: str = "",
) -> dict[str, Any]:
    if etapa not in VALID_ETAPAS:
        raise ValueError(f"etapa invalida: {etapa!r}")
    if status not in VALID_STATUS:
        raise ValueError(f"status invalido: {status!r}")

    table_id = ensure_pipeline_runs_table(bq, project_id)
    end = finished_at or datetime.now(timezone.utc)
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    duration = (end - started_at).total_seconds()
    # INSERT DML (append) — visivel no SELECT imediato (evita streaming buffer).
    sql = f"""
    INSERT INTO `{table_id}` (
      run_id, etapa, started_at, finished_at, duration_seconds,
      rows_in, rows_out, status, bytes_processed,
      latency_min_s, latency_max_s, latency_avg_s, detail
    ) VALUES (
      @run_id, @etapa, TIMESTAMP(@started_at), TIMESTAMP(@finished_at),
      @duration_seconds, @rows_in, @rows_out, @status, @bytes_processed,
      @latency_min_s, @latency_max_s, @latency_avg_s, @detail
    )
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("run_id", "STRING", run_id),
            bigquery.ScalarQueryParameter("etapa", "STRING", etapa),
            bigquery.ScalarQueryParameter("started_at", "STRING", started_at.isoformat()),
            bigquery.ScalarQueryParameter("finished_at", "STRING", end.isoformat()),
            bigquery.ScalarQueryParameter("duration_seconds", "FLOAT64", float(duration)),
            bigquery.ScalarQueryParameter("rows_in", "INT64", rows_in),
            bigquery.ScalarQueryParameter("rows_out", "INT64", rows_out),
            bigquery.ScalarQueryParameter("status", "STRING", status),
            bigquery.ScalarQueryParameter("bytes_processed", "INT64", bytes_processed),
            bigquery.ScalarQueryParameter("latency_min_s", "FLOAT64", latency_min_s),
            bigquery.ScalarQueryParameter("latency_max_s", "FLOAT64", latency_max_s),
            bigquery.ScalarQueryParameter("latency_avg_s", "FLOAT64", latency_avg_s),
            bigquery.ScalarQueryParameter("detail", "STRING", detail or None),
        ]
    )
    bq.query(sql, job_config=job_config).result()
    row = {
        "run_id": run_id,
        "etapa": etapa,
        "started_at": started_at.isoformat(),
        "finished_at": end.isoformat(),
        "duration_seconds": float(duration),
        "rows_in": rows_in,
        "rows_out": rows_out,
        "status": status,
        "bytes_processed": bytes_processed,
        "latency_min_s": latency_min_s,
        "latency_max_s": latency_max_s,
        "latency_avg_s": latency_avg_s,
        "detail": detail or None,
    }
    print(
        f"[OK] pipeline_runs append etapa={etapa} run_id={run_id} "
        f"status={status} duration_s={duration:.3f}"
    )
    return row


def ensure_alert_topic(project_id: str, topic_id: str = ALERT_TOPIC_ID) -> str:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    try:
        publisher.get_topic(request={"topic": topic_path})
    except gcp_exceptions.NotFound:
        publisher.create_topic(request={"name": topic_path})
        print(f"[OK] topico Pub/Sub criado: {topic_path}")
    return topic_path


def publish_alert(
    project_id: str,
    *,
    run_id: str,
    etapa: str,
    detail: str = "",
    status: str = "failed",
    topic_id: str = ALERT_TOPIC_ID,
) -> dict[str, Any]:
    topic_path = ensure_alert_topic(project_id, topic_id)
    publisher = pubsub_v1.PublisherClient()
    payload = {
        "run_id": run_id,
        "etapa": etapa,
        "status": status,
        "detail": detail,
        "alerted_at": datetime.now(timezone.utc).isoformat(),
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    message_id = publisher.publish(topic_path, data).result(timeout=60)
    print(f"[OK] alerta publicado topic={topic_id} message_id={message_id}")
    return {"topic": topic_path, "message_id": message_id, "payload": payload}


def finish_run(
    bq: bigquery.Client,
    project_id: str,
    *,
    run_id: str,
    etapa: str,
    started_at: datetime,
    status: str,
    rows_in: int | None = None,
    rows_out: int | None = None,
    bytes_processed: int | None = None,
    latency_min_s: float | None = None,
    latency_max_s: float | None = None,
    latency_avg_s: float | None = None,
    detail: str = "",
    publish_on_failure: bool = True,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Append em pipeline_runs; se failed, publica em alfabetizacao-alertas."""
    row = append_pipeline_run(
        bq,
        project_id,
        run_id=run_id,
        etapa=etapa,
        started_at=started_at,
        rows_in=rows_in,
        rows_out=rows_out,
        status=status,
        bytes_processed=bytes_processed,
        latency_min_s=latency_min_s,
        latency_max_s=latency_max_s,
        latency_avg_s=latency_avg_s,
        detail=detail,
    )
    alert: dict[str, Any] | None = None
    if status == "failed" and publish_on_failure:
        alert = publish_alert(
            project_id,
            run_id=run_id,
            etapa=etapa,
            detail=detail,
            status=status,
        )
    return row, alert
