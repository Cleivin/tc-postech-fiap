# Passo 7 — Streaming simulado

- comandos:
  - `python streaming/producer.py --n 20 --seed 7`
  - `python streaming/consumer.py --max-messages 50 --timeout 30`
- topic: `alfabetizacao-stream-topic`
- subscription: `alfabetizacao-stream-sub`
- tabela: `tc-postech-fiap.alfabetizacao_gold.eventos_stream`
- projeto: `tc-postech-fiap`

## Metricas do consumer

| metrica | valor |
|---------|-------|
| mensagens_recebidas (lag do lote) | 20 |
| valid_inserted | 18 |
| duplicates_skipped | 1 |
| invalid_quarantine | 1 |
| latency_min_s | 7.423083 |
| latency_max_s | 23.701744 |
| latency_avg_s | 8.79770361111111 |
| latency_gt_0 | yes |
| max_n_por_event_id | 1 |
| oficial_inalterado | yes |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `producer_stdout.txt` | publish OK |
| `consumer_stdout.txt` | latencia, dups, quarentena |
| `eventos_stream_sample.csv` | linhas `origem=simulado` |
| `dedupe_check.csv` | `event_id` unico; valor nao dobrado |
| `quarentena_uris.txt` | path GCS do invalido |
| `oficial_inalterado.csv` | Gold oficial CE 2024 inalterada |
