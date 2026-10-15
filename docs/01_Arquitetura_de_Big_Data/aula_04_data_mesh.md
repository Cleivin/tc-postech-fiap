# Data Mesh

**Arquitetura de Big Data** · Aula 4 · Fase 2 — Data Prepare

Arquitetura Data Mesh: domínio, produtos de dados e governança descentralizada.

**Tópicos:** `Data Mesh` · `produtos de dados` · `governança` · `domínio`

📄 [PDF da aula](./aula_04_data_mesh.pdf)

---

## Conteúdo

### Página 1

Data Mesh

DATA MESH

### Página 2

Data Mesh

### Página 3

Data Mesh

À medida que as organizações crescem e se tornam cada vez mais orientadas
por dados, os modelos centralizados de analytics começam a mostrar seus limites.
Times sobrecarregados, gargalos de entrega, dados pouco confiáveis e uma distância
crescente entre quem produz e quem consome informação passam a ser problemas
recorrentes. É nesse contexto que o Data Mesh surge não apenas como uma nova
arquitetura de dados, mas como uma mudança profunda de mentalidade, combinando
tecnologia, organização e cultura.
Nesta etapa, você vai avançar para além dos fundamentos e entender para
onde o Data Mesh está evoluindo . Vamos discutir como princípios como data as a
product, domain ownership  e self-serve data platforms  estão sendo aplicados na
prática, quais desafios ainda precisam ser superados e como o Data Mesh se conecta
com tendências como plataformas cloud -native, governança automatizada e
inteligência artificial. A ideia aqui é provocar: será que o futuro dos dados está menos
em grandes pipelines centralizados e mais em ecossistemas distribuídos, porém bem
governados?

### Página 4

Data Mesh

Antes de iniciar as atividades práticas, é fundamental garantir que o conjunto
de dados utilizado no hands on esteja acessível no ambiente Databricks. Nesta aula,
será utilizado um dataset público que já vem disponível nativamente no Databricks
Community Edition , armazenado no DBFS (Databricks File System) . O arquivo
utilizado encontra-se no seguinte caminho:
/databricks-datasets/samples/population-vs-
price/data_geo.csv
Para validar a existência do arquivo, o primeiro passo é executar um comando
simples diretamente no notebook do Databricks. Essa verificação faz parte da rotina
profissional de quem trabalha com dados em ambientes distribuídos, garantindo que
a fonte esteja disponível antes de iniciar qualquer processamento.
dbutils.fs.ls("/databricks-datasets/samples/population-vs-
price")
Ao executar esse comando, o Databricks retornará a lista de arquivos presentes
no diretório, incluindo o arquivo data_geo.csv. Caso o arquivo seja exibido, o
ambiente está pronto para a execução do hands on. Essa etapa dispensa qualquer
necessidade de upload manual de dados, tornando a atividade totalmente reprodutível
mesmo em ambientes gratuitos.
Com o dataset validado, inicia -se a manipulação de dados utilizando Apache
Spark por meio da API de DataFrames. Nesta etapa, você irá carregar o arquivo CSV,
explorando suas colunas e compreendendo sua estrutura inicial, como parte do
processo de análise exploratória.
Passo a Passo — Preparando o Ambiente
Passo 1 — Acessar o Databricks Free
1. Acesse: https://community.cloud.databricks.com.
2. Faça login ou crie uma conta gratuita.
3. Após o login, você será direcionado ao Workspace.

### Página 5

Data Mesh

Passo 2 — Criar um Notebook
1. No menu lateral esquerdo, clique em Workspace.
2. Clique com o botão direito → Create → Notebook.
Nomeie o notebook, por exemplo:

 HandsOn_SparkAgg_Databricks
Selecione:
• Language: Python.
• Cluster: Starter (padrão do Community Edition).
Passo 3 — Validar o Ambiente
Execute a célula abaixo para validar o ambiente Spark:
Python.
Spark.
Se o objeto SparkSession for exibido, o ambiente está pronto.
Introdução ao Hands On
Nesta etapa prática, o objetivo é conduzir o aluno a vivenciar o Data Mesh como
um modelo arquitetural e organizacional aplicado a um cenário realista. Ao longo do
hands on, o (a) estudante será inserido (a) no contexto de uma empresa digital que
passou por rápido crescimento e começou a enfrentar limitações em seu modelo
centralizado de dados, como atrasos na entrega de análises, sobrecarga do time
central e dificuldade em identificar responsabilidades sobre  a qualidade da
informação.
O cenário adotado é o de um marketplace digital organizado por domínios de
negócio. Para simular essa estrutura no Databricks Community Edition, o ambiente é
inicialmente preparado com a separação lógica dos domínios, representados por

### Página 6

Data Mesh

diferentes bases de dados. Cada domínio passa a operar de forma relativamente
independente, refletindo a ideia central do Data Mesh de descentralização da
responsabilidade sobre os dados. Na prática, essa separação é realizada por meio da
criação de bases específicas, como sales, customers, logistics e analytics,
que simbolizam os limites organizacionais entre os times.
A partir desse contexto, o hands on inicia a construção do primeiro produto de
dados do domínio de Vendas. Utilizando dados brutos de pedidos armazenados na
camada raw, o domínio de Vendas publica o data product sales_orders, que
consolida informações essenciais como identificador do pedido, data, cliente, status e
valor total. Esse produto de dados é criado com um schema explícito, reforçando a
noção de contrato, e passa a ser a fonte oficial para análises relacionadas a
faturamento e pedidos. Durante essa etapa, o aluno observa que o domínio de Vendas
é responsável tanto pela estrutura quanto pela qualidade desse dado, não delegando
essa função a um time central.
Em seguida, o hands on avança para o domínio de Clientes, que publica seu
próprio produto de dados, denominado customer_profile. Esse data product
consolida informações cadastrais e de segmentação dos clientes, sendo construído
de forma independente do domínio de Vendas. A separação entre esses produtos
reforça o princípio de desacoplamento entre domínios, ao mesmo tempo em que
evidencia a necessidade de contratos claros, uma vez que esses dados serão
consumidos por outros times. O(a) aluno(a) é levado a refletir que qualquer mudança
no significado ou na estrutura desses dados deve ser tratada como uma decisão de
produto, e não como um ajuste técnico isolado.
Ao longo do hands on, são apresentados exemplos práticos de governança
computacional aplicada. Em vez de processos manuais ou validações pontuais, o
aluno acompanha consultas simples que verificam a integridade dos dados
publicados, como a ausência de valores nulos em chaves primárias ou a identificação
de valores inconsistentes. Essas validações ilustram como regras de qualidade podem
ser incorporadas ao próprio ciclo de publicação dos dados, tornando a governança
parte do código e não apenas de políticas documentais.
Na sequência, o domínio de Logística publica o data product
delivery_status, responsável por informações relacionadas ao status das

### Página 7

Data Mesh

entregas e atrasos. Com esse novo produto disponível, o hands on demonstra o papel
do domínio Analytics, que atua exclusivamente como consumidor de dados. Nesse
momento, são criadas visões analíticas que cruzam informações de Vendas, Clientes
e Logística para gerar indicadores de negócio, como receita por segmento de cliente
ou atraso médio nas entregas. O foco dessa etapa não está na complexidade das
consultas SQL, mas na facilidade de consumo dos dados, que já se encontram
padronizados, documentados e com responsáveis claramente definidos.
Ao final da atividade prática, o (a) aluno(a) consegue perceber de forma
concreta os benefícios e desafios do Data Mesh. Caso um problema seja identificado
em um indicador, torna -se evidente qual domínio deve ser acionado, eliminando
ambiguidades comuns em arquiteturas centralizadas. O hands on, portanto, evidencia
que o Data Mesh não se resume a uma mudança tecnológica, mas representa uma
transformação na forma como dados são tratados como produtos, como a governança
é aplicada e como as organizações escalam o uso analítico de dados.
Importante para aula:
Execute todos os comandos abaixo em um Notebook SQL usando %%sql (ou
%sql por célula).
Preparação do ambiente por domínios
No Databricks Community Edition, os domínios são representados por
Databases (Schemas) dentro do metastore padrão.
CREATE DATABASE IF NOT EXISTS raw;
CREATE DATABASE IF NOT EXISTS sales;
CREATE DATABASE IF NOT EXISTS customers;
CREATE DATABASE IF NOT EXISTS logistics;
CREATE DATABASE IF NOT EXISTS analytics;
Boa prática Databricks (didática)
Sempre referencie objetos como database.table, evitando depender de
USE database.

### Página 8

Data Mesh

Criação dos dados brutos (simulação do legado)
Tabela de pedidos — raw.orders
CREATE TABLE IF NOT EXISTS raw.orders (
  order_id STRING,
  order_timestamp TIMESTAMP,
  customer_id STRING,
  status STRING,
  total_value DOUBLE
)
USING DELTA;

INSERT INTO raw.orders VALUES
('O1', current_timestamp(), 'C1', 'COMPLETED', 250.0),
('O2', current_timestamp(), 'C2', 'COMPLETED', 120.0),
('O3', current_timestamp(), 'C1', 'CANCELLED', 90.0);
Código- fonte 1: Tabela de pedidos - SQL (Structured Query Language).
Fonte: Elaborado pelo autor (2026)

Tabela de clientes — raw.customers
CREATE TABLE IF NOT EXISTS raw.customers (
  id STRING,
  name STRING,
  segment STRING,
  status STRING,
  created_at TIMESTAMP
)
USING DELTA;

INSERT INTO raw.customers VALUES
('C1', 'Ana', 'Premium', 'ACTIVE', current_timestamp()),
('C2', 'João', 'Standard', 'ACTIVE', current_timestamp());
Código- fonte 2: Tabela de clientes - SQL (Structured Query Language).
Fonte: Elaborado pelo autor (2026)

Tabela de entregas — raw.deliveries
CREATE TABLE IF NOT EXISTS raw.deliveries (
  order_id STRING,
  delivery_timestamp TIMESTAMP,
  status STRING,
  delay_days INT
)
USING DELTA;

INSERT INTO raw.deliveries VALUES

### Página 9

Data Mesh

('O1', current_timestamp(), 'DELIVERED', 0),
('O2', current_timestamp(), 'DELIVERED', 2);
Código- fonte 3: Tabela de entregas - SQL (Structured Query Language).
Fonte: Elaborado pelo autor (2026)

Mensagem didática importante
 Essas tabelas não são Data Products — são apenas dados operacionais
brutos.

Domínio Vendas — Publicação do Data Product
Criação do produto de dados
CREATE TABLE IF NOT EXISTS sales.sales_orders (
  order_id STRING NOT NULL,
  order_date DATE,
  customer_id STRING,
  order_status STRING,
  total_amount DOUBLE,
  created_at TIMESTAMP
)
USING DELTA;
Código- fonte 4: Criação do produto de dados - SQL (Structured Query Language).
Fonte: Elaborado pelo autor (2026)

Publicação do Data Product
INSERT INTO sales.sales_orders
SELECT
  order_id,
  CAST(order_timestamp AS DATE) AS order_date,
  customer_id,
  status AS order_status,
  total_value AS total_amount,

### Página 10

Data Mesh

  current_timestamp() AS created_at
FROM raw.orders;
Código- fonte 5: Tabela de entregas - Publicação do Data Product - SQL (Structured Query
Language).
Fonte: Elaborado pelo autor (2026)
Ponto-chave de Data Mesh
 O domínio define, publica e responde pelo dado.

Domínio Clientes — Produto independente
CREATE TABLE IF NOT EXISTS customers.customer_profile (
  customer_id STRING NOT NULL,
  customer_name STRING,
  customer_segment STRING,
  customer_status STRING,
  created_at TIMESTAMP
)
USING DELTA;

INSERT INTO customers.customer_profile
SELECT
  id AS customer_id,
  name AS customer_name,
  segment AS customer_segment,
  status AS customer_status,
  current_timestamp() AS created_at
FROM raw.customers;
Código- fonte 6: Tabela de entregas – Domínio de clientes - SQL (Structured Query Language).
Fonte: Elaborado pelo autor (2026)
Importante para aula
 Nenhuma dependência direta com o domínio de Vendas.
Governança computacional — qualidade como código
Checagem de contrato (schema)
DESCRIBE TABLE sales.sales_orders;
Integridade da chave primária
SELECT
  COUNT(*) AS total_rows,

### Página 11

Data Mesh

  COUNT(order_id) AS valid_order_ids
FROM sales.sales_orders;
Código- fonte 7: Código SQL
Fonte: Elaborado pelo autor (2026)

Regra de qualidade (exemplo simples)
SELECT *
FROM sales.sales_orders
WHERE total_amount < 0;
Código- fonte 8: Código SQL
Fonte: Elaborado pelo autor (2026)

Mensagem forte para os alunos
 Governança no Data Mesh é SQL executável, não reunião.
Domínio Logística — Novo Data Product
CREATE TABLE IF NOT EXISTS logistics.delivery_status (
  order_id STRING NOT NULL,
  delivery_date DATE,
  delivery_status STRING,
  delay_days INT,
  created_at TIMESTAMP
)
USING DELTA;

INSERT INTO logistics.delivery_status
SELECT
  order_id,
  CAST(delivery_timestamp AS DATE) AS delivery_date,
  status AS delivery_status,
  delay_days,
  current_timestamp() AS created_at
FROM raw.deliveries;
Código- fonte 8: Código SQL
Fonte: Elaborado pelo autor (2026)
Aprendizado-chave
 Novos domínios entram sem quebrar o que já existe.
Domínio Analytics — Consumo entre domínios

### Página 12

Data Mesh

Receita por segmento
CREATE OR REPLACE VIEW analytics.revenue_by_segment AS
SELECT
  c.customer_segment,
  SUM(s.total_amount) AS total_revenue
FROM sales.sales_orders s
JOIN customers.customer_profile c
  ON s.customer_id = c.customer_id
WHERE s.order_status = 'COMPLETED'
GROUP BY c.customer_segment;

SELECT * FROM analytics.revenue_by_segment;
Código- fonte 9: Código SQL
Fonte: Elaborado pelo autor (2026)

Atraso médio por segmento
CREATE OR REPLACE VIEW analytics.avg_delay_by_segment AS
SELECT
  c.customer_segment,
  AVG(d.delay_days) AS avg_delay
FROM sales.sales_orders s
JOIN customers.customer_profile c
  ON s.customer_id = c.customer_id
JOIN logistics.delivery_status d
  ON s.order_id = d.order_id
GROUP BY c.customer_segment;

SELECT * FROM analytics.avg_delay_by_segment;
Código- fonte 10: Código SQL
Fonte: Elaborado pelo autor (2026)

Mensagem final de Data Mesh
 Analytics não cria pipeline — consome produtos confiáveis.

### Página 13

Data Mesh

A crescente dependência das organizações em relação aos dados para a
tomada de decisão evidenciou limitações relevantes dos modelos tradicionais de
arquitetura analítica. Durante muitos anos, arquiteturas centralizadas, como Data
Warehouses e Data Lakes gerenciados por um único time de dados, foram suficientes
para atender às necessidades iniciais das organizações. Esse modelo centralizado
favorecia o controle, a padronização e a governança, especialmente em contextos nos
quais o volume de dados e o número de usuários analíticos ainda eram limitados. No
entanto, à medida que as empresas escalaram seus produtos digitais, diversificaram
seus canais de interação e passaram a operar com múltiplos times de negócio
autônomos, essas arquiteturas começaram a apresentar gargalos estruturais.
Em arquiteturas centralizadas, todo o fluxo de dados — desde a ingestão até a
modelagem e a disponibilização para consumo analítico — costuma ficar sob
responsabilidade de um time central de dados. Esse time passa a atender
simultaneamente diferentes áreas da organização, cada uma com prioridades, prazos
e interpretações de negócio distintas. Como consequência, surgem atrasos
recorrentes, conflitos de priorização e dificuldade em identificar claramente quem é
responsável pela qualidade final da informação. Esse cenário frequentemente resulta
em perda de confiança nos dados e no surgimento de soluções paralelas, como
planilhas e bases locais, enfraquecendo a governança corporativa.

Figura 1 – Arquitetura de Dados Centralizada
Fonte: Elaborado pelo autor (2026)

### Página 14

Data Mesh

É nesse contexto que o Data Mesh surge como uma abordagem alternativa,
propondo uma mudança estrutural na forma como dados são organizados, produzidos
e consumidos. Diferentemente de uma simples evolução tecnológica, o Data Mesh
parte do princípio de que problemas de escalabilidade em dados são, na maioria das
vezes, reflexos diretos de problemas de escalabilidade organizacional. Assim, em vez
de concentrar responsabilidades em um único time, o modelo propõe a distribuição da
responsabilidade sobre os dados  entre os próprios domínios de negócio, alinhando
arquitetura de dados e estrutura organizacional

Figura 2 – Arquitetura Data Mesh
Fonte: Elaborado pelo autor (2026)

Um dos pilares centrais do Data Mesh é o conceito de data as a product. Nesse
modelo, os dados deixam de ser tratados como um subproduto técnico de sistemas
transacionais ou pipelines de ingestão e passam a ser encarados como produtos de
negócio. Isso implica que cada conjunto de dados relevante deve possuir um
responsável c laramente definido, um propósito explícito, usuários identificáveis e
critérios mínimos de qualidade. Assim como ocorre com produtos digitais, produtos de
dados devem ser versionados, monitorados e continuamente evoluídos ao longo do
tempo. Essa abordagem desloca o foco da construção de pipelines para a entrega
efetiva de valor por meio dos dados.

### Página 15

Data Mesh

Figura 3 – Representação de um produto de Dados
Fonte: Elaborado pelo autor (2026)

A orientação por domínios constitui outro elemento essencial do Data Mesh.
Em vez de organizar os dados exclusivamente por camadas técnicas, como raw,
trusted ou curated, a arquitetura passa a refletir os domínios de negócio da
organização. Domínios como Vendas, Clientes ou Logística tornam -se unidades
autônomas de produção e manutenção de dados analíticos. Essa organização reduz
a distância entre o conhecimento de negóci o e a modelagem dos dados, pois os
próprios especialistas do domínio passam a definir o  significado, o contexto e o uso
esperado das informações que produzem. No hands on desenvolvido, essa orientação
é representada pela criação de bases de dados independentes no Databricks,
reforçando que os limites organizacionais também devem se refletir na estrutura
técnica.
A descentralização promovida pelo Data Mesh, entretanto, não implica
ausência de padrões ou perda de controle. Para evitar fragmentação e
inconsistências, o modelo introduz o conceito de governança computacional.
Diferentemente da governança tradicional, b aseada em processos manuais,
aprovações formais e validações tardias, a governança computacional propõe que
regras de qualidade, contratos de dados e políticas de acesso sejam incorporados

### Página 16

Data Mesh

diretamente ao código e às plataformas de dados. Dessa forma, a governança ocorre
de maneira contínua, automática e escalável, acompanhando o ciclo de vida dos
dados desde sua publicação até o consumo.

Figura 4 – Governança Computacional
Fonte: Elaborado pelo autor (2026)

Outro componente fundamental do Data Mesh é a existência de uma plataforma
de dados orientada ao autosserviço. Essa plataforma tem como objetivo fornecer
capacidades comuns — como armazenamento escalável, processamento distribuído,
versionamento, segurança e observabilidade — para que os domínios possam criar,
publicar e consumir produtos de dados de forma eficiente. O papel da plataforma não
é centralizar a lógica de negócio, mas habilitar a autonomia dos domínios por meio de
serviços padronizados e reutilizáveis. No contexto prático apresentado, o uso de uma
arquitetura lakehouse permite ilustrar esse conceito ao combinar flexibilidade,
governança e desempenho analítico.

### Página 17

Data Mesh

Figura 5 – Plataforma de Dados
Fonte: Elaborado pelo autor (2026)

A adoção do Data Mesh também redefine o papel dos times analíticos dentro
das organizações. Em arquiteturas tradicionais, analistas e cientistas de dados
frequentemente assumem responsabilidades que vão além da análise, como limpeza,
correção e reinterpretação de dados. No modelo Data Mesh, espera-se que os dados
já estejam prontos para consumo, com contratos claros e garantias mínimas de
qualidade oferecidas pelos domínios produtores. Assim, o domínio Analytics atua
predominantemente como consumidor de pro dutos de dados, concentrando seus
esforços na geração de insights e na criação de valor para o negócio.
Apesar de seus benefícios, o Data Mesh não deve ser encarado como uma
solução universal. Sua adoção exige maturidade organizacional, clareza na definição
de domínios e investimento em cultura de responsabilidade sobre dados.
Organizações que tentam impleme ntar o modelo apenas como uma mudança
tecnológica tendem a enfrentar dificuldades, pois o Data Mesh pressupõe uma
transformação conjunta de arquitetura, processos e mentalidade. Em muitos casos, a
transição ocorre de forma gradual, coexistindo com arquiteturas tradicionais até que a
organização atinja maior maturidade.
Por fim, é importante destacar que o Data Mesh não elimina arquiteturas
consolidadas como Data Warehouses ou Data Lakes, mas redefine seu papel dentro

### Página 18

Data Mesh

do ecossistema de dados. Essas estruturas continuam existindo, porém passam a
atuar como infraestrutura compartilhada que suporta produtos de dados distribuídos.
O verdadeiro valor do Data Mesh está em alinhar tecnologia e organização, permitindo
que os da dos escalem no mesmo ritmo que os times e os produtos digitais da
empresa, promovendo autonomia, confiança e eficiência no uso analítico da
informação.

### Página 19

Data Mesh

A adoção do Data Mesh no mercado tem crescido à medida que organizações
digitais enfrentam desafios cada vez mais complexos relacionados à escalabilidade
de dados e de times. Empresas que operam com múltiplos produtos, canais e
unidades de negócio perceber am que arquiteturas centralizadas, embora eficientes
em estágios iniciais, tornam -se progressivamente menos sustentáveis conforme o
volume de dados e o número de consumidores analíticos aumentam. Nesse cenário,
o Data Mesh passa a ser discutido não como um a tendência teórica, mas como uma
resposta prática a problemas reais de governança, autonomia e velocidade analítica.
Diversas organizações globais passaram a experimentar ou adotar princípios
do Data Mesh de forma incremental. Um dos principais responsáveis pela
popularização do conceito é Zhamak Dehghani, que apresentou o Data Mesh a partir
de experiências reais em gran des empresas de tecnologia. Seu trabalho ajudou o
mercado a compreender que o desafio não está apenas na arquitetura de dados, mas
no alinhamento entre estrutura organizacional, cultura e tecnologia.
Uma leitura fundamental para compreender a origem e os fundamentos do Data
Mesh é o livro:
DEHGHANI, Zhamak. Data Mesh: Delivering Data -Driven Value at Scale .
Sebastopol: O’Reilly Media, 2022.  A obra apresenta os quatro pilares do Data Mesh
— orientação por domínios, dados como produto, plataforma de autosserviço e
governança computacional — ilustrados por exemplos do mundo real, sendo
considerada a principal referência conceitual sobre o tema.
Além dos livros, artigos técnicos e publicações especializadas têm
desempenhado papel importante na disseminação do Data Mesh no mercado. O
próprio site da autora reúne textos que detalham desafios, armadilhas e aprendizados
obtidos em implementações reais, sendo uma fonte recorrente de atualização sobre o
tema:
DEHGHANI, Zhamak. How to Move Beyond a Monolithic Data Lake to a
Distributed Data Mesh . Martin Fowler, 2020.  Esse artigo é amplamente citado por
contextualizar o Data Mesh como uma evolução natural de arquiteturas distribuídas,

### Página 20

Data Mesh

conectando o conceito a práticas consolidadas de engenharia de software, como
Domain-Driven Design.
Do ponto de vista de mercado, grandes consultorias e empresas de tecnologia
passaram a publicar análises críticas sobre a adoção do Data Mesh. Esses materiais
reforçam que o modelo não deve ser encarado como uma solução universal, mas
como uma abordagem ad equada a organizações com certo grau de maturidade em
dados e autonomia dos times:
THOUGHTWORKS. Technology Radar – Data Mesh . A ThoughtWorks
destaca o Data Mesh  como uma técnica relevante para ambientes complexos,
alertando para os riscos de adoções superficiais que ignoram aspectos culturais e
organizacionais.
Outro ponto recorrente no mercado é a relação entre Data Mesh e plataformas
modernas de dados em nuvem. Provedores de tecnologia passaram a produzir
conteúdos educativos e estudos de caso mostrando como arquiteturas lakehouse
podem atuar como habilitadoras  do modelo, oferecendo recursos de governança,
versionamento e isolamento lógico:
DATABRICKS. What is Data Mesh?  Esse material ajuda a conectar os
conceitos discutidos teoricamente com a prática demonstrada no hands on,
especialmente no uso de plataformas analíticas modernas.
Além de artigos e livros, podcasts e vídeos técnicos também têm contribuído
para o debate sobre Data Mesh. Esses formatos são particularmente úteis para
discutir desafios reais de adoção, experiências de falha e aprendizados
organizacionais:
Podcast Software Engineering Daily – Data Mesh with Zhamak Dehghani.
No episódio, são discutidos os limites do modelo, o papel da liderança organizacional
e os riscos de tratar o Data Mesh apenas como uma mudança tecnológica.
Por fim, observa -se uma tendência clara de amadurecimento do discurso em
torno do Data Mesh. Se, inicialmente, o conceito foi tratado como uma ruptura
completa com arquiteturas tradicionais, o mercado passou a adotar uma visão mais
equilibrada, reconhecendo a coexistência entre Data Mesh, Data Warehouses e Data
Lakes. Essa visão híbrida reforça que o Data Mesh não elimina arquiteturas

### Página 21

Data Mesh

consolidadas, mas redefine seu papel dentro de ecossistemas de dados cada vez
mais distribuídos e orientados ao domínio.

### Página 22

Data Mesh

Nesta aula, você conheceu o Data Mesh como uma abordagem arquitetural e
organizacional voltada à escalabilidade do uso de dados em ambientes complexos.
Ao longo do conteúdo, foi possível compreender que os desafios enfrentados por
arquiteturas de dados centralizadas não são apenas técnicos, mas também refletem
limitações na forma como as responsabilidades sobre os dados são distribuídas
dentro das organizações.
Você aprendeu que o Data Mesh propõe uma mudança de paradigma ao tratar
dados como produtos de negócio, com donos claramente definidos, propósito explícito
e critérios mínimos de qualidade. Esse conceito ficou evidente tanto na discussão
teórica quanto no hands on realizado, no qual domínios como Vendas, Clientes e
Logística passaram a ser responsáveis pela criação e manutenção de seus próprios
produtos de dados, enquanto o domínio Analytics atuou exclusivamente como
consumidor dessas informações.
Outro ponto central da aula foi a compreensão do papel da governança
computacional. Em vez de processos manuais e centralizados, a governança foi
apresentada como um conjunto de regras automatizadas e incorporadas ao próprio
ciclo de vida dos dados. A part ir de exemplos práticos, foi possível observar como
validações de schema, integridade e qualidade podem ser aplicadas diretamente na
plataforma, garantindo consistência sem comprometer a autonomia dos domínios.
A aula também destacou a importância das plataformas de dados orientadas
ao autosserviço como elemento habilitador do Data Mesh. Você viu como arquiteturas
modernas, como o lakehouse, permitem que diferentes domínios publiquem e
consumam dados de forma pad ronizada, escalável e governada, reduzindo gargalos
operacionais e acelerando a geração de valor analítico.
Por fim, ao conectar conceitos, prática e exemplos de mercado, esta aula
reforçou que o Data Mesh não é uma solução universal ou puramente tecnológica.
Sua adoção exige maturidade organizacional, clareza na definição de domínios e uma
mudança cultural na f orma como dados são produzidos, compartilhados e
consumidos. Com isso, você está mais preparado (a) para analisar criticamente

### Página 23

Data Mesh

iniciativas de Data Mesh e avaliar sua aplicabilidade em diferentes contextos
organizacionais.

### Página 24

Data Mesh

DATABRICKS. The Lakehouse Architecture . Disponível em:
https://www.databricks.com/product/data-lakehouse. Acesso em: 26 fev. 2026.
DATABRICKS. What is Data Mesh?  2023. Disponível em:
https://www.databricks.com/glossary/data-mesh. Acesso em: 26 fev. 2026.
DEHGHANI, Zhamak. Data Mesh: Delivering Data -Driven Value at Scale .
Sebastopol: O’Reilly Media, 2022.
DEHGHANI, Zhamak. How to move beyond a monolithic data lake to a distributed
data mesh . Martin Fowler , 2020. Disponível em:
https://martinfowler.com/articles/data-mesh-principles.html. Acesso em: 26 fev. 2026.
KLEPPMANN, Martin. Designing Data -Intensive Applications: The Big Ideas
Behind Reliable, Scalable, and Maintainable Systems. Sebastopol: O’Reilly Media,
2017.
SADALAGE, Pramod J.; FOWLER, Martin. NoSQL Distilled: A Brief Guide to the
Emerging World of Polyglot Persistence. Boston: Addison-Wesley, 2013.
SOFTWARE ENGINEERING DAILY. Data Mesh with Zhamak Dehghani . Podcast,
2021. Disponível em: https://softwareengineeringdaily.com/2021/05/17/data -mesh-
with-zhamak-dehghani/. Acesso em: 26 fev. 2026.
THOUGHTWORKS. Technology Radar: Data Mesh . Disponível em:
https://www.thoughtworks.com/radar/techniques/data-mesh. Acesso em: 26 fev. 2026.

### Página 25

Data Mesh

PALAVRAS-CHAVE
Data Mesh, Governança Computacional, Data Products

### Página 26

Data Mesh
