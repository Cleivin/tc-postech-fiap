# FinOps — custo medido (Passo 9)

**Data do snapshot:** 2026-10-18  
**Precos publicos consultados em:** 2026-10-18  
**Fontes:** [GCS](https://cloud.google.com/storage/pricing) · [BigQuery](https://cloud.google.com/bigquery/pricing) · [Pub/Sub](https://cloud.google.com/pubsub/pricing) · [Always Free](https://cloud.google.com/free)

## Premissa de cadencia (projecao)

Os **bytes** e as **duracoes** abaixo vieram de API/log do projeto. A **cadencia** e premissa hipotetica de producao — nao e o que roda hoje:

- **Batch:** 30 execucao(oes)/mes (≈ 1 batch/dia)
- **Stream:** 1000 eventos/dia
- A execucao atual do challenge (poucas runs manuais + demo de 20 eventos) **cabe no Always Free**. A coluna da direita e o custo **se** essa cadencia rodasse de forma continua **fora da cota gratuita** (apos descontar o free tier).

## Tabela de custo

| Servico | Unidade | Quantidade medida | Preco unitario | Custo mensal projetado |
|---------|---------|-------------------|----------------|------------------------|
| Cloud Storage | GiB-mes | 0.192310 GiB | $0.020/GiB-mes | $0.00 |
| BigQuery | TiB processados/mes | 0.020743 TiB/mes | $6.25/TiB | $0.00 |
| Pub/Sub | GiB mensagens/mes | 0.013405 GiB/mes | $40/TiB | $0.00 |
| Computacao do job | segundos (serverless) | 56.2 s (ref. 1 ciclo) | embutido (serverless) | $0.00 |
| **Total projetado (apos free tier)** | | | | **$0.00** |

> **Leitura:** com a cadencia acima, o uso estimado ainda fica **dentro do Always Free** (custo projetado ≈ $0 apos o free tier). O valor didatico da tabela e mostrar a conta com quantidade real, nao inventar fatura.

## De onde veio cada quantidade

### Cloud Storage (tamanho real do bucket)

- Bucket: `tc-postech-fiap-datalake`
- Objetos: **135**
- Bytes: **206491009** (0.192310 GiB)

| prefixo | objetos | bytes | GiB |
|---------|---------|-------|-----|
| `bronze` | 120 | 204191600 | 0.190168 |
| `gold` | 15 | 2299409 | 0.002141 |

### BigQuery (`pipeline_runs` + dry_run Gold)

Bytes/duracao por etapa — `pipeline_runs` quando existir; senao evidencias dos passos anteriores (mesmos jobs, sem chute):

| etapa | run_id | duration_s | bytes_processed | fonte |
|-------|--------|------------|-----------------|-------|
| bronze | `20d3623d0430` | n/d | 271547681 | `evidence/passo_03/manifest_20d3623d0430.csv` |
| silver | `20d3623d0430` | 56.157 | 276408457 | `pipeline_runs` |
| gold | `20d3623d0430` | n/d | 212275516 | `evidence/passo_06/dry_run_bytes.csv + export_*.csv` |
| stream | `passo_07_demo` | n/d | 0 | `evidence/passo_07/consumer_stdout.txt` |

- Soma batch (bronze+silver+gold) por execucao: **760231654** bytes
- Dry-run Gold (`evidence/passo_06/dry_run_bytes.csv`): **202322630** bytes
- Duracao batch medida: **56.2** s
- Latencia media stream (Passo 7/8): **8.798** s

### Pub/Sub (bytes do teste)

- Lote demo igual ao producer (`n=20`, seed=42): **4798** bytes de payload
- Media por mensagem: **239.9** B
- Throughput estimado (publish + subscribe ≈ 2×): **9596** B no lote de teste
- Projecao: media × 1000 eventos/dia × 30 × 2

## Decisoes de arquitetura que a aula de FinOps pede

| Decisao | Por que baixa o custo neste projeto |
|---------|-------------------------------------|
| **Parquet comprimido** no lake | Menos GiB no GCS e menos bytes lidos quando o BigQuery varre external/export |
| **Particao** por `ingestion_date`/`run_id` (Bronze) e por `ano` (Silver/Gold) | Evita full scan; dry_run do Passo 6 mostra o volume real por statement |
| **Colunas explicitas** (sem `SELECT *` na extracao) | Menos `bytes_processed` no EXPORT e nas transforms |
| **GCS `us-central1` + BigQuery `US`** | Mesma area geografica; sem cobranca de transferencia desnecessaria lake→warehouse |
| **Pub/Sub + consumer sob demanda** (sem cluster Kafka 24/7) | Paga so pelo throughput do evento; aula trata cluster ligado o tempo todo como custo continuo |
| **SQL serverless no BigQuery** (sem Spark/GKE) | Job liga e desliga; a linha de computacao nao tem VM ociosa |
| **Alerta de billing R$ 1,00** (Passo 1) | Freio financeiro antes do uso sair do free tier |

## Como reproduzir

```powershell
python ops/finops_snapshot.py
python ops/finops_snapshot.py --batch-per-month 30 --events-per-day 1000
```

Artefatos: `gcs_objects_by_prefix.csv`, `pipeline_runs_snapshot.csv`, `cost_projection.csv`, `pubsub_payload_sample.csv`, este `custo.md`.
