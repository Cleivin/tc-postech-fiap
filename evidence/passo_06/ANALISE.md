# Passo 6 — análise das evidências

Run `20d3623d0430`. Dataset `alfabetizacao_gold`. Export em `gs://tc-postech-fiap-datalake/gold/`.

| Arquivo | Papel |
|---------|--------|
| `manifest_*.csv` | Linhas dos cinco produtos |
| `conferencia.csv` | CE 2024 rede 5 = 85,31; Brasil 2024 = 59,2 com meta 80 e status `nao_atingiu` |
| `dry_run_bytes.csv` | Bytes que cada `CREATE` leria |
| `export_*.csv` | Prefixo Parquet de cada produto |
| `README.md` | Resumo |

A conferência é o critério de pronto: o número da Gold é o número anotado no perfil, não um arredondamento novo. Tolerância do CE: 0,05 pp. O observado foi exatamente 85,31. Brasil: 59,2 e meta 80,0.

## Por que as contagens são essas

- `indicador_municipio` 23.995 e `indicador_uf` 145 copiam o agregado oficial inteiro, todas as redes. O painel não pode nascer só do recorte que tem meta.
- `meta_vs_resultado` 10.947 = 10.896 (municipal rede 3) + 49 (UF rede 5) + 2 (Brasil). A aritmética fecha com a Silver.
- `evolucao_temporal` 24.140 = 23.995 + 145. Há dois anos, então metade das séries nasce com `taxa_anterior` nula. Isso é o `LAG`, não dado faltando por engano.
- `validacao_microdado` 12.408 é menor porque o microdado só tem redes 2, 3 e 4 e o join é interno na mesma rede. Rede 5 (pública composta) e rede 0 (total) não têm par no aluno.

## Onde o byte é gasto

| Statement | Bytes no dry run |
|-----------|------------------|
| indicador município | 3.418.524 |
| indicador UF | 19.519 |
| meta × resultado | 1.049.767 |
| evolução | 2.343.267 |
| validação do microdado | 195.491.553 |

96,6% da Gold está na validação, que varre `alunos`. Os quatro produtos de painel juntos ficam em cerca de 6,8 MiB. Particionar e não reprocessar o microdado “por precaução” é o que segura a conta do Passo 9.

## Leitura analítica (consulta de volta em 2026-10-18)

Os CSV deste passo provam integridade e conferência. A distribuição abaixo foi lida de `alfabetizacao_gold` e registrada em [`../passo_10/insights_consultas.md`](../passo_10/insights_consultas.md).

**Meta municipal (rede 3), 5.448 municípios por ano**

| Ano | Atingiu 80 | Não atingiu | Sem meta |
|-----|------------|-------------|----------|
| 2023 | 935 (17%) | 4.367 | 146 |
| 2024 | 1.141 (21%) | 4.211 | 96 |

Quem atingiu tem taxa média 88,5. Quem não atingiu, 55,2. Quem está sem meta, 53,7 — a lacuna de cadastro não é “município que já passou e ficou de fora da meta”. O gap desses 242 é nulo de propósito.

**UF rede pública.** Só o Ceará ≥ 80, nos dois anos. As outras 47 linhas UF×ano estão `nao_atingiu` (média 54,2, gap médio −25,8 pp). Brasil: −24,1 pp em 2023 e −20,8 pp em 2024. Subiu, e o status continua `nao_atingiu` porque a régua é 80, não a meta intermediária de 59,9 em 2024.

**Microdado.** Em 12.408 linhas, a diferença absoluta mediana é 0,0037 pp e o p95 é 0,046 pp. 57 linhas passam de 1 pp. A maior é −36,06 pp (município 2305100, rede 3, 2023, peso 72, oficial 91,67 contra micro 55,61). O caso típico confirma o agregado; a cauda fica visível em `diff_pp` em vez de ser escondida.

**Níveis de proficiência.** 2023: 11.547 linhas municipais com `proporcao_aluno_nivel_0` nula. 2024: 12.448 linhas, zero nulos nessa coluna. Feature de composição por nível não existe para 2023. Preencher com 0 diria que ninguém está no nível 0.
