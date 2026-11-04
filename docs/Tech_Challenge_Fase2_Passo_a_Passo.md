# Tech Challenge Fase 2 — Passo a passo de implementação

Guia único para construir o projeto **neste repositório**, na ordem em que o código deve nascer.

Enunciado oficial: `POSTECH - IAST - Tech Challenge - Fase 2.pdf`. Mapa das aulas: [ROTEIRO_ESTUDO.md](./ROTEIRO_ESTUDO.md).

---

## Decisões já travadas

O README da raiz e o `.env.example` já fecharam a arquitetura. Os passos abaixo seguem isso.

| Decisão | Valor neste projeto |
|---------|---------------------|
| Cloud | GCP, região `us-central1`, BigQuery em `US` |
| Projeto | `GCP_PROJECT_ID` (exemplo: `tc-postech-fiap`) |
| Lake | Bucket `GCP_BUCKET_NAME`, Parquet particionado |
| Warehouse | BigQuery, SQL nas camadas Silver e Gold |
| Datasets BQ | **`alfabetizacao_<camada>`** — `alfabetizacao_bronze`, `alfabetizacao_silver`, `alfabetizacao_gold`, `alfabetizacao_ops`. Proibido o invertido (`bronze_alfabetizacao`, etc.). Paths GCS (`bronze/`, `silver/`, `gold/`) são pasta do lake, não nome de dataset |
| Fonte | Dataset público `basedosdados.br_inep_avaliacao_alfabetizacao` |
| Padrão de carga | **ELT**: extrair e gravar cru; transformar no BigQuery |
| Streaming | Pub/Sub, tópico `alfabetizacao-stream-topic` (o papel do Kafka da aula) |
| Arquitetura de processamento | Híbrida **Lambda**: batch no histórico oficial + speed layer simulada |
| Custo | Always Free + alerta de billing em R$ 1,00; a tabela FinOps projeta o custo se a cadência fosse de produção |

Motivo de cada escolha (vai para a seção Decisões do README):

- **GCS + BigQuery** é o lakehouse da aula de arquitetura, no stack serverless da aula de Cloud Data. O dado oficial já está no BigQuery da Base dos Dados, então a extração não copia o país inteiro para o notebook.
- **Pub/Sub** cumpre mensageria, retenção e entrega *at-least-once* sem um cluster Kafka 24/7. A aula de FinOps trata cluster de streaming ligado o tempo todo como custo contínuo; neste volume simulado isso estoura o teto gratuito sem ganho analítico.
- **Pandas + SQL no BigQuery** no lugar de um cluster Spark. A aula de Spark ensina o padrão Medalhão (ler cru, limpar, agregar). O volume do indicador cabe em SQL serverless. Spark fica como evolução se o microdado passar a não caber na cota.

---

## O que o repositório já tem

| Item | Estado |
|------|--------|
| `.env.example`, `.gitignore`, `requirements.txt` | Pronto |
| `test_gcp_connection.py` | Pronto (Storage + BigQuery + Pub/Sub `get_topic`) |
| README de setup (venv, chave, teste) | Pronto |
| `sql/00_perfil.sql`, `docs/contrato_dados.md` | Pronto (passo 2) |
| `bronze/ingest_batch.py`, dataset `alfabetizacao_bronze` | Pronto (passo 3) |
| `quality/validate.py`, `quality/prove_failure.py`, `alfabetizacao_ops.quality_checks` | Pronto (passo 4) |
| `silver/transform.py`, `sql/02_silver.sql`, dataset `alfabetizacao_silver` | Pronto (passo 5) |
| `gold/build.py`, `sql/03_gold.sql`, dataset `alfabetizacao_gold` | Pronto (passo 6) |
| `streaming/producer.py`, `streaming/consumer.py`, `eventos_stream` | Pronto (passo 7) |
| `ops/telemetry.py`, `ops/prove_observability.py`, `pipeline_runs` + alerta | Pronto (passo 8) |
| `ops/finops_snapshot.py`, `evidence/passo_09/custo.md` | Pronto (passo 9) |
| README da raiz, `requirements.txt` com pin, `evidence/passo_10/` | Pronto (passo 10) |
| Evidências em `evidence/passo_01/` … `passo_10/` | Pronto |
| Vídeo | Ainda não (passo 11) |

Credencial fica em `credentials/gcp-sa-key.json`. Ela não sobe no Git.

### Progresso dos passos

| Passo | Status | Evidência |
|-------|--------|-----------|
| 1 Ambiente | **Feito** | `evidence/passo_01/` |
| 2 Perfil / contrato | **Feito** | `evidence/passo_02/` + `docs/contrato_dados.md` |
| 3 Bronze | **Feito** | `evidence/passo_03/` |
| 4 Qualidade Bronze | **Feito** | `evidence/passo_04/` |
| 5 Silver | **Feito** | `evidence/passo_05/` |
| 6 Gold | **Feito** | `evidence/passo_06/` |
| 7 Streaming | **Feito** | `evidence/passo_07/` |
| 8 Observabilidade | **Feito** | `evidence/passo_08/` |
| 9 FinOps | **Feito** | `evidence/passo_09/` |
| 10 README / clone | **Feito** | `evidence/passo_10/` + README da raiz |
| 11 Vídeo | Pendente | ainda não gravado |

---

## Mapa: aula → onde entra no projeto

Use a aula como repertório. O código do challenge aplica o conceito no indicador de alfabetização, no dataset da aula (vendas, GlobalTech, Kafka local).

| Aula | O que levar para o código |
|------|---------------------------|
| [Capítulo Data Prepare](./00_Capitulo_de_Projeto/00_capitulo_de_projeto_data_prepare.md) | CRISP-DM: entender a fonte e a qualidade **antes** de modelar. A Gold é o terreno da Fase 3. |
| [Lake vs Warehouse](./01_Arquitetura_de_Big_Data/aula_01_arquitetura_de_dados_data_lake_vs_data_warehouse.md) | Lake = Parquet cru no GCS. Warehouse = tabelas SQL no BigQuery. Os dois convivem. |
| [Hadoop e Spark](./01_Arquitetura_de_Big_Data/aula_02_processamento_distribuido_hadoop_e_spark.md) | Pensar em partição e em não trazer a base inteira para a RAM. A execução daqui é SQL no BigQuery. |
| [Spark / Medalhão](./01_Arquitetura_de_Big_Data/aula_03_manipulacao_de_dados_com_spark.md) | Três cargas separadas: Bronze sem regra de negócio, Silver com limpeza e join, Gold com agregação. Prática da aula: `05_Extras_GitHub/_repo/Fase 2/Arquitetura de Big Data/` (`02_`, `03_`, `04_carga_camada_*`). |
| [Data Mesh](./01_Arquitetura_de_Big_Data/aula_04_data_mesh.md) | Cada tabela Gold é um produto com schema explícito, dono e checagem antes de publicar. |
| [SQL relacional](./02_Bancos_de_Dados_Relacionais/aula_01_banco_de_dados_relacionais.md) | Chaves de UF, município, ano, rede e série. `dicionario` traduz código; não invente o de-para. |
| [Agregações e subqueries](./02_Bancos_de_Dados_Relacionais/aula_02_sql_para_analise_avancada_agregacoes_e_subqueries.md) | Gold em CTE: indicador, meta × resultado, evolução. `NULL` permanece `NULL` nas médias. |
| [Índices e partições](./02_Bancos_de_Dados_Relacionais/aula_03_otimizacao_de_queries_indices_particoes_e_boas_praticas.md) | Particionar por `ano`, clusterizar por município/UF, `SELECT` só das colunas usadas, `dry_run` antes da query grande. |
| [NoSQL — conceitos](./03_NoSQL_para_Ciencia_de_Dados/aula_01_introducao_ao_nosql_conceitos_e_diferencas_do_modelo_relacional.md) | Indicador oficial fica relacional. Evento simulado é documento JSON. |
| [Modelagem NoSQL](./03_NoSQL_para_Ciencia_de_Dados/aula_02_modelagem_nosql_chave_valor_documentos_colunas_e_grafos.md) | O payload do Pub/Sub é um documento: um evento, um JSON, chave = `event_id`. |
| [Consultas NoSQL](./03_NoSQL_para_Ciencia_de_Dados/aula_03_consultas_em_nosql_operadores_filtros_e_agregacoes.md) | No consumer: filtrar inválido, deduplicar, agregar janela curta antes de gravar. |
| [Banco vetorial](./03_NoSQL_para_Ciencia_de_Dados/aula_04_banco_vetorial.md) | Fora do escopo desta entrega. Cite no README como uso futuro da Gold (busca por municípios parecidos), sem implementar. |
| [ETL / ELT](./04_ETL_Pipelines/aula_01_pipelines_etl_elt_extracao_transformacao_carga.md) | Batch = extração completa com histórico. Stream = extração incremental. Bronze no lake; transformação no warehouse. |
| [Kafka](./04_ETL_Pipelines/aula_02_integracao_de_dados_em_tempo_real_kafka.md) | Produtor, tópico, consumidor, lag, duplicata, carimbo de tempo de produção separado do de ingestão. Prática: notebooks em `05_Extras_GitHub/_repo/Fase 2/ETL Pipelines/02_Kafka/`. |
| [Cloud Data](./04_ETL_Pipelines/aula_03_cloud_data_aws_s3_gcp_bigquery_azure_data_lake.md) | GCS no papel do lake; BigQuery no papel do warehouse serverless (partição, cluster, custo por bytes lidos). |
| [FinOps](./04_ETL_Pipelines/aula_04_finops_em_ambiente_cloud.md) | Parquet, compressão, partição, mesma região, job que liga e desliga, tabela com quantidade medida. |

---

## Ordem de construção

`Ambiente → perfil da fonte → Bronze → qualidade da Bronze → Silver + joins → Gold → streaming → métricas e alerta → FinOps → README e evidências → vídeo`

Cada passo termina com um critério de pronto. Só avance com ele verdadeiro.

---

### Passo 1 — Travar o ambiente

**Status:** feito · **Evidência:** `evidence/passo_01/`

**Aulas:** Cloud Data, FinOps.

1. [x] Ative a `.venv`, instale `requirements.txt`, copie `.env.example` para `.env`, coloque a chave em `credentials/`.
2. [x] Rode `python test_gcp_connection.py` e guarde a saída em `evidence/passo_01/`.
3. No console GCP, confirme:
   - [x] bucket na região `us-central1` (print do teste)
   - [x] tópico `alfabetizacao-stream-topic` (`get_topic` OK)
   - [x] subscription (pull) ligada a esse tópico (`pubsub-subscription.png` — Pull, retenção 7 dias)
   - [x] orçamento com alerta em R$ 1,00 (`billing-alertas-1-real.png`)
4. [x] Ajuste o teste de Pub/Sub para falhar se `get_topic` não achar o tópico.

**Pronto quando:** Storage, BigQuery (5 linhas do `dicionario`) e o tópico real respondem, e o print está em `evidence/passo_01/`. ✅

---

### Passo 2 — Entender as 6 entidades (Data Understanding)

**Status:** feito · **Evidência:** `evidence/passo_02/` · **Contrato:** `docs/contrato_dados.md`

**Aulas:** Capítulo Data Prepare, SQL relacional, agregações.

Dataset: `basedosdados.br_inep_avaliacao_alfabetizacao`.

| Entidade que a banca cobra | Tabela |
|----------------------------|--------|
| Alunos | `alunos` |
| Município | `municipio` |
| UF | `uf` |
| Meta Brasil | `meta_alfabetizacao_brasil` |
| Meta UF | `meta_alfabetizacao_uf` |
| Meta município | `meta_alfabetizacao_municipio` |
| Tradução de códigos | `dicionario` (apoio; não substitui nenhuma das seis) |

Faça em `sql/00_perfil.sql` (e salve o resultado em `evidence/passo_02/`):

1. [x] `SELECT` com limite e a lista de colunas de cada tabela. Anote o nome real de ano, UF, município, rede, série, taxa, proficiência, presença e peso. Não chute o nome da coluna.
2. [x] Conte linhas, anos distintos, nulos nas chaves e códigos que não existem no `dicionario`.
3. [x] Confira a meta pactuada: rede pública, `meta_alfabetizacao_2030` = **80**. Universalização é outro número e entra no relatório como cenário, com outro nome de coluna.
4. [x] Escreva em `docs/contrato_dados.md` (curto):
   - grain de cada tabela (o que é uma linha)
   - chaves de join, com o tipo de cada lado
   - uma anomalia real encontrada (vira diferencial e limitação do README) — encoding de `rede` código vs rótulo
5. [x] Exploração extra em `sql/01_exploracao.sql` (runner `sql/run_exploracao.py`): distribuição por rede, ranking/gap de UF, presença×proficiência, cobertura do join com meta e consistência micro→município. CSVs `06_*` em `evidence/passo_02/`.

**Pronto quando:** as seis tabelas têm grain, chave e uma anomalia anotada, e nenhuma coluna do contrato foi inventada. ✅

---

### Passo 3 — Bronze (raw, com histórico)

**Status:** feito · **Evidência:** `evidence/passo_03/`

**Aulas:** Lake vs Warehouse, Medalhão (carga Bronze), ETL/ELT (extração completa).

Script: `bronze/ingest_batch.py`.

Para cada uma das 6 tabelas + `dicionario`:

1. [x] Ler do BigQuery público **só as colunas que o contrato listou** (aula de otimização: não usar `SELECT *`).
2. [x] Gravar Parquet no GCS, sem alterar valor de negócio:

```text
gs://<bucket>/bronze/<entidade>/ingestion_date=YYYY-MM-DD/run_id=<id>/part-*.parquet
```

3. [x] Modo de escrita: **append de uma partição nova**. Uma run nova cria outro `run_id`. Não use overwrite do prefixo `bronze/<entidade>/`, nem `WRITE_TRUNCATE` da tabela inteira.
4. [x] Colunas técnicas permitidas na Bronze (não são regra de negócio): `ingestion_ts`, `run_id`, `source_table` (`ingestion_ts`/`source_table` no Parquet; `ingestion_date`/`run_id` como partições Hive da external table).
5. [x] Registrar no BigQuery external tables Hive, dataset `alfabetizacao_bronze`, para a Silver consultar SQL sem baixar o Parquet no pandas.

Evidência: job id do BigQuery, contagem de linhas por entidade, caminho do objeto. Grave em `evidence/passo_03/`.

**Pronto quando:** uma segunda execução deixa a primeira intacta no bucket e as seis entidades aparecem com contagem > 0. ✅ (runs `f92c40cfe9a7` e `20d3623d0430`)

---

### Passo 4 — Regras de qualidade (antes de publicar a camada seguinte)

**Status:** feito · **Evidência:** `evidence/passo_04/`

**Aulas:** Data Mesh (governança no código), ETL (falha de extração degrada o modelo).

Pacote: `quality/` — neste passo, **somente Bronze** (`python quality/validate.py --layer bronze`). Taxa de match do join fica para o Passo 5.

Duas classes de regra:

| Classe | Se falhar |
|--------|-----------|
| Bloqueante | O script sai com código ≠ 0 e **não grava** a camada seguinte |
| Informativa | Grava o resultado e segue |

Mínimo bloqueante (Bronze):

- [x] chave nula (`null_keys`)
- [x] duplicata da chave da entidade (`duplicate_keys`)
- [x] código de rede ou série ausente no `dicionario` — limiar **0** (justificado no contrato; perfil Passo 2)
- taxa de match do join abaixo do limiar → **Passo 5** (fora deste passo)

Persistir cada resultado em `alfabetizacao_ops.quality_checks` com `append` (`run_id`, regra, camada, status, valor, limiar, `checked_at`). Log de terminal não conta. [x]

Prova obrigatória: `quality/prove_failure.py` injeta uma linha duplicada (fixture `alfabetizacao_ops.fixture_dup_keys`, sem alterar o lake GCS), a regra bloqueante dispara, e o registro da falha fica na tabela de checks. Salve stdout + a linha da tabela em `evidence/passo_04/`. [x]

`except` que só imprime e devolve sucesso anula o critério.

**Pronto quando:** existe uma execução que falha de propósito, com evidência, e outra execução limpa que passa. ✅ (`validate` exit 0 em `run_id=20d3623d0430`; `prove_failure` exit 1)

---

### Passo 5 — Silver (limpar, tipar, juntar)

**Status:** feito · **Evidência:** `evidence/passo_05/`

**Aulas:** Medalhão (carga Silver), SQL (chaves, `NULL`, CTE), otimização (partição).

Script: `silver/transform.py` + `sql/02_silver.sql`.

1. [x] Ler a Bronze da **última** `ingestion_date`/`run_id` (ou a que o parâmetro mandar).
2. [x] Padronizar nomes e tipos. Traduzir códigos com join no `dicionario`. Código sem tradução vira a categoria `desconhecido`, e a contagem dessa categoria entra na qualidade.
3. [x] Normalizar a chave dos dois lados do join (mesmo tipo: string com string, inteiro com inteiro) **antes** do `JOIN`. De-para `rede`: `3`↔`Municipal`, `5`↔`Pública` (contrato).
4. [x] Depois de **cada** join, calcular:

```text
taxa_match = linhas_com_par / linhas_do_lado_esquerdo
```

Gravar a taxa em `quality_checks`. Se ficar abaixo do limiar justificado no contrato (**≥ 0.95**), a regra bloqueante interrompe o job (`exit 1`).

5. [x] `NULL` continua `NULL`. Não preencha proficiência nem meta com 0.
6. [x] Coluna `origem` = `oficial` em tudo que veio da Base dos Dados.

Joins materializados na Silver:

- [x] município × meta municipal (`municipio_com_meta`, rede `3`)
- [x] UF × meta da UF (`uf_com_meta`, rede `5`)
- [x] Brasil (agregado UF) × meta Brasil (`brasil_com_meta`)
- [x] `alunos` tipados (uso na Gold fica para o passo 6)

Dataset de saída: `alfabetizacao_silver`, tabelas particionadas por ano (`RANGE_BUCKET`).

**Pronto quando:** taxa de match de cada join está persistida, o limiar está escrito no README, e as seis entidades têm coluna usada adiante. ✅ (`run_id=20d3623d0430`; municipio match ≈ 0,978; uf/brasil = 1,0)

---

### Passo 6 — Gold (produto analítico)

**Status:** feito · **Evidência:** `evidence/passo_06/`

**Aulas:** Medalhão (carga Gold), agregações/CTE/window, Data Mesh, otimização.

Script: `gold/build.py` + `sql/03_gold.sql`. Dataset `alfabetizacao_gold`.

Publique só se a qualidade bloqueante da Silver passou. Cada tabela é um produto: nome estável, schema no contrato, descrição de uma linha.

| Produto | Uma linha é | Uso |
|---------|-------------|-----|
| `indicador_municipio` | município + ano + rede + série | painel e Fase 3 |
| `indicador_uf` | UF + ano + rede + série | comparação estadual |
| `meta_vs_resultado` | mesmo grain da meta | distância até a meta **pactuada** |
| `evolucao_temporal` | série no tempo (window `LAG`) | trajetória, não previsão |
| `validacao_microdado` | recorte em que der para recalcular | diferencial: taxa pelos `alunos` vs taxa oficial |

Regras de cálculo:

- [x] Comparar meta e resultado na **mesma** rede e na **mesma** série.
- [x] Meta ausente é um terceiro estado (`sem_meta`), separado de `atingiu` e `nao_atingiu`.
- [x] Indicador nacional ou de UF segue o peso da fonte (alunos / peso amostral). Se alguma coluna for média simples de municípios, o nome da coluna diz isso (`media_simples_municipios` / `media_simples_ufs` na Silver).
- [x] Taxa a partir de `alunos`: denominador = avaliados, com peso amostral. Presença e alfabetizado vêm do `dicionario`.
- Projeção até 2030, se existir, chama-se cenário. Não chame de previsão. (não implementada neste passo)
- [x] Guardar a Gold (tabelas BigQuery + export Parquet em `gs://<bucket>/gold/`) para a Fase 3. No README, diga quais colunas são alvo de ML e quais seriam vazamento se entrassem como feature (a própria taxa que o modelo tentaria prever, e a meta do mesmo ano).

Partição por `ano`. Cluster por `id_municipio` ou `sigla_uf` / `nivel_geo`, conforme o grain. [x] `QueryJobConfig.dry_run` + `total_bytes_processed` em `evidence/passo_06/dry_run_bytes.csv`.

**Pronto quando:** as três perguntas do enunciado têm tabela (indicador por município, meta × resultado, evolução) e um `SELECT` de conferência bate com um número oficial que você anotou no perfil. ✅ (`run_id=20d3623d0430`; CE 2024 rede 5 = 85,31; Brasil 2024 taxa 59,2 / meta 80)

---

### Passo 7 — Streaming simulado

**Status:** feito · **Evidência:** `evidence/passo_07/`

**Aulas:** Kafka (produtor, tópico, consumidor, duplicata, tempo), NoSQL documento, ETL incremental, Lambda.

Pasta: `streaming/` — `producer.py` + `consumer.py`.

Isto é a camada rápida. Ela não regrava o histórico oficial.

**Produtor** (`streaming/producer.py`):

- [x] Publica no tópico documentos JSON (atualização fictícia de indicador municipal).
- [x] Campos mínimos: `event_id`, `produced_at` (relógio no momento do `publish`), `entidade`, `chave` (município/ano/rede/série), `valor`, `origem = "simulado"`.
- [x] `produced_at` é gerado uma vez, na produção. O consumer não copia esse campo para o relógio de ingestão.
- [x] Demo `--n 20`: 18 válidos + 1 inválido + 1 duplicata.

**Consumidor** (`streaming/consumer.py`):

- [x] Pull da subscription `alfabetizacao-stream-sub`.
- [x] `ingested_at` = agora, na ingestão. Latência = `ingested_at - produced_at`.
- [x] Evento inválido → `gs://<bucket>/bronze/stream_quarentena/`; ack só depois de persistir.
- [x] Duplicata (`event_id` já visto): contabilizar e não somar de novo (*at-least-once* + MERGE).
- [x] Evento bom → `gs://<bucket>/bronze/stream/ingestion_date=.../` + upsert `alfabetizacao_gold.eventos_stream`.
- [x] Métrica de lag: `mensagens_recebidas` do lote + latência min/max/média.

Separação obrigatória: consultas do indicador oficial filtram `origem = 'oficial'`. A tabela de eventos deixa `origem = 'simulado'` visível. [x]

No README, três linhas comparando com o batch: latência / frequência / garantia. [x]

**Pronto quando:** um evento válido chega na Gold de streaming com latência > 0, um duplicado não dobra o valor, um inválido fica na quarentena, e a tabela oficial não muda de número por causa do simulador. ✅ (`received=20`, `inserted=18`, `dups=1`, `quarantine=1`, latência min ≈ 7,4 s; CE 2024 oficial inalterada)

---

### Passo 8 — Observabilidade

**Status:** feito · **Evidência:** `evidence/passo_08/`

**Aulas:** FinOps (operar), Kafka (lag), Data Mesh (checagem na publicação).

Pacote: `ops/telemetry.py` + instrumentação em bronze / silver / gold / stream. Prova: `ops/prove_observability.py`.

Tabela `alfabetizacao_ops.pipeline_runs`, sempre `append` (`INSERT`):

| Campo | Exemplo |
|-------|---------|
| `run_id` | uuid |
| `etapa` | bronze / silver / gold / stream |
| `started_at`, `finished_at` | timestamps |
| `duration_seconds` | medido |
| `rows_in`, `rows_out` | contagens |
| `status` | success / failed |
| `bytes_processed` | dry run ou job statistics do BigQuery |
| `latency_*_s` | min/max/média do lote (stream) |

Alerta que alguém receberia em produção:

- [x] Falha bloqueante publica mensagem no tópico `alfabetizacao-alertas`.
- [x] README: quem descobre a falha é quem executou o comando, no mesmo processo; a linha `failed` fica em `pipeline_runs`. E-mail, Slack ou política ficam para quando não houver operador na sessão. O e-mail de R$ 1,00 é só custo. Sem PagerDuty.

Latência de streaming nas colunas `latency_min_s` / `latency_max_s` / `latency_avg_s` de `pipeline_runs` quando `etapa = stream`. [x]

**Pronto quando:** duas runs seguidas aparecem como duas linhas (a segunda não apagou a primeira) e uma falha gerou registro + mensagem de alerta, com print em `evidence/passo_08/`. ✅

---

### Passo 9 — FinOps com número medido

**Status:** feito · **Evidência:** `evidence/passo_09/`

**Aula:** FinOps. Apoio: otimização de SQL e Cloud Data.

Script: `ops/finops_snapshot.py`. Lê tamanho dos objetos no bucket, `total_bytes_processed` dos jobs e duração em `pipeline_runs`. Escreve `evidence/passo_09/custo.md`.

1. [x] GCS: soma real via Storage API (`list_blobs`) — bucket ≈ **0,19 GiB** / 135 objetos.
2. [x] BigQuery: bytes de `pipeline_runs` + evidências dos jobs (Bronze manifest, dry_run/export Gold); ≈ **760 MiB/batch** → ≈ **0,021 TiB/mês** na cadência 1/dia.
3. [x] Pub/Sub: payload do lote demo (`n=20`) medido — média ≈ **240 B/msg**; projeção com 1.000 eventos/dia × 2 (publish+subscribe).
4. [x] Computação: duração medida (Silver ≈ 56 s); motor serverless (sem VM 24/7).
5. [x] Tabela + premissa de cadência + decisões FinOps na mesma página (`custo.md`). Preços públicos consultados em **2026-10-18**.
6. [x] Execução atual e projeção com essa cadência **cabem no Always Free** (custo projetado ≈ $0 após free tier).

Tabela que entra no README (preços públicos GCP na região usada; cite a data da consulta):

| Serviço | Unidade | Quantidade medida | Preço unitário | Custo mensal projetado |
|---------|---------|-------------------|----------------|------------------------|
| Cloud Storage | GB-mês | tamanho real do bucket | | |
| BigQuery | TiB processados | bytes do dry run × cadência | | |
| Pub/Sub | GiB de mensagens | bytes publicados no teste × cadência | | |
| Computação do job | — | duração medida; aqui o motor é serverless | | |

Cadência para a projeção (escreva a premissa): por exemplo 1 batch/dia e 1.000 eventos/dia. O número de bytes é o medido; a cadência é a premissa. Diga que a execução atual cabe no Always Free e que a coluna da direita é o custo se essa cadência rodasse fora da cota.

Decisões que a aula pede para aparecer no texto: Parquet comprimido, partição por data de ingestão e por ano, colunas explícitas, GCS e processamento na mesma região, consumer de streaming que não fica com cluster ligado. [x]

**Pronto quando:** a tabela tem quantidade tirada de log/API, não de chute, e a premissa da cadência está na mesma página. ✅ (`python ops/finops_snapshot.py` → `evidence/passo_09/custo.md`)

---

### Passo 10 — README, evidências e clone limpo

**Status:** feito · **Evidência:** `evidence/passo_10/` · **Avaliação:** `docs/avaliacao_conformidade.md`


**Aulas:** todas as decisões acima viram a seção Decisões.

O README da raiz já cobre setup. Complete as seções que a banca lê:

1. Contexto do Compromisso Nacional e do corte de 743 pontos.
2. Diagrama do que **rodou** (GCS, BigQuery, Pub/Sub, as três camadas, o ramo de quarentena).
3. Tecnologias: o que está no repo e o que fica para depois (orquestrador, Spark, banco vetorial).
4. Trade-offs: ELT, Lambda, lake + warehouse, Pub/Sub no lugar de Kafka, SQL no lugar de cluster, BigQuery público no lugar de download.
5. Monitoramento + tabela FinOps.
6. Uso em IA: Gold pronta para a Fase 3 e colunas que vazam o alvo.
7. Limitações: simulação, lacuna que você achou no passo 2, free tier.
8. Link do vídeo (passo 11).

Organização que o avaliador precisa achar:

```text
bronze/  silver/  gold/  quality/  streaming/  ops/  sql/
evidence/
  passo_01/ … passo_11/   # prints, job ids, contagens, falha, finops (por passo)
```

Teste de reprodutibilidade: outro diretório, clone, `.env` novo, chave, `pip install -r requirements.txt`, comandos do README até a Gold. Ajuste o README até esse caminho funcionar. Versões no `requirements.txt` com pin (`==`), não só `>=`, antes da entrega.

Nenhuma chave no Git. Confira `git status` em `credentials/` e `.env`.

**Pronto quando:** um clone limpo, seguindo só o README, chega na Gold e no consumo de um evento.

---

### Passo 11 — Vídeo (≤ 5 min)

**Status:** feito · **Evidência:** `evidence/passo_11/` · **Vídeo:** https://youtu.be/xUfqOCZPeNk

Roteiro, nesta ordem:

1. Problema: alfabetização até o 2º ano, indicador, meta pactuada 80.
2. Arquitetura em uma frase: batch histórico + evento simulado, Bronze → Silver → Gold no GCP.
3. Um número analítico que está na Gold (município ou UF, ano, rede, série), igual ao do repositório.
4. O que a Fase 3 pode prever e o que não pode entrar como feature.

Eixos de gráfico com rótulo. Link no README.

---

## Checklist da rubrica

| Pts | Critério | Onde se prova |
|-----|----------|----------------|
| 15 | Batch + streaming | passos 3 e 7, com `origem` |
| 15 | Medalhão | caminhos GCS + datasets `alfabetizacao_bronze/silver/gold` |
| 10 | Qualidade | passo 4, incluindo a falha provocada e a taxa de join |
| 10 | Monitoramento | `pipeline_runs` acumulada + alerta |
| 10 | FinOps | tabela do passo 9 |
| 10 | Cloud + repo | jobs reais em `evidence/` + clone limpo |
| 5 | README | passo 10 |
| 15 | Vídeo | passo 11 |

Diferenciais, se sobrar tempo, nesta ordem: validação cruzada do microdado (já está na Gold), uma anomalia documentada (passo 2), um teste automatizado da regra de join. Orquestrador e Terraform são bônus; não bloqueiam a nota se o README não fingir que existem.

---

## Comandos-alvo (quando os scripts existirem)

```powershell
python test_gcp_connection.py
python bronze/ingest_batch.py
python quality/validate.py --layer bronze
python silver/transform.py
python quality/validate.py --layer silver
python gold/build.py
python streaming/producer.py --n 20
python streaming/consumer.py
python quality/prove_failure.py
python ops/prove_observability.py
python ops/finops_snapshot.py
```

`prove_failure.py` e `prove_observability.py` devem terminar com erro (exit ≠ 0).
