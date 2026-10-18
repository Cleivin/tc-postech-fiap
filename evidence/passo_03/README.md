# Passo 3 — Bronze (Parquet no GCS + external tables)

- comando: `python bronze/ingest_batch.py`
- run_id (esta execucao / manifesto abaixo): `20d3623d0430`
- run_id anterior (intacta): `f92c40cfe9a7` — ver `manifest_f92c40cfe9a7.csv`
- ingestion_date (UTC): `2026-10-18`
- bucket: `tc-postech-fiap-datalake`
- dataset BQ canônico: `alfabetizacao_bronze` (único Bronze; não usar `bronze_alfabetizacao`)
- listagem acumulada de prefixos: `gcs_run_prefixes.txt`

Bronze e raw: sem regra de negocio. A anomalia de encoding de `rede` (codigo vs rotulo nas metas) e preservada para a Silver.

Colunas tecnicas: `ingestion_ts` e `source_table` no Parquet; `ingestion_date` e `run_id` como particoes Hive da external table (consulta SQL enxerga as quatro).

## Manifesto desta run

| entidade | n_linhas | export_job_id | bytes_processed | gcs_prefix | n_parquet | external_table |
|----------|----------|---------------|-----------------|------------|-----------|----------------|
| alunos | 3867999 | `997dd56e-c5bf-4c87-ba41-4767502c8625` | 268545240 | `gs://tc-postech-fiap-datalake/bronze/alunos/ingestion_date=2026-10-18/run_id=20d3623d0430` | 11 | `tc-postech-fiap.alfabetizacao_bronze.alunos` |
| municipio | 23995 | `68a51cc8-76c0-4733-91e4-b0aa350ac5c4` | 1832061 | `gs://tc-postech-fiap-datalake/bronze/municipio/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.municipio` |
| uf | 145 | `41687206-a4d3-448d-80a4-58dda9624514` | 10330 | `gs://tc-postech-fiap-datalake/bronze/uf/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.uf` |
| meta_alfabetizacao_brasil | 3 | `dc42e164-1b02-49d0-8718-cf91a37f31a2` | 270 | `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_brasil/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.meta_alfabetizacao_brasil` |
| meta_alfabetizacao_uf | 81 | `56e40cb1-a351-4af5-bdc5-a3634c0ab542` | 7374 | `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_uf/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.meta_alfabetizacao_uf` |
| meta_alfabetizacao_municipio | 10704 | `61b08af1-e02a-4f83-8b90-4343593200fd` | 1151232 | `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_municipio/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.meta_alfabetizacao_municipio` |
| dicionario | 27 | `52f7082d-8ed3-46b5-9230-9d93a1b0355b` | 1174 | `gs://tc-postech-fiap-datalake/bronze/dicionario/ingestion_date=2026-10-18/run_id=20d3623d0430` | 1 | `tc-postech-fiap.alfabetizacao_bronze.dicionario` |

## Prova de historico (append)

Cada run cria um novo `run_id` sob `bronze/<entidade>/`. Prefixos existentes nao sao apagados.

### alunos

- `gs://tc-postech-fiap-datalake/bronze/alunos/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/alunos/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### municipio

- `gs://tc-postech-fiap-datalake/bronze/municipio/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/municipio/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### uf

- `gs://tc-postech-fiap-datalake/bronze/uf/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/uf/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### meta_alfabetizacao_brasil

- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_brasil/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_brasil/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### meta_alfabetizacao_uf

- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_uf/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_uf/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### meta_alfabetizacao_municipio

- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_municipio/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/meta_alfabetizacao_municipio/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

### dicionario

- `gs://tc-postech-fiap-datalake/bronze/dicionario/ingestion_date=2026-10-18/run_id=20d3623d0430/`
- `gs://tc-postech-fiap-datalake/bronze/dicionario/ingestion_date=2026-10-18/run_id=f92c40cfe9a7/`

## Como a Silver deve ler

Filtrar a **ultima** `ingestion_date` / `run_id` (ou a passada por parametro). Nao fazer `SELECT *` misturando runs.

Arquivo maquina: `evidence/passo_03/manifest_20d3623d0430.csv` (e `manifest.csv` = ultima run).
