# Ops — observabilidade e FinOps

Decisões: [`DECISOES.md`](DECISOES.md).

| Script | Passo | Papel |
|--------|-------|--------|
| [`telemetry.py`](telemetry.py) | 8 | `pipeline_runs` (append) + alerta Pub/Sub |
| [`prove_observability.py`](prove_observability.py) | 8 | prova: 2 success + 1 failed com alerta |
| [`finops_snapshot.py`](finops_snapshot.py) | 9 | mede GCS / BQ / Pub/Sub e gera `custo.md` |

## Passo 8 — o que grava

**Tabela:** `alfabetizacao_ops.pipeline_runs` (sempre `INSERT`, nunca truncate).

**Tópico de alerta:** `alfabetizacao-alertas` — criado sob demanda em `ensure_alert_topic`.

**Instrumentado em:** `bronze/ingest_batch.py`, `silver/transform.py`, `gold/build.py`, `streaming/consumer.py` via `finish_run`.

Latência de stream: colunas `latency_min_s` / `latency_max_s` / `latency_avg_s` quando `etapa = stream`.

## Prova (Passo 8)

```powershell
python ops/prove_observability.py --run_id 20d3623d0430
```

Exit esperado: `1` (falha provocada no final). Evidência em `evidence/passo_08/`.

## Passo 9 — FinOps

```powershell
python ops/finops_snapshot.py
python ops/finops_snapshot.py --batch-per-month 30 --events-per-day 1000
```

O script **não inventa** quantidade: lista o bucket, lê `pipeline_runs` (e completa com evidências dos passos 3/6/7 se alguma etapa ainda não tiver telemetria), mede o payload do producer e aplica preços públicos GCP (data da consulta no `custo.md`).

Saída: `evidence/passo_09/custo.md` + CSVs. Premissa padrão de projeção = 1 batch/dia + 1.000 eventos/dia.
