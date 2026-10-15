# Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

**ETL Pipelines** · Aula 3 · Fase 2 — Data Prepare

Serviços de armazenamento e analytics em AWS, GCP e Azure.

**Tópicos:** `S3` · `BigQuery` · `Azure Data Lake` · `cloud storage`

📄 [PDF da aula](./aula_03_cloud_data_aws_s3_gcp_bigquery_azure_data_lake.pdf)

---

## Conteúdo

### Página 1

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

CLOUD DATA (AWS S3,
GCP BIGQUERY, AZURE
DATA LAKE)

### Página 2

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

### Página 3

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

O conceito de Cloud Data representa uma transformação estrutural na forma
como dados são armazenados, processados e consumidos. Mais do que a simples
migração de servidores físicos para data centers remotos, Cloud Data define um
ecossistema de serviços gerenciados no qual a infraestrutura é abstraída, permitindo
que o foco esteja em escalabilidade, governança, análise e geração de valor para o
negócio.
Historicamente, as arquiteturas de dados eram baseadas em sistemas
monolíticos, nos quais computação e armazenamento estavam rigidamente
acoplados. Bancos relacionais e appliances de Data Warehouse exigiam crescimento
conjunto de CPU, memória e disco, resu ltando em baixa elasticidade, alto custo e
ineficiência operacional. A computação em nuvem rompe esse paradigma ao
introduzir a separação entre computação e armazenamento, princípio fundamental
das arquiteturas modernas de dados.
Nesse novo modelo, os dados são persistidos de forma durável e econômica
em Object Storage, enquanto a computação é provisionada sob demanda e de forma
efêmera. Clusters podem ser criados apenas pelo tempo necessário para executar
cargas analíticas intensi vas e desligados em seguida, viabilizando elasticidade
extrema e otimização financeira, algo impraticável em ambientes tradicionais.
Esse movimento é impulsionado pelo crescimento acelerado do volume de
dados, resultado da digitalização, da proliferação de dispositivos conectados e da
adoção de inteligência artificial. Nesse contexto, Cloud Data deixa de ser apenas uma
escolha tecnológi ca e passa a representar o modelo dominante de arquitetura de
dados. Como aponta a Gartner, a nuvem se consolidou como a base para a inovação
digital, permitindo o uso de dados de forma segura, escalável e orientada a valor.
Este módulo introduz esse cenário, preparando você para compreender como
e por que os pipelines ETL/ELT evoluem na nuvem, e qual é o papel do Cloud Data
nas arquiteturas modernas orientadas a dados, explorando as abordagens dos
principais provedores do mercado: AWS, GCP e Azure.

### Página 4

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Laboratório Teórico: Arquitetura de Cloud Data
Contexto do Problema
Você faz parte de uma empresa de médio porte do setor de varejo digital. A
empresa opera um e -commerce nacional, com crescimento acelerado de vendas,
campanhas sazonais frequentes e forte investimento em analytics e inteligência
artificial para personalização da experiência do cliente.
Atualmente, a organização enfrenta dificuldades para escalar suas análises de
dados. O ambiente existente é majoritariamente on -premises, com um Data
Warehouse tradicional que recebe cargas noturnas em batch. Esse modelo não
atende mais às necessidades do negócio, que exige dados mais atualizados, maior
flexibilidade analítica e redução de custos operacionais.
A liderança decide, então, iniciar a modernização da arquitetura de dados,
adotando uma estratégia baseada em Cloud Data.
Critérios de Decisão Arquitetural
Antes de escolher uma estratégia de migração, é fundamental avaliar o
workload a partir dos seguintes critérios:
● Criticidade para o negócio: o sistema é essencial para a operação diária?
Impacta diretamente receita ou clientes?
● Complexidade técnica atual:  o pipeline é simples, legado, fortemente
acoplado ou já modularizado?
● Volume e crescimento dos dados: o volume cresce rapidamente? Há
picos sazonais ou cargas imprevisíveis?
● Necessidade de escalabilidade e elasticidade: o workload se beneficia
de computação sob demanda?
● Custo operacional atual:  a manutenção do ambiente atual é alta? Exige
muito esforço manual?

### Página 5

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

● Horizonte de longo prazo:  esse pipeline será base para analytics
avançado, IA ou novos produtos de dados?
Com essas perguntas respondidas, podemos utilizar as estratégias de
Migração para a Nuvem – Os 6 Rs
Estratégia Descrição Exemplo prático Quando utilizar
Rehost (Lift and
Shift)
Migração direta da
infraestrutura
existente para a
nuvem, sem
alterações
relevantes na
arquitetura ou no
código.
Mover um banco
de dados ou job
on-premise para
uma VM na
nuvem.
Quando há
necessidade de
migração rápida,
com baixo risco e
pouco tempo para
reengenharia.
Replatform (Lift
and Reshape)
Migração com
pequenas
adaptações para
uso de serviços
gerenciados,
mantendo a lógica
principal da
aplicação.
Migrar um cluster
Hadoop local para
Amazon EMR ou
Google Dataproc.
Quando se deseja
reduzir o esforço
operacional sem
reescrever
totalmente o
sistema.
Refactor (Re-
architect)
Reescrita da
solução para um
modelo cloud-
native, explorando
separação de
computação e
armazenamento e
serviços
serverless.
Substituir jobs
legados por
pipelines PySpark
em AWS Glue ou
Google Dataflow.
Quando o objetivo
é escalabilidade,
eficiência e
inovação no longo
prazo.
Repurchase Substituição da
solução atual por
um produto ou
serviço SaaS
nativo em nuvem.
Trocar um ETL on-
premise por uma
ferramenta SaaS
de integração de
dados.
Quando há
soluções de
mercado maduras
que atendem ao
negócio com
menor custo
operacional.
Retain Manutenção do
workload no
ambiente atual (on-
premise ou
legado).
Manter sistemas
críticos que não
podem ser
migrados no curto
prazo.
Quando existem
restrições técnicas,
legais ou
estratégicas para a
migração.

### Página 6

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Retire Descontinuação do
sistema ou pipeline
que não agrega
mais valor ao
negócio.
Desativar pipelines
antigos sem uso
ou redundantes.
Quando o custo de
manter supera o
valor gerado.

Etapas do Laboratório
1. Escolha da Estratégia de Migração (6 Rs)
Antes de pensar em ferramentas, você deve decidir como o pipeline será
migrado.
Nesta etapa, você deve analisar o cenário apresentado e definir qual estratégia
de migração melhor atende às necessidades da empresa. Considere se o objetivo é
apenas sair rapidamente do ambiente on-premises, reduzir o esforço operacional ou,
de fato, construir uma arquitetura moderna, escalável e preparada para o futuro.
Explique qual estratégia dos 6 Rs você adotaria para o pipeline principal de
dados e justifique sua decisão considerando criticidade para o negócio, crescimento
esperado, custo operacional atual e horizonte de longo prazo.
2. Definição da Estratégia de Armazenamento de Dados
Com a estratégia de migração definida, o próximo passo é pensar como os
dados serão armazenados, independentemente de tecnologia ou cloud específica.
Nesta etapa, você deve descrever:
● Como os dados serão organizados ao longo do tempo;
● Se haverá separação entre dados brutos, tratados e analíticos;
● Ccomo o armazenamento deve suportar reprocessamento, auditoria e
evolução do pipeline.
Explique por que uma arquitetura baseada em separação entre computação e
armazenamento é adequada para o cenário e como isso impacta escalabilidade e
custo.

### Página 7

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

3. Política de Retenção e Ciclo de Vida dos Dados
Nem todos os dados precisam ser armazenados indefinidamente da mesma
forma. Definir tempo de retenção é uma decisão essencial de arquitetura e
governança.
Nesta etapa, descreva:
● Por quanto tempo os dados brutos devem ser mantidos;
● Quando dados podem ser agregados, arquivados ou descartados;
● Como exigências legais, auditoria e análises históricas influenciam essas
decisões.
Explique como uma política clara de retenção contribui para controle de custos
e conformidade regulatória.
4. Definição do Modelo de Ingestão dos Dados
A migração para a nuvem representa uma oportunidade para reavaliar a forma
como os dados são processados, e não apenas onde eles são armazenados.
Nesta etapa, você deve analisar se o modelo atual de processamento atende
às necessidades do negócio ou se há ganhos ao adotar um modelo diferente. Explique
quais dados podem continuar sendo processados em batch, quais se beneficiaram de
processamento em t empo real e se um modelo híbrido faz mais sentido para a
empresa.
Justifique suas decisões considerando latência, valor de negócio, custo e
complexidade operacional, lembrando que nem todo dado precisa ser processado em
streaming para gerar valor.
5. Orquestração e Fluxo do Pipeline
Com o modelo de ingestão definido, é necessário pensar em como o pipeline
será coordenado. A orquestração garante que as etapas do processamento ocorram
na ordem correta, que falhas sejam tratadas e que o pipeline seja observável.
Nesta etapa, descreva como o pipeline deve ser orquestrado, considerando
dependências entre etapas, reprocessamento, controle de falhas e agendamento.
Explique por que a orquestração é um elemento central em arquiteturas de Cloud Data
e como ela contribui para confiabilidade e governança.

### Página 8

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

6. Segurança, Governança e Observabilidade
Antes de qualquer escolha tecnológica, é fundamental definir como a
arquitetura lidará com segurança, governança e monitoramento.
Explique como o controle de acesso aos dados deve ser estruturado, como a
rastreabilidade das transformações será garantida e de que forma a qualidade dos
dados e a saúde do pipeline serão monitoradas. Considere também aspectos
regulatórios, como privacidade e conformidade, e explique como essas preocupações
influenciam o desenho da arquitetura.
7. Escolha da Cloud e das Tecnologias
Somente após todas as decisões conceituais anteriores, você deve escolher o
provedor de nuvem e as tecnologias que melhor materializam a arquitetura definida.
Nesta etapa, escolha uma cloud (AWS, GCP ou Azure) e explique como os
serviços dessa plataforma atendem às decisões já tomadas sobre ingestão,
armazenamento, processamento, orquestração e consumo. Justifique suas escolhas
mostrando coerência entre necessidade de negócio, arquitetura e tecnologia.
8. Desenho da Arquitetura Final
Com todas as decisões consolidadas, você deverá produzir o desenho
arquitetural final da solução, além do diagrama, descreva o fluxo de dados ponta a
ponta, explicando como cada decisão tomada anteriormente se reflete na arquitetura
final.
Desafio Extra: Implementação de um Pipeline Cloud Data
Neste laboratório prático, você irá implementar uma versão simplificada da
arquitetura de Cloud Data definida no laboratório teórico. O objetivo não é apenas
executar um pipeline, mas validar na prática as decisões arquiteturais tomadas
anteriormente, expl orando serviços gerenciados de nuvem, separação entre
computação e armazenamento e boas práticas de engenharia de dados. Você poderá
escolher AWS, Google Cloud Platform ou Microsoft Azure, priorizando serviços com
camada gratuita (free tier) ou alternativa s de baixo custo, simulando um cenário
realista de aprendizado e prototipação.

### Página 9

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Cloud Data: Definição e Evolução Arquitetural
O conceito de Cloud Data representa uma transformação estrutural na forma
como dados são armazenados, processados e consumidos. Mais do que apenas
migrar servidores físicos para data centers remotos, Cloud Data refere -se a um
ecossistema integrado de serviços gerenciados, no qual a infraestrutura é abstraída e
o foco desloca-se para governança, escalabilidade, análise e valor de negócio.
Historicamente, arquiteturas de dados eram baseadas em sistemas monolíticos
rigidamente acoplados, onde computação e armazenamento cresciam juntos,
resultando em baixa elasticidade e alto custo. A computação em nuvem rompe esse
paradigma introduzindo a separação entre computação e armazenamento, o princípio
fundamental das arquiteturas modernas de dados.
Nesse modelo, dados são persistidos de forma durável e econômica em
armazenamento de objetos (object storage), enquanto a computação é provisionada
sob demanda, de forma efêmera, permitindo escalar processamento sem replicar
dados. Clusters e motores analí ticos podem ser criados por minutos para executar
cargas intensivas e desligados em seguida, viabilizando elasticidade e otimização de
custos.
Atualmente, o mercado de Cloud Data é dominado por três grandes provedores
– Amazon Web Services (AWS), Google Cloud Platform (GCP) e Microsoft Azure –
cada um com filosofias arquiteturais distintas e um amplo leque de serviços
gerenciados. Apesar das dife renças, todos convergem na ideia de tirar dos
engenheiros de dados a carga de gerenciar infraestrutura de baixo nível, permitindo
foco em arquiteturas lógicas e requisitos de negócio.
Gerações de Arquitetura de Dados
A evolução arquitetural do gerenciamento de dados pode ser compreendida em
três gerações principais, cada uma surgindo para superar limitações da anterior:

### Página 10

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

GERAÇÃO DESCRIÇÃO CARACTERÍSTICAS LIMITAÇÕES
Data Warehouse
Ambientes de
armazenamento de
dados estruturados,
altamente otimizados
para consultas SQL
e Business
Intelligence,
geralmente
baseados em
bancos de dados
relacionais ou
appliances
proprietários.
• Forte consistência e
confiabilidade
• Alta performance
para consultas
complexas
• Modelo schema-on-
write
• Ideal para relatórios
e BI corporativo
• Baixa flexibilidade
para dados semi e
não estruturados
• Alto custo de
escalabilidade
• Escalabilidade
vertical ou via
appliances
• Planejamento
rígido de
capacidade e
subutilização de
recursos
Data Lake Repositório
centralizado para
armazenamento de
grandes volumes de
dados estruturados,
semi-estruturados e
não estruturados,
geralmente baseado
em sistemas de
arquivos distribuídos
ou object storage.
• Alta escalabilidade
horizontal
• Baixo custo de
armazenamento
• Suporte a múltiplos
formatos de dados
• Modelo schema-on-
read
• Adequado para
analytics exploratório
e ciência de dados
• Governança e
qualidade mais
complexas
• Ausência de
controles
transacionais
nativos
• Risco de se tornar
um Data Swamp
sem boas práticas
• Performance
inconsistente para
BI tradicional
Lakehouse Arquitetura que
combina a
flexibilidade e
economia do Data
Lake com as
garantias e a
performance do Data
Warehouse,
utilizando formatos
abertos e camadas
de gerenciamento
transacional.
• Dados em formatos
abertos (Parquet,
ORC, Avro)
• Suporte a
transações ACID
• Time travel e
versionamento de
dados
• Updates e deletes
eficientes
• Acesso unificado
para BI, Analytics e
Machine Learning
• Maior
complexidade
conceitual
• Dependência de
camadas adicionais
de gerenciamento
• Exige maior
maturidade
arquitetural e de
governança
Tabela 1 – Gerações de arquitetura de dados
Fonte: elaborado pelo autor (2026)

### Página 11

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Para organizar os dados dentro de um Lakehouse (ou mesmo de um data lake
tradicional) adota-se frequentemente a Medallion Architecture – uma divisão lógica em
camadas Bronze, Silver e Gold que já conhecemos anteriormente e representam
estágios crescentes de qualidade e estrutura. Essa progressão incremental melhora
a qualidade e a organização a cada etapa, facilitando governança e reuso dos dados.
Para ficar fácil na memória, uma arquitetura de Data Warehouse tradicional lida
bem apenas com dados estruturados, fornecendo consistência e desempenho SQL
altos, mas com pouca elasticidade e alto custo por escala limitada. O Data Lake
expande para todos o s tipos de dados com baixo custo, porém sacrificando as
garantias transacionais e exigindo esforço para evitar desorganização. O Lakehouse,
por sua vez, busca entregar confiabilidade e governança equivalentes a um
warehouse diretamente sobre dados no lake,  unificando cenários analíticos e de
ciência de dados em uma única plataforma.

Figura 1 - Exemplificação das gerações de arquitetura de dados
Fonte: Databricks - Data lakehouse (2025)
Vantagens Estratégicas do Cloud Data
Eficiência de Custos e Elasticidade
Em ambientes de Cloud Data, o modelo pay-as-you-go permite pagar apenas
pelos recursos utilizados, eliminando a necessidade de infraestrutura
superdimensionada. A elasticidade da nuvem possibilita escalar computação e
armazenamento de forma independente, ativando alto poder de processamento

### Página 12

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

apenas quando necessário e reduzindo custos em períodos de ociosidade. Essa
flexibilidade diminui desperdícios, viabiliza estratégias como o uso de instâncias spot
e permite escalar em segundos, pagando somente pelo tempo efetivo de uso.
Isolamento de Performance
A separação entre armazenamento e computação permite que diferentes
workloads utilizem os mesmos dados simultaneamente, sem competir por recursos.
Com isso, equipes de BI, engenharia de dados, ciência de dados e Machine Learning
podem operar de forma isolada, cada uma com seu próprio poder computacional,
garantindo escalabilidade independente e evitando impactos de performance entre
aplicações. Essa arquitetura aumenta a confiabilidade e mantém desempenho
consistente mesmo em cenários de alta concorrência.
Escalabilidade e Alta Disponibilidade
Nas nuvens públicas, escalar recursos deixou de ser um obstáculo: é possível
expandir serviços e instâncias em minutos, acompanhando o crescimento de dados e
usuários quase em tempo real. Além disso, os serviços de nuvem oferecem altíssima
durabilidade e d isponibilidade, com dados replicados automaticamente e
infraestrutura tolerante a falhas, por exemplo, o Amazon S3 garante durabilidade de
99,999999999% (11 noves) dos objetos armazenados, replicando dados
automaticamente em múltiplas zonas. O resultado sã o arquiteturas de dados mais
escaláveis, resilientes e confiáveis, acessíveis sob demanda mesmo para empresas
de menor porte.
Camada de Armazenamento: Object Storage como Fundamento
O armazenamento de objetos é a base das arquiteturas Cloud Data. Diferente
de armazenamento em sistema de arquivos (NAS) ou em blocos (SAN), onde dados
ficam em diretórios hierárquicos ou volumes fixos, o object storage gerencia dados
como objetos independ entes, cada objeto possui um identificador único global e
metadados descritivos ricos. Essa abordagem traz escala praticamente ilimitada e
simplicidade de acesso (via APIs REST), tornando-a ideal para data lakes na nuvem.
Todos os grandes provedores oferecem object storage altamente durável e
escalável: o Amazon S3, o Azure Blob Storage (e ADLS Gen2) e o Google Cloud
Storage (GCS). Embora semelhantes no conceito, cada um possui características
evolutivas importantes:

### Página 13

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Amazon S3
O Amazon S3 consolidou -se como padrão de object storage  e evoluiu ao
oferecer consistência forte de leitura após escrita, simplificando pipelines de dados.
Com múltiplas classes de armazenamento, permite alinhar custo e frequência de
acesso ao longo do ciclo de vida dos dados. Sua alta durabilidade, grande throughput
e recursos como leitura otimizada e integração nativa de metadados fazem do S3 uma
base robusta para arquiteturas modernas de dados.
Azure Data Lake Storage Gen2 (ADLS Gen2)
O ADLS Gen2 estende o Azure Blob Storage para Big Data ao oferecer
namespace hierárquico, permitindo operações eficientes sobre diretórios e reduzindo
latência em workloads analíticos. O suporte a ACLs no estilo POSIX, integrado ao
Azure Active Directory, garante controle de acesso granular e governança diretamente
no storage. Essas capacidades tornam o ADLS Gen2 ideal para cenários corporativos,
desde que o uso do namespace hierárquico seja adequado ao tipo de workload.
Google Cloud Storage
O Google Cloud Storage oferece simplicidade e desempenho consistente, com
acesso imediato aos dados em todas as classes de armazenamento, inclusive as de
arquivamento, facilitando estratégias de tiering e consultas históricas sob demanda.
Complementando es sa abordagem, o BigQuery atua como um data warehouse
serverless totalmente gerenciado, abstraindo a infraestrutura e permitindo análises em
larga escala via SQL com alta agilidade e produtividade para times de analytics e data
science.
Em resumo, o GCP foca em entregar experiência unificada e de baixo atrito,
enquanto AWS e Azure tendem a oferecer maior controle e variedade de ferramentas
(com possível complexidade extra).
Camada de Computação e Analytics
Acima do armazenamento bruto residem os motores de processamento
responsáveis por transformar dados e extrair insights. Cada provedor de nuvem tem

### Página 14

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

uma abordagem distinta para essa camada, refletindo também estratégias de
mercado e perfis de usuários alvo:
AWS Abordagem Modular
A AWS adota uma abordagem modular, oferecendo serviços especializados
que podem ser combinados conforme a necessidade, como Glue para ETL, Athena
para consultas SQL serverless, EMR para processamento distribuído e Redshift para
data warehousing. Essa estra tégia garante alta flexibilidade e permite montar
arquiteturas sob medida, com integração crescente entre os serviços e separação de
armazenamento e computação. Em contrapartida, essa liberdade vem acompanhada
de maior complexidade operacional e curva de aprendizado, exigindo mais esforço de
orquestração e governança.
Azure – Abordagem de Convergência (Synapse)
A Microsoft apostou na unificação com o Azure Synapse Analytics, que reúne
em um único ambiente data warehouse, big data e integração de dados. A plataforma
permite alternar entre SQL, Spark e pipelines ETL compartilhando o mesmo data lake
e governança, co m forte integração ao ecossistema Microsoft. Essa abordagem
aumenta a produtividade em cenários enterprise, oferecendo uma experiência de
ponta a ponta, ainda que internamente utilize motores distintos conforme o tipo de
workload.
GCP – Abordagem Serverless e Autônoma
O Google Cloud destaca -se pela abstração total da infraestrutura, com o
BigQuery como principal serviço analítico serverless e altamente escalável. Os
recursos são alocados automaticamente conforme as consultas, garantindo alto
desempenho e concorrência co m mínima gestão operacional. Em comparação,
enquanto AWS e Azure oferecem mais controle e modularidade, o GCP prioriza
simplicidade, automação e eficiência na operação.
BigQuery (GCP)
O BigQuery exemplifica o modelo de data warehouse totalmente gerenciado e
serverless, com separação entre armazenamento e computação, permitindo escalar

### Página 15

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

consultas sob demanda e pagar apenas pelos dados processados. Recursos como
particionamento, clusterização, cache e reclustering automático mantêm a
performance mesmo em grandes volumes, enquanto integrações com dados externos
e inteligência artificial amp liam seus casos de uso. Ao eliminar a gestão de
infraestrutura, o BigQuery permite rápida experimentação e escala por equipes
pequenas, exigindo que a otimização de custo e desempenho seja feita principalmente
por meio de boas práticas de modelagem e uso eficiente dos recursos disponíveis.
Azure Synapse Analytics
O Azure Synapse é uma plataforma analítica unificada que combina SQL,
Spark e integração de dados em um único workspace. Ele permite executar consultas
SQL serverless sobre dados no Data Lake, usar pools dedicados para workloads
previsíveis e rodar jobs Spark integrados ao mesmo ambiente, compartilhando dados
entre essas camadas de forma simples. Sua principal vantagem está na produtividade
e integração, reunindo ingestão, transformação, analytics e governança em uma única
solução, com flexibilidade de cust os e controle operacional, especialmente voltada a
cenários corporativos.
AWS - Portfólio Modular de Serviços Analíticos
Na AWS, não há um “Synapse” ou “BigQuery ” único, em vez disso, há um
ecossistema de serviços analíticos que podem ser combinados conforme a
necessidade. Alguns componentes notáveis:
● Amazon Athena: serviço de SQL serverless que permite executar queries
ANSI SQL diretamente em arquivos no S3 (formatos Parquet, ORC, CSV,
JSON, etc.). Baseado no Presto (Trino), o Athena é ideal para análises ad -
hoc em dados do data lake, sem precisar carregar esses dad os em um
banco. O usuário paga por TB lido (também cerca de $5 por TB), então
otimizar partições e colunas dos arquivos é importante. Athena se integra
ao Glue Data Catalog para conhecer os schemas das tabelas no S3,
funcionando como um “virtual warehouse” simples para BI.
● AWS Glue: serviço gerenciado de ETL que executa jobs Spark de forma
serverless, simplificando a criação e a orquestração de pipelines batch e
streaming sem a necessidade de gerenciar infraestrutura. Ele se destaca

### Página 16

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

pelo Glue Data Catalog, que centraliza metadados e viabiliza governança e
integração com serviços como Athena e Redshift Spectrum. Com recursos
como geração automática de código, suporte a streaming e ferramentas
visuais de preparação de dados, o Glue atua  como uma solução versátil e
integrada para ETL no ecossistema AWS.
● Amazon EMR:  indicado para quem busca maior controle sobre clusters
Hadoop e Spark, permitindo configurar instâncias, dimensionamento e
softwares conforme o workload. Ele atende bem cenários complexos ou
contínuos, pode reduzir custos com uso de instâncias spot e ofer ece
múltiplos engines de processamento, além do modo EMR Serverless. É
comum em arquiteturas AWS quando há expertise prévia em Hadoop ou
quando manter clusters ativos se mostra mais econômico para grandes
pipelines de processamento.
● Amazon Redshift:  é a solução de data warehouse MPP da AWS, que
evoluiu de clusters fixos para modelos mais flexíveis com separação entre
armazenamento e computação, como o RA3 e o Redshift Serverless. Ele
permite consultar dados no próprio warehouse ou diretamente no S3 v ia
Redshift Spectrum, integrando lake e warehouse. Fortemente integrado ao
ecossistema AWS e familiar para equipes SQL, o Redshift oferece alto
desempenho e consistência para workloads analíticos, embora exija maior
atenção a tuning e distr ibuição de dados em comparação a soluções
totalmente autogerenciadas.
● Outros Serviços: a AWS ainda possui o Amazon QuickSight (ferramenta
BI serverless integrada, para dashboards), o AWS SageMaker (plataforma
de ML gerenciada, que lida bem com dados no S3/Redshift), o Amazon
Kinesis (para ingestão de streaming de eventos em tempo real, com
variantes Data Streams, Data Firehose, etc.), e serviços de orquestração
como o AWS Step Functions ou Managed Workflows for Apache Airflow
(MWAA) para coordenar pipelines multi-serviço.
Em resumo, a camada de computação na AWS é composta por Lego pieces:
Athena para SQL on -demand, Glue/EMR para ETL e processamento, Redshift para
data warehousing clássico, e outros componentes plugáveis. Isso dá poder de ajustar
a arquitetura exatamente às necessidades, mas exige do arquiteto uma boa visão do

### Página 17

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

trade-off de cada serviço e como integrá-los (ex: usar Glue jobs para preparar dados
que serão consumidos no Redshift ou Athena; ou descarregar parte das consultas do
Redshift para Spectrum no S3 quando dados crescerem muito, etc.). A AWS fornece
padrões de referência (arquiteturas Lake House AWS) que guiam essas integrações,
muitas vezes usando o S3 como ponto central (data lake) cercado por esses motores
especializados.
Estruturas Arquiteturais Modernas
A maturidade do ecossistema Cloud Data impulsionou também novas
abordagens arquiteturais em nível organizacional e sistêmico. Três conceitos que
ganharam destaque nos últimos anos são o Lakehouse, o Data Mesh e o Data Fabric.
Eles não se excluem mutuamente , muitas vezes, coexistem e se complementam
dentro de grandes organizações, mas convém entender seus focos:
● Lakehouse: representa uma evolução arquitetural que une data lakes e
data warehouses ao adotar formatos abertos com metadados e garantias
ACID. Essa abordagem permite aplicar esquemas medalhão, time travel e
suportar workloads analíticos, preditivos e de streaming s obre uma única
fonte de dados, reduzindo duplicações e custos. Impulsionado por
ferramentas modernas e incorporado gradualmente por soluções
tradicionais, o Lakehouse se consolida como um padrão arquitetural, cujo
uso depende das necessidades da empresa e da maturidade desejada na
convergência entre BI e Data Science.
● Data Mesh:  introduzido por Zhamak Dehghani em 2019, propõe uma
mudança organizacional na engenharia de dados ao descentralizar a
responsabilidade dos dados por domínio de negócio. Nesse modelo, cada
área passa a tratar seus dados como produtos, com qualidade,
documentação e SLAs, apoiada por uma plataforma self -service e
governança federada. O objetivo é eliminar gargalos de times centralizados,
aumentar a autonomia dos domínios e escalar a produção e o uso de dados
de forma alinhada ao negócio, sendo a ado ção muito mais um desafio
cultural e de processos do que apenas tecnológico.
● Data Fabric: é uma abordagem arquitetural e tecnológica que busca unificar
o acesso a dados distribuídos por meio de uma camada lógica sobreposta

### Página 18

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

às fontes existentes. Diferente do Data Mesh, que foca na organização, o
Fabric enfatiza virtualização, metadados, automação e governança para
permitir consultas e integrações transparentes entre sistemas
heterogêneos. Essa abordagem é especialmente útil e m ambientes com
muitos silos, legados ou multi -cloud, ao simplificar o acesso e o consumo
de dados sem exigir sua consolidação física em um único repositório.
O Data Fabric não substitui Data Lakes ou Data Mesh, mas atua de forma
complementar, oferecendo uma camada de acesso unificado sobre dados
distribuídos. Ele permite integrar domínios de um Data Mesh ou conviver com
arquiteturas Lakehouse e sistemas legados  sem migração imediata, simplificando o
consumo de dados. Grandes fornecedores têm adotado essa abordagem ao integrar
integração, catálogo, qualidade e segurança em soluções únicas.
Exemplos de Arquitetura ETL em cada Provedor
Para concretizar os conceitos, vejamos como se parece uma pipeline de dados
em nuvem mapeada nos serviços de AWS, GCP e Azure. Apesar das implementações
variarem, notamos uma estrutura comum.
Camada da
Arquitetura
AWS GCP AZURE
Ingestão Batch AWS DMS, AWS
Glue Crawlers,
AWS Data Pipeline
Cloud Datastream,
Storage Transfer
Service
Azure Data
Factory, Azure
Database
Migration Service
Ingestão
Streaming /
Eventos
Amazon Kinesis
Data Streams,
Amazon MSK
(Kafka), AWS
Lambda
Pub/Sub, Dataflow
(streaming)
Event Hubs, Azure
Stream Analytics
Raw/ Bronze
(Data Lake)
Amazon S3 Google Cloud
Storage (GCS)
Azure Blob
Storage / ADLS
Gen2
Catálogo de
dados
AWS Glue Data
Catalog
Data Catalog Azure Purview
(Microsoft Purview)
Governança de
dados
AWS Lake
Formation
Dataplex Microsoft Purview

### Página 19

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Processamento
Batch
AWS Glue Jobs
(Spark), Amazon
EMR

Dataflow (Batch),
Dataproc (Spark)
Azure Synapse
Spark, Azure
Databricks
Processamento
Streaming
Kinesis Data
Analytics (Flink),
Spark Streaming
(EMR)
Dataflow (Apache
Beam)
Azure Stream
Analytics, Spark
Structured
Streaming
Silver/Gold
(Lakehouse)
S3 + Apache Hudi
/ Delta Lake /
Iceberg
BigQuery +
BigLake / GCS +
Delta/Iceberg
ADLS + Delta Lake
(Databricks)
DW / Consulta
SQL
Amazon Athena,
Amazon Redshift
(Spectrum)
BigQuery Azure Synapse
Analytics
(Serverless /
Dedicated)
BI / Visualização Amazon
QuickSight
Looker / Looker
Studio
Power BI
Machine Learning Amazon
SageMaker
Vertex AI,
BigQuery ML
Azure Machine
Learning
Orquestração MWAA (Airflow),
Step Functions,
EventBridge
Cloud Composer
(Airflow),
Workflows, Cloud
Scheduler
Azure Data
Factory, Azure
Logic Apps
Observabilidade /
Monitoramento
CloudWatch, AWS
CloudTrail
Cloud Monitoring,
Cloud Logging
Azure Monitor, Log
Analytics
Tabela 2 – Tecnologias para criar a esteira de pipeline
Fonte: elaborado pelo autor (2026)

### Página 20

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Figura 2 - Exemplificação do desenho de uma arquitetura para pipeline ETL utilizando GCP
Fonte: Criado pelo autor utilizando a ferramenta Canva (2026)

Figura 3 - Exemplificação do desenho de uma arquitetura para pipeline ETL utilizando AWS
Fonte: Criado pelo autor utilizando a ferramenta Canva (2026)

Figura 4 - Exemplificação do desenho de uma arquitetura para pipeline ETL utilizando Azure
Fonte: Criado pelo autor utilizando a ferramenta Canva (2026)
Em última análise, os três provedores suportam plenamente arquiteturas
modernas de dados, cabendo aos profissionais selecionar os componentes que
melhor se encaixam às preferências e restrições do projeto, sabendo que os padrões

### Página 21

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

de arquitetura são transferíveis, quem entende a fundo uma pipeline em AWS
conseguirá mapear facilmente conceitos equivalentes em GCP ou Azure.
Custos, Riscos e Decisões Arquiteturais
Embora a nuvem ofereça enorme flexibilidade e potencial de inovação rápida,
ela também introduz riscos, especialmente financeiros, se a arquitetura não for
cuidadosamente planejada com custos em mente. Alguns pontos de atenção incluem:
● Custos de Transferência de Dados (Egress):  a movimentação de dados
na nuvem, especialmente entre regiões ou para fora do provedor, pode
gerar custos elevados de egress que muitas vezes passam despercebidos.
Transferências automáticas, como replicações e backups, podem impactar
significativamente a f atura. Por isso, arquiteturas multi -regionais ou multi -
cloud devem ser desenhadas para minimizar egress, mantendo o
processamento próximo aos dados e monitorando ativamente fluxos de
transferência para evitar surpresas de custo ao longo do tempo.
● Consultas Mal Otimizadas e Custos de Computação:  em data
warehouses serverless, o custo está diretamente ligado aos dados lidos ou
processados, tornando consultas sem filtros ou sem uso de partições
potencialmente muito caras. Em ambientes provisionados, consultas
ineficientes aumentam o consumo de CPU e, consequentemente, os custos.
Por isso, uma boa modelagem com particionamento, indexação ou
clusterização, aliada a limites, alertas e monitoramento contínuo das
consultas, é essencial para controlar gastos e evitar surpresas financeiras.
● Dimensionamento e Over -Provisioning: na nuvem podemos escalar
facilmente, mas isso também facilita gastar demais se não formos diligentes.
Um risco comum é manter recursos maiores do que o necessário por
esquecimento ou por segurança exagerada. Exemplos: manter um cluster
de 10 nós no fim de s emana quando ninguém usa; alocar armazenamento
provisionado de DW bem acima do uso real; não desligar clusters de teste.
A cultura do auto-scaling e auto-shutdown deve ser incorporada em cada
arquitetura. Muitos serviç os gerenciados já oferecem schedules ou idle
timeout – configurá-los evita surpresas.

### Página 22

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

● Escolha inadequada de serviços ou classes:  decisões arquiteturais
inadequadas podem elevar significativamente os custos em nuvem, como
usar bancos relacionais para dados históricos ou manter informações pouco
acessadas em classes de armazenamento caras. Conhecer bem as opções
de storage e processame nto, aplicar políticas de lifecycle e escolher a
ferramenta adequada para cada tipo de workload são ações essenciais para
evitar desperdícios. Por isso, arquitetos de dados precisam incorporar
práticas de FinOps,  monitorando custos por pipeline e ajustando
continuamente a arquitetura para maximizar o retorno sobre o investimento.
● Riscos de Complexidade e Operação:  embora a nuvem facilite a
construção rápida de sistemas complexos, arquiteturas com muitos
componentes aumentam o risco operacional e os pontos de falha. Priorizar
simplicidade e serviços gerenciados reduz esforço de operação,
monitoramento e manutenção. Ao  mesmo tempo, é importante equilibrar
agilidade e lock -in tecnológico, avaliando o custo total e a estratégia de
longo prazo antes de escolher entre soluções proprietárias ou mais flexíveis.
Em suma, arquitetar em Cloud Data exige um balanço entre desempenho,
governança e eficiência econômica. As arquiteturas bem -sucedidas incorporam
considerações de custo desde o desenho inicial, em vez de tratar finanças como
reflexão tardia. Há até práticas  de “arquitetura orientada a custo”, ex.: projetar
pipelines pensando qual o custo por TB ingerido e transformado, escolhendo design
de dados que minimize movimentação e duplicação. Com monitoramento e ajustes
contínuos, é possível usufruir da escala e poder da nuvem sem estourar o orçamento,
entregando valor de negócio de forma sustentável.
CONCLUSÃO
O advento do Cloud Data consolidou-se como base das arquiteturas modernas
de dados, deslocando o foco da engenharia de dados de tarefas de infraestrutura
(provisionar servidores, ajustar discos, gerenciar clusters manualmente) para
decisões arquiteturais de alto nível e alinhamento ao negócio. Nesta transformação, a
separação entre computação e armazenamento emergiu como princípio -chave,
permitindo escalabilidade elástica e isolada de componentes, e padrões como o

### Página 23

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Lakehouse habilitaram novos patamares de unificação entre dados operacionais,
analíticos e de ciência de dados.
Um profissional de dados atual precisa dominar não apenas ferramentas
específicas, mas principalmente os trade-offs envolvidos em cada escolha
arquitetural: por que usar um fluxo de streaming vs batch, quando armazenar dados
em Parquet no lake vs inserir num warehouse, qual combinação de serviços equilibra
melhor custo e performance para determinado caso, como garantir  qualidade e
segurança ao mesmo tempo em que se democratiza acesso aos dados, entre outros
desafios. Em outras palavras, o engenheiro de dados na era do Cloud Data é também
um arquiteto, navegando pelas ofertas de nuvem e compondo soluções modulares
que melhor atendam às necessidades da organização.
Este módulo abordou os pilares de Cloud Data com ênfase prática nas
arquiteturas ETL em nuvem. Vimos que, independentemente do provedor, existem
conceitos comuns (ETL/ELT, bronze -prata-ouro, stream vs batch, data lake, data
warehouse, etc.) e vantagens significativas a explorar (elasticidade, isolamento,
serviços gerenciados). Ao mesmo tempo, ressaltamos cuidados para evitar
armadilhas de custos e complexidade excessiva.

### Página 24

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Entre as principais tendências do mercado, destaca -se o crescimento do
Analytics Engineering, que aproxima cientistas de dados e analistas da camada de
transformação, utilizando práticas de engenharia de software aplicadas a SQL.
Ferramentas como DBT popularizaram conceitos como versionamento, testes
automatizados e modularização das transformações, reforçando a adoção de
pipelines ELT em ambientes de nuvem. Essa abordagem tem se mostrado essencial
em arquiteturas modernas baseadas em Data Lake e Lakehouse.
Do ponto de vista de mercado, observa -se também uma forte convergência
entre Cloud Data e Inteligência Artificial. Provedores de nuvem vêm posicionando
seus serviços analíticos como base para aplicações de IA generativa, reforçando a
importância de pipelines escaláveis, dados bem organizados e governança desde o
desenho da arquitetura.
Indicação de material para consumo:
“Google - The key pillars of building a modern data platform - Youtube:
https://www.youtube.com/watch?v=UwKXKs0CCt8
“AWS Skill Builder – Aprendizado em Cloud e Dados”
A plataforma oficial de treinamento da AWS, o AWS Skill Builder oferece
diversas trilhas de aprendizagem voltadas à engenharia de dados, arquiteturas
serverless, orquestração de pipelines, analytics e serviços de armazenamento.
Disponível em: https://skillbuilder.aws/
“Google Cloud Skill Boosts”
O Google Cloud Skill Boosts (antigo Qwiklabs/Cloud Skills Boost) oferece
laboratórios práticos e trilhas de aprendizagem para desenvolvimento em Google
Cloud, incluindo tópicos de ingestão de dados, BigQuery, Dataflow, Pub/Sub,
orquestração e pipelines ELT . Muitos badges podem ser obtidos gratuitamente por
programas de créditos iniciais.
Disponível em: https://www.skills.google/catalog?skill-badge

### Página 25

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

Nesta aula, você compreendeu como o conceito de Cloud Data vai além da
simples migração de ambientes on -premises para a nuvem, representando uma
mudança estrutural na forma como dados são armazenados, processados e
consumidos. Foram discutidos os fundamentos das arquiteturas modernas, baseadas
na separação entre computação e armazenamento, que permitem maior elasticidade,
escalabilidade e otimização de custos.
Você explorou como pipelines de dados evoluem na nuvem, passando de
modelos rígidos e batch para arquiteturas mais flexíveis, que podem combinar
processamento em batch, streaming ou modelos híbridos, sempre orientados às
necessidades reais do negócio. Essa  análise mostrou que a modernização de
pipelines é tanto uma decisão técnica quanto estratégica.
Ao longo do conteúdo, você foi guiado (a) por um processo estruturado de
tomada de decisão arquitetural, aprendendo a definir estratégia de migração,
organização e retenção de dados, modelo de ingestão, orquestração, governança,
segurança e observabilidade antes mesmo de escolher tecnologias ou provedores de
nuvem.
Na parte prática, viu como essas decisões se materializam em arquiteturas de
Cloud Data, com exemplos de tecnologias oferecidas por AWS, Google Cloud e Azure.
Mapa Mental

Figura 4 - Mapa mental com o conteúdo abordado
Fonte: Elaborado pelo autor utilizando a ferramenta Canva IA (2026)

### Página 26

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

AWS Documentation. Disponível em: https://docs.aws.amazon.com/. Acesso em: 25
mar. 2026.
AWS Whitepaper. What is a modern data architecture?. Acesso em: 25 mar. 2026.
Google Cloud Documentation. Disponível em:
https://docs.cloud.google.com/docs?hl=pt-br. Acesso em: 25 mar. 2026.
KLEPPMANN, Martin. Designing Data-Intensive Applications. Sebastopol:
O’Reilly Media, 2017.
Microsoft Azure Documentation. Disponível em: https://learn.microsoft.com/en-
us/azure/. Acesso em: 25 mar. 2026.
REIS, Joe; HOUSLEY, Matt. Fundamentals of Data Engineering: Plan and Build
Robust Data Systems. Sebastopol: O’Reilly Media, 2022.

SAKHATSKY, Michael. Modern Data Architectures Explained: A Critical
Examination of Modern Strategies and Their Impacts. Medium.
Disponível em: https://medium.com/@msakhatsky/modern-data-architectures-
explained-a9a4e0c8d8ed. Acesso em: 25 mar. 2026.

### Página 27

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)

PALAVRAS-CHAVE
Cloud Data. Arquitetura de dados. Estratégia de migração.

### Página 28

Cloud Data (AWS S3, GCP BigQuery, Azure Data Lake)
