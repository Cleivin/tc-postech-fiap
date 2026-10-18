# SQL — decisões

Scripts: [`00_perfil.sql`](00_perfil.sql), [`01_exploracao.sql`](01_exploracao.sql), [`02_silver.sql`](02_silver.sql), [`03_gold.sql`](03_gold.sql).  
Runners: [`run_perfil.py`](run_perfil.py), [`run_exploracao.py`](run_exploracao.py). A Silver e a Gold são executadas por `silver/transform.py` e `gold/build.py`.

Há também [`01_explocarcao_v2.sql`](01_explocarcao_v2.sql) (nome com typo). É um rascunho de exploração com joins no dicionário. Não é o caminho do pipeline e não gera os CSVs `06_*`. O runner oficial da exploração é `01_exploracao.sql`.

## O que o challenge pede

Perfil com nomes reais de coluna, grain e anomalia antes de modelar. Silver em SQL, com tipo alinhado antes do `JOIN`, `NULL` preservado e taxa de match depois de cada join. Gold em CTE/window, comparando meta e resultado na mesma rede, com `sem_meta` separado de `atingiu` e `nao_atingiu`.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Perfil e exploração como SQL versionado, não notebook | Consulta solta no console | O avaliador precisa refazer a conta. Cada CSV de `evidence/passo_02/` tem `job_id`. |
| De-para explícito `3 → Municipal` e `5 → Pública` | `JOIN` por igualdade de `rede` | O Passo 2 mediu encodings diferentes. Igualdade de string daria match ~0 e a qualidade mentiria ou travaria sem explicação. |
| `LEFT JOIN` a partir do fato | `INNER JOIN` | Município sem meta continua na tabela, com `tem_meta = false`. O match 0,978 existe porque 242 linhas ficam sem par. |
| Brasil oficial = `taxa_alfabetizacao` da meta Brasil | `AVG` das UFs como “taxa do Brasil” | A média simples tem outro nome (`media_simples_ufs`) e não alimenta o status nacional. A conferência usa 59,2, que é o número da fonte, não a média das UFs. |
| `NULL` sem `COALESCE` em taxa, meta e proficiência | Preencher com 0 | Zero seria “ninguém alfabetizado”. RR e o caderno vazio deixariam de ser lacuna. |
| Código sem rótulo vira `desconhecido` | Dropar a linha ou inventar rótulo | Nesta run o contador deu 0. A categoria existe para a próxima carga não passar calada. |
| Status da meta usa só `meta_alfabetizacao_2030` | Comparar com `meta_alfabetizacao_2024` (59,9 no Brasil) | O guia chama de meta pactuada o valor 80. A meta do ano é outro número, já extraído na Bronze, e não entra no status. Em 2024 o Brasil está a 0,7 pp da meta daquele ano e a 20,8 pp da meta de 2030. O status `nao_atingiu` é contra 2030. |
| `sem_meta` quando não há par, quando a meta é nula ou quando a taxa é nula | Tratar nulo como `nao_atingiu` | São estados diferentes. Gap de nulo permanece nulo. |
| Taxa do microdado = peso dos alfabetizados presentes / peso dos presentes | Dividir contagem simples, ou usar ausente no denominador | O guia pede denominador de avaliados com peso amostral. Ausente tem proficiência nula e flag 0. |
| `evolucao_temporal` com `LAG` por geo + rede + série | Diferença calculada no pandas, ou modelo até 2030 | São dois anos. A primeira observação fica com `taxa_anterior` nula. Isso é trajetória, não previsão. |
| Partição `RANGE_BUCKET(ano, 2020…2036)` e cluster geo | Tabela sem partição | A aula de otimização pede partição por ano e cluster por município ou UF. O `dry_run` da Gold mostra o efeito: os quatro produtos agregados leem poucos MiB; o microdado é que varre ~195 MiB. |
| `CREATE OR REPLACE` na Silver e na Gold | Append de várias runs na mesma tabela de produto | O guia pede nome estável de produto. O histórico da extração fica no lake (`run_id`). A tabela publicada é a run pedida. |

## Corte de 743 pontos, medido no microdado

Consulta feita em 2026-10-18 sobre `alfabetizacao_silver.alunos` (50.045.282 bytes). Registro em [`evidence/passo_10/insights_consultas.md`](../evidence/passo_10/insights_consultas.md).

| alfabetizado | presença | n | proficiência nula | mín | máx | ≥ 743 | < 743 |
|--------------|----------|---|-------------------|-----|-----|-------|-------|
| 0 | ausente | 512.153 | 512.153 | — | — | 0 | 0 |
| 0 | presente | 1.371.300 | 1.185 | 578,46 | 743,00 exibido | 0 | 1.370.115 |
| 1 | presente | 1.984.546 | 0 | 743,00 | 904,38 | 1.984.546 | 0 |

Quem tem flag `1` está todo em 743 ou acima. Quem tem flag `0` e nota preenchida não tem nenhum caso `>= 743` (o máximo impresso com duas casas arredonda para 743,00, mas a contagem `>= 743` é zero). O pipeline não recalcula o corte: usa a flag do Inep e, nos agregados, a taxa oficial.
