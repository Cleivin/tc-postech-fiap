# Passo 1 — análise das evidências

O passo não gera dado de alfabetização. Prova que a conta GCP usada pelo restante do pipeline existe e responde.

| Arquivo | O que é | O que se conclui |
|---------|---------|------------------|
| `test_gcp_connection.png` | Saída de `python test_gcp_connection.py` | O bucket está em `us-central1`. O BigQuery leu 5 linhas de `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`. `get_topic` achou `alfabetizacao-stream-topic`. |
| `billing-alertas-1-real.png` | Console de orçamento | Há alerta de billing em R$ 1,00. É o freio financeiro do free tier. Não é um PagerDuty. |
| `pubsub-subscription.png` | Console do Pub/Sub | Subscription **Pull** `alfabetizacao-stream-sub` no tópico de streaming, retenção de 7 dias. O consumer do Passo 7 faz pull nessa subscription; o código não a cria. |

## Ajuste feito no Passo 10

O script imprimia `[ERRO]` e, mesmo assim, encerrava com sucesso e a frase de ambiente pronto. Isso anulava o critério “falhar se `get_topic` não achar o tópico”. Agora Storage, BigQuery ou o tópico de streaming derrubam o processo (exit 1).

O tópico `alfabetizacao-alertas` não faz parte dessa trava. Ele é criado no Passo 8. Num clone em que o Passo 8 ainda não rodou, o teste avisa e segue.

## O que estes prints não dizem

Não medem custo, não contam linhas das seis entidades e não provam a subscription via API — a subscription está no print de console. Quem for reproduzir precisa criar bucket, tópico e subscription antes do teste, como está no README.
