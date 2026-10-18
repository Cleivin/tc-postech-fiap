# Passo 8 — análise das evidências

| Arquivo | O que prova |
|---------|-------------|
| `pipeline_runs_two_success.csv` | Duas linhas `success` da mesma run Silver, horários diferentes |
| `pipeline_runs_failed.csv` | Uma linha `failed` que não apagou as anteriores |
| `pipeline_runs_console.png` | As três linhas no console do BigQuery |
| `alert_publish.txt` | `message_id` no tópico `alfabetizacao-alertas` |
| `prove_stdout.txt` e `prove_stdout_console.txt` | A prova termina com erro, de propósito |
| `README.md` | Índice |

## Append

As duas execuções de `20d3623d0430` / `etapa = silver`:

| Início (UTC) | Duração | Linhas | Bytes | Status |
|--------------|---------|--------|-------|--------|
| 19:52:42 | 58,08 s | 3.913.901 | 276.408.457 | success |
| 19:53:43 | 56,16 s | 3.913.901 | 276.408.457 | success |

A segunda não substituiu a primeira. 3.913.901 é a soma das dez tabelas Silver (espelhos + três joins), coerente com o manifesto do Passo 5. Os bytes (~276 MiB) são a leitura da transformação, maior que o export da Bronze (~272 MiB) porque a Silver varre de novo o que a external table expõe e grava tabela nativa.

## Falha e alerta

`prove_fail_81ee7cf0f8ea`: duração 0,57 s, `rows_in = 0`, `bytes_processed = 0`, `status = failed`. O detalhe diz que Silver/Gold não são publicáveis. Não houve `CREATE` de produto nessa prova — o tempo curto e o zero de bytes são o sinal disso.

`alert_publish.txt`: tópico `projects/tc-postech-fiap/topics/alfabetizacao-alertas`, `message_id = 22579172021738768`, payload com o mesmo `run_id` e o mesmo texto da linha `failed`. Quem faz pull nesse tópico recebe o alerta. O e-mail de orçamento (Passo 1) é o outro canal, e não disparou aqui porque a prova não gasta cota.

## Limite desta evidência

Este pacote não contém linha `etapa = bronze`, `gold` ou `stream`. A instrumentação desses scripts existe; a fotografia usada no Passo 8 e no Passo 9 é a Silver mais a falha simulada. Duração de Bronze e de Gold não deve ser citada como se estivesse nesta tabela.
