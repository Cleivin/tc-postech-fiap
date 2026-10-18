# Passo 2 — análise das evidências

Fonte: `basedosdados.br_inep_avaliacao_alfabetizacao`. Os CSV `01_`–`05_` vêm de `sql/00_perfil.sql`. Os `06_` vêm de `sql/01_exploracao.sql`. O [`README.md`](README.md) desta pasta é o dump da saída; este arquivo é a leitura.

Alguns trechos do README mostram `PÃºblica` e `NÃ£o`. Isso é o markdown gravado com a decodificação errada. Nos CSV de exploração (`06_gap_meta_uf.csv` e afins) o texto está `Pública`. O dado de origem não perdeu o acento.

## O que cada grupo de arquivo responde

| Arquivos | Pergunta | Resposta medida |
|----------|----------|-----------------|
| `01_amostra_*.csv`, `01_dicionario_completo.csv` | Quais são os nomes reais? | Ano `ano`, município `id_municipio`, UF `sigla_uf`, taxa `taxa_alfabetizacao`, proficiência `proficiencia`, presença `presenca`, peso `peso_aluno`. Série observada: `2` (2º ano). Nada disso foi inventado. |
| `02_contagens_*.csv` | Qual é o tamanho e o nulo de chave? | Alunos 3.867.999 (2023–2024), chaves com 0 nulos. Proficiência e peso nulos: 513.338 cada. Município 23.995 e UF 145, taxa sem nulo. Meta Brasil 3/3 com meta 80. Meta UF 81, das quais 2 com meta 2030 nula. Meta município 10.704, todas com meta 80. |
| `03_meta_pactuada_brasil.csv` | A meta pactuada é 80? | Rede pública: 55,9 (2023), 59,2 (2024), 66,0 (2025), todas com `meta_alfabetizacao_2030 = 80`. `percentual_participacao` é outro número (86,00 / 87,37 / 88,00). |
| `04_codigos_orfos_*.csv` | Há código fora do dicionário? | Não. Presença, caderno, alfabetizado, rede e série dos alunos estão `OK`. |
| `05_anomalia_rede_encoding.csv` | Dá para juntar fato e meta por `rede`? | Não. Alunos usam `2,3,4`. UF e município usam `0,2,3,5`. Metas usam `Pública` ou `Municipal`. |
| `05_anomalia_meta_uf_nula.csv` | Onde o nulo é estrutural? | RR 2023 e 2024: taxa, meta 2030 e participação nulas. |
| `06_distribuicao_rede_alunos.csv` | De quem é o microdado? | Quase só rede municipal e estadual. Privada: 25 alunos em 2024 (taxa simples 66,7% em 24 presentes) — não serve de comparação. |
| `06_taxa_uf_ranking.csv`, `06_gap_meta_uf.csv` | Quem está perto da meta 80? | Em 2024, só o CE (85,31). BA fecha em 35,96. Maior alta: MG +12,26 pp. Maior queda: RS −18,76 pp. |
| `06_presenca_vs_proficiencia.csv` | Os 513.338 nulos são o quê? | 512.153 ausentes com caderno vazio + 1.185 presentes com caderno vazio. Quem preencheu o caderno tem 0 nulos de proficiência e de peso. |
| `06_cobertura_join_meta.csv` | Quantos municípios do microdado têm meta? | 96,37% em 2023 (177 sem meta) e 96,97% em 2024 (167 sem meta). É a justificativa do limiar 0,95. |
| `06_consistencia_micro_vs_muni.csv` | A taxa oficial é a taxa ponderada dos alunos? | Na amostra de rede municipal, a diferença fica na segunda casa (0,00 a 0,07 pp). |

O CSV `04_codigos_orfos_municipio_uf.csv` repete a mesma chave duas ou três vezes. É fan-out da consulta de perfil, não duplicata do dado: o Passo 4 mediu `duplicate_keys = 0` nas mesmas entidades.

## Insights que mudam o desenho do pipeline

**O indicador já nasce agregado.** Município e UF trazem `taxa_alfabetizacao`. O microdado serve para auditar essa taxa, não para substituí-la. A flag `alfabetizado` é 0/1 para todo aluno (1.984.546 “sim” e 1.883.453 “não”, soma = 3.867.999). Dividir “sim” pelo total dá 51,3% e **não** é a taxa oficial: o denominador oficial são os presentes com peso. A taxa simples entre presentes fica na faixa 58–62% (rede estadual/municipal), perto dos 59,2 nacionais de 2024, mas não é o mesmo cálculo.

**Dois encodings de rede.** Sem o de-para `3 ↔ Municipal` e `5 ↔ Pública`, o join fato×meta perde. Rede `5` existe no agregado (“pública = estadual + municipal”) e não existe no microdado, que só tem 2, 3 e 4. Por isso a validação cruzada da Gold só compara a mesma rede.

**A meta 80 não é a meta do ano.** Em 2024 a coluna `meta_alfabetizacao_2024` do Brasil é 59,9 e o resultado é 59,2. A coluna de 2030 é 80. O status da Gold usa 2030, como o enunciado pede. Participação (~87%) não entra nessa conta.

**O país não está perto da meta, e a dispersão é o fato.** Do 55,9 ao 59,2 há +3,3 pp. O 66,0 de 2025 está na tabela de meta Brasil e ainda não está no agregado de UF (que para em 2024). Mesmo 66 continua 14 pp abaixo de 80. No ranking de 2024, o intervalo entre CE (85,31) e BA (35,96) é de quase 50 pp. A queda do RS (−18,76) está no dado oficial; este repositório não tem variável para explicar a causa.

**2023 não trouxe a composição por nível.** Na amostra de município, `proporcao_aluno_nivel_0` … `_8` vêm nulos. A confirmação por ano está no Passo 10: em 2023 as 11.547 linhas municipais têm nível 0 nulo; em 2024, nenhuma das 12.448. Não se preenche com zero.

**Roraima é lacuna de meta, e o agregado de UF também não lista RR nem DF em rede pública.** O ranking de 2024 tem 25 UFs. Faltam RR e DF. AC entra só em 2024 (51,38), com 2023 vazio. A Gold não completa essas linhas.
