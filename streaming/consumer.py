"""Pub/Sub consumer — Bronze stream + quarentena + Gold eventos_stream (Passo 7).

Uso:
  python streaming/consumer.py
  python streaming/consumer.py --max-messages 50 --timeout 30
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from google.api_core import exceptions as gcp_exceptions
from google.cloud import bigquery, pubsub_v1, storage
from google.cloud.exceptions import NotFound

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.telemetry import finish_run
from quality.config import GOLD_DATASET
from quality.ops import load_env_and_client

SUBSCRIPTION_ID = "alfabetizacao-stream-sub"
OUT = ROOT / "evidence" / "passo_07"
ACK_DEADLINE_SECONDS = 600

REQUIRED_TOP = ("event_id", "produced_at", "entidade", "chave", "valor", "origem")
REQUIRED_CHAVE = ("id_municipio", "ano", "rede", "serie")


def load_env_full(root: Path) -> tuple[str, str, bigquery.Client]:
    project_id, bq = load_env_and_client(root)
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    if not bucket_name:
        raise SystemExit("[ERRO] GCP_BUCKET_NAME e obrigatorio no .env.")
    return project_id, bucket_name, bq


def ensure_eventos_stream_table(bq: bigquery.Client, project_id: str) -> str:
    dataset_ref = bigquery.Dataset(f"{project_id}.{GOLD_DATASET}")
    dataset_ref.location = "US"
    try:
        bq.get_dataset(dataset_ref)
    except NotFound:
        bq.create_dataset(dataset_ref, exists_ok=True)
        print(f"[OK] dataset {GOLD_DATASET} criado (US)")

    table_id = f"{project_id}.{GOLD_DATASET}.eventos_stream"
    schema = [
        bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("produced_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("latency_seconds", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("entidade", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("id_municipio", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ano", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("rede", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("serie", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("valor", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("origem", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ingestion_date", "DATE", mode="REQUIRED"),
    ]
    try:
        bq.get_table(table_id)
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        bq.create_table(table)
        print(f"[OK] tabela {table_id} criada")
    return table_id


def parse_produced_at(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def validate_event(data: Any) -> tuple[dict | None, str | None]:
    if not isinstance(data, dict):
        return None, "payload_nao_objeto"

    for key in REQUIRED_TOP:
        if key not in data:
            return None, f"campo_ausente:{key}"

    if data.get("origem") != "simulado":
        return None, "origem_diferente_de_simulado"
    if data.get("entidade") != "municipio":
        return None, "entidade_invalida"

    chave = data.get("chave")
    if not isinstance(chave, dict):
        return None, "chave_ausente_ou_invalida"
    for key in REQUIRED_CHAVE:
        if key not in chave or chave[key] is None or str(chave[key]).strip() == "":
            return None, f"chave_campo_ausente:{key}"

    produced_at = parse_produced_at(data.get("produced_at"))
    if produced_at is None:
        return None, "produced_at_invalido"

    try:
        valor = float(data["valor"])
    except (TypeError, ValueError):
        return None, "valor_nao_numerico"
    if valor < 0.0 or valor > 100.0:
        return None, "valor_fora_dominio_0_100"

    event_id = str(data["event_id"]).strip()
    if not event_id:
        return None, "event_id_vazio"

    try:
        ano = int(chave["ano"])
    except (TypeError, ValueError):
        return None, "ano_invalido"

    return {
        "event_id": event_id,
        "produced_at": produced_at,
        "entidade": "municipio",
        "id_municipio": str(chave["id_municipio"]).strip(),
        "ano": ano,
        "rede": str(chave["rede"]).strip(),
        "serie": str(chave["serie"]).strip(),
        "valor": valor,
        "origem": "simulado",
    }, None


def write_gcs_json(gcs: storage.Client, bucket_name: str, blob_path: str, payload: bytes) -> str:
    bucket = gcs.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_string(payload, content_type="application/json")
    return f"gs://{bucket_name}/{blob_path}"


def existing_event_ids(bq: bigquery.Client, table_id: str, ids: list[str]) -> set[str]:
    if not ids:
        return set()
    sql = f"""
    SELECT event_id
    FROM `{table_id}`
    WHERE event_id IN UNNEST(@ids)
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ArrayQueryParameter("ids", "STRING", ids)]
    )
    return {str(r["event_id"]) for r in bq.query(sql, job_config=job_config).result()}


def merge_events_batch(bq: bigquery.Client, table_id: str, rows: list[dict]) -> int:
    """MERGE em lote; retorna quantidade inserida."""
    if not rows:
        return 0

    # Serializa para JSON e usa JSON_VALUE no SQL (evita STRUCT complexo).
    payload = [
        {
            "event_id": r["event_id"],
            "produced_at": r["produced_at"].isoformat(),
            "ingested_at": r["ingested_at"].isoformat(),
            "latency_seconds": r["latency_seconds"],
            "entidade": r["entidade"],
            "id_municipio": r["id_municipio"],
            "ano": r["ano"],
            "rede": r["rede"],
            "serie": r["serie"],
            "valor": r["valor"],
            "origem": r["origem"],
            "ingestion_date": r["ingestion_date"].isoformat(),
        }
        for r in rows
    ]
    sql = f"""
    MERGE `{table_id}` T
    USING (
      SELECT
        JSON_VALUE(j, '$.event_id') AS event_id,
        TIMESTAMP(JSON_VALUE(j, '$.produced_at')) AS produced_at,
        TIMESTAMP(JSON_VALUE(j, '$.ingested_at')) AS ingested_at,
        CAST(JSON_VALUE(j, '$.latency_seconds') AS FLOAT64) AS latency_seconds,
        JSON_VALUE(j, '$.entidade') AS entidade,
        JSON_VALUE(j, '$.id_municipio') AS id_municipio,
        CAST(JSON_VALUE(j, '$.ano') AS INT64) AS ano,
        JSON_VALUE(j, '$.rede') AS rede,
        JSON_VALUE(j, '$.serie') AS serie,
        CAST(JSON_VALUE(j, '$.valor') AS FLOAT64) AS valor,
        JSON_VALUE(j, '$.origem') AS origem,
        DATE(JSON_VALUE(j, '$.ingestion_date')) AS ingestion_date
      FROM UNNEST(@payload) AS j
    ) S
    ON T.event_id = S.event_id
    WHEN NOT MATCHED THEN
      INSERT (
        event_id, produced_at, ingested_at, latency_seconds, entidade,
        id_municipio, ano, rede, serie, valor, origem, ingestion_date
      )
      VALUES (
        S.event_id, S.produced_at, S.ingested_at, S.latency_seconds, S.entidade,
        S.id_municipio, S.ano, S.rede, S.serie, S.valor, S.origem, S.ingestion_date
      )
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter(
                "payload",
                "STRING",
                [json.dumps(p, ensure_ascii=False) for p in payload],
            )
        ]
    )
    job = bq.query(sql, job_config=job_config)
    job.result()
    stats = getattr(job, "dml_stats", None)
    if stats is None:
        return 0
    return int(getattr(stats, "inserted_row_count", 0) or 0)


def snapshot_oficial(bq: bigquery.Client, project_id: str) -> dict:
    sql = f"""
    SELECT
      COUNT(*) AS n_rows,
      ROUND(SUM(taxa_alfabetizacao), 4) AS sum_taxa,
      ROUND(AVG(taxa_alfabetizacao), 4) AS avg_taxa
    FROM `{project_id}.{GOLD_DATASET}.indicador_uf`
    WHERE sigla_uf = 'CE' AND ano = 2024 AND rede = '5'
    """
    rows = list(bq.query(sql).result())
    if not rows:
        return {"n_rows": 0, "sum_taxa": None, "avg_taxa": None}
    r = rows[0]
    return {
        "n_rows": int(r["n_rows"] or 0),
        "sum_taxa": float(r["sum_taxa"]) if r["sum_taxa"] is not None else None,
        "avg_taxa": float(r["avg_taxa"]) if r["avg_taxa"] is not None else None,
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_evidence(
    *,
    project_id: str,
    bq: bigquery.Client,
    table_id: str,
    metrics: dict,
    quarantine_uris: list[str],
    before: dict,
    after: dict,
    latencies: list[float],
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sample_rows = [
        dict(r)
        for r in bq.query(
            f"""
            SELECT event_id, produced_at, ingested_at, latency_seconds, id_municipio, ano,
                   rede, serie, valor, origem
            FROM `{table_id}`
            WHERE origem = 'simulado'
            ORDER BY ingested_at DESC
            LIMIT 25
            """
        ).result()
    ]
    for row in sample_rows:
        for k, v in list(row.items()):
            if hasattr(v, "isoformat"):
                row[k] = v.isoformat()
    write_csv(
        OUT / "eventos_stream_sample.csv",
        sample_rows,
        [
            "event_id",
            "produced_at",
            "ingested_at",
            "latency_seconds",
            "id_municipio",
            "ano",
            "rede",
            "serie",
            "valor",
            "origem",
        ],
    )

    dedupe_rows = []
    max_n = 0
    for r in bq.query(
        f"""
        SELECT event_id, COUNT(*) AS n, ROUND(SUM(valor), 4) AS sum_valor,
               ROUND(ANY_VALUE(valor), 4) AS valor
        FROM `{table_id}`
        WHERE origem = 'simulado'
        GROUP BY event_id
        ORDER BY n DESC, event_id
        LIMIT 50
        """
    ).result():
        n = int(r["n"])
        max_n = max(max_n, n)
        dedupe_rows.append(
            {
                "event_id": r["event_id"],
                "n": n,
                "sum_valor": r["sum_valor"],
                "valor": r["valor"],
                "ok_sem_dobra": (
                    "yes"
                    if n == 1 and abs(float(r["sum_valor"]) - float(r["valor"])) < 1e-9
                    else "no"
                ),
            }
        )
    write_csv(
        OUT / "dedupe_check.csv",
        dedupe_rows,
        ["event_id", "n", "sum_valor", "valor", "ok_sem_dobra"],
    )

    (OUT / "quarentena_uris.txt").write_text(
        "\n".join(quarantine_uris) + ("\n" if quarantine_uris else ""),
        encoding="utf-8",
    )

    oficial_ok = before == after
    write_csv(
        OUT / "oficial_inalterado.csv",
        [
            {
                "check": "indicador_uf_CE_2024_rede5",
                "moment": "before",
                "n_rows": before["n_rows"],
                "sum_taxa": before["sum_taxa"],
                "avg_taxa": before["avg_taxa"],
            },
            {
                "check": "indicador_uf_CE_2024_rede5",
                "moment": "after",
                "n_rows": after["n_rows"],
                "sum_taxa": after["sum_taxa"],
                "avg_taxa": after["avg_taxa"],
            },
            {
                "check": "indicador_uf_CE_2024_rede5",
                "moment": "equal",
                "n_rows": 1 if oficial_ok else 0,
                "sum_taxa": None,
                "avg_taxa": None,
            },
        ],
        ["check", "moment", "n_rows", "sum_taxa", "avg_taxa"],
    )

    lat_min = min(latencies) if latencies else None
    lat_max = max(latencies) if latencies else None
    lat_avg = (sum(latencies) / len(latencies)) if latencies else None

    readme = f"""# Passo 7 — Streaming simulado

- comandos:
  - `python streaming/producer.py --n 20 --seed 7`
  - `python streaming/consumer.py --max-messages 50 --timeout 30`
- topic: `alfabetizacao-stream-topic`
- subscription: `alfabetizacao-stream-sub`
- tabela: `{table_id}`
- projeto: `{project_id}`

## Metricas do consumer

| metrica | valor |
|---------|-------|
| mensagens_recebidas (lag do lote) | {metrics["received"]} |
| valid_inserted | {metrics["valid_inserted"]} |
| duplicates_skipped | {metrics["duplicates_skipped"]} |
| invalid_quarantine | {metrics["invalid_quarantine"]} |
| latency_min_s | {lat_min} |
| latency_max_s | {lat_max} |
| latency_avg_s | {lat_avg} |
| latency_gt_0 | {"yes" if lat_min is not None and lat_min > 0 else "no"} |
| max_n_por_event_id | {max_n} |
| oficial_inalterado | {"yes" if oficial_ok else "no"} |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `producer_stdout.txt` | publish OK |
| `consumer_stdout.txt` | latencia, dups, quarentena |
| `eventos_stream_sample.csv` | linhas `origem=simulado` |
| `dedupe_check.csv` | `event_id` unico; valor nao dobrado |
| `quarentena_uris.txt` | path GCS do invalido |
| `oficial_inalterado.csv` | Gold oficial CE 2024 inalterada |
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def extend_ack(
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
    ack_ids: list[str],
) -> None:
    if not ack_ids:
        return
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": ack_ids,
            "ack_deadline_seconds": ACK_DEADLINE_SECONDS,
        }
    )


def process_batch(
    *,
    received_messages: list,
    gcs: storage.Client,
    bucket_name: str,
    bq: bigquery.Client,
    table_id: str,
    seen: set[str],
    quarantine_uris: list[str],
    latencies: list[float],
    metrics: dict[str, int],
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
) -> None:
    ack_ids = [m.ack_id for m in received_messages]
    extend_ack(subscriber, subscription_path, ack_ids)

    ingested_at = datetime.now(timezone.utc)
    ingestion_date = date.today()

    to_insert: list[dict] = []

    for msg in received_messages:
        raw = msg.message.data
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = None
            reason = "json_quebrado"
            event = None
        else:
            event, reason = validate_event(data)

        if reason is not None:
            qid = data.get("event_id") if isinstance(data, dict) else None
            blob_name = (
                f"bronze/stream_quarentena/"
                f"{qid or uuid.uuid4()}_{uuid.uuid4().hex[:8]}.json"
            )
            envelope = {
                "reason": reason,
                "ingested_at": ingested_at.isoformat(),
                "raw": raw.decode("utf-8", errors="replace"),
            }
            uri = write_gcs_json(
                gcs,
                bucket_name,
                blob_name,
                json.dumps(envelope, ensure_ascii=False).encode("utf-8"),
            )
            quarantine_uris.append(uri)
            metrics["invalid_quarantine"] += 1
            print(f"  [QUARANTINE] reason={reason} uri={uri}")
            continue

        assert event is not None
        event_id = event["event_id"]
        if event_id in seen:
            metrics["duplicates_skipped"] += 1
            print(f"  [DUP-MEM] event_id={event_id}")
            continue

        latency = (ingested_at - event["produced_at"]).total_seconds()
        row = {
            **event,
            "ingested_at": ingested_at,
            "latency_seconds": latency,
            "ingestion_date": ingestion_date,
        }
        to_insert.append(row)
        seen.add(event_id)  # evita dup no mesmo lote antes do MERGE

    # Dedupe contra BQ (at-least-once de runs anteriores).
    candidate_ids = [r["event_id"] for r in to_insert]
    already = existing_event_ids(bq, table_id, candidate_ids)
    fresh_rows = [r for r in to_insert if r["event_id"] not in already]
    skipped = [r for r in to_insert if r["event_id"] in already]
    metrics["duplicates_skipped"] += len(skipped)
    for r in skipped:
        print(f"  [DUP-BQ] event_id={r['event_id']}")

    inserted_n = merge_events_batch(bq, table_id, fresh_rows)
    metrics["valid_inserted"] += inserted_n

    for row in fresh_rows:
        event_id = row["event_id"]
        latency = row["latency_seconds"]
        latencies.append(latency)
        stream_blob = (
            f"bronze/stream/ingestion_date={ingestion_date.isoformat()}/"
            f"event_id={event_id}.json"
        )
        uri = write_gcs_json(
            gcs,
            bucket_name,
            stream_blob,
            json.dumps(
                {
                    k: (v.isoformat() if hasattr(v, "isoformat") else v)
                    for k, v in row.items()
                },
                ensure_ascii=False,
            ).encode("utf-8"),
        )
        print(f"  [OK] inserted event_id={event_id} latency_s={latency:.4f} uri={uri}")

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Consome eventos Pub/Sub (stream simulado)")
    parser.add_argument("--max-messages", type=int, default=50)
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout total (s)")
    parser.add_argument(
        "--no-evidence",
        action="store_true",
        help="Nao grava CSVs em evidence/passo_07/",
    )
    parser.add_argument(
        "--drain",
        action="store_true",
        help="Aceita lote so de duplicatas/quarentena (exit 0) para esvaziar a fila",
    )
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    stream_run_id = uuid.uuid4().hex[:12]
    project_id, bucket_name, bq = load_env_full(ROOT)
    gcs = storage.Client(project=project_id)
    table_id = ensure_eventos_stream_table(bq, project_id)

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, SUBSCRIPTION_ID)

    print(f"[INFO] projeto={project_id} sub={SUBSCRIPTION_ID} bucket={bucket_name}")
    print(f"[INFO] stream_run_id={stream_run_id}")
    print("[INFO] snapshot oficial (antes)...")
    before = snapshot_oficial(bq, project_id)
    print(f"  before={before}")

    metrics = {
        "received": 0,
        "valid_inserted": 0,
        "duplicates_skipped": 0,
        "invalid_quarantine": 0,
    }
    seen: set[str] = set()
    quarantine_uris: list[str] = []
    latencies: list[float] = []

    status = "success"
    detail = ""
    exit_code = 0
    lat_min = lat_max = lat_avg = None
    skip_telemetry = False

    try:
        deadline = datetime.now(timezone.utc).timestamp() + args.timeout
        empty_streak = 0
        while datetime.now(timezone.utc).timestamp() < deadline:
            remaining = int(args.max_messages) - metrics["received"]
            if remaining <= 0:
                break
            pull_timeout = min(
                5.0, max(1.0, deadline - datetime.now(timezone.utc).timestamp())
            )
            try:
                response = subscriber.pull(
                    request={
                        "subscription": subscription_path,
                        "max_messages": min(remaining, 25),
                    },
                    timeout=pull_timeout,
                )
            except gcp_exceptions.DeadlineExceeded:
                empty_streak += 1
                if metrics["received"] > 0 and empty_streak >= 2:
                    break
                continue

            if not response.received_messages:
                empty_streak += 1
                if metrics["received"] > 0 and empty_streak >= 2:
                    break
                continue

            empty_streak = 0
            batch_n = len(response.received_messages)
            metrics["received"] += batch_n
            print(
                f"[INFO] pull recebeu {batch_n} mensagem(ns) "
                f"(total={metrics['received']})"
            )

            process_batch(
                received_messages=list(response.received_messages),
                gcs=gcs,
                bucket_name=bucket_name,
                bq=bq,
                table_id=table_id,
                seen=seen,
                quarantine_uris=quarantine_uris,
                latencies=latencies,
                metrics=metrics,
                subscriber=subscriber,
                subscription_path=subscription_path,
            )

        print("[INFO] snapshot oficial (depois)...")
        after = snapshot_oficial(bq, project_id)
        print(f"  after={after}")

        lat_min = min(latencies) if latencies else None
        lat_max = max(latencies) if latencies else None
        lat_avg = (sum(latencies) / len(latencies)) if latencies else None
        print(
            f"[OK] received={metrics['received']} "
            f"inserted={metrics['valid_inserted']} "
            f"dups={metrics['duplicates_skipped']} "
            f"quarantine={metrics['invalid_quarantine']} "
            f"latency_min={lat_min} latency_max={lat_max} latency_avg={lat_avg}"
        )

        if not args.no_evidence:
            write_evidence(
                project_id=project_id,
                bq=bq,
                table_id=table_id,
                metrics=metrics,
                quarantine_uris=quarantine_uris,
                before=before,
                after=after,
                latencies=latencies,
            )
            print(f"[OK] evidencia em {OUT}")

        if before != after:
            status = "failed"
            detail = "Gold oficial mudou apos o consumer"
            exit_code = 1
            raise SystemExit(f"[ERRO] {detail}")

        if args.drain:
            detail = "drain"
            skip_telemetry = metrics["received"] == 0
            return

        if metrics["received"] == 0:
            status = "failed"
            detail = "nenhuma mensagem recebida"
            exit_code = 1
            raise SystemExit(f"[ERRO] {detail} — rode o producer antes")

        if metrics["valid_inserted"] < 1:
            status = "failed"
            detail = "nenhum evento valido inserido"
            exit_code = 1
            raise SystemExit(f"[ERRO] {detail} em eventos_stream")
        if lat_min is None or lat_min <= 0:
            status = "failed"
            detail = "latencia deve ser > 0"
            exit_code = 1
            raise SystemExit(f"[ERRO] {detail}")
        if metrics["invalid_quarantine"] < 1:
            print("[WARN] nenhum invalido em quarentena neste lote")
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        status = "failed"
        detail = str(exc)
        exit_code = 1
        print(f"[ERRO] {exc}")
    finally:
        if not skip_telemetry:
            finish_run(
                bq,
                project_id,
                run_id=stream_run_id,
                etapa="stream",
                started_at=started_at,
                status=status,
                rows_in=metrics["received"],
                rows_out=metrics["valid_inserted"],
                bytes_processed=0,
                latency_min_s=lat_min,
                latency_max_s=lat_max,
                latency_avg_s=lat_avg,
                detail=detail,
                publish_on_failure=not args.drain,
            )

    if exit_code:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
