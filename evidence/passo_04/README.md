# Passo 4 — Qualidade da Bronze

Escopo: somente Bronze (sem join / Silver).

Limiar `orphan_codes` = **0** (ver `docs/contrato_dados.md` → Limiares de qualidade).  
Tabela de checks: `alfabetizacao_ops.quality_checks` (append).

## Validate limpo

- comando: `python quality/validate.py --layer bronze`
- run_id: `20d3623d0430`
- blocking fails: **0**
- exit esperado: `0` se blocking fails = 0
- snapshot: `evidence/passo_04/validate_bronze_20d3623d0430.csv`

| entity | rule | class | status | value | threshold |
|--------|------|-------|--------|-------|-----------|
| alunos | null_keys | blocking | pass | 0.0 | 0.0 |
| alunos | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| alunos | orphan_codes | blocking | pass | 0.0 | 0.0 |
| alunos | row_count | informative | pass | 3867999.0 | 1.0 |
| municipio | null_keys | blocking | pass | 0.0 | 0.0 |
| municipio | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| municipio | orphan_codes | blocking | pass | 0.0 | 0.0 |
| municipio | row_count | informative | pass | 23995.0 | 1.0 |
| uf | null_keys | blocking | pass | 0.0 | 0.0 |
| uf | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| uf | orphan_codes | blocking | pass | 0.0 | 0.0 |
| uf | row_count | informative | pass | 145.0 | 1.0 |
| meta_alfabetizacao_brasil | null_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_brasil | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_brasil | row_count | informative | pass | 3.0 | 1.0 |
| meta_alfabetizacao_uf | null_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_uf | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_uf | row_count | informative | pass | 81.0 | 1.0 |
| meta_alfabetizacao_municipio | null_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_municipio | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| meta_alfabetizacao_municipio | row_count | informative | pass | 10704.0 | 1.0 |
| dicionario | null_keys | blocking | pass | 0.0 | 0.0 |
| dicionario | duplicate_keys | blocking | pass | 0.0 | 0.0 |
| dicionario | row_count | informative | pass | 27.0 | 1.0 |

---

## Prove failure

- comando: `python quality/prove_failure.py`
- prove_run_id: `prove_0c6d9f10ea09`
- fixture: `alfabetizacao_ops.fixture_dup_keys` (1 linha de `uf` duplicada)
- regra: `duplicate_keys` (blocking) → **fail**
- lake GCS Bronze: **nao** alterado
- exit esperado: `1`
- arquivos: `prove_failure_stdout.txt`, `prove_failure_checks.csv`

| run_id | layer | entity | rule | status | value | threshold |
|--------|-------|--------|------|--------|-------|-----------|
| prove_0c6d9f10ea09 | fixture | uf | duplicate_keys | **fail** | 1.0 | 0.0 |
