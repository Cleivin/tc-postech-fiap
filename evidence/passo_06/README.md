# Passo 6 — Gold (produto analitico)

- comando: `python gold/build.py --run_id 20d3623d0430`
- run_id_bronze: `20d3623d0430`
- dataset: `alfabetizacao_gold`
- bucket export: `gs://tc-postech-fiap-datalake/gold/`
- gate Silver join_match: **pass**
- conferencia fails: **0**
- exit esperado: `0` se conferencia fails = 0
- job_ids (amostra): `766879c2-d145-4a64-9c78-55ac87580a83, 839bf9df-6ccd-438b-925e-feb92f38af2f, 13201921-06ab-470f-ba26-3acfb222d9ad...`

## Contagens

| table | rows |
|-------|------|
| indicador_municipio | 23995 |
| indicador_uf | 145 |
| meta_vs_resultado | 10947 |
| evolucao_temporal | 24140 |
| validacao_microdado | 12408 |

## dry_run (bytes)

| step | total_bytes_processed | label |
|------|----------------------|-------|
| 1 | 3418524 | `CREATE OR REPLACE TABLE `tc-postech-fiap.alfabetizacao_gold.` |
| 2 | 19519 | `CREATE OR REPLACE TABLE `tc-postech-fiap.alfabetizacao_gold.` |
| 3 | 1049767 | `CREATE OR REPLACE TABLE `tc-postech-fiap.alfabetizacao_gold.` |
| 4 | 2343267 | `CREATE OR REPLACE TABLE `tc-postech-fiap.alfabetizacao_gold.` |
| 5 | 195491553 | `CREATE OR REPLACE TABLE `tc-postech-fiap.alfabetizacao_gold.` |

## Conferencia

| check | status | expected | observed | detail |
|-------|--------|----------|----------|--------|
| CE_2024_rede5 | pass | 85.31 | 85.31 | tol=0.05 |
| brasil_2024_meta | pass | 59.2 | 59.2 | meta_obs=80.0 meta_exp=80.0 status=nao_atingiu |

## Export Parquet

| table | uri_prefix |
|-------|------------|
| indicador_municipio | `gs://tc-postech-fiap-datalake/gold/indicador_municipio/ingestion_date=2026-10-18/run_id=20d3623d0430/` |
| indicador_uf | `gs://tc-postech-fiap-datalake/gold/indicador_uf/ingestion_date=2026-10-18/run_id=20d3623d0430/` |
| meta_vs_resultado | `gs://tc-postech-fiap-datalake/gold/meta_vs_resultado/ingestion_date=2026-10-18/run_id=20d3623d0430/` |
| evolucao_temporal | `gs://tc-postech-fiap-datalake/gold/evolucao_temporal/ingestion_date=2026-10-18/run_id=20d3623d0430/` |
| validacao_microdado | `gs://tc-postech-fiap-datalake/gold/validacao_microdado/ingestion_date=2026-10-18/run_id=20d3623d0430/` |

Snapshots: `manifest_*.csv`, `dry_run_bytes.csv`, `conferencia.csv`, `export_*.csv`.
