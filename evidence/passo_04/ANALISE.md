# Passo 4 — análise das evidências

Escopo: qualidade da Bronze da run `20d3623d0430`, mais uma falha provocada fora do lake.

| Arquivo | O que prova |
|---------|-------------|
| `validate_bronze_20d3623d0430.csv` e `validate_bronze_latest.csv` | 0 falhas bloqueantes. Exit esperado 0. |
| `prove_failure_stdout.txt` | `prove_failure.py` terminou em falha. |
| `prove_failure_checks.csv` | A linha `duplicate_keys` com status `fail` foi para `quality_checks`. |

## Carga limpa

Cada entidade de fato (alunos, município, UF) passou em `null_keys`, `duplicate_keys` e `orphan_codes`, todos com valor 0 e limiar 0. Metas e dicionário passaram em chave nula e chave duplicada. `row_count` só registra: 3.867.999, 23.995, 145, 3, 81, 10.704, 27 — os mesmos inteiros do perfil e da Bronze.

`orphan_codes` não roda nas metas. Se rodasse, `Pública` e `Municipal` apareceriam como código órfão e a carga oficial seria reprovada por uma anomalia já explicada no Passo 2. A decisão está em [`quality/DECISOES.md`](../../quality/DECISOES.md).

O CSV de órfãos do Passo 2 repete linhas de município/UF por causa da consulta. Aqui `duplicate_keys = 0` fecha essa dúvida: o grain da Bronze é único.

## Falha provocada

`prove_run_id = prove_0c6d9f10ea09`. Fixture `alfabetizacao_ops.fixture_dup_keys`: uma linha de UF duplicada. A regra bloqueante viu `value = 1` contra limiar 0 e gravou `fail`. O Parquet em `gs://…/bronze/` não foi mexido.

Isso separa duas coisas que o guia pede juntas: a regra sabe falhar, e a falha não destrói o histórico. Um `except` que imprimisse o erro e devolvesse sucesso não teria deixado esta linha com status `fail` nem exit 1.
