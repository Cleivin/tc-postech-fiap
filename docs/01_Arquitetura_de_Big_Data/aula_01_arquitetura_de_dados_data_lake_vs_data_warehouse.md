# Arquitetura de dados: Data Lake vs Data Warehouse

**Arquitetura de Big Data** · Aula 1 · Fase 2 — Data Prepare

Compara Data Lake e Data Warehouse, casos de uso e quando combinar (lakehouse).

**Tópicos:** `Data Lake` · `Data Warehouse` · `Lakehouse` · `dados brutos vs curados`

📄 [PDF da aula](./aula_01_arquitetura_de_dados_data_lake_vs_data_warehouse.pdf)

---

## Conteúdo

### Página 1

Arquitetura de dados: Data Lake vs Data Warehouse

ARQUITETURA DE
DADOS: DATA LAKE VS
DATA WAREHOUSE

### Página 2

Arquitetura de dados: Data Lake vs Data Warehouse

MERCADO, CASES E TENDÊNCIAS 21

### Página 3

Arquitetura de dados: Data Lake vs Data Warehouse

Quando abordamos arquitetura de dados, inevitavelmente falamos de decisões
que impactam diretamente a forma como uma organização gera valor a partir da
informação. Muito antes do Big Data, dois grandes pensadores moldaram a forma
como empresas organizam seus dados analíticos: Ralph Kimball e Bill Inmon. Suas
abordagens, embora diferentes, seguem influenciando arquiteturas modernas até
hoje.
Neste material, você vai entender quem são Kimball e Inmon, quais são suas
modelagens, as diferenças conceituais entre elas e como essas ideias evoluíram até
o surgimento do Data Lake. Além disso, veremos na prática como essas arquiteturas
convivem no mundo real, implementando um Data Warehouse  e um Data Lake
utilizando o Databricks, uma das plataformas mais adotadas atualmente em
ambientes de Big Data.

### Página 4

Arquitetura de dados: Data Lake vs Data Warehouse

Data Warehouse E Data Lake No Databricks
Este hands on transforma conceitos arquiteturais em prática real. Você irá
implementar duas arquiteturas no mesmo ambiente: primeiro um Data Warehouse
tradicional, depois um Data Lake em camadas, evidenciando diferenças de
modelagem, ingestão e consumo de dados.
A ideia central é mostrar que Data Warehouse e Data Lake não competem —
eles se complementam dentro de uma arquitetura moderna (Lakehouse). Todo o
cenário será construído no Databricks, simulando um ambiente corporativo completo:
criação do workspace, inge stão de dados, transformação, modelagem e consumo
analítico.

### Página 5

Arquitetura de dados: Data Lake vs Data Warehouse

Introdução ao Databricks
O Databricks é uma plataforma unificada de dados e analytics criada pelos
próprios autores do Apache Spark,  e projetada para simplificar o trabalho com
engenharia de dados, analytics, ciência de dados e Machine Learning em um único
ambiente colaborativo. Ele abstrai grande parte da complexidade de infraestrutura,
permitindo que times foquem na arquitetura, nos dados e no valor de negócio.
Na prática, o Databricks viabiliza o conceito de Lakehouse, combinando o
melhor dos dois mundos:  a governança, performance e confiabilidade dos Data
Warehouses com a flexibilidade e escalabilidade dos Data Lakes
Tudo isso usando notebooks, SQL, jobs, clusters elásticos  e
armazenamento desacoplado, o que o torna ideal para simular cenários
corporativos reais, como faremos neste hands on.
Por que Databricks neste tutorial?
Porque ele permite implementar, no mesmo ambiente , tanto um Data
Warehouse tradicional quanto um Data Lake em camadas, evidenciando diferenças
de abordagem sem trocar de ferramenta  — exatamente como acontece em
arquiteturas modernas de dados.
Para o hands on (na seção anterior) , utilizaremos o Databricks Community
Edition, uma versão gratuita da plataforma, ideal para estudos, provas de conceito
e aprendizado prático. Apesar de ter limitações de escala e recursos corporativos,
ela mantém os principais conceitos e ferramentas da plataforma: notebooks, Spark,
SQL e armazenamento de dados, sendo perfeita para experimentar arquiteturas de
Data Warehouse e Data Lake.
Por que usar o Databricks Community?
• Não exige cartão de crédito.
• Ambiente pronto para uso em minutos.
• Suporte a SQL, Python e Spark.

### Página 6

Arquitetura de dados: Data Lake vs Data Warehouse

• Ideal para aulas, laboratórios e estudos individuais.
Tudo o que será construído aqui reflete práticas reais de mercado — apenas
adaptadas ao contexto educacional da Community Edition.
Parte 0 – Acessando o Databricks Community Edition
Criar sua conta:
1. Acesse o site.
2. Crie uma conta gratuita ou faça login.
3. Após o login, você será direcionado automaticamente para o Workspace.
No Community Edition, o cluster já vem pré-configurado e iniciado.

Figura 1 – Criando conta
Fonte: Databricks (2026)

Escolha a opção “Sign Up for Free Edition” e a forma de fazer o login.

### Página 7

Arquitetura de dados: Data Lake vs Data Warehouse

Figura 2 – Inscrição
Fonte: Databricks (2026)

Entendendo o Ambiente

Figura 3 – Ambiente
Fonte: Databricks (2026)

Menu lateral esquerdo
• Home → Visão geral.
• Workspace → Onde você cria notebooks e organiza pastas ( é aqui que
vamos trabalhar).

### Página 8

Arquitetura de dados: Data Lake vs Data Warehouse

• Catalog → Metadados e tabelas.
• Compute → (limitado no Free Edition, já vem pronto).
• SQL Editor → Consultas SQL.
• Dashboards → Visualização analítica.
• Jobs & Pipelines → Execuções (não usaremos aqui).
 Importante:
 No Free Edition, não é necessário criar cluster manualmente — o ambiente
já está pronto para executar notebooks.
ETAPA 0 – Criar o Volume (Storage)
Criar Volume no Catalog
1. No menu esquerdo, clique em Catalog.
2. Selecione:
o Catalog: workspace;
o Schema: default.
3. Clique em Create → Volume.
4. Configure:
o Name: tutorial_fiap;
Type: Managed.
5. Clique em Create.
Isso cria o caminho físico: /Volumes/workspace/default/tutorial_fiap/
 Upload do arquivo CSV para o Volume
Ainda em Catalog:
• Navegue até:  workspace → default → tutorial_fiap.
• Clique em Upload e faça upload do arquivo:  vendas.csv.
• Confirme que o arquivo aparece em:
Volumes/workspace/default/tutorial_fiap/vendas.csv.

### Página 9

Arquitetura de dados: Data Lake vs Data Warehouse

Upload do arquivo CSV para o Volume
Ainda em Catalog:
• Navegue até: workspace → default → tutorial_fiap.
• Clique em Upload e  faça upload do arquivo:  vendas.csv.
Confirme que o arquivo aparece em:
/Volumes/workspace/default/tutorial_fiap/vendas.csv.
ETAPA 1 – Criar os Notebooks
Criar Notebook SQL – Data Warehouse:
• Clique em Workspace.
• Clique em Create ▾ → Notebook.
• Configure:
o Name: 01_dw_hands_on;
o Language: SQL;
o Location: seu usuário.
Criar Notebook SQL – Data Lake
• Clique em Workspace.
• Clique em Create ▾ → Notebook.
• Configure:
o Name: 02_dl_hands_on.
o Language: SQL.
Usaremos somente SQL neste hands on para reforçar o foco arquitetural.
PARTE 1 – Data Warehouse (Notebook 01_dw_hands_on)
Criar Database de Staging: CREATE DATABASE IF NOT EXISTS dw_staging;
Criar Tabela Staging (CTAS + read_files()).

### Página 10

Arquitetura de dados: Data Lake vs Data Warehouse

Código-fonte 1 – SQL
Fonte: elaborado pelo autor (2026)

Criar Database Analítico: CREATE DATABASE IF NOT EXISTS dw;
Modelagem Dimensional
Dimensão Cliente:
Código-fonte 2 – SQL
Fonte: elaborado pelo autor (2026)

Dimensão Produto
CREATE TABLE dw_staging.vendas_raw
AS
SELECT
  CAST(id_venda AS INT)       AS id_venda,
  CAST(id_cliente AS INT)     AS id_cliente,
  CAST(id_produto AS INT)     AS id_produto,
  CAST(data_venda AS DATE)    AS data_venda,
  CAST(quantidade AS INT)     AS quantidade,
  CAST(valor_total AS DOUBLE) AS valor_total
FROM read_files(
  '/Volumes/workspace/default/tutorial_fiap/vendas.csv',
  format => 'csv',
  header => 'true'
);
CREATE TABLE dw.dim_cliente AS
SELECT DISTINCT
  id_cliente,
  CONCAT('Cliente ', id_cliente) AS nome_cliente
FROM dw_staging.vendas_raw;

### Página 11

Arquitetura de dados: Data Lake vs Data Warehouse

Código-fonte 3 – SQL
Fonte: elaborado pelo autor (2026)

Fato Vendas
Código-fonte 4 – SQL
Fonte: elaborado pelo autor (2026)

Consulta Analítica
Código-fonte 5 – SQL
Fonte: elaborado pelo autor (2026)

PARTE 2 – Data Lake (Notebook 02_dl_hands_on)
CREATE TABLE dw.dim_produto AS
SELECT DISTINCT
  id_produto,
  CONCAT('Produto ', id_produto) AS nome_produto
FROM dw_staging.vendas_raw;
CREATE TABLE dw.fato_vendas AS
SELECT
  id_venda,
  id_cliente,
  id_produto,
  data_venda,
  quantidade,
  valor_total
FROM dw_staging.vendas_raw;
SELECT
  p.nome_produto,
  SUM(f.valor_total) AS faturamento
FROM dw.fato_vendas f
JOIN dw.dim_produto p
  ON f.id_produto = p.id_produto
GROUP BY p.nome_produto;

### Página 12

Arquitetura de dados: Data Lake vs Data Warehouse

Criar Database do Data Lake: CREATE DATABASE IF NOT EXISTS datalake.

Camada RAW
Código-fonte 6 – SQL
Fonte: elaborado pelo autor (2026)

Camada REFINED
Código-fonte 7 – SQL
Fonte: elaborado pelo autor (2026)

 Camada CURATED
CREATE TABLE datalake.raw_vendas
AS
SELECT *
FROM read_files(
  '/Volumes/workspace/default/tutorial_fiap/vendas.csv',
  format => 'csv',
  header => 'true'
);
CREATE TABLE datalake.refined_vendas
AS
SELECT
  CAST(id_venda AS INT)       AS id_venda,
  CAST(id_cliente AS INT)     AS id_cliente,
  CAST(id_produto AS INT)     AS id_produto,
  CAST(data_venda AS DATE)    AS data_venda,
  CAST(quantidade AS INT)     AS quantidade,
  CAST(valor_total AS DOUBLE) AS valor_total
FROM datalake.raw_vendas;

### Página 13

Arquitetura de dados: Data Lake vs Data Warehouse

Código-fonte 8 – SQL
Fonte: elaborado pelo autor (2026)

Kimball e Inmon: quem são e por que são tão importantes?
Ralph Kimball é conhecido como o principal defensor da abordagem bottom-
up para Data Warehousing. Sua proposta parte das áreas de negócio, criando Data
Marts específicos que, juntos, formam o Data Warehouse corporativo. Sua principal
contribuição é a modelagem dimensional, focada em simplicidade, performance e
facilidade de uso para análise.
Bill Inmon , por outro lado, é considerado o “pai do Data Warehouse”. Ele
defende uma abordagem top-down, onde primeiro se constrói um Data Warehouse
corporativo centralizado, altamente normalizado, para depois derivar Data Marts
específicos. Sua visão prioriza integração, consistência e governança desde a origem.
MODELAGEM KIMBALL – DIMENSIONAL
Star Schema
CREATE TABLE datalake.curated_faturamento_produto
AS
SELECT
  id_produto,
  SUM(valor_total) AS faturamento_total
FROM datalake.refined_vendas
GROUP BY id_produto;

### Página 14

Arquitetura de dados: Data Lake vs Data Warehouse

Figura 4 - Star Schema
Fonte: Elaborado pelo autor (2026)

Snowflake Schema

### Página 15

Arquitetura de dados: Data Lake vs Data Warehouse

Figura 5 - Snowflake Schema
Fonte: Elaborado pelo autor (2026)

A modelagem de Kimball utiliza estruturas como Star Schema e Snowflake
Schema, organizando os dados em:
• Tabelas Fato: métricas e eventos de negócio.
Tabelas Dimensão: contexto descritivo (tempo, cliente, produto).
Essa abordagem é amplamente utilizada em ambientes analíticos por oferecer:
• Alta performance em consultas.
• Facilidade de entendimento pelo negócio.
• Forte aderência a ferramentas de BI.

Modelagem Inmon – Corporativa Normalizada

### Página 16

Arquitetura de dados: Data Lake vs Data Warehouse

Figura 6 - Modelagem Inmon – Corporativa Normalizada
Fonte: Elaborado pelo autor (2026)

A proposta de Inmon é construir um Data Warehouse corporativo em 3ª forma
normal, altamente integrado, servindo como fonte única da verdade. A partir dele, os
Data Marts são derivados conforme a necessidade das áreas de negócio.
Essa abordagem oferece:
• Alto nível de governança.
• Consistência semântica.
• Maior complexidade de implementação.
• Menor flexibilidade para mudanças rápidas.

COMO SURGIU O DATA LAKE?
Com o crescimento exponencial de dados não estruturados e semiestruturados,
as arquiteturas tradicionais passaram a enfrentar limitações. Surgiu então o Data
Lake, impulsionado por tecnologias como Hadoop e armazenamento em cloud.
O Data Lake nasceu para resolver três grandes desafios:
• Armazenar grandes volumes de dados a baixo custo.

### Página 17

Arquitetura de dados: Data Lake vs Data Warehouse

• Suportar múltiplos formatos de dados.
• Permitir novos tipos de análise, como Machine Learning.
Diferente do Data Warehouse, o Data Lake adota o conceito de schema -on-
read, onde a estrutura dos dados é definida no momento do consumo.
DATA WAREHOUSE X DATA LAKE: UMA VISÃO EVOLUTIVA DA
ARQUITETURA DE DADOS

Figura 7 - Data Warehouse X Data Lake
Fonte: Elaborado pelo autor (2026)

A evolução das arquiteturas de dados reflete diretamente a transformação da
forma como as organizações utilizam informação para gerar valor. Inicialmente, o foco
estava em consolidar dados estruturados para relatórios gerenciais. Com o tempo,
surgiram nova s demandas analíticas, novos tipos de dados e a necessidade de
respostas mais rápidas e preditivas. Esse movimento levou à transição de arquiteturas
tradicionais para modelos mais flexíveis e, posteriormente, para arquiteturas
unificadas.
Essa evolução não ocorreu por modismo tecnológico, mas como resposta
prática ao crescimento exponencial do volume de dados, à diversidade de formatos e

### Página 18

Arquitetura de dados: Data Lake vs Data Warehouse

à necessidade de análises cada vez mais avançadas, indo além do simples reporte
histórico.
DATA WAREHOUSE: O PILAR DA ANÁLISE ESTRUTURADA E CONFIÁVEL
O Data Warehouse representa a primeira grande consolidação da arquitetura
analítica corporativa. Ele foi projetado para armazenar dados estruturados ,
provenientes de sistemas transacionais como ERPs, CRMs e sistemas financeiros.
Antes de serem armazenados, esses dados passam por processos rigorosos de ETL
(Extract, Transform, Load), garantindo padronização, qualidade e integração.
Essa abordagem oferece benefícios claros para o negócio, como:
• Alta consistência e confiabilidade das informações.
• Forte governança e controle dos dados.
• Excelente desempenho para consultas analíticas, BI e relatórios.
No entanto, o Data Warehouse é naturalmente orientado a análises históricas,
respondendo principalmente à pergunta “o que aconteceu?” . A inclusão de novos
tipos de dados ou novas perguntas analíticas costuma exigir mudanças estruturais
nos pipelines e nos modelos, tornando essa arquitetura menos flexível frente a
cenários de inovação, dados não estruturados e análises avançadas.
DATA LAKE: FLEXIBILIDADE, ESCALA E EXPLORAÇÃO ANALÍTICA
Com o crescimento de dados semiestruturados e não estruturados — como
logs, eventos, arquivos de mídia e dados de sensores — surgiu a necessidade de uma
arquitetura mais flexível. O Data Lake atende a esse cenário ao permitir o
armazenamento de dados em seu formato bruto, independentemente de estrutura.
Nessa abordagem, o Data Lake torna -se a base central da arquitetura de
dados, possibilitando:
• Exploração direta por equipes de Data Science.
• Acesso a grandes volumes de dados históricos para Machine Learning.
• Transformação seletiva de dados para consumo analítico tradicional.

### Página 19

Arquitetura de dados: Data Lake vs Data Warehouse

O conceito de schema-on-read é um dos principais diferenciais do Data Lake,
pois a estrutura dos dados é definida apenas no momento do uso. Isso amplia
significativamente a capacidade de experimentação e inovação, mas também traz
desafios importantes relacionados à governança, catalogação e qualidade dos dados.
Sem controles adequados, o Data Lake pode perder valor e se tornar um repositório
desorganizado, conhecido como data swamp.
Nesse contexto, o Data Warehouse não desaparece, mas passa a atuar como
uma camada de consumo refinado, alimentada por dados preparados a partir do Data
Lake.
DATA LAKEHOUSE: A CONVERGÊNCIA ENTRE CONTROLE E FLEXIBILIDADE
A arquitetura de Data Lakehouse surge como uma resposta à complexidade
crescente dos ambientes híbridos. Seu objetivo é unificar os pontos fortes do Data
Warehouse e do Data Lake em uma única arquitetura coerente.
No modelo Lakehouse:
• Os dados permanecem armazenados no Data Lake.
• Existe uma camada explícita de metadados, governança e controle.
• O mesmo conjunto de dados pode ser utilizado para BI, relatórios, Data
Science e Machine Learning.
• Consultas analíticas SQL são executadas diretamente sobre o lake, com
desempenho.
Essa convergência reduz a duplicação de dados, simplifica pipelines, diminui
custos operacionais e acelera o tempo entre ingestão e geração de insights.
Tecnologias modernas permitem aplicar controle de esquema, versionamento,
transações ACID, auditoria e otimização de performance diretamente sobre o Data
Lake.

A evolução arquitetural em perspectiva
De forma consolidada, essa evolução arquitetural atende a necessidades
específicas ao longo do tempo:

### Página 20

Arquitetura de dados: Data Lake vs Data Warehouse

• Data Warehouse  resolve a necessidade de análises estruturadas,
governadas e confiáveis.
• Data Lake  atende à necessidade de escala, diversidade de dados e
inovação analítica.
Data Lakehouse resolve a fragmentação arquitetural, unificando consumo
analítico e exploração avançada.
Essa transição representa uma mudança de mentalidade: de arquiteturas
rígidas e centradas exclusivamente em BI para arquiteturas data-driven, capazes de
sustentar decisões operacionais, estratégicas e preditivas dentro de um único
ecossistema de dados.
Conexão com o papel do arquiteto de Big Data
Para o arquiteto de Big Data, compreender essa evolução é essencial. A
decisão arquitetural moderna não é mais escolher entre Data Lake ou Data
Warehouse, mas definir como essas abordagens se combinam de forma eficiente
e sustentável.
Essa decisão deve considerar:
• Casos de uso e objetivos do negócio.
• Requisitos de governança, segurança e compliance.
• Custos de armazenamento e processamento.
• Escalabilidade e desempenho das soluções.
• Maturidade analítica e organizacional da empresa.
Arquiteturas modernas não descartam modelos anteriores — elas absorvem,
estendem e evoluem esses conceitos para atender às demandas atuais e futuras do
uso de dados.

### Página 21

Arquitetura de dados: Data Lake vs Data Warehouse

A forma como as organizações arquitetam seus dados evoluiu
significativamente nos últimos anos. O aumento do volume de dados, a diversidade
de formatos e a necessidade de análises mais rápidas e avançadas impulsionaram
mudanças profundas nas arquiteturas corporativas. Hoje, Data Warehouse, Data Lake
e Data Lakehouse não são apenas escolhas técnicas, mas decisões estratégicas que
impactam diretamente competitividade, inovação e eficiência operacional.
Arquiteturas modernas no mercado
Empresas data -driven adotam arquiteturas híbridas, nas quais o Data Lake
atua como repositório central de dados e o Data Warehouse  permanece como
camada analítica governada para BI e relatórios executivos. Esse modelo permite
atender, simultaneamente, áreas de negócio, analytics avançado e ciência de dados,
reduzindo silos e duplicação de dados.
Plataformas unificadas, como o Databricks, ganharam destaque ao viabilizar
o conceito de Lakehouse, oferecendo governança, performance analítica e
flexibilidade no mesmo ambiente. Esse movimento tem reduzido a complexidade
arquitetural e acelerado o tempo entre ingestão e geração de valor.
A evolução das arquiteturas de dados tem sido amplamente discutida por
especialistas da indústria e da academia, refletindo a necessidade crescente de
arquiteturas mais flexíveis, escaláveis e orientadas a múltiplos tipos de análise. Para
aprofundar esse debate e conectar o conteúdo da aula com o que há de mais atual no
mercado, recomenda -se o acompanhamento de materiais que abordam tanto os
fundamentos quanto as tendências emergentes da área.
Artigo recomendado
Databricks Lakehouse Data Modeling: Myths, Truths, and Best Practices: Artigo
que discute como conceitos clássicos de modelagem (Kimball e Inmon) são aplicados
e reinterpretados em arquiteturas Lakehouse, apresentando boas práticas para
ambientes modernos de dados.

### Página 22

Arquitetura de dados: Data Lake vs Data Warehouse

Podcast recomendado
Data Engineering Podcast : Podcast voltado a arquiteturas modernas
de dados, abordando temas como Data Lake, Data Warehouse, Lakehouse,
engenharia de dados e analytics em escala, sempre com convidados atuantes
no mercado.

Livro recomendado
The Data Warehouse Toolkit – Ralph Kimball
Livro clássico que fundamenta a modelagem dimensional e continua sendo
referência para arquiteturas analíticas modernas, inclusive em contextos de Data
Lakehouse.

### Página 23

Arquitetura de dados: Data Lake vs Data Warehouse

Nesta aula, você compreendeu que arquitetura de dados é uma decisão
estratégica, capaz de impactar diretamente a forma como as organizações
transformam dados em valor de negócio.
Você conheceu os principais pensadores que fundamentaram a área de Data
Warehousing, Ralph Kimball e Bill Inmon, entendendo suas abordagens, diferenças
conceituais e como suas modelagens influenciam arquiteturas analíticas até os dias
atuais.
Explorou, de forma teórica e prática, a evolução das arquiteturas de dados,
desde o Data Warehouse tradicional, passando pelo surgimento do Data Lake, até
chegar ao conceito moderno de Data Lakehouse , que unifica governança,
flexibilidade e múltiplos tipos de consumo analítico.
Por fim, você conectou teoria, prática e mercado, entendendo que arquiteturas
modernas não substituem modelos anteriores , mas os absorvem e evoluem , e
que o papel do arquiteto de Big Data é justamente decidir como combinar essas
abordagens de acordo com objetivos de negócio, governança, custo e maturidade
analítica da organização.

### Página 24

Arquitetura de dados: Data Lake vs Data Warehouse

DATABRICKS. Databricks Free Edition . Disponível em:
https://www.databricks.com/learn/free-edition. Acesso em: 26 fev. 2026.
DATABRICKS. Databricks Lakehouse Data Modeling : Myths, Truths, and Best
Practices. 2023. Disponível em: https://www.databricks.com/blog/databricks -
lakehouse-data-modeling-myths-truths-and-best-practices. Acesso em: 26 fev. 2026.
DATABRICKS. Introduction to Databricks . Disponível em:
https://docs.databricks.com/en/introduction/. Acesso em: 26 fev. 2026.
DATABRICKS. What is a Data Lakehouse?.  2020. Disponível em:
https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html. Acesso
em: 26 fev. 2026.
INMON, W. H. Building the Data Warehouse. Hoboken: John Wiley & Sons, 2005.
KIMBALL, R. The Data Warehouse Toolkit: The Definitive Guide to Dimensional
Modeling. Hoboken: John Wiley & Sons, 2013.

### Página 25

Arquitetura de dados: Data Lake vs Data Warehouse

PALAVRAS-CHAVE
Data Warehouse. Data Lake. Databricks.

### Página 26

Arquitetura de dados: Data Lake vs Data Warehouse
