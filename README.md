# Tech Challenge — Fase 2: Pipeline híbrido de alfabetização

**Pós-graduação:** POSTECH — AI Scientist (IAST) | **FIAP**  
**Cloud:** Google Cloud Platform, região do lake `us-central1`, BigQuery em `US`

Pipeline batch + streaming sobre o indicador de alfabetização do Inep (Base dos Dados), em arquitetura Medalhão. A comparação de cada passo com o enunciado está em [`docs/avaliacao_conformidade.md`](docs/avaliacao_conformidade.md). O guia de construção é [`docs/Tech_Challenge_Fase2_Passo_a_Passo.md`](docs/Tech_Challenge_Fase2_Passo_a_Passo.md).

---

## Contexto

O [Compromisso Nacional Criança Alfabetizada](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao) reúne União, estados, Distrito Federal e municípios em torno de uma meta: toda criança alfabetizada até o fim do 2º ano do ensino fundamental. O Inep fixou o padrão nacional em **743 pontos** na escala de proficiência do Saeb. O Indicador Criança Alfabetizada é o percentual de estudantes que chegaram nesse ponto.

Neste repositório a meta **pactuada** é a coluna `meta_alfabetizacao_2030`. Na rede pública ela vale **80**. Outra coluna, `percentual_participacao`, é participação/universalização e não entra no status. As metas intermediárias (`meta_alfabetizacao_2024` = 59,9 no Brasil, e as dos anos seguintes) estão na Bronze e na Silver; o produto Gold compara o resultado com 80.

O microdado já traz a flag `alfabetizado`. Na Silver da run de referência, quem tem flag `1` está todo com proficiência ≥ 743 (mínimo 743,00; 1.984.546 alunos). Quem tem flag `0` e nota preenchida não tem nenhum caso ≥ 743. Ausente (512.153) não tem nota. O pipeline não recalcula o corte: usa a flag do Inep no microdado e a `taxa_alfabetizacao` oficial nos agregados. A conta está em [`evidence/passo_10/insights_consultas.md`](evidence/passo_10/insights_consultas.md).

Números oficiais que a Gold reproduz (run `20d3623d0430`):

| Recorte | Taxa | Meta 2030 | Status |
|---------|------|-----------|--------|
| Brasil, 2024, rede pública | 59,2 | 80 | `nao_atingiu` (gap −20,8 pp) |
| Ceará, 2024, rede pública (`rede = 5`) | 85,31 | 80 | acima da meta; única UF nesse recorte |

Em 2024, 1.141 de 5.448 municípios da rede municipal atingiram 80 (21%). Em 2023 eram 935 (17%).

---

## O que rodou

```mermaid
flowchart TB
  subgraph fonte [Fonte]
    BD["BigQuery público<br/>basedosdados.br_inep_avaliacao_alfabetizacao"]
  end
  subgraph gcs [Cloud Storage us-central1]
    BZ["bronze/entidade/ingestion_date/run_id<br/>Parquet cru"]
    ST["bronze/stream/"]
    Q["bronze/stream_quarentena/"]
    GL["gold/produto/ingestion_date/run_id"]
  end
  subgraph bq [BigQuery US]
    BR["alfabetizacao_bronze<br/>external tables"]
    SV["alfabetizacao_silver"]
    GD["alfabetizacao_gold<br/>origem = oficial"]
    EV["alfabetizacao_gold.eventos_stream<br/>origem = simulado"]
    OPS["alfabetizacao_ops<br/>quality_checks + pipeline_runs"]
  end
  subgraph ps [Pub/Sub]
    TOP["alfabetizacao-stream-topic"]
    SUB["alfabetizacao-stream-sub<br/>Pull, retenção 7 dias"]
    AL["alfabetizacao-alertas"]
  end
  BD --> BZ --> BR --> SV --> GD --> GL
  SV --> OPS
  GD --> OPS
  TOP --> SUB
  SUB -->|evento válido| ST
  SUB -->|evento válido| EV
  SUB -->|inválido| Q
  OPS -->|falha bloqueante| AL
```

A Silver não tem pasta no lake. A transformação é SQL no BigQuery. O histórico cru fica no GCS; o produto analítico fica no BigQuery e é exportado de novo para `gold/`.

---

## Tecnologias

| No repositório | Fora desta entrega |
|----------------|--------------------|
| Python 3.14, pandas e PyArrow só na borda (evidência, tipos) | Spark / cluster |
| BigQuery (extração, Silver, Gold, checagens) | Orquestrador (Airflow, Composer) e Terraform |
| Cloud Storage, Parquet particionado | Kafka ligado 24/7 |
| Pub/Sub (stream simulado + alerta) | Banco vetorial |
| Scripts na ordem do README | Projeção / cenário até 2030 |

Uso futuro da Gold que a aula de banco vetorial sugere, e que **não** foi implementado: buscar municípios com trajetória parecida. A tabela `indicador_municipio` seria a fonte dessa busca.

---

## Trade-offs

| Escolha | O que se ganha | O que se abre mão |
|---------|----------------|-------------------|
| **ELT** | A Bronze guarda o valor oficial. A regra fica em SQL, auditável, sem rebaixar 3,8 milhões de linhas para a máquina. | Não há um dataframe “já limpo” no notebook. |
| **Lambda** | O histórico oficial é batch. O evento fictício chega em segundos e não regrava o país. | Não existe feed real do Inep. A camada rápida é simulação. |
| **Lake + warehouse** | Parquet no GCS é o histórico (`run_id`). BigQuery é o lugar da pergunta. | A Silver não é um segundo Parquet. Quem quiser arquivo da Silver precisa exportar. |
| **Pub/Sub no lugar de Kafka** | Produtor, tópico, consumidor, duplicata e dois relógios, sem cluster. | Não há partição de log nem consumer group no sentido do Kafka. O lag medido é `ingested_at − produced_at`. |
| **SQL no lugar de Spark** | O volume cabe na cota. O job liga e desliga. | Se o microdado deixar de caber, o padrão Medalhão da aula de Spark é a evolução, não o caminho atual. |
| **BigQuery público no lugar de download** | A extração pede só as colunas do contrato e grava direto no bucket. | Depende da Base dos Dados continuar pública e do schema não mudar de nome. |

De-para de rede, obrigatório por causa da anomalia do Passo 2: código `3` ↔ meta `Municipal`; código `5` ↔ meta `Pública`. Limiar bloqueante do join: **≥ 0,95**, justificado pela cobertura de 96–97% medida no perfil ([contrato](docs/contrato_dados.md)).

Batch versus stream:

| | Batch | Stream |
|--|--------|--------|
| Latência | Run Silver medida em ~56 s; a carga completa é da ordem de minutos | 7–24 s entre produção e ingestão na demo |
| Frequência | Uma run, o histórico inteiro | Uma mensagem por evento |
| Garantia | Snapshot da fonte naquela `run_id` | *At-least-once*, dedupe por `event_id` |

---

## Clone limpo

Testado o contrato dos comandos contra os scripts deste repositório. Um segundo projeto GCP não foi criado aqui: a prova de que o caminho produz Gold e consome evento é a run `20d3623d0430`, em `evidence/`. Um clone novo gera outro `run_id`.

### 1. Máquina

- Python **3.14** (o ambiente das evidências é 3.14.7)
- Git
- Conta GCP com faturamento (o uso deste desenho cabe no Always Free; o alerta de R$ 1,00 é o freio)
- [Google Cloud SDK](https://cloud.google.com/sdk) se for criar bucket e tópico pela linha de comando

### 2. Código e ambiente

```bash
git clone https://github.com/Cleivin/tc-postech-fiap.git
cd tc-postech-fiap
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edite `.env`:

```env
GCP_PROJECT_ID=seu-projeto-gcp
GCP_BUCKET_NAME=seu-bucket-datalake
GOOGLE_APPLICATION_CREDENTIALS=credentials/gcp-sa-key.json
GCP_LOCATION=us-central1
BIGQUERY_LOCATION=US
```

A chave JSON da service account fica em `credentials/gcp-sa-key.json`. `.env` e `credentials/*.json` não entram no Git.

A conta de serviço precisa conseguir: rodar query no BigQuery (inclusive no dataset público), criar dataset e tabela, ler e gravar objetos no bucket, publicar e fazer pull no Pub/Sub, e criar o tópico de alerta.

### 3. Recursos que o script não cria

O código cria os datasets `alfabetizacao_bronze`, `alfabetizacao_silver`, `alfabetizacao_gold` e `alfabetizacao_ops`. Também cria `alfabetizacao-alertas` na primeira falha do Passo 8.

Estes quatro ficam a cargo de quem clona (console ou `gcloud`):

```bash
gcloud storage buckets create gs://SEU_BUCKET --location=us-central1 --uniform-bucket-level-access
gcloud pubsub topics create alfabetizacao-stream-topic --project=SEU_PROJETO
gcloud pubsub subscriptions create alfabetizacao-stream-sub \
  --topic=alfabetizacao-stream-topic \
  --ack-deadline=60 \
  --message-retention-duration=7d \
  --project=SEU_PROJETO
```

No console de billing, crie um orçamento com alerta em **R$ 1,00**. Sem isso o pipeline roda, mas o freio do Passo 1 não existe.

### 4. Da conexão até a Gold e um evento

Com a `.venv` ativa, na raiz do repositório:

```powershell
python test_gcp_connection.py
python bronze/ingest_batch.py
python quality/validate.py --layer bronze
python silver/transform.py
python quality/validate.py --layer silver
python gold/build.py
python streaming/producer.py --n 20
python streaming/consumer.py
```

Saída esperada: `[OK]` no teste (exit 0), validate Bronze e Silver com exit 0, Gold com exit 0. O producer publica 18 eventos válidos, 1 inválido e 1 duplicata. O consumer precisa rodar **depois**, enquanto a subscription ainda tem essas mensagens: 18 inserts, 1 duplicata ignorada, 1 arquivo em `bronze/stream_quarentena/`, latência > 0. A taxa oficial não muda.

Opcional, na mesma ordem do guia:

```powershell
python quality/prove_failure.py
python ops/prove_observability.py
python ops/finops_snapshot.py
```

Os dois primeiros **terminam com exit 1** de propósito (falha bloqueante provocada). O terceiro regrava [`evidence/passo_09/custo.md`](evidence/passo_09/custo.md).

Não passe `--run_id` se quiser a última Bronze. O `run_id` impresso pela ingestão é o que Silver e Gold usam quando o parâmetro vem vazio.

---

## Monitoramento

Cada etapa instrumentada faz **append** em `alfabetizacao_ops.pipeline_runs` (`run_id`, duração, linhas, status, bytes; stream também grava latência mínima, máxima e média).

Canais que existem de fato:

1. E-mail do orçamento de R$ 1,00 (console de billing).
2. Tópico `alfabetizacao-alertas`. Uma falha bloqueante publica um JSON. Prova: `python ops/prove_observability.py` e [`evidence/passo_08/`](evidence/passo_08/).

Não há PagerDuty nem Slack.

Na fotografia do Passo 9, `pipeline_runs` tem a etapa Silver (duas linhas `success`, ~56 s e ~58 s, 276.408.457 bytes) e a falha provocada. Bytes de Bronze e de Gold usados na conta vieram dos manifests e do `dry_run`, não dessa tabela.

## FinOps

`python ops/finops_snapshot.py`. Preços públicos consultados em **2026-10-18**. Premissa da projeção: **1 batch/dia** e **1.000 eventos/dia**. A execução atual e essa cadência ficam dentro do Always Free. A coluna da direita é o custo **depois** de descontar a cota, não uma fatura.

| Serviço | Unidade | Quantidade medida | Preço unitário | Custo mensal projetado |
|---------|---------|-------------------|----------------|------------------------|
| Cloud Storage | GiB-mês | 0,192 GiB (135 objetos, API) | US$ 0,020 / GiB-mês | US$ 0,00 (5 GiB grátis) |
| BigQuery | TiB/mês | 0,0207 TiB (760.231.654 bytes/batch × 30) | US$ 6,25 / TiB | US$ 0,00 (1 TiB grátis) |
| Pub/Sub | GiB/mês | 0,013 GiB (média 240 B × 1.000 eventos/dia × 30 × 2) | US$ 40 / TiB | US$ 0,00 (10 GiB grátis) |
| Computação | segundos | 56,2 s na Silver medida; motor serverless | embutido em BigQuery / Pub/Sub | US$ 0,00 |

O que segura esse número: Parquet, partição por `ingestion_date`/`run_id` e por `ano`, colunas explícitas no export, bucket em `us-central1` com BigQuery em `US`, consumer que não fica ligado, SQL em vez de cluster.

Detalhe e premissa: [`evidence/passo_09/custo.md`](evidence/passo_09/custo.md).

---

## Uso em IA (Fase 3)

A Gold está pronta como terreno de modelo: `indicador_municipio` (município × ano × rede × série), `evolucao_temporal` (trajetória com `LAG`) e `meta_vs_resultado` (distância até 80). Arquivo em `gs://<bucket>/gold/`.

Alvo típico: a `taxa_alfabetizacao` de um ano que ainda não aconteceu, ou `status_meta` / `gap_pp`.

**Vazam o alvo se entrarem como feature do mesmo ano:** a própria `taxa_alfabetizacao`, a `meta_alfabetizacao_2030` e o `status_meta` ou `gap_pp` calculados com ela.

Features que não são o rótulo: taxa e delta de anos anteriores, rede, série, e a composição `proporcao_aluno_nivel_*` **somente em 2024** (em 2023 essa coluna veio inteira nula; não imputar zero). Filtrar `origem = 'oficial'`. Não treinar com `eventos_stream`.

`validacao_microdado` mostra que, no caso típico, a taxa oficial e a taxa ponderada dos alunos diferem na terceira casa decimal (mediana absoluta 0,0037 pp). 57 de 12.408 linhas passam de 1 pp. O modelo deve usar a taxa oficial como alvo, não a reconstrução, quando as duas divergem.

---

## Limitações

Três origens diferentes. O que está fora por desenho não é lacuna da fonte, e o que a fonte não traz o pipeline preserva em vez de imputar.

### Decisão de arquitetura

O desenho cabe no Always Free: lake no GCS, transformação em SQL no BigQuery, evento no Pub/Sub, job que liga e desliga. O alerta de billing em R$ 1,00 é o freio se uma query sair da cota.

| Fora do repositório | Por quê |
|---------------------|---------|
| **Spark** | A aula ensina o Medalhão. O volume (~3,8 milhões de alunos) cabe em SQL serverless. Cluster ficaria ligado e sairia do free tier sem ganho analítico. Spark volta a fazer sentido se o microdado deixar de caber na cota. |
| **Kafka** | Pub/Sub cumpre produtor, tópico, consumidor, entrega *at-least-once*, duplicata e os dois relógios. Cluster 24/7, neste volume simulado, é custo contínuo. |
| **Terraform e orquestrador** | Bônus do guia. Bucket, tópico e subscription nascem uma vez (console ou `gcloud`); datasets e o tópico de alerta nascem nos scripts. A reprodução é a sequência de comandos deste README, não um DAG nem estado de infra. |
| **Banco vetorial** | Fora do escopo. Uso futuro: buscar municípios de trajetória parecida a partir de `indicador_municipio`. |
| **Cenário até 2030** | O guia permite a conta, com o nome de cenário. Não há tabela de projeção, para a reta não ser lida como previsão. |

### Limite da fonte

O Inep / Base dos Dados chega assim. A Bronze guarda o valor cru; a Gold não completa o que a fonte não publicou.

| O que aparece | Por que acontece | O que o pipeline faz |
|---------------|------------------|----------------------|
| Dois encodings de `rede` | Agregado usa código (`3`, `5`); meta usa rótulo (`Municipal`, `Pública`) | De-para na Silver, só esses dois pares. Igualdade direta de `rede` perde a meta. |
| ~3% `sem_meta` (242 linhas de rede 3: 146 em 2023, 96 em 2024) | A meta municipal não cobre todo o fato. Taxa média dessas linhas: 53,7, parecida com quem ficou abaixo de 80 | `LEFT JOIN` e status `sem_meta`. O gap permanece nulo. |
| RR, DF e AC | Meta de RR nula em 2023–2024. O agregado `uf` não traz RR nem DF em rede pública. AC entra nessa rede só em 2024 | A linha não é fabricada. |
| Brasil 2025 = 66,0 só na tabela de meta | O fato de UF vai até 2024 | O produto Brasil da Gold tem 2023 e 2024, os anos do lado esquerdo. |
| Níveis 0–8 nulos em 2023 | A composição por nível veio preenchida em 2024 (12.448 linhas) e vazia em 2023 (11.547) | Não vira zero. Zero diria que ninguém está no nível 0. |
| Rede privada: 25 alunos em 2024 | Quase não há microdado privado | A taxa (66,7% em 24 presentes) não entra em comparação. |

### Escopo desta entrega

- **Streaming simulado.** O Inep não publica este indicador em tempo real. O evento leva `origem = simulado` e não altera a taxa oficial.
- **Telemetria do Passo 9.** A duração em `pipeline_runs` nessa fotografia é a da Silver (~56 s). Bytes de Bronze e de Gold vieram do manifesto e do `dry_run`. O código já grava as outras etapas; essa run de referência foi medida antes dessas linhas existirem na tabela.
- **Vídeo.** O Passo 11 ainda não foi gravado. A seção seguinte reserva o link.

---

## Vídeo (Passo 11)

Ainda não gravado. Quando existir, o link entra aqui.

Roteiro previsto: o problema (2º ano, indicador, meta 80), a arquitetura em uma frase (batch histórico + evento simulado, Bronze → Silver → Gold no GCP), um número da Gold igual ao deste README (Ceará 2024, rede pública, 85,31, ou Brasil 2024, 59,2 contra meta 80), e o que a Fase 3 pode prever sem usar a taxa do mesmo ano como feature.

---

## Mapa do repositório

```text
tc-postech-fiap/
├── README.md                      # este arquivo
├── .env.example                   # variáveis; .env não sobe
├── requirements.txt               # versões pinadas com ==
├── test_gcp_connection.py
├── docs/
│   ├── contrato_dados.md
│   ├── avaliacao_conformidade.md  # pedido do challenge × o que foi feito
│   └── Tech_Challenge_Fase2_Passo_a_Passo.md
├── sql/          DECISOES.md      # perfil, exploração, Silver, Gold
├── bronze/       DECISOES.md
├── quality/      DECISOES.md
├── silver/       DECISOES.md
├── gold/         DECISOES.md
├── streaming/    DECISOES.md
├── ops/          DECISOES.md
└── evidence/
    ├── passo_01/ … passo_09/      # cada pasta tem ANALISE.md
    ├── passo_10/                  # este README e as consultas de leitura
    └── passo_11/                  # vídeo, ainda vazio
```

Contrato de grain, chave e limiar: [`docs/contrato_dados.md`](docs/contrato_dados.md).

---

## Problemas comuns

| Sintoma | O que fazer |
|---------|-------------|
| `python` não encontrado | Use `python3`, ou instale Python 3.14 e marque “Add to PATH” |
| PowerShell bloqueia a `.venv` | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `[FALHA]` no teste de conexão | Confira projeto, bucket, chave e se o tópico `alfabetizacao-stream-topic` existe. Exit 1 é o teste funcionando |
| `[AVISO]` sobre `alfabetizacao-alertas` | Normal antes do Passo 8. O tópico nasce na prova de observabilidade |
| Consumer recebe 0 mensagens | Rode o producer primeiro. A subscription é Pull; mensagem já confirmada (ack) não volta |
| `prove_failure` ou `prove_observability` saem com erro | Esperado. Exit 1 é o critério de pronto |
| Silver ou Gold vazias | A Bronze precisa ter terminado. Sem `--run_id`, os scripts usam a última `ingestion_ts` |
