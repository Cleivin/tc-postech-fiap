# Avaliação passo a passo — o que o challenge pediu e o que o repositório entrega

Run de referência das evidências: `20d3623d0430` (ingestão em 2026-10-18).  
Decisões locais: `DECISOES.md` em `bronze/`, `sql/`, `quality/`, `silver/`, `gold/`, `streaming/` e `ops/`.  
Leitura dos artefatos: `evidence/passo_XX/ANALISE.md`.

A rubrica do guia está em [`Tech_Challenge_Fase2_Passo_a_Passo.md`](Tech_Challenge_Fase2_Passo_a_Passo.md). Este arquivo diz, para cada passo, se o critério de pronto foi atingido e onde a prova está.

| Passo | Critério de pronto do guia | Situação | Prova |
|-------|----------------------------|----------|--------|
| 1 Ambiente | Storage, BigQuery (5 linhas do dicionário) e o tópico real respondem | Atendido | `evidence/passo_01/` + `test_gcp_connection.py` (exit 1 se Storage, BigQuery ou o tópico de stream falhar) |
| 2 Perfil | Seis entidades com grain, chave e uma anomalia; nenhuma coluna inventada | Atendido | `docs/contrato_dados.md`, `evidence/passo_02/` |
| 3 Bronze | Segunda run não apaga a primeira; seis entidades com contagem > 0 | Atendido | runs `f92c40cfe9a7` e `20d3623d0430`; contagens iguais às do perfil |
| 4 Qualidade | Uma execução que falha de propósito e outra limpa que passa | Atendido | `validate` exit 0; `prove_failure` exit 1 |
| 5 Silver | `join_match` persistido, limiar no contrato, seis entidades com coluna usada adiante | Atendido | município 0,978; UF e Brasil 1,0; limiar 0,95 |
| 6 Gold | Indicador municipal, meta × resultado, evolução, e um SELECT que bate com o perfil | Atendido | CE 2024 rede 5 = 85,31; Brasil 2024 = 59,2 / meta 80 |
| 7 Streaming | Válido na Gold de stream com latência > 0; duplicata não dobra; inválido na quarentena; oficial inalterado | Atendido | 18 inserts, 1 dup, 1 quarentena; CE 2024 permanece 85,31 |
| 8 Observabilidade | Duas runs em append e uma falha com registro + alerta | Atendido | duas linhas `success` + `prove_fail_81ee7cf0f8ea` + `message_id` |
| 9 FinOps | Quantidade medida (não chute) e premissa de cadência na mesma página | Atendido | `evidence/passo_09/custo.md` |
| 10 README / clone | Clone seguindo só o README chega na Gold e no consumo de um evento | Atendido no texto e nos pins | [`README.md`](../README.md), `evidence/passo_10/` |
| 11 Vídeo | Roteiro de até 5 min com um número da Gold | Pendente | sem link |

## Rubrica

| Pts | Critério | Onde se prova | Leitura |
|-----|----------|----------------|---------|
| 15 | Batch + streaming, com `origem` | Passos 3 e 7 | Oficial = `oficial`. Evento = `simulado`, tabela separada. O simulador não altera CE 2024. |
| 15 | Medalhão | GCS `bronze/` e `gold/` + datasets `alfabetizacao_bronze/silver/gold` | Três cargas separadas. Bronze sem regra de negócio. |
| 10 | Qualidade | Passo 4 + taxa de join do Passo 5 | Bloqueante sai com exit ≠ 0 e grava `quality_checks`. |
| 10 | Monitoramento | `pipeline_runs` + tópico `alfabetizacao-alertas` | Append comprovado. A duração medida na tabela, no snapshot do Passo 9, é a da Silver. |
| 10 | FinOps | Passo 9 | 0,19 GiB no bucket; ~0,021 TiB/mês de query na cadência 1 batch/dia; custo projetado $0 dentro do Always Free. |
| 10 | Cloud + repo | `evidence/` + README | Jobs reais. Chave e `.env` fora do Git. |
| 5 | README | Passo 10 | Contexto, diagrama, trade-offs, FinOps, vazamento de alvo, limitações. |
| 15 | Vídeo | Passo 11 | Não entregue. |

Diferenciais que já estão no repositório: validação cruzada do microdado (`validacao_microdado`), anomalia de `rede` documentada, e a regra de join executável (`quality/validate.py --layer silver` + `prove_failure.py`). Não há orquestrador nem Terraform, e o README não afirma que existam.

## O que ficou de fora de propósito

| Item | Por quê não está no código |
|------|----------------------------|
| Cluster Spark | O volume cabe em SQL serverless. Spark seria a evolução se o microdado deixasse de caber na cota. |
| Kafka 24/7 | Pub/Sub cumpre produtor, tópico, consumidor, duplicata e dois relógios, sem cluster ligado. |
| Banco vetorial | Fora do escopo. Uso futuro: buscar municípios parecidos a partir da Gold. |
| Projeção até 2030 | O guia permite cenário, com esse nome, e não exige a conta. Não há tabela de cenário. |
| Orquestrador / Terraform | Bônus. A reprodução é a sequência de scripts do README. |

## Lacunas reais (não são o desenho)

1. **`pipeline_runs` no snapshot do Passo 9 só tem a etapa Silver** (duas `success` e uma `failed`). Bronze, Gold e stream gravam telemetria no código atual, mas essa run de referência foi medida antes dessas linhas existirem na tabela. Bytes de Bronze e Gold vieram dos manifests e do `dry_run`, não de uma duração em `pipeline_runs`.
2. **A taxa nacional de 2025 (66,0) não entra na Gold.** Ela existe em `meta_alfabetizacao_brasil`. O produto Brasil é ancorado nos anos do agregado de UF (2023–2024).
3. **Roraima e o Distrito Federal não têm linha de rede pública no agregado `uf`.** A meta de RR está nula; o fato oficial simplesmente não traz essas UFs em `rede = 5`. A Gold não inventa a linha.
4. **O teste de conexão, até o Passo 10, imprimia erro e ainda assim encerrava com sucesso.** Passou a sair com código 1 se Storage, BigQuery ou o tópico de streaming falharem. O tópico de alerta continua opcional nesse teste, porque o Passo 8 o cria.
5. **Vídeo (Passo 11) não existe.** O README deixa o espaço do link explícito.
