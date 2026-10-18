# Passo 7 — análise das evidências

Demo com `--n 20 --seed 7`. Tópico `alfabetizacao-stream-topic`, subscription `alfabetizacao-stream-sub`.

| Arquivo | O que mostra |
|---------|----------------|
| `producer_stdout.txt` | 20 publishes aceitos pelo tópico |
| `consumer_stdout.txt` | 20 recebidas, 18 inserts, 1 dup, 1 quarentena, latências |
| `eventos_stream_sample.csv` | Linhas com `origem = simulado` |
| `dedupe_check.csv` | Cada `event_id` com `n = 1` e `ok_sem_dobra = yes` |
| `quarentena_uris.txt` | Um objeto em `bronze/stream_quarentena/` |
| `oficial_inalterado.csv` | CE 2024 rede 5 = 85,31 antes e depois |
| `README.md` | Tabela-resumo |

## Latência

O mínimo é 7,42 s (`aa926729-…`) e o máximo é 23,70 s (`57eb3b3d-…`). Esse máximo é a mensagem que chegou no segundo pull, cerca de 15 s depois do primeiro lote. Não é tempo de transformação: o consumer não agrega o país, só valida, grava JSON e faz `MERGE`. A métrica cumpre o papel do lag da aula de Kafka com o relógio que o Pub/Sub deixa medir.

A latência é maior que zero em todas as linhas inseridas. `produced_at` não foi copiado para `ingested_at`.

## Duplicata e inválido

A duplicata reconhecida em memória foi `51c2722f-0b71-4f3b-96fb-d1f5c5d6658b`. O valor dela entra uma vez. O `dedupe_check.csv` lista dezenas de `event_id` além dos 18 desta demo: a tabela `eventos_stream` acumula execuções anteriores do simulador. O que a demo prova é o contador `duplicates_skipped = 1` e que nenhuma chave ficou com `n > 1`.

A mensagem rejeitada teve motivo `valor_fora_dominio_0_100` (o produtor sorteou valor 150, não JSON quebrado). O URI está em `quarentena_uris.txt`. Ela não aparece em `eventos_stream`. O ack foi depois da gravação no GCS.

## O oficial não se move

`oficial_inalterado.csv`: uma linha, soma 85,31, média 85,31, nos dois momentos. O simulador escreve `origem = simulado` numa tabela separada. Consulta de indicador oficial que filtre `origem = 'oficial'` não vê esses valores (43–93 na amostra de dedupe), que são aleatórios e não são taxa do Inep.

Os ~240 bytes por mensagem medidos no Passo 9 não estão nestes stdout; o tamanho do payload foi medido à parte, porque o log não guarda o tamanho.
