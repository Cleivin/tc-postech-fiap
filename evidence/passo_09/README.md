# Passo 9 — FinOps com numero medido

- comando: `python ops/finops_snapshot.py`
- saida principal: [`custo.md`](custo.md)
- precos publicos GCP consultados em: **2026-10-18**
- cadencia de projecao (premissa): **1 batch/dia** + **1000 eventos/dia**
- leitura: execucao atual do challenge cabe no Always Free; projecao com cadencia = **dentro do Always Free**

## Criterio de pronto

| check | resultado |
|-------|-----------|
| quantidade GCS via API | `gcs_objects_by_prefix.csv` |
| bytes/duracao de `pipeline_runs` | `pipeline_runs_snapshot.csv` |
| dry_run Gold (Passo 6) | referenciado em `custo.md` |
| bytes Pub/Sub do lote demo | `pubsub_payload_sample.csv` |
| tabela custo + premissa na mesma pagina | `custo.md` |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `custo.md` | tabela + premissas + decisoes FinOps |
| `cost_projection.csv` | mesma tabela em CSV |
| `gcs_objects_by_prefix.csv` | tamanho real do bucket |
| `pipeline_runs_snapshot.csv` | bytes e duracao medidos |
| `pubsub_payload_sample.csv` | bytes do payload do teste |
