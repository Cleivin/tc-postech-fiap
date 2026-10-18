# Evidências do Tech Challenge — Fase 2

Organização por passo do guia [`docs/Tech_Challenge_Fase2_Passo_a_Passo.md`](../docs/Tech_Challenge_Fase2_Passo_a_Passo.md).

| Pasta | Passo | Conteúdo |
|-------|-------|----------|
| `passo_01/` | Ambiente GCP | Teste GCP + alertas R$ 1,00 + subscription Pub/Sub |
| `passo_02/` | Data Understanding | CSVs do perfil (`01_`–`05_`) + exploração (`06_*` via `sql/run_exploracao.py`) |
| `passo_03/` | Bronze | Parquet GCS + external tables `alfabetizacao_bronze` (`manifest_*.csv`, prova 2× `run_id`) |
| `passo_04/` | Qualidade Bronze | `validate` limpo + `prove_failure` (fixture duplicata); `alfabetizacao_ops.quality_checks` |
| `passo_05/` | Silver | `transform` + `validate --layer silver`; joins `*_com_meta`; `join_match` ≥ 0.95 |
| `passo_06/` | Gold | produtos `alfabetizacao_gold` + Parquet + dry_run + conferência |
| `passo_07/` | Streaming | producer/consumer Pub/Sub; `eventos_stream`; quarentena; dedupe; oficial inalterada |
| `passo_08/` | Observabilidade | `pipeline_runs` append (2 success) + failed + alerta Pub/Sub |
| `passo_09/` | FinOps | `custo.md` + CSVs medidos; leitura em `ANALISE.md` |
| `passo_10/` | README / clone | README da raiz, pins, consultas de leitura da Gold |
| `passo_11/` | Vídeo | ainda não gravado |

Cada pasta `passo_01/` … `passo_09/` tem um `ANALISE.md` com a leitura do artefato e, quando o arquivo é dado, o insight. Decisões de implementação: `DECISOES.md` na pasta do código (`bronze/`, `sql/`, `quality/`, `silver/`, `gold/`, `streaming/`, `ops/`). Comparação com o enunciado: [`docs/avaliacao_conformidade.md`](../docs/avaliacao_conformidade.md).
