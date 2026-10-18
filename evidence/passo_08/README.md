# Passo 8 — Observabilidade

- comando: `python ops/prove_observability.py --run_id 20d3623d0430`
- tabela: `alfabetizacao_ops.pipeline_runs` (sempre **append**)
- topico alerta: `alfabetizacao-alertas`
- silver run_id usado nas 2 successes: `20d3623d0430`

## Criterio de pronto

| check | resultado |
|-------|-----------|
| duas runs success (append) | **2** linhas em `pipeline_runs_two_success.csv` |
| falha registra status=failed | run_id=`prove_fail_81ee7cf0f8ea` |
| alerta Pub/Sub | message_id=`22579172021738768` |
| exit da prova | `1` (falha provocada) |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `pipeline_runs_console.png` | print BigQuery: 2 success + 1 failed |
| `pipeline_runs_two_success.csv` | 2a run nao apagou a 1a |
| `pipeline_runs_failed.csv` | linha failed |
| `alert_publish.txt` | publish no topico de alertas |
| `prove_stdout.txt` | stdout completo |
