# Passo 5 — Silver (limpar, tipar, juntar)

- comando: `python silver/transform.py --run_id 20d3623d0430`
- run_id_bronze: `20d3623d0430`
- dataset: `alfabetizacao_silver`
- limiar join_match (blocking): **0.95**
- blocking fails: **0**
- exit esperado: `0` se blocking fails = 0
- job_ids (amostra): `f13187c0-e947-4eb0-96bf-119385ed91d1, a9c21f8d-d8b3-4a83-9055-60e9f639d5f4, 67b95987-fa39-461a-b64b-e735a2eb2f9d...`

## Contagens

| table | rows |
|-------|------|
| dicionario | 27 |
| alunos | 3867999 |
| municipio | 23995 |
| uf | 145 |
| meta_alfabetizacao_municipio | 10704 |
| meta_alfabetizacao_uf | 81 |
| meta_alfabetizacao_brasil | 3 |
| municipio_com_meta | 10896 |
| uf_com_meta | 49 |
| brasil_com_meta | 2 |

## join_match

| entity | taxa_match | threshold | status | linhas_esquerda | linhas_com_par |
|--------|------------|-----------|--------|-----------------|----------------|
| municipio_com_meta | 0.9777900146842878 | 0.95 | pass | 10896 | 10654 |
| uf_com_meta | 1.0 | 0.95 | pass | 49 | 49 |
| brasil_com_meta | 1.0 | 0.95 | pass | 2 | 2 |

Snapshots: `manifest_*.csv`, `join_match_*.csv`.
