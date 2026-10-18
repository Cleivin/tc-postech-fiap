# Passo 9 — análise das evidências

A página de custo é [`custo.md`](custo.md). Este arquivo diz de qual CSV cada número saiu e o que a conta permite afirmar.

| Arquivo | Origem do número |
|---------|------------------|
| `gcs_objects_by_prefix.csv` | `list_blobs` no bucket `tc-postech-fiap-datalake` |
| `pipeline_runs_snapshot.csv` | Três linhas de `pipeline_runs` (só Silver) |
| `dry_run_gold_ref.csv` | Cópia de referência dos bytes do Passo 6 |
| `pubsub_payload_sample.csv` | Tamanho do JSON do producer, lote de 20 |
| `cost_projection.csv` | A tabela do `custo.md` em colunas |

## Estoque e processamento

135 objetos, 206.491.009 bytes (0,192 GiB). Bronze 120 objetos / 0,190 GiB — são as duas runs Parquet mais os JSON do stream e da quarentena. Gold 15 objetos / 0,002 GiB — os cinco produtos exportados. Não há prefixo `silver/` no lake: a Silver ficou no BigQuery, que é o desenho ELT.

Bytes de um batch, somados como o `custo.md` declara:

| Etapa | Bytes | De onde |
|-------|-------|---------|
| Bronze | 271.547.681 | Soma do manifesto `20d3623d0430` |
| Silver | 276.408.457 | `pipeline_runs` |
| Gold | 212.275.516 | dry run dos `CREATE` (202.322.630) + export |
| Soma | 760.231.654 | ~0,71 GiB por batch |

× 30 batches = 0,0207 TiB/mês, contra 1 TiB gratuito de query. A linha que manda nesse total, dentro da Gold, é a validação do microdado (~195 MiB no dry run). Repetir só os indicadores de município e UF custaria uma fração disso.

Duração citada: 56,2 s. É a Silver das 19:54 UTC, não a soma Bronze+Gold. O snapshot não tem essas outras durações.

## Pub/Sub e a projeção

Média de 239,9 bytes por mensagem no lote de 20 (4.798 bytes no total). A projeção usa 1.000 eventos/dia × 30 × 2 (publish e subscribe) = 0,013 GiB/mês, contra 10 GiB gratuitos. A demo de 20 mensagens não é o volume mensal; a cadência está escrita como premissa no `custo.md`.

## O que a tabela de preço afirma — e o que não afirma

Com os preços de lista consultados em 2026-10-18 (Storage US$ 0,020/GiB-mês, BigQuery US$ 6,25/TiB, Pub/Sub US$ 40/TiB) e os free tiers de 5 GiB, 1 TiB e 10 GiB, as três linhas caem em US$ 0,00. Não é uma fatura do billing exportada. É a conta “se a cadência rodasse e a cota gratuita ainda existisse”. Fora da cota, o mesmo uso seria pequeno, mas o README não troca o $0,00 medido dentro do free tier por um custo inventado.

O alerta de R$ 1,00 continua sendo o limite operacional: a projeção cabe na cota, e o orçamento avisa se um `SELECT` sem filtro ou um loop de export sair dela.

Parquet, partição, colunas explícitas e a ausência de cluster 24/7 são o que mantém o bucket em 0,19 GiB mesmo com duas runs completas de Bronze. Uma terceira run acrescenta outra partição; não regrava a anterior.
