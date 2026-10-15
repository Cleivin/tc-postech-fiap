# FinOps em ambiente Cloud

**ETL Pipelines** · Aula 4 · Fase 2 — Data Prepare

Gestão de custo em cloud: trade-offs de performance, escala e orçamento.

**Tópicos:** `FinOps` · `custo cloud` · `otimização` · `particionamento` · `Parquet`

📄 [PDF da aula](./aula_04_finops_em_ambiente_cloud.pdf)

---

## Conteúdo

### Página 1

FinOps em ambiente Cloud

FINOPS EM AMBIENTE
CLOUD

### Página 2

FinOps em ambiente Cloud

### Página 3

FinOps em ambiente Cloud

FinOps (Financial Operations ) surgiu como uma disciplina que integra
princípios de gestão financeira às operações e engenharia de nuvem. Em termos
simples, trata -se de aproximar as equipes de finanças e tecnologia para controlar
melhor os custos de cloud, promovendo responsabilidade compartilhada pelos gastos
e maximizando o ROI (retorno sobre investimento) das soluções em nuvem. No
contexto de arquiteturas de dados em nuvem, o FinOps ganha relevância adicional: à
medida que organizações expandem pipelines de dados, data lakes e inici ativas de
Big Data, os custos de computação e armazenamento podem escalar de forma
imprevisível. A promessa do FinOps é garantir inovações contínuas em dados sem
estourar o orçamento, fornecendo visibilidade e governança financeira constantes.
A transição para nuvem trouxe uma mudança de mentalidade de um modelo
CAPEX (grandes investimentos de capital em hardware próprio) para OPEX (custos
operacionais variáveis conforme o uso). Nesse novo paradigma, pagar somente pelo
uso traz agilidade, mas também pode gerar “sustos” na fatura se não houver controle.
Diferentemente do data center tradicional – onde custos eram fixos e previsíveis (pois
o equipamento era comprado antecipadamente) – na nuvem cada consulta de dados,
cada hora de instância e cada g igabyte transferido aparece na conta. Isso exige que
engenheiros e cientistas de dados desenvolvam um modelo mental orientado a
custos, incorporando considerações financeiras já no design de sistemas de dados.
Em outras palavras, eficiência de custo torna -se tão importante quanto desempenho
e escalabilidade.
Vamos explorar a aplicação do framework FinOps no contexto de pipelines
ETL, integração em tempo real com sistemas como Apache Kafka e gerenciamento
de grandes volumes de dados em nuvem.

### Página 4

FinOps em ambiente Cloud

Laboratório Teórico: Pipeline ETL com Validação de Qualidade
Você faz parte de um time e foi convidado a participar de um comitê de adoção
de FinOps em uma empresa que está expandindo seus investimentos em IA e análise
preditiva na nuvem. A empresa deseja adotar práticas modernas de controle de
custos, porém ainda n ão possui processos maduros de governança financeira na
infraestrutura de dados.
Sua missão será avaliar a maturidade atual da organização, identificar riscos
ocultos, propor estratégias de integração de práticas FinOps com MLOps e sugerir
ferramentas que viabilizem essa governança. Além disso, deverá justificar a escolha
de métodos e tecnologias, embasando sua proposta com fundamentos do conteúdo
estudado e pesquisas complementares.
Etapas do Laboratório
1. Diagnóstico Inicial – “Onde estamos” : simule o preenchimento de uma
autoavaliação de maturidade FinOps (disponível em:
https://www.finops.org/wg/finops-assessment/) com base em um cenário
fictício (ou inspirado em uma empresa real conhecida). Registre os pontos
fortes, ausências e oportunidades de melhoria.
2. Mapeamento de riscos financeiros ocultos : liste ao menos 3 fontes
potenciais de desperdício financeiro em workloads de dados (ETL, ML,
armazenamento, streaming), considerando formatos, transferência e uso de
instâncias não otimizadas.
3. Integração com MLOps e Cultura DevFinOps : descreva uma estratégia de
integração de práticas FinOps a um ciclo de Machine Learning típico. Inclua
etapas como: treinamento com GPU, ambientes interativos, versionamento de
modelos, tagging por ID de experimento, entre outros. Considere o papel do
time financeiro no processo.

### Página 5

FinOps em ambiente Cloud

4. Proposta Final de Estratégia : com base nas etapas anteriores, redija uma
proposta de com recomendações para adoção de FinOps  na organização
analisada. Inclua sugestões técnicas, ferramentas, estratégias de tagging e
ações de curto prazo (quick wins).

### Página 6

FinOps em ambiente Cloud

FinOps para Ambiente Cloud
A transição das arquiteturas de dados corporativas para ambientes nativos em
nuvem alterou fundamentalmente a economia da ciência e da engenharia de dados.
Se os estágios iniciais da adoção da nuvem foram caracterizados por uma busca
incessante por escalab ilidade bruta e agilidade, o paradigma atual exige
responsabilidade financeira e a otimização sistemática do valor de negócio. FinOps,
um portmanteau de "Finance" e "DevOps", emergiu como um framework operacional
e uma prática cultural crítica que facilita  a colaboração entre as equipes de
engenharia, finanças e negócios para maximizar o retorno dos investimentos em
nuvem.
O Ciclo de Vida FinOps nos Pipelines de Dados
A prática de FinOps é estruturada em três fases iterativas: Informar, Otimizar
e Operar.
 Na fase de Informação, o objetivo é dar visibilidade clara sobre custos, uso e
eficiência da nuvem, viabilizando alocação precisa por meio de tagging, hierarquias
de contas e automação, com destaque para padrões como o FOCUS, que unificam
dados de faturamento entre provedores.
Na fase de Otimização, o foco é reduzir custos sem perder performance,
atuando tanto no uso dos recursos, por meio de rightsizing e ajustes de retenção,
quanto nas taxas, aproveitando modelos de desconto por compromisso como RIs,
Savings Plans e CUDs.
Na fase de Operação, o FinOps é institucionalizado com governança, políticas
e mudança cultural, incentivando engenheiros e cientistas de dados a tratar custo
como métrica de eficiência, apoiados por automação e feedback contínuo para manter
o controle financeiro em ambientes elásticos.

### Página 7

FinOps em ambiente Cloud

Figura 1 - Ciclo de vida do FinOps ilustrado como um ciclo contínuo com três fases principais
– Informar (Visibilidade & Alocação de custos), Otimizar (Taxas & Uso eficiente) e Operar (Melhoria
Contínua & Governança Operacional).
Fonte: Elaborado pelo autor utilizando a ferramenta Canva (2026)
Pilares da Engenharia de Dados sob a Ótica Financeira
A eficiência de um pipeline ETL depende do equilíbrio entre quatro pilares
fundamentais de engenharia, cada um com seus próprios gatilhos de custo.
A Computação é geralmente o maior motor de custos. Plataformas como o
Databricks utilizam motores de execução otimizados (como o Photon) para reduzir o
tempo de execução e, consequentemente, o custo total, mesmo com taxas de
licenciamento premium. O uso de instâncias baseadas em arquitetura Graviton (ARM)
pode oferecer até 24% menos custo para a mesma carga de trabalho.
No Armazenamento, a estratégia de camadas é a chave. Manter dados
históricos em discos SSD de alto desempenho pode ser um desperdício. O modelo de
tiering permite mover dados raramente acessados para classes como S3 Glacier,
reduzindo custos em até 90%. O uso de formatos colunares como Parquet ou Delta
Lake também é uma decisão financeira: por serem compactos e permitirem a leitura
de colunas específicas (predicate pushdown), eles reduzem o volume de dados

### Página 8

FinOps em ambiente Cloud

escaneados e o custo de consulta em ferramentas como Amazon Athena ou Google
BigQuery.
Os custos de Rede e Egress são os "vilões ocultos". Transferir grandes
volumes de dados entre diferentes regiões da nuvem ou para a internet pode exceder
o custo do processamento em si. Estratégias de FinOps exigem a colocação de
recursos (manter processam ento e armazenamento na mesma zona de
disponibilidade) ou o uso de réplicas locais para evitar taxas de tráfego inter-AZ.
Por fim, a Orquestração garante que clusters efêmeros sejam criados apenas
durante o processamento e destruídos imediatamente após, eliminando o custo de
ociosidade (idle cost).
FinOps em Tempo Real e Machine Learning
A integração com o Apache Kafka introduz desafios únicos porque os clusters
de streaming operam 24/7. Diferente de jobs batch, a ineficiência aqui é faturada a
cada segundo. O excesso de partições aumenta a carga de metadados, enquanto
políticas de retenção longas multiplicam o custo de armazenamento replicado. Para
otimizar, é recomendado alinhar o tempo de retenção às necessidades reais de
recuperação e utilizar o suporte a rack awareness para que consumidores leiam de
réplicas locais, eliminando taxas de rede.
No campo da Ciência de Dados, o FinOps diferencia o Treinamento (custo
finito, similar a CAPEX) da Inferência (custo contínuo, OpEx). Enquanto o treinamento
pode ser otimizado com instâncias spot e GPU pooling, a inferência escala com o
número de usuários. Se um modelo de IA custar mais por chamada do que a receita
que gera, ele é economicamente inviável.
FATOR IMPACTO ESTRATÉGIA DE
MITIGAÇÃO
Janela de contexto Tokens de entrada/saída Limitar tokens e “forçar”
respostas concisas
Complexidade do modelo Hardware de alto custo Implementar “Model
tiering”
Arquitetura de suporte Busca vetorial e RAG Otimizar cache semÂntico

### Página 9

FinOps em ambiente Cloud

e bancos vetoriais
Tabela 1 – Exemplos de fatores de custo na inferência de IA
Fonte: elaborado pelo autor (2026)

Equilíbrio entre Custo e Performance
Um dos principais desafios do FinOps em dados é equilibrar custo e
desempenho, avaliando se os ganhos técnicos realmente justificam o aumento de
gastos. A proposta do FinOps é tornar esse trade -off explícito nas decisões
arquiteturais, buscando a melhor re lação custo -benefício. Em vez de maximizar
performance a qualquer custo, a abordagem recomendada é otimizar primeiro
consultas e modelos de dados, alcançar um desempenho adequado ao negócio e só
então investir mais quando o impacto financeiro ou estratégico realmente justificar.
O FinOps mostra que custo e performance não são necessariamente opostos:
boas práticas de engenharia podem melhorar ambos simultaneamente. O uso de
formatos colunares, compressão e particionamento reduz a quantidade de dados
lidos, acelerando consultas e diminuind o significativamente os custos. Da mesma
forma, o rightsizing de clusters busca o equilíbrio ideal entre tempo de execução e
gasto, evitando tanto recursos insuficientes quanto capacidade ociosa. Com
monitoramento e autoscaling, é possível ajustar continua mente a infraestrutura para
manter desempenho adequado com o menor custo possível.
FinOps ensina a não aceitar custo desproporcional como “custo de fazer
negócio”, quase sempre há algo a otimizar no pipeline para trazer a relação
custo/performance a patamares sustentáveis.
Em síntese, custo e desempenho devem ser considerados lados da mesma
moeda no desenho de soluções de dados. O objetivo não é nem ser o mais barato
nem o mais rápido a qualquer preço, mas maximizar o valor obtido por real gasto. Nas
próximas seções, explora remos práticas concretas onde decisões inteligentes
permitem ganhos de eficiência financeira sem comprometer (e às vezes até
melhorando) a performance das aplicações de dados.
Métricas de Sucesso e Unit Economics
Para medir a maturidade do FinOps, não basta olhar para o total da fatura. É
necessário calcular o Custo Unitário, como o custo por transação ou por modelo

### Página 10

FinOps em ambiente Cloud

treinado. Isso permite que o negócio entenda se o aumento do gasto na nuvem está
acompanhando o crescimento da receita.
As fórmulas essenciais incluem:

Figura 2 - Fórmula do cálculo TCO e Waste.
Fonte: Adaptado pelo autor a do site FinOps KPIs (2026)

KPIs de Utilização e Performance
Além das métricas financeiras, devemos monitorar a utilização de recursos.
Operar abaixo de 40% de eficiência de CPU/Memória é frequentemente considerado
um desperdício de capital. Alvos ideais para produção situam -se entre 70% e 80%,
equilibrando performance e custo.
KPI DEFINIÇÃO ALVO RECOMENDADO
Taxa de Alocação % do gasto atribuído a
etiquetas válidas
> 95% (maturidade run)
Cobertura de desconto % do gasto coberto por
RIs ou Savings Plans
70% - 80% das cargas
estáveis

### Página 11

FinOps em ambiente Cloud

Acurácia de previsão Variância entre gastos
previsto e real
Dentro de +/- 5% (95%
acurácia)
MTTR da Anomalia Tempo médio para
detectar e corrigir picos
de custo
< 24 horas para evitar
surpresas na fatura
Tabela 2 – Exemplos de KPI para acompanhamento da utilização de recursos.
Fonte: elaborado pelo autor (2026)

Estratégias de Otimização de Custos em Engenharia de Dados
Nesta seção, vamos ver algumas práticas técnicas que possibilitam reduzir
custos em ambientes de dados, mantendo ou melhorando a efetividade dos pipelines.
Abordaremos otimizações em consultas e modelagem de dados, uso de formatos de
armazenamento eficient es, e estratégias de particionamento e ciclo de vida dos
dados.
Otimização de Queries e Modelagem de Dados
A forma como estruturamos dados e escrevemos consultas SQL (ou código
equivalente) tem influência massiva sobre os custos. Consultas não otimizadas podem
varrer terabytes desnecessariamente, consumindo mais CPU, memória e I/O, o que,
em sistemas de cobrança por uso, significa conta mais alta. Já uma boa modelagem
de dados e queries bem escritas realizam o mesmo trabalho escaneando menos
dados e usando menos ciclos computacionais.
Um princípio fundamental é trazer filtros o mais cedo possível ( predicate
pushdown). Em data warehouses e frameworks tipo Spark, isso significa aplicar
cláusulas WHERE e projetar colunas (SELECT apenas as necessárias) para evitar ler
dados que não serão usados. Por exemplo, em vez de SELECT * FROM vendas
para depois filtrar em aplicativo, faça SELECT colunas_necessarias FROM
vendas WHERE ano = 2023 . Parece óbvio, mas muitos pipelines cometem o erro
de extrair conjuntos enormes e filtrar só no final. Sistema s modernos conseguem
“empurrar” esses predicados para a leitura dos arquivos, reduzindo o volume lido e
processado, economia direta de custo, já que muitos serviços cobram por volume de
dados lido. (É preciso, porém, que os dados estejam formatados e parti cionados de
forma compatível, como veremos adiante.)

### Página 12

FinOps em ambiente Cloud

Na modelagem de dados, um conceito aliado ao FinOps é projetar esquemas
que facilitem consultas seletivas. Por exemplo, se sabemos que a maioria das análises
de um conjunto de eventos será por data e região, vale particionar ou indexar por
essas colunas. Assim, uma consulta filtrando uma região numa data específica acessa
só aquela partição, ignorando o resto (economizando tempo e dinheiro). Em data
warehouses, é recomendável usar clustering ou partition keys  nas colunas mais
filtradas. Outra prática é pré -agregar ou materializar resultados frequentes se isso
reduzir ordens de grandeza de processamento para cada consulta futura. Imagine que
todo dia dezenas de consultas calculam a média móvel de 30 dias das ve ndas: em
vez de cada query recalcule do zero 30 dias de dados (custo repetido), pode -se criar
uma tabela materializada ou sumarizada diariamente. Claro, isso implica custo de
armazenamento extra para guardar agregados, mas se bem dimensionado o saldo
pode ser positivo, paga -se um pouco de storage para economizar muito compute
diário.
Por outro lado, é preciso cuidado: excesso de pré -cálculo ou duplicação pode
desperdiçar recursos se as suposições mudarem. FinOps é contra over-engineering:
materialize ou indexe somente o que traz economia comprovada ou atende
necessidades claras, pois cada materialização tem custo de manutenção. Monitorar o
cache hit ou uso efetivo desses artefatos ajuda a decidir se valem a pena continuar.
Uma query bem otimizada não é só mais rápida, ela consome menos recursos
e, na nuvem, menos recursos = menos dinheiro gasto. Como diz um dos princípios do
FinOps: “a eficiência de engenharia agora inclui custo como métrica” . Adotar essa
mentalidade no design de consultas e esquemas é dar um passo largo rumo à
excelência FinOps.
Formatos Colunares e Compressão de Dados
A escolha do formato de armazenamento impacta diretamente o custo e a
performance do processamento de dados. Formatos colunares como Parquet e ORC,
aliados à compressão, reduzem significativamente o volume armazenado e permitem
ler apenas as colunas necess árias, gerando economia tanto em storage quanto em
consultas. Por isso, tornaram -se o padrão em workloads analíticos, sendo menos

### Página 13

FinOps em ambiente Cloud

indicados apenas em cenários de escrita frequente ou acesso pontual a registros
individuais, onde formatos orientados a linha podem ser mais eficientes.
Particionamento de Dados e Ciclo de Vida
O particionamento inteligente é uma técnica essencial para reduzir custos, pois
divide grandes conjuntos de dados em segmentos lógicos, permitindo que consultas
leiam apenas as partes relevantes por meio de partition pruning. Isso evita varreduras
completas e diminui significativamente o volume de dados processados. Além disso,
o particionamento facilita a gestão do ciclo de vida dos dados, possibilitando mover
informações antigas para camadas de armazenamento mais baratas po r meio de
políticas automáticas,  mantendo desempenho adequado para dados recentes e
custos controlados para dados frios.
Particionamento também reduz custos indiretos. Por exemplo, melhora cache
hit ratio em consultas repetidas (já que menos dados a ler aumenta chance de cache),
e facilita paralelismo eficiente (vários nós trabalhando em diferentes partições sem
competir, evitando gargalos
Um cuidado: as partições devem ser definidas com granularidade certa. Se
forem muito amplas (ex.: partição por ano quando consultas são diárias), não ajudam
muito; se forem muito finas (ex.: por minuto), viram sobrecarga. FinOps não dita a
granularidade, m as observa o padrão de uso: analise logs de consultas e acesso,
identifique campos comuns nos filtros e volumes envolvidos, então particione de
acordo. E revise periodicamente, se o padrão de acesso mudar, ajuste as partições.
Ações de Infraestrutura Econômica
Indo além das otimizações no nível dos dados e software, existem estratégias
de infraestrutura cloud que podem trazer economia significativa sem sacrificar (muito)
a qualidade de serviço. Aqui exploraremos algumas abordagens como: uso de
instâncias Spot/Preemptible, orquestração de clusters efêmeros, escolhas de serviços
gerenciados vs. autogerenciados, e considerações de localidade de dados para
reduzir custos. Trata-se de olhar para a base de recursos computacionais com lentes
de FinOps e identificar opor tunidades para pagar menos pelo mesmo poder de
processamento.

### Página 14

FinOps em ambiente Cloud

Instâncias Spot e Preemptible: são recursos de computação oferecidos pelos
provedores a preços bem inferiores (até 90% mais baratos) que o normal, com a
contrapartida de serem interruptíveis. A AWS possui as Spot Instances, o Google
Cloud tem Preemptible V Ms (integradas hoje ao conceito de Spot VMs também), e
Azure tem Azure Spot, cada um com suas regras.
É importante, porém, entender as diferenças de comportamento entre
provedores: Instâncias Spot/Preemptible variam entre provedores e isso impacta o
planejamento. Na AWS e no Azure, elas podem ser encerradas a qualquer momento
conforme disponibilidade ou pr eço, sem limite fixo de duração; já no GCP, as VMs
preemptible têm tempo máximo de 24 horas, sendo finalizadas obrigatoriamente após
esse período. Por isso, workloads longos ou críticos precisam de tolerância a falhas,
como checkpoints e retomada, para apr oveitar esses recursos de menor custo sem
comprometer a execução.
Clusters Efêmeros e Auto-Desligamento
Uma prática essencial de FinOps é evitar manter a infraestrutura ligada sem
uso. Clusters e instâncias devem ser efêmeros, iniciados apenas quando necessários
e desligados automaticamente ao final do processamento, usando recursos como
auto-terminate, jobs transitórios ou agendamentos. Isso elimina custos de ociosidade,
que podem gerar desperdícios significativos quando recursos ficam ativos sem
utilização. A combinação de disciplina operacional com automação e alertas de baixa
utilização é fundamental para prevenir gastos desnecessários.
Uma extensão desse conceito é usar arquiteturas serverless ou sob demanda
quando possível, em vez de manter servidores fixos. Por exemplo, em vez de rodar
um servidor ETL continuamente esperando dados, usar AWS Lambda que cobra
apenas por execução quando e ventos chegam. Ou utilizar serviços gerenciados de
data processing como AWS Glue, Google Dataflow, Azure Data Factory, que alocam
recursos só durante a execução e depois liberam. Assim, paga -se apenas pelo
trabalho realizado. Claro que há trade-offs (limites de serviço, tempo de cold start,
configurações restritas), mas vale avaliar, especialmente para cargas eventuais ou
imprevisíveis. A mensagem fundamental é: desligue ou não provisione recursos antes

### Página 15

FinOps em ambiente Cloud

da hora. FinOps gosta de ephemerality, infra que vem e vai conforme a demanda, sem
faturas residuais.
Reservas e Planos de Economia
 Embora Spots e serverless sejam ótimos para workloads variáveis, muitos
sistemas de dados têm uma carga base estável e contínua – por exemplo, um cluster
Kafka rodando 24/7, ou um banco de dados analítico que precisa estar sempre
disponível. Para esses ca sos, FinOps recomenda aproveitar os descontos de
comprometimento oferecidos: Reserved Instances e Savings Plans (AWS), Committed
Use Discounts (GCP), Azure Reservations, etc. Basicamente, você se compromete a
pagar por certa capacidade ou gasto mínimo por 1 ou 3 anos e ganha descontos de
30-60% comparado ao preço sob demanda. Essa estratégia converte OPEX variável
em um semi-CAPEX planejado, garantindo economia em workloads previsíveis. Por
exemplo, se você sabe que sempre precisará de 3 nós XLarge no clust er ETL, pode
reservá-los por 1 ano com desconto. O FinOps aqui envolve planejamento e
colaboração com finanças, pois requer aprovação para compromissos de longo prazo.
Localidade e Arquitetura de Rede:  como discutido nos custos de
transferência, uma ação de infraestrutura é alinhar a topologia para minimizar o
tráfego caro. Isso significa, por exemplo, manter sistemas que se comunicam muito
dentro da mesma região ou VPC. Se você tem seu data lake no us-east-1, procure
rodar as VMs de análise também em us-east-1, para não pagar egress inter-region.
E dentro da região, use endereços privados ou endpoints VPC, se um serviço A chama
a API de serviço B via internet pública, muitas vezes a nuvem cobra saída e en trada,
enquanto via endpoint privado poderia ser isento ou bem mais barato. FinOps
demanda atenção a essas configurações “chatas” de rede, mas que podem fazer
diferença em grandes fluxos de dados. Consolidar recursos em menos regiões
também ajuda (embora h aja casos de multi -região por redundância ou latência, aí
equilibra-se necessidade vs. custo).
Um ponto interessante:  diferentes clouds têm instâncias especializadas e
preços variados para hardware semelhante. Em projetos flexíveis multi -cloud, às
vezes pode ser vantajoso rodar um certo workload onde é mais barato, por exemplo,
cargas intensivas em GPU poderiam ser trein adas na cloud que oferece GPU mais

### Página 16

FinOps em ambiente Cloud

barata ou descontos melhores, e então os resultados trazidos de volta. Contudo, deve-
se tomar cuidado para não gastar mais em transferência entre clouds do que se
economizou em compute.
Por fim, considerações de arquitetura distribuída: alguns sistemas permitem
segmentar dados e processamento geograficamente para evitar movimentação. Por
exemplo, em vez de centralizar um data warehouse global e pagar toneladas de
egress consolidando dados  de vários países, uma empresa pode optar por manter
data warehouses regionais e só agregar resultados sumarizados centralmente (menos
volume movimentado). Ou usar um modelo federado onde cada região processa
localmente e compartilha apenas pequenos indicadores. Essa engenharia arquitetural
é avançada e altamente dependente do caso de uso, mas ilustra como FinOps e
arquitetura de sistemas andam juntos, decisões de design podem custar ou
economizar milhões a longo prazo.
Comparação de Ecossistemas de Dados em Nuvem
A escolha do provedor de nuvem (AWS, Azure ou GCP) dita as ferramentas de
FinOps disponíveis e as estratégias de otimização mais eficazes. Cada nuvem possui
uma filosofia arquitetônica distinta que impacta o trabalho do cientista de dados.
Amazon Web Services Flexibilidade e Controle
A AWS oferece o ecossistema mais maduro e configurável, ideal para equipes
que possuem expertise técnica profunda e desejam controle total sobre a
infraestrutura. O Amazon SageMaker é a plataforma para ML, oferecendo visibilidade
granular através do Cost Explorer e Budgets.
● Vantagem FinOps: mercado de instâncias spot altamente líquido e planos
de poupança (Savings Plans) extremamente flexíveis que cobrem EC2,
Lambda e Fargate.
● Desafio: a vasta gama de opções (mais de 200 serviços) pode levar à
complexidade excessiva e dificuldade em manter uma governança
centralizada sem automação robusta.

### Página 17

FinOps em ambiente Cloud

Microsoft Azure Integração Corporativa e IA
O Azure brilha em ambientes corporativos que já utilizam o ecossistema
Microsoft. A integração com Active Directory e o uso de ferramentas familiares como
Power BI facilitam a adoção de relatórios de FinOps para stakeholders não técnicos.
● Vantagem FinOps: o "Azure Hybrid Benefit" permite reutilizar licenças de
software on -premises na nuvem, reduzindo custos de SQL Server e
Windows em até 76%.
● Desafio: o provisionamento de recursos pode ser menos ágil que no GCP
ou AWS em certos cenários de escalonamento global massivo.
Google Cloud Platform
Simplicidade e Serverless O GCP é construído com uma mentalidade de
"serverless-first", abstraindo grande parte da gestão de infraestrutura. O BigQuery é o
coração desta estratégia, oferecendo um modelo de custo baseado em dados
processados que é ideal para equipes de análise pura.
● Vantagem FinOps: descontos por Uso Sustentado (SUD) são aplicados
automaticamente para instâncias que rodam por grande parte do mês, sem
necessidade de compromisso prévio. Além disso, a separação total entre
armazenamento e computação no BigQuery permite otimizações de cust o
muito agressivas.
● Desafio: portfólio de serviços menor que o da AWS, o que pode limitar
opções para arquiteturas de nicho.

Observabilidade de Custos e Governança Financeira
Implementar FinOps não se resume a técnicas pontuais, requer também
mecanismos de governança e monitoramento de custos. Nesta seção, discutiremos a
importância de tagueamento de recursos, alocação de custos
(showback/chargeback), uso de métricas e dashboards de custos, orçamentos e
alertas, além da cultura organizacional necessária para sustentar FinOps.

### Página 18

FinOps em ambiente Cloud

Tagging e Atribuição de Custos
Uma base imprescindível da governança FinOps  é conseguir atribuir cada
gasto de nuvem a um responsável, projeto ou unidade de negócio. Para isso, usamos
tags (etiquetas) ou separação por contas/projetos. Cada recurso na nuvem (VM,
bucket, banco de dados, etc.) deve receber metadados indicando, por exemplo:
Projeto = Marketing-CampanhaX, Ambiente = Dev, Time = DataScience, Dono =
Fulano. Assim, quando a conta chegar, é possível fatiar: “quanto custou a campanha
X? E o ambiente Dev vs Prod? E qual time gerou mais despesas?”. Sem tags, a fatura
da nuvem é uma caixa-preta por serviço, difícil dizer qual iniciativa consumiu o quê.
Com tags, ganha -se visibilidade granular e promove -se a responsabilização
descentralizada, os times tomam posse de seus gastos, pois sabem que estarão
identificados.
Na prática, muitas empresas adotam showback ou chargeback para dar
visibilidade dos custos de nuvem por time, incentivando comportamento mais
responsável e decisões orientadas a valor. Ferramentas nativas dos provedores e
soluções especializadas permitem d etalhar gastos por tags, projetos e ambientes. A
recomendação de FinOps é padronizar tags mínimas (projeto, equipe, ambiente,
centro de custo) e, em ciência de dados, incluir identificadores de experimentos ou
modelos, conectando diretamente custo e inovaç ão e permitindo avaliar se o
investimento técnico realmente compensou os resultados obtidos.
Showback vs. Chargeback
São modelos de alocação. No showback, você mostra para os times quanto
eles gastaram, mas o pagamento sai de um orçamento central, é mais educativo, para
visibilidade. Já no chargeback, cada departamento tem seu próprio orçamento e
literalmente “paga” (internamente) por seu uso de nuvem. O FinOps inicial geralmente
começa com showback, pois ainda está fomentando cultura. Com maturidade,
algumas organizações adotam chargeback parcial ou total, inserindo custos de cloud
nas unidades de negócio. Isso cria ince ntivos financeiros diretos: por exemplo, o
departamento A pode decidir não rodar certa análise caríssima porque gastaria todo
seu budget, se realmente quiser, precisa justificar o valor ou otimizar.
Independentemente do modelo, o importante é mensurar e di vulgar os custos de

### Página 19

FinOps em ambiente Cloud

maneira compreensível. As métricas devem ser levadas às equipes de engenharia
regularmente, assim como se acompanha performance ou qualidade. Em dashboards
internos, pode haver um gráfico “custo por 1000 usuários atendidos” ou “gasto por
pipeline executada”, indicadores de eficiência que orientam decisões.
Orçamentos e Alertas
Uma prática preventiva de FinOps é configurar limites de orçamento e alarmes
de custo. Todos os provedores oferecem isso: define -se um valor mensal ou diário
esperado, e se o gasto real o atingir (ou projetar atingi-lo), um alerta é enviado (email,
SMS, Slack etc.). Isso pode ser refinado por serviço, por tag, por projeto.\ Por exemplo,
“alertar se gastos do projeto DataScience-Experimentação excederem R$10k no
mês”. Esses alarmes não bloqueiam (a não ser que você programe algo), mas
funcionam como um sinal de fumaça para anomalias. Se um job entrar em loop infinito
lendo dados e gastando sem parar, o alerta vai disparar muito antes da fatura fechar,
dando chance de intervenção.
Além de alertas de limite absoluto, existem ferramentas de detecção de
anomalias de gasto usando ML (ex.: AWS Cost Anomaly Detection, Azure Cost Alerts,
ou terceiros). Elas aprendem seu padrão de consumo e avisam se algo fora do comum
acontece (ex.: “custo do serviço X está 50% maior do que o usual nesta altura do
mês”). É uma camada extra de proteção, útil especialmente em ambientes complexos
com muitos serviços.
Cultura e Processo:  por fim, nenhuma ferramenta substitui a cultura e
processos organizacionais. FinOps prospera em culturas onde há colaboração
multifuncional, times de engenharia, produto e finanças trabalhando juntos
continuamente, e onde valor de negócio guia decisões técn icas. Para inculcar isso,
algumas ações são úteis:
● Treinamento e conscientização:  capacitar engenheiros de dados a
entender a fatura da cloud, a usar as ferramentas de custo, a pensar em
otimização. Workshops internos de boas práticas FinOps, etc.
● Políticas e guardrails oficiais: por exemplo, padronizar que todo projeto
novo deve estimar seu custo esperado e ter tags adequadas; ou estabelecer
que nenhum recurso caro fica em Dev/projeto pessoal sem aprovação após

### Página 20

FinOps em ambiente Cloud

X dias. FinOps não visa engessar a inovação, mas algumas regras claras
evitam deslizes (similar a políticas de segurança).
● Revisões periódicas de custo:  incluir discussões de custo em sprints e
post-mortems. Se um pipeline foi caro demais no mês, analisar o porquê e
planejar ajuste. Tratar picos de gasto como incidentes de produção,
entender causa raiz (e.g., “consulta ineficiente escrita pelo time X”), ação
corretiva (“refatorar consulta ou a umentar partições”) e ação preventiva
(“adicionar alerta ou documentação para evitar repetição”).
● Objetivos compartilhados: definir metas de eficiência, como “reduzir custo
por pipeline em 15% neste trimestre” ou “manter gastos de cloud estáveis
enquanto volume de dados cresce 20%”, isso tende a engajar os times a
buscar ativamente oportunidades FinOps.
Quando todos na organização se sentem responsáveis pelo uso consciente,
atinge o nível do FinOps esperado: não é mais alguém “policiando” custos de fora, e
sim as próprias equipes otimizando porque entendem que isso libera recursos para
inovação e garante sustentabilidade. Esse é o cenário ideal em que FinOps deixa de
ser um projeto à parte e vira parte da operação diária, tão importante quanto monitorar
uptime ou qualidade dos dados.
Para ajudar organizações a avaliar seu nível de maturidade em FinOps, pode-
se usar checklists de autoavaliação.
FinOps é uma responsabilidade multidisciplinar
O sucesso da implementação de FinOps depende da colaboração diária entre
os times. Embora as responsabilidades técnicas sejam distintas, os objetivos
financeiros são compartilhados.
STAKEHOLDER RESPONSABILIDADES
DE EXEMPLOS
EXEMPLO
Finanças Previsão de gastos,
relatórios e orçamento
Alocação de custos por
projeto/modelo
(chargeback interno)
Liderança/Executivos Definir metas e suportar
iniciativas FinOps
Priorizar investimentos
em dados com base no
ROI esperado

### Página 21

FinOps em ambiente Cloud

Engenheiros de Dados Otimização técnica da
infraestrutura
Uso de instâncias Spot
em jobs ETL; automação
de desligamento
Cientistas de Dados Experimentação
sustentável com custo em
mente
Taguear recursos de
treino de modelos para
monitorar gastos
Tabela 3 – Responsabilidade dos times com base em FinOps.
Fonte: elaborado pelo autor (2026)

Conclusão
O avanço das práticas de FinOps no contexto de dados em nuvem representa
não apenas uma tendência, mas uma necessidade estratégica para empresas que
buscam escalar suas operações de forma sustentável. Ao integrar governança
financeira diretamente aos pipelines de dados e modelos de Machine Learning, torna-
se possível transformar decisões técnicas em ações alinhadas ao valor de negócio,
promovendo maior eficiência e controle de gastos.
Ferramentas emergentes, como as plataformas FinOps -as-a-Service e os
mecanismos de tagueamento automatizado por inteligência artificial, demonstram que
a evolução tecnológica está a serviço da maturidade operacional. Essas soluções
elevam o nível de visibilidade sobre os custos e permitem que times multidisciplinares,
engenheiros, cientistas de dados e analistas financeiros, colaborem com base em
métricas concretas e atualizadas em tempo real.
Mais do que uma disciplina técnica, o FinOps  estabelece uma nova cultura
organizacional, como exemplificado pela abordagem DevFinOps. Ao envolver o time
financeiro desde a concepção arquitetural, rompe -se a separação entre orçamento e
infraestrutura, criando um ambiente onde custo, performance e ino vação caminham
juntos. Essa transformação cultural é o alicerce para que organizações tomem
decisões sustentáveis, transparentes e orientadas a valor.

### Página 22

FinOps em ambiente Cloud

A integração do FinOps ao MLOps tem ganhado destaque à medida que
ferramentas de governança de custos passam a ser incorporadas nativamente a
pipelines de Machine Learning e plataformas como MLflow e Vertex AI, permitindo
maior controle e previsibilidade financeira durante o ciclo de vida dos modelos.
Paralelamente, observa -se o avanço do uso de inteligência artificial para
automatizar o processo de etiquetagem de custos, aplicando tags por dataset, pipeline
ou modelo, o que reduz a dependência de processos manuais e aumenta a
granularidade da visibilidade financeira. Outro movimento importante no mercado é o
crescimento de plataformas FinOps-as-a-Service, como CloudZero, Zesty e nOps, que
oferecem análises preditivas de gastos com base no comportamento de uso de dados
e recursos.
Complementando esse cenário, surge a cultura DevFinOps, que propõe a
inclusão do time financeiro já nas fases iniciais de desenho técnico das arquiteturas,
promovendo uma colaboração mais próxima entre engenharia, dados e finanças, e
conectando diretamente as decisões técnicas ao impacto orçamentário.
“FinOps Fridays – Cloud Cost Optimization” - Podcast: Designing Cloud
Cost Visibility for Data Teams
Este episódio aborda como a visibilidade de custos impacta decisões em times de
dados, desde a escolha de ferramentas até o gerenciamento de ambientes de
machine learning.
https://open.spotify.com/show/0Mjr4VlDXQbuHU0Lltys6L
“Cloud FinOps: Collaborative, Real-Time Cloud Financial Management” –
J. R. Wilde, M. Broude, M. Fuller : este livro é considerado a principal referência
técnica e estratégica sobre práticas FinOps. A segunda edição traz casos atualizados,
frameworks de governança e estratégias específicas para workloads de dados e
machine learning.
“FinOps Foundation” – Tendências e Boas Práticas - A principal referência
global para a evolução do FinOps: Disponivel em: https://www.finops.org

### Página 23

FinOps em ambiente Cloud

Começamos definindo FinOps e entendendo seus pilares (Informar, Otimizar,
Operar) aplicados ao ciclo de vida dos dados. Passamos pelos fundamentos de onde
surgem os custos em arquiteturas de dados e enfatizamos a necessidade de equilíbrio
entre gasto e desempenho. Em seguida, detalhamos uma série de técnicas concretas,
da otimização de queries ao uso de instâncias Spot, demonstrando que decisões
técnicas inteligentes podem simultaneamente melhorar performance e reduzir
despesas.
Integrar FinOps em um ambiente de dados significa adotar um modelo mental
no qual cada ação técnica tem visibilidade de seu impacto econômico. Isso não quer
dizer colocar dinheiro acima de tudo, quer dizer alinhar as decisões tecnológicas aos
objetivos de negócio, assegurando que cada real investido em nuvem traga retorno
tangível em valor de dados. À medida que a disciplina de FinOps evoluiu, ficou claro
que não é só um “braço de finanças tentando cortar custos”, mas sim uma função
interdisciplinar. Sucess o em FinOps vem quando engenharia, produto e financeiro
trabalham juntos com dados compartilhados e metas comuns. Por exemplo, definem
métricas de unidade (como custo por modelo treinado com sucesso) e se guiam por
elas para melhorar continuamente.
Por fim, reforçamos que FinOps não é “pão -durismo tecnológico”. Pelo
contrário, trata -se de gastar para acelerar negócios, mas gastando de forma
inteligente. Às vezes, o FinOps mostrará que vale a pena investir mais em certo
aspecto para colher retorno mui to maior, por exemplo, pagar por uma ferramenta de
monitoramento de custo que evita desperdícios grandes, ou expandir um pipeline que
traz receita direta. A diferença está em ter os dados e critérios para fazer essas
escolhas conscientemente, e não às cegas.
Mapa Mental

### Página 24

FinOps em ambiente Cloud

Figura 2 - Mapa mental com o conteúdo abordado
Fonte: Elaborado pelo autor utilizando a ferramenta Canva IA (2026)

### Página 25

FinOps em ambiente Cloud

AMAZON WEB SERVICES. AWS Cost Optimization. AWS Well-Architected
Framework, 2023. Disponível em:
https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/. Acesso
em: 25 mar. 2026.
AZURE. Monitoramento e controle de custos na Azure. Microsoft Learn, 2023.
Disponível em: https://learn.microsoft.com/pt-br/azure/cost-management-billing/.
Acesso em: 25 mar. 2026.
DOIT INTERNATIONAL. Essential FinOps KPIs to Optimize Cloud Spend. [S. l.],
2023. Disponível em: https://www.doit.com/blog/finops-kpis/. Acesso em: 25 mar.
2026.
FINOPS FOUNDATION. FinOps Assessment Working Group. [S. l.], 2023.
Disponível em: https://www.finops.org/wg/finops-assessment/. Acesso em: 25 mar.
2026.
MICROSOFT. FinOps Framework. Microsoft Learn, 2023. Disponível em:
https://learn.microsoft.com/pt-br/cloud-computing/finops/framework/finops-framework.
Acesso em: 25 mar. 2026.
PELANOR. Learn Essential FinOps KPIs. Pelanor Learning Center, 2023. Disponível
em: https://www.pelanor.io/learning-center/learn-essential-finops-kpis. Acesso em: 25
mar. 2026.
WILDE, J. R.; BROUD, M.; FULLER, M. Cloud FinOps – Tomada de decisões
colaborativas em tempo real sobre o valor da nuvem. 2. ed. Rio de Janeiro: Alta
Books, 2024.

### Página 26

FinOps em ambiente Cloud

PALAVRAS-CHAVE
FinOps. MLOps. Governança Financeira.

### Página 27

FinOps em ambiente Cloud
