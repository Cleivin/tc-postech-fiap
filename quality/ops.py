"""Dataset alfabetizacao_ops + append em quality_checks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from quality.config import OPS_DATASET, QUALITY_TABLE


def load_env_and_client(root) -> tuple[str, bigquery.Client]:
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    load_dotenv(root / ".env")
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds and not Path(creds).is_absolute():
        creds = str(root / creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds or ""

    if not creds or not Path(creds).exists():
        raise SystemExit(
            "[ERRO] Credencial GCP nao encontrada. "
            "Salve credentials/gcp-sa-key.json e confira GOOGLE_APPLICATION_CREDENTIALS no .env."
        )

    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise SystemExit("[ERRO] GCP_PROJECT_ID e obrigatorio no .env.")

    return project_id, bigquery.Client(project=project_id, location="US")


def ensure_ops_dataset(bq: bigquery.Client, project_id: str) -> None:
    dataset_ref = bigquery.Dataset(f"{project_id}.{OPS_DATASET}")
    dataset_ref.location = "US"
    try:
        bq.get_dataset(dataset_ref)
    except NotFound:
        bq.create_dataset(dataset_ref, exists_ok=True)
        print(f"[OK] dataset {OPS_DATASET} criado (US)")


def ensure_quality_table(bq: bigquery.Client, project_id: str) -> str:
    ensure_ops_dataset(bq, project_id)
    table_id = f"{project_id}.{OPS_DATASET}.{QUALITY_TABLE}"
    schema = [
        bigquery.SchemaField("run_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("layer", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("entity", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("rule", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("class", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("value", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("threshold", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("detail", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("checked_at", "TIMESTAMP", mode="REQUIRED"),
    ]
    try:
        bq.get_table(table_id)
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        bq.create_table(table)
        print(f"[OK] tabela {table_id} criada")
    return table_id


def append_check(
    bq: bigquery.Client,
    project_id: str,
    *,
    run_id: str,
    layer: str,
    entity: str,
    rule: str,
    rule_class: str,
    status: str,
    value: float,
    threshold: float,
    detail: str = "",
    checked_at: datetime | None = None,
) -> dict[str, Any]:
    table_id = ensure_quality_table(bq, project_id)
    ts = checked_at or datetime.now(timezone.utc)
    row = {
        "run_id": run_id,
        "layer": layer,
        "entity": entity,
        "rule": rule,
        "class": rule_class,
        "status": status,
        "value": float(value),
        "threshold": float(threshold),
        "detail": detail,
        "checked_at": ts.isoformat(),
    }
    errors = bq.insert_rows_json(table_id, [row])
    if errors:
        raise RuntimeError(f"Falha ao inserir quality_checks: {errors}")
    return {
        "run_id": run_id,
        "layer": layer,
        "entity": entity,
        "rule": rule,
        "class": rule_class,
        "status": status,
        "value": float(value),
        "threshold": float(threshold),
        "detail": detail,
        "checked_at": ts.isoformat(),
    }
