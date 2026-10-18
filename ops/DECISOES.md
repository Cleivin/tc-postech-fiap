# Ops — decisões

Passos 8 e 9. Código: [`telemetry.py`](telemetry.py), [`prove_observability.py`](prove_observability.py), [`finops_snapshot.py`](finops_snapshot.py).  
Guia da pasta: [`README.md`](README.md). Evidência: [`evidence/passo_08/`](../evidence/passo_08/) e [`evidence/passo_09/`](../evidence/passo_09/).

## Observabilidade — o que o challenge pede

Tabela `alfabetizacao_ops.pipeline_runs` sempre em append, com duração, linhas, status e bytes. Falha bloqueante aparece no terminal, sai com exit diferente de zero e publica no tópico `alfabetizacao-alertas`. Duas runs seguidas não se apagam. Uma falha deixa registro e mensagem.

## Decisões de observabilidade

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| `INSERT` em `pipeline_runs` | `WRITE_TRUNCATE` ou uma linha “última run” | O guia pede histórico. As duas Silver de `20d3623d0430` (58,1 s e 56,2 s) convivem na tabela. |
| Quem descobre a falha, nesta entrega, é quem rodou o comando | E-mail, Slack ou política de Monitoring agora | A execução é manual, sem DAG. O aviso é o exit ≠ 0 no mesmo processo (na prova, 0,57 s). A linha `failed` fica em `pipeline_runs`. O tópico `alfabetizacao-alertas` recebe o JSON para quando houver agenda sem operador; hoje não há subscription. O e-mail de R$ 1,00 é só custo. |
| A prova de falha não roda a Silver de novo | Derrubar a Silver real para gerar o alerta | `prove_observability.py` grava `status=failed` e publica o JSON. Exit 1. A Gold oficial não é republicada por essa prova. |
| Latência de stream nas colunas `latency_*_s` quando `etapa = stream` | Tabela de métricas separada | O guia lista esses campos em `pipeline_runs`. |
| Tópico de alerta criado na primeira necessidade | Exigir o tópico já no teste de conexão | Um clone limpo ainda não passou pelo Passo 8. O teste de ambiente avisa e segue; a prova de observabilidade cria o tópico. |

### O que o snapshot realmente tem

`evidence/passo_09/pipeline_runs_snapshot.csv` contém três linhas, todas `etapa = silver`: duas `success` da run `20d3623d0430` e a falha `prove_fail_81ee7cf0f8ea`. Bronze, Gold e stream **não** aparecem nessa fotografia, embora `finish_run` já esteja ligado nesses scripts. A duração citada no FinOps (56,2 s) é a Silver que terminou às 19:54:39 UTC. Bytes de Bronze e de Gold foram lidos dos CSV de evidência, não dessa tabela.

`rows_in = rows_out = 3.913.901` na Silver é a soma das dez tabelas (os sete espelhos mais os três joins), não a contagem de alunos.

## FinOps — o que o challenge pede

Quantidade tirada de API ou de log, preço público com data, e uma cadência escrita como premissa. A execução atual cabe no Always Free. A coluna de custo é o que seria pago fora da cota.

## Decisões de FinOps

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Medir o bucket com `list_blobs` | Chutar “menos de 1 GB” | 135 objetos, 206.491.009 bytes (0,192 GiB). Bronze 0,190 GiB; Gold 0,002 GiB. |
| Bytes de query = soma Bronze + Silver + Gold da run de referência | Usar só o `dry_run` da Gold | O `dry_run` da Gold é 202.322.630 bytes. A conta do batch inteiro é 760.231.654 bytes (~0,021 TiB × 30). Os dois números estão no `custo.md`, com origem diferente. |
| Cadência 1 batch/dia e 1.000 eventos/dia | Tratar a demo de 20 mensagens como volume mensal | O guia separa o byte medido da premissa. A demo não é a projeção. |
| Payload Pub/Sub medido de novo (`n=20`, média 239,9 B) | Reusar só o stdout do Passo 7 | O stdout não guarda o tamanho em bytes. O script mede o JSON. A seed dessa medida não precisa ser a seed 7 da demo. |
| Preço de lista em 2026-10-18, região US / `us-central1` | Preço de memória de aula | GCS US$ 0,020/GiB-mês, BigQuery US$ 6,25/TiB, Pub/Sub US$ 40/TiB. Free tier: 5 GiB-mês, 1 TiB/mês, 10 GiB/mês. A projeção fica em US$ 0,00 depois da cota. |
| Computação = duração do job serverless | VM ou cluster no custo | Não há GCE nem GKE. O tempo entra como evidência de que o job liga e desliga; o dólar está nas linhas de BigQuery e Pub/Sub. |
| Parquet, partição, coluna explícita, mesma região, consumer que não fica ligado | Spark ou Kafka permanentes “porque a aula teve” | São as alavancas da aula de FinOps que este volume consegue usar. |

Reexecutar o batch acrescenta outra partição `run_id` no bucket. O estoque de 0,19 GiB já inclui duas runs de Bronze. Ainda fica longe dos 5 GiB do free tier de Storage.
