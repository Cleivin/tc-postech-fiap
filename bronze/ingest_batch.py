"""Ingestão Bronze: BigQuery público -> Parquet no GCS + external tables.

Passo 3 — Tech Challenge Fase 2.
Layout: gs://<bucket>/bronze/<entidade>/ingestion_date=YYYY-MM-DD/run_id=<id>/part-*.parquet

Colunas técnicas:
  - no Parquet: ingestion_ts, source_table
  - no path Hive (e na external table): ingestion_date, run_id
Assim run_id nao duplica schema arquivo vs particao.
"""
from __future__ import annotations

import csv
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.telemetry import finish_run

OUT = ROOT / "evidence" / "passo_03"
DATASET_ID = "alfabetizacao_bronze"
SOURCE_DATASET = "basedosdados.br_inep_avaliacao_alfabetizacao"

ENTITIES: dict[str, list[str]] = {
    "alunos": [
        "ano",
        "id_municipio",
        "id_escola",
        "id_aluno",
        "caderno",
        "serie",
        "rede",
        "presenca",
        "preenchimento_caderno",
        "alfabetizado",
        "proficiencia",
        "peso_aluno",
    ],
    "municipio": [
        "ano",
        "id_municipio",
        "serie",
        "rede",
        "taxa_alfabetizacao",
        "media_portugues",
        "proporcao_aluno_nivel_0",
        "proporcao_aluno_nivel_1",
        "proporcao_aluno_nivel_2",
        "proporcao_aluno_nivel_3",
        "proporcao_aluno_nivel_4",
        "proporcao_aluno_nivel_5",
        "proporcao_aluno_nivel_6",
        "proporcao_aluno_nivel_7",
        "proporcao_aluno_nivel_8",
    ],
    "uf": [
        "ano",
        "sigla_uf",
        "serie",
        "rede",
        "taxa_alfabetizacao",
        "media_portugues",
        "proporcao_aluno_nivel_0",
        "proporcao_aluno_nivel_1",
        "proporcao_aluno_nivel_2",
        "proporcao_aluno_nivel_3",
        "proporcao_aluno_nivel_4",
        "proporcao_aluno_nivel_5",
        "proporcao_aluno_nivel_6",
        "proporcao_aluno_nivel_7",
        "proporcao_aluno_nivel_8",
    ],
    "meta_alfabetizacao_brasil": [
        "ano",
        "rede",
        "taxa_alfabetizacao",
        "meta_alfabetizacao_2024",
        "meta_alfabetizacao_2025",
        "meta_alfabetizacao_2026",
        "meta_alfabetizacao_2027",
        "meta_alfabetizacao_2028",
        "meta_alfabetizacao_2029",
        "meta_alfabetizacao_2030",
        "percentual_participacao",
    ],
    "meta_alfabetizacao_uf": [
        "ano",
        "sigla_uf",
        "rede",
        "taxa_alfabetizacao",
        "meta_alfabetizacao_2024",
        "meta_alfabetizacao_2025",
        "meta_alfabetizacao_2026",
        "meta_alfabetizacao_2027",
        "meta_alfabetizacao_2028",
        "meta_alfabetizacao_2029",
        "meta_alfabetizacao_2030",
        "percentual_participacao",
    ],
    "meta_alfabetizacao_municipio": [
        "ano",
        "id_municipio",
        "rede",
        "taxa_alfabetizacao",
        "meta_alfabetizacao_2024",
        "meta_alfabetizacao_2025",
        "meta_alfabetizacao_2026",
        "meta_alfabetizacao_2027",
        "meta_alfabetizacao_2028",
        "meta_alfabetizacao_2029",
        "meta_alfabetizacao_2030",
        "nivel_alfabetizacao",
        "percentual_participacao",
    ],
    "dicionario": [
        "id_tabela",
        "nome_coluna",
        "chave",
        "cobertura_temporal",
        "valor",
    ],
}


def load_env() -> tuple[str, str]:
    load_dotenv(ROOT / ".env")
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds and not Path(creds).is_absolute():
        creds = str(ROOT / creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds or ""

    if not creds or not Path(creds).exists():
        raise SystemExit(
            "[ERRO] Credencial GCP nao encontrada. "
            "Salve credentials/gcp-sa-key.json e confira GOOGLE_APPLICATION_CREDENTIALS no .env."
        )

    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    if not project_id or not bucket_name:
        raise SystemExit("[ERRO] GCP_PROJECT_ID e GCP_BUCKET_NAME sao obrigatorios no .env.")
    return project_id, bucket_name


def ensure_dataset(bq: bigquery.Client, project_id: str) -> None:
    dataset_ref = bigquery.Dataset(f"{project_id}.{DATASET_ID}")
    dataset_ref.location = "US"
    try:
        bq.get_dataset(dataset_ref)
        print(f"[OK] dataset {DATASET_ID} ja existe")
    except NotFound:
        bq.create_dataset(dataset_ref, exists_ok=True)
        print(f"[OK] dataset {DATASET_ID} criado (US)")


def export_sql(
    entity: str,
    columns: list[str],
    uri_prefix: str,
) -> str:
    source = f"{SOURCE_DATASET}.{entity}"
    cols = ",\n  ".join(columns)
    # overwrite=true so se aplica so ao URI desta run (pasta nova / vazia).
    # run_id fica so no path Hive (partition column da external table).
    return f"""
EXPORT DATA OPTIONS (
  uri='{uri_prefix}/part-*.parquet',
  format='PARQUET',
  overwrite=true
) AS
SELECT
  {cols},
  CURRENT_TIMESTAMP() AS ingestion_ts,
  '{source}' AS source_table
FROM `{source}`
"""


def count_source(bq: bigquery.Client, entity: str) -> tuple[int, str]:
    sql = f"SELECT COUNT(*) AS n FROM `{SOURCE_DATASET}.{entity}`"
    job = bq.query(sql)
    row = next(job.result())
    return int(row["n"]), job.job_id


def create_external_table(
    bq: bigquery.Client,
    project_id: str,
    bucket_name: str,
    entity: str,
) -> str:
    """External table Hive: ingestion_date + run_id no path; resto no Parquet."""
    table_id = f"{project_id}.{DATASET_ID}.{entity}"
    hive_prefix = f"gs://{bucket_name}/bronze/{entity}"
    ddl = f"""
CREATE OR REPLACE EXTERNAL TABLE `{table_id}`
WITH PARTITION COLUMNS (
  ingestion_date DATE,
  run_id STRING
)
OPTIONS (
  format = 'PARQUET',
  uris = ['{hive_prefix}/*'],
  hive_partition_uri_prefix = '{hive_prefix}',
  require_hive_partition_filter = false
)
"""
    job = bq.query(ddl)
    job.result()
    return table_id


def list_parquet_blobs(
    gcs: storage.Client,
    bucket_name: str,
    prefix: str,
) -> list[str]:
    bucket = gcs.bucket(bucket_name)
    names = [
        f"gs://{bucket_name}/{b.name}"
        for b in bucket.list_blobs(prefix=prefix)
        if b.name.endswith(".parquet")
    ]
    return names


def list_run_prefixes(
    gcs: storage.Client,
    bucket_name: str,
    entity: str,
) -> list[str]:
    """Lista prefixos run_id= sob bronze/<entity>/ (para prova de historico)."""
    bucket = gcs.bucket(bucket_name)
    base = f"bronze/{entity}/"
    prefixes: set[str] = set()
    for blob in bucket.list_blobs(prefix=base):
        # bronze/entidade/ingestion_date=.../run_id=.../file
        parts = blob.name.split("/")
        if len(parts) >= 4 and parts[2].startswith("ingestion_date=") and parts[3].startswith(
            "run_id="
        ):
            prefixes.add("/".join(parts[:4]))
    return sorted(prefixes)


def count_external_run(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    run_id: str,
) -> int | None:
    table_id = f"{project_id}.{DATASET_ID}.{entity}"
    sql = f"SELECT COUNT(*) AS n FROM `{table_id}` WHERE run_id = @run_id"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("run_id", "STRING", run_id)]
    )
    try:
        job = bq.query(sql, job_config=job_config)
        row = next(job.result())
        return int(row["n"])
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] COUNT external {entity}: {exc}")
        return None


def write_manifest(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_readme(
    rows: list[dict],
    run_id: str,
    ingestion_date: str,
    bucket_name: str,
    history: dict[str, list[str]],
    path: Path,
) -> None:
    lines = [
        "# Passo 3 — Bronze (Parquet no GCS + external tables)",
        "",
        f"- comando: `python bronze/ingest_batch.py`",
        f"- run_id (esta execucao): `{run_id}`",
        f"- ingestion_date (UTC): `{ingestion_date}`",
        f"- bucket: `{bucket_name}`",
        f"- dataset BQ: `{DATASET_ID}`",
        "",
        "Bronze e raw: sem regra de negocio. A anomalia de encoding de `rede` "
        "(codigo vs rotulo nas metas) e preservada para a Silver.",
        "",
        "## Manifesto desta run",
        "",
        "| entidade | n_linhas | export_job_id | bytes_processed | gcs_prefix | n_parquet | external_table |",
        "|----------|----------|---------------|-----------------|------------|-----------|----------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['entidade']} | {r['n_linhas']} | `{r['bq_export_job_id']}` | "
            f"{r['bytes_processed']} | `{r['gcs_uri_prefix']}` | {r['n_arquivos_parquet']} | "
            f"`{r['external_table']}` |"
        )

    lines.extend(
        [
            "",
            "## Prova de historico (append)",
            "",
            "Cada run cria um novo `run_id` sob `bronze/<entidade>/`. "
            "Prefixos existentes nao sao apagados.",
            "",
        ]
    )
    for entity, prefixes in history.items():
        lines.append(f"### {entity}")
        lines.append("")
        if not prefixes:
            lines.append("- (nenhum prefixo listado)")
        else:
            for p in prefixes:
                lines.append(f"- `gs://{bucket_name}/{p}/`")
        lines.append("")

    lines.extend(
        [
            "## Como a Silver deve ler",
            "",
            "Filtrar a **ultima** `ingestion_date` / `run_id` "
            "(ou a passada por parametro). Nao fazer `SELECT *` misturando runs.",
            "",
            f"Arquivo maquina: `evidence/passo_03/manifest_{run_id}.csv` "
            f"(e `manifest.csv` = ultima run).",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    project_id, bucket_name = load_env()
    started_at = datetime.now(timezone.utc)
    ingestion_date = started_at.strftime("%Y-%m-%d")
    run_id = uuid.uuid4().hex[:12]

    print("=" * 60)
    print(f"BRONZE ingest | project={project_id} bucket={bucket_name}")
    print(f"ingestion_date={ingestion_date} run_id={run_id}")
    print("=" * 60)

    bq = bigquery.Client(project=project_id, location="US")
    gcs = storage.Client(project=project_id)
    ensure_dataset(bq, project_id)
    OUT.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    failures: list[str] = []
    status = "success"
    detail = ""
    exit_code = 0
    rows_in = 0
    rows_out = 0
    bytes_total = 0

    try:
        for entity, columns in ENTITIES.items():
            gcs_prefix = (
                f"bronze/{entity}/ingestion_date={ingestion_date}/run_id={run_id}"
            )
            uri_prefix = f"gs://{bucket_name}/{gcs_prefix}"
            print(f"\n--- {entity} ---")
            print(f"  uri: {uri_prefix}/part-*.parquet")

            try:
                n_source, count_job_id = count_source(bq, entity)
                print(f"  source COUNT={n_source} (job={count_job_id})")

                sql = export_sql(entity, columns, uri_prefix)
                job = bq.query(sql)
                job.result()
                bytes_processed = job.total_bytes_processed or 0
                print(f"  EXPORT job={job.job_id} bytes={bytes_processed}")

                blobs = list_parquet_blobs(gcs, bucket_name, gcs_prefix + "/")
                print(f"  parquet files: {len(blobs)}")
                if not blobs:
                    raise RuntimeError("nenhum arquivo .parquet no prefixo da run")

                table_id = create_external_table(bq, project_id, bucket_name, entity)
                print(f"  external table: {table_id}")

                n_ext = count_external_run(bq, project_id, entity, run_id)
                if n_ext is not None:
                    print(f"  external COUNT(run_id)={n_ext}")
                    if n_ext != n_source:
                        print(
                            f"  [WARN] COUNT external ({n_ext}) != source ({n_source})"
                        )

                rows_in += int(n_source)
                rows_out += int(n_ext if n_ext is not None else n_source)
                bytes_total += int(bytes_processed)

                rows.append(
                    {
                        "entidade": entity,
                        "run_id": run_id,
                        "ingestion_date": ingestion_date,
                        "bq_export_job_id": job.job_id,
                        "bq_count_job_id": count_job_id,
                        "n_linhas": n_source,
                        "n_linhas_external": n_ext if n_ext is not None else "",
                        "bytes_processed": bytes_processed,
                        "gcs_uri_prefix": uri_prefix,
                        "n_arquivos_parquet": len(blobs),
                        "external_table": table_id,
                        "sample_object": blobs[0],
                    }
                )
                print(f"  [OK] {entity}")
            except Exception as exc:  # noqa: BLE001
                failures.append(entity)
                print(f"  [ERRO] {entity}: {exc}")
                rows.append(
                    {
                        "entidade": entity,
                        "run_id": run_id,
                        "ingestion_date": ingestion_date,
                        "bq_export_job_id": "",
                        "bq_count_job_id": "",
                        "n_linhas": 0,
                        "n_linhas_external": "",
                        "bytes_processed": 0,
                        "gcs_uri_prefix": uri_prefix,
                        "n_arquivos_parquet": 0,
                        "external_table": f"{project_id}.{DATASET_ID}.{entity}",
                        "sample_object": "",
                        "error": str(exc),
                    }
                )

        history = {
            entity: list_run_prefixes(gcs, bucket_name, entity) for entity in ENTITIES
        }

        manifest_run = OUT / f"manifest_{run_id}.csv"
        manifest_latest = OUT / "manifest.csv"
        write_manifest(rows, manifest_run)
        write_manifest(rows, manifest_latest)
        write_readme(
            rows,
            run_id,
            ingestion_date,
            bucket_name,
            history,
            OUT / "README.md",
        )

        hist_path = OUT / "gcs_run_prefixes.txt"
        with hist_path.open("a", encoding="utf-8") as f:
            f.write(f"\n# after run_id={run_id} ingestion_date={ingestion_date}\n")
            for entity, prefixes in history.items():
                f.write(f"[{entity}]\n")
                for p in prefixes:
                    f.write(f"  gs://{bucket_name}/{p}/\n")

        print("\n" + "=" * 60)
        print(f"DONE -> {OUT.relative_to(ROOT).as_posix()}/")
        print(f"manifest: {manifest_latest.relative_to(ROOT).as_posix()}")
        if failures:
            status = "failed"
            detail = f"entidades com falha: {', '.join(failures)}"
            exit_code = 1
            print(f"[ERRO] {detail}")
        else:
            print("[OK] todas as entidades ingeridas")
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
            etapa="bronze",
            started_at=started_at,
            status=status,
            rows_in=rows_in,
            rows_out=rows_out,
            bytes_processed=bytes_total,
            detail=detail,
        )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
