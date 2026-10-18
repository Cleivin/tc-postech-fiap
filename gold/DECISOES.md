# Gold — decisões

Passo 6. Código: [`build.py`](build.py) e [`sql/03_gold.sql`](../sql/03_gold.sql).  
Guia da camada: [`README.md`](README.md). Evidência: [`evidence/passo_06/`](../evidence/passo_06/).  
Números lidos de volta na Gold em 2026-10-18: [`evidence/passo_10/insights_consultas.md`](../evidence/passo_10/insights_consultas.md).

## O que o challenge pede

Cinco produtos com nome estável, publicados só se a Silver passou no gate. As três perguntas do enunciado são indicador por município, distância até a meta pactuada e evolução. A validação do microdado é o diferencial. Partição por ano, cluster geográfico, `dry_run` com bytes, e export Parquet para a Fase 3. Dizer quais colunas vazam o alvo.

## O que a run publicou

| Produto | Linhas | Conta que fecha |
|---------|--------|-----------------|
| `indicador_municipio` | 23.995 | Igual ao agregado oficial, todas as redes |
| `indicador_uf` | 145 | Igual ao agregado de UF |
| `meta_vs_resultado` | 10.947 | 10.896 + 49 + 2 |
| `evolucao_temporal` | 24.140 | 23.995 + 145 |
| `validacao_microdado` | 12.408 | Só o grain em que existe microdado e agregado com a mesma rede |

Conferência: CE 2024, rede 5, taxa 85,31. Brasil 2024, taxa 59,2, meta 80, status `nao_atingiu`.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Indicador municipal/UF copia o agregado oficial, não recalcula pelo microdado | Substituir a taxa do Inep pela taxa dos alunos | O produto de painel tem de bater com o número oficial. O microdado entra numa tabela própria, com `diff_pp`. |
| Meta × resultado só no grain que tem de-para (municipal rede 3, UF rede 5, Brasil) | Cruzar meta com todas as 23.995 linhas | Rede estadual pura não tem meta `Pública`. Forçar o join misturaria recortes. |
| Três estados: `atingiu`, `nao_atingiu`, `sem_meta` | Dois estados, com nulo virando “não atingiu” | 242 linhas municipais estão sem meta (146 em 2023, 96 em 2024). A taxa média delas é 53,7 — não são um vazio aleatório de quem já passou de 80. |
| Status contra a meta 80, não contra a meta do ano | `meta_alfabetizacao_2024` = 59,9 | O challenge define a meta pactuada como 80. O Brasil 2024 ficaria “quase na meta do ano” (−0,7 pp) e continua longe de 2030 (−20,8 pp). As colunas anuais permanecem na Bronze/Silver. |
| Sem tabela de cenário 2030 | Projetar a reta 55,9 → 59,2 → 66,0 | O guia diz para chamar de cenário, se existir, e não de previsão. Não foi construída. |
| `validacao_microdado` em `INNER JOIN` na mesma rede | Comparar microdado rede 3 com a taxa pública (rede 5) | O microdado não tem código 5. Rede 5 é a soma estadual+municipal já feita pelo Inep. Comparar redes diferentes produziria um `diff_pp` sem sentido. |
| Export Parquet em `gs://…/gold/<produto>/ingestion_date=/run_id=/` | Deixar a Gold só no BigQuery | A Fase 3 precisa do arquivo. O `CREATE OR REPLACE` no BigQuery mantém o nome estável; o path com `run_id` guarda o arquivo daquela publicação. |
| `dry_run` antes de cada `CREATE` | Estimar bytes no olho | O Passo 9 usa esse número. A validação do microdado é 195.491.553 dos 202.322.630 bytes dos cinco `CREATE`. |

## Uso em modelo (Fase 3)

Alvo típico: `taxa_alfabetizacao` de um ano futuro, ou `status_meta` / `gap_pp` derivados dela.

Não entram como feature **do mesmo ano que se quer prever**:

- `taxa_alfabetizacao`
- `meta_alfabetizacao_2030` (é constante 80 onde existe; onde não existe, o nulo é informação da meta, não uma causa)
- `status_meta` e `gap_pp` do mesmo ano

Candidatas a feature: taxa e delta de anos anteriores (`taxa_anterior`, `delta_pp`), composição dos níveis 0–8 **em 2024** (em 2023 a coluna veio inteira nula), rede, série e o próprio histórico municipal. `origem` deve ser filtrada para `oficial` antes de qualquer treino. `eventos_stream` não entra nesse treino.

## Leitura curta dos produtos

Entre os municípios com meta, 935 de 5.448 atingiram 80 em 2023 (17%) e 1.141 de 5.448 em 2024 (21%). A média de quem atingiu fica em 88,5; a de quem não atingiu, em 55,2.

Nas UFs de rede pública, só o Ceará está em 80 ou acima (84,46 em 2023 e 85,31 em 2024). As outras 47 linhas UF×ano estão abaixo. Não há linha de Roraima nem do Distrito Federal nesse recorte: o agregado oficial não as trouxe em `rede = 5`.

No microdado, a diferença absoluta mediana contra a taxa oficial é 0,0037 ponto percentual (12.408 linhas). 57 linhas passam de 1 pp. A maior é −36,06 pp no município de código 2305100, rede municipal, peso amostral 72. O pipeline guarda os dois números; não “corrige” o oficial pelo microdado.
