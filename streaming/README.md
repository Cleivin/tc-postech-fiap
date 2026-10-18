# Streaming — speed layer simulada (Passo 7)

Decisões: [`DECISOES.md`](DECISOES.md). Análise da demo: [`evidence/passo_07/ANALISE.md`](../evidence/passo_07/ANALISE.md).

Camada rápida da arquitetura Lambda. **Não** regrava o histórico oficial da Bronze/Silver/Gold batch.

| Peça | Papel |
|------|--------|
| `producer.py` | Publica documentos JSON no tópico Pub/Sub |
| `consumer.py` | Pull, valida, quarentena / dedupe / upsert |
| Tópico | `alfabetizacao-stream-topic` |
| Subscription (Pull) | `alfabetizacao-stream-sub` |
| Eventos bons (lake) | `gs://<bucket>/bronze/stream/ingestion_date=YYYY-MM-DD/` |
| Inválidos | `gs://<bucket>/bronze/stream_quarentena/` |
| Gold de stream | `alfabetizacao_gold.eventos_stream` (`origem = 'simulado'`) |

## Comandos

```powershell
python streaming/producer.py --n 20 --seed 42
python streaming/consumer.py --max-messages 50 --timeout 30
```

O producer, com `--n 20`, inclui ~18 válidos, **1 inválido** e **1 duplicata** do primeiro `event_id`.

## Payload (documento)

```json
{
  "event_id": "uuid",
  "produced_at": "2026-10-18T19:00:00+00:00",
  "entidade": "municipio",
  "chave": {"id_municipio": "2304400", "ano": 2024, "rede": "5", "serie": "2"},
  "valor": 72.5,
  "origem": "simulado"
}
```

- `produced_at`: gerado **só** no producer, no momento do publish.
- `ingested_at`: gerado **só** no consumer, no momento da ingestão.
- Latência = `ingested_at - produced_at` (nunca zero por construção se os relógios forem distintos entre os dois processos).

## Regras do consumer

| Caso | Ação |
|------|------|
| JSON quebrado / chave ausente / valor ∉ [0, 100] | Quarentena GCS; **não** entra em `eventos_stream`; ack após persistir |
| `event_id` já visto (memória ou MERGE) | Conta duplicata; **não** soma `valor` de novo |
| Evento bom | Append JSON em `bronze/stream/` + `MERGE` (insert se novo) em `eventos_stream` |

Ack só depois de persistir quarentena ou evento bom (at-least-once com dedupe).

## Separação oficial × simulado

Consultas do indicador oficial (produtos do Passo 6) usam `origem = 'oficial'`.  
A tabela `eventos_stream` deixa `origem = 'simulado'` visível. Número do simulador **não** entra na taxa oficial.

## Evidência

Run de prova em [`evidence/passo_07/`](../evidence/passo_07/).
