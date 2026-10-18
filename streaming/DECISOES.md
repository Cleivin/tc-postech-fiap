# Streaming — decisões

Passo 7. Código: [`producer.py`](producer.py), [`consumer.py`](consumer.py).  
Guia da pasta: [`README.md`](README.md). Evidência: [`evidence/passo_07/`](../evidence/passo_07/).

## O que o challenge pede

Camada rápida da arquitetura Lambda. Documento JSON no Pub/Sub, com `event_id`, `produced_at` no produtor, chave municipal e `origem = simulado`. O consumidor grava `ingested_at`, mede latência, manda inválido para quarentena, não soma duplicata e não altera o indicador oficial.

## O que a demo mostrou

`producer --n 20 --seed 7` e o consumer na subscription `alfabetizacao-stream-sub`: 20 mensagens, 18 inserts, 1 duplicata, 1 quarentena (`valor_fora_dominio_0_100`). Latência mínima 7,42 s, máxima 23,70 s, média 8,80 s. CE 2024 rede 5 permaneceu 85,31 antes e depois.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Pub/Sub no lugar de Kafka | Cluster Kafka local ou gerenciado | O conceito da aula (produtor, tópico, consumidor, lag, duplicata, dois relógios) cabe no serviço gerenciado. Cluster ligado o tempo todo estoura o free tier neste volume. |
| Evento fictício, não um feed do Inep | “Streaming” relendo a Bronze | O Inep não publica este indicador em tempo real. A camada rápida é simulada e o README diz isso. |
| `produced_at` só no `publish`; `ingested_at` só no consumer | Um único timestamp | A latência é a diferença. Se o consumidor copiasse o relógio de produção, a latência seria zero por construção. |
| Duplicata = reenvio do mesmo payload (mesmo `event_id` e mesmo `produced_at`) | Segundo evento com outro relógio e o mesmo id | É o comportamento *at-least-once*: a mesma mensagem entregue de novo. O `MERGE` por `event_id` não soma `valor` outra vez. |
| Inválido aleatório entre JSON quebrado, chave ausente e valor 150 | Sempre o mesmo defeito | A demo de 2026-10-18 caiu em valor fora de [0, 100]. O arquivo foi para `bronze/stream_quarentena/` e só então houve ack. |
| Evento bom em `bronze/stream/` + `MERGE` em `alfabetizacao_gold.eventos_stream` | Atualizar `indicador_municipio` | A tabela oficial tem `origem = oficial`. Misturar o simulacro mudaria o 85,31 do Ceará, que a evidência mostra intacto. |
| Latência do lote = min/média/máx das mensagens recebidas | Lag de partição no estilo Kafka | Não há partição de log para inspecionar. O número que existe é o relógio. Os ~7 s são o tempo até o pull; os 23,7 s são uma mensagem que chegou no pull seguinte, não um cálculo pesado. |
| Consumer sob demanda | Processo 24/7 | A cadência do challenge é uma demo. Deixar o consumidor ligado seria o custo contínuo que a aula de FinOps pede para evitar. |

## Comparação com o batch

| | Batch (Passos 3–6) | Stream (Passo 7) |
|--|--------------------|------------------|
| Latência | A run Silver medida levou ~56 s, e o batch inteiro é da ordem de minutos | Segundos entre `produced_at` e `ingested_at` (7–24 s nesta demo) |
| Frequência | Carga completa, quando alguém roda o script | Uma mensagem por evento |
| Garantia | Snapshot da fonte naquela run (`run_id`) | *At-least-once*, com dedupe por `event_id` |

O CSV `dedupe_check.csv` tem mais de 18 `event_id` porque `eventos_stream` acumula demos anteriores. O critério desta demo é outro: cada `event_id` aparece uma vez (`n = 1`) e o consumer contou `duplicates_skipped = 1`.
