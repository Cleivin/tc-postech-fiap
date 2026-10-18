# Silver — decisões

Passo 5. Código: [`transform.py`](transform.py) e [`sql/02_silver.sql`](../sql/02_silver.sql).  
O guia operacional da camada está em [`README.md`](README.md). Este arquivo é o registro da escolha. Evidência: [`evidence/passo_05/`](../evidence/passo_05/).

## O que o challenge pede

Ler uma run da Bronze, tipar, traduzir código pelo dicionário, normalizar o tipo dos dois lados antes do join, materializar município × meta, UF × meta e Brasil × meta, gravar a taxa de match e interromper se ficar abaixo de 0,95. `NULL` continua `NULL`. `origem = oficial`.

## O que a run produziu

| Tabela | Linhas | Leitura |
|--------|--------|---------|
| Sete espelhos (dicionário, alunos, município, UF, três metas) | iguais à Bronze | A tipagem não descartou linha |
| `municipio_com_meta` | 10.896 | Só `rede = 3`. São 5.448 municípios × 2023 e 2024 |
| `uf_com_meta` | 49 | Só `rede = 5`: 24 UFs em 2023 e 25 em 2024 |
| `brasil_com_meta` | 2 | Um ano para cada ano presente no agregado de UF |

Match: 0,9778 (município), 1,0 (UF), 1,0 (Brasil). `desconhecido_count` = 0.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Transformar no BigQuery | Limpar com pandas | 3,8 milhões de alunos já estão no warehouse. Trazer para a máquina desfaz o ELT. |
| Uma `run_id` por execução (`--run_id` ou a última `ingestion_ts`) | `SELECT` sem filtro, misturando as duas runs do bucket | A external table enxerga `f92c40cfe9a7` e `20d3623d0430`. Sem filtro a Silver dobraria o país. |
| `rede_para_meta` só em 3 e 5 | Mapear também estadual (`2`) para `Pública` | A meta de UF/Brasil se chama `Pública` e o agregado correspondente no Inep é o código `5` (estadual + municipal). Estadual pura é outro recorte e não tem meta com esse nome. |
| Brasil parte dos anos da UF, não dos anos da meta | Incluir 2025 porque a meta Brasil tem taxa 66,0 | Não há fato de UF em 2025 neste dataset (o agregado vai até 2024). Criar a linha de 2025 seria inventar um lado esquerdo. A taxa 66,0 permanece na tabela de meta, não no produto Brasil. |
| Coluna nacional usada adiante = taxa oficial da meta Brasil | Publicar `media_simples_ufs` como indicador do país | Média de UF trata Acre e São Paulo com o mesmo peso. O nome da média simples existe justamente para não ser confundida com a taxa oficial. |
| Partição por `ano` | Partição por `run_id` | A pergunta analítica filtra ano. O `run_id_bronze` fica como coluna de rastreio. |
| Gate com exit 1 dentro do próprio `transform.py` | Só validar depois, num segundo comando | O guia diz que a falha bloqueante não grava a camada seguinte. O `validate --layer silver` repete a conta e gera a evidência; não é a única trava. |

As regras de limiar estão em [`quality/DECISOES.md`](../quality/DECISOES.md) e no contrato.
