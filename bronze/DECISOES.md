# Bronze — decisões

Passo 3. Código: [`ingest_batch.py`](ingest_batch.py). Evidência: [`evidence/passo_03/`](../evidence/passo_03/).  
Comparação com o enunciado: [`docs/avaliacao_conformidade.md`](../docs/avaliacao_conformidade.md).

## O que o challenge pede

Extrair as seis entidades e o `dicionario` do BigQuery público, gravar Parquet cru no GCS com histórico (uma run nova não apaga a anterior) e registrar external tables em `alfabetizacao_bronze` para a Silver consultar em SQL.

## O que foi feito

Run de referência `20d3623d0430`. A run anterior `f92c40cfe9a7` continua no bucket, no mesmo `ingestion_date=2026-10-18`. As contagens batem com o perfil do Passo 2, linha a linha: alunos 3.867.999, município 23.995, UF 145, meta Brasil 3, meta UF 81, meta município 10.704, dicionário 27. A contagem lida de volta pela external table é igual à contagem exportada.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| ELT: copiar o valor oficial sem regra de negócio | Limpar `rede` ou preencher nulo já na extração | A anomalia de encoding (código versus rótulo) e o nulo de RR precisam chegar intactos. A regra mora na Silver. |
| Só as colunas do contrato | `SELECT *` | Menos bytes no EXPORT. Alunos sozinho é 268.545.240 dos 271.547.681 bytes desta run. |
| `EXPORT DATA` do BigQuery direto para o GCS | Baixar 3,8 milhões de linhas no pandas | O microdado não precisa passar pela RAM da máquina. O padrão da aula de Spark (não trazer a base inteira) vale aqui com SQL. |
| Path `bronze/<entidade>/ingestion_date=/run_id=/` | Sobrescrever `bronze/<entidade>/` | O guia exige append de partição. `overwrite=true` do EXPORT vale só para o URI da run nova, que nasce vazio. |
| `run_id` e `ingestion_date` só no path Hive | Repetir `run_id` também como coluna do Parquet | Evita coluna duplicada entre arquivo e partição. `ingestion_ts` e `source_table` ficam no arquivo. |
| External table no prefixo da entidade (`bronze/alunos/*`) | Uma external table por run | A Silver filtra `run_id`. O histórico permanece consultável. `require_hive_partition_filter = false` porque o script de qualidade também conta a partição explicitamente. |
| Dataset `alfabetizacao_bronze` em `US` | `bronze_alfabetizacao` ou região do bucket | O guia trava o nome. BigQuery do projeto está em `US`; o bucket está em `us-central1`, que fica nessa multi-região. |
| `dicionario` entra na Bronze | Tratar o dicionário como arquivo solto no repo | A tradução de código não pode ser uma tabela digitada à mão. |

Colunas técnicas permitidas e usadas: `ingestion_ts`, `source_table` no Parquet; `ingestion_date` e `run_id` na partição.

## O que esta camada não faz

Não traduz `rede`, não calcula taxa, não descarta RR e não escolhe a “rede certa” para a meta. Isso é Silver.
