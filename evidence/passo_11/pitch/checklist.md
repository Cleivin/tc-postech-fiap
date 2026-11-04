# Checklist do pitch — requisitos, diagnóstico e números

Run de referência: `20d3623d0430`. Enunciado: `docs/POSTECH - IAST - Tech Challenge - Fase 2.pdf`.

## O que o PDF pede e o que o projeto entrega

A meta usada para distância até o resultado é a pactuada: `meta_alfabetizacao_2030` = **80** na rede pública. Universalização é outra leitura.

| O que o PDF exige | O que o repositório entrega |
|---|---|
| Seis entidades usadas de fato: alunos, município, UF, meta Brasil, meta UF, meta município, mais o dicionário | As seis entram na Bronze e seguem até a Gold. O dicionário traduz códigos. |
| Batch do histórico + streaming simulado, com origem separada | Batch oficial (`origem = oficial`). Evento fictício em `eventos_stream` (`origem = simulado`), sem alterar a taxa oficial. |
| Bronze crua e com histórico; Silver tratada e integrada; Gold analítica | Bronze em Parquet no Cloud Storage, uma run não apaga a outra. Silver no BigQuery. Gold com cinco produtos e export em Parquet. |
| Três leituras na Gold: indicador municipal, meta × resultado, evolução | `indicador_municipio`, `meta_vs_resultado`, `evolucao_temporal`. |
| Guardar a Gold para modelo na Fase 3 | Tabelas no BigQuery e Parquet em `gold/`. Nenhum modelo treinado. |
| Qualidade bloqueante, taxa de join, falha demonstrada | Chave nula, duplicata e código órfão bloqueiam. `join_match` ≥ 0,95. `prove_failure.py` termina com erro de propósito. |
| Três estados: atingiu, não atingiu, sem meta. Nulo não vira zero | Implementado. 242 linhas municipais ficam `sem_meta`. |
| Monitoramento persistido e alerta; FinOps com quantidade medida | `pipeline_runs` e tópico de alerta. Custo medido dentro do Always Free, premissa de 1 batch/dia. |
| README reproduzível e vídeo de até 5 minutos | README cobre o clone até a Gold. Vídeo: https://youtu.be/xUfqOCZPeNk |

A rubrica soma 90 pontos. Pela avaliação interna (`docs/avaliacao_conformidade.md`), 75 pontos estão atendidos. Faltam os 15 do vídeo.

## Diagnóstico usado no pitch

- Corte oficial: **743** pontos no Saeb. O projeto não recalcula esse corte.
- Brasil, 2024, rede pública: **59,2**, meta **80**, status `nao_atingiu`, distância **−20,8** pontos percentuais. Em 2023: **55,9**.
- Ceará, 2024, rede pública: **85,31**. Única UF nesse recorte em 80 ou acima. Em 2023: **84,46**.
- Bahia, 2024, rede pública: **35,96**. Distância até o Ceará: **49,35** pontos percentuais.
- Rede municipal: **1.141 de 5.448** municípios atingiram 80 em 2024 (cerca de 21%). Em 2023: **935** (cerca de 17%).
- Minas Gerais, rede pública, 2023 para 2024: **+12,26** pontos. Rio Grande do Sul: **−18,76**.
- Sem meta: **242** linhas municipais, taxa média **53,7**. Quem não atingiu: média **55,2**.
- Cruzamento: município **0,9778**; UF e Brasil **1,0**; limiar **0,95**.
- Microdado: **3.867.999** registros. Diferença absoluta mediana contra a taxa oficial: **0,0037** ponto percentual, em 12.408 linhas.

## Onde cada número está

| Fala | Onde conferir |
|------|----------------|
| Ceará 2024 = 85,31; Brasil 2024 = 59,2 e meta 80 | `evidence/passo_06/conferencia.csv` |
| Brasil 2023 = 55,9; 1.141 e 935 municípios; 242 sem meta; mediana 0,0037 | `evidence/passo_10/insights_consultas.md` |
| Bahia 35,96; Minas +12,26; Rio Grande do Sul −18,76 | `evidence/passo_02/06_taxa_uf_ranking.csv` e a seção de IA do README. A Gold copia o agregado oficial de UF. |
| Ceará 2023 = 84,46 | `gold/DECISOES.md` e `insights_consultas.md` |
| Join 0,9778 / 1,0 / 1,0 | `evidence/passo_05/ANALISE.md` |
| 3.867.999 alunos | `docs/contrato_dados.md` |

Antes de gravar, confira o slide 2 contra `conferencia.csv` e `insights_consultas.md`.

## Aderência do vídeo

| Exigência do vídeo no PDF | Situação neste roteiro |
|---|---|
| Até 5 minutos, linguagem executiva | Frases curtas em `roteiro.md`, com pausa. Alvo: dentro de 5 minutos |
| Problema de negócio | Compromisso, 2º ano, corte 743, meta pactuada 80 |
| Arquitetura, no que a liderança precisa ouvir | Bronze, Silver, Gold, trava de 95%, evento simulado separado |
| Valor para análise educacional | Território, três status, trajetória de MG e RS, municípios em 80 |
| Potencial de IA, como evolução | Alvo futuro e insumos do passado. Modelo não apresentado como pronto |
| Números iguais aos do repositório | Conferidos na Gold, no README e em `insights_consultas.md` |
| Eixos rotulados, se houver gráfico | Slide 2: taxa (%), rede pública, 2024, linha da meta 80 |
| Link no README | https://youtu.be/xUfqOCZPeNk |

## O que não apresentar como entregue

- Modelo treinado, aplicação de IA, dashboard ou tabela de cenário até 2030.
- A taxa nacional de 2025 (66,0). Ela existe na tabela de meta e não entra no produto Brasil da Gold, porque o fato vai até 2024.
- Linha de rede pública para Roraima ou para o Distrito Federal no agregado de UF. O agregado oficial não traz essas UFs nesse recorte.
- O valor do evento simulado. A trilha é demonstração e não entra na análise.
- Orquestrador, Terraform e banco vetorial. São diferenciais não implementados. O PDF não os torna obrigatórios.

FinOps e o alerta operacional estão no README e ficam de fora da narração. Se perguntarem: a operação medida cabe no nível gratuito, e uma falha bloqueante fica registrada.

## Se a banca perguntar

- “Por que 80 e não a meta de 2024?” A régua do desafio é `meta_alfabetizacao_2030`. O Brasil em 59,2 ficaria perto da meta intermediária de 59,9 e continua a 20,8 pontos de 2030.
- “O Ceará prova que a política funciona?” O dado mostra que o Ceará está acima de 80. O projeto não observa a intervenção e não estima efeito de política.
- “Dá para prever 2030?” Com 2023 e 2024, não como previsão. Se um dia houver conta, o nome é cenário.
