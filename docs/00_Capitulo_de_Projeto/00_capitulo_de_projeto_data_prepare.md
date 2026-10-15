# Capítulo de Projeto — Data Prepare

**Capítulo de Projeto — Data Prepare** · Aula 0 · Fase 2 — Data Prepare

Introdução oficial da Fase 2 (Data Prepare) no CRISP-DM. Explica por que cientistas de dados precisam dominar engenharia de dados, arquitetura, SQL, NoSQL e ETL antes da modelagem.

**Tópicos:** `CRISP-DM Data Understanding e Data Preparation` · `Relação engenharia de dados × ciência de dados` · `Visão das 4 disciplinas da fase` · `Escala, qualidade e custo dos dados`

📄 [PDF da aula](./00_capitulo_de_projeto_data_prepare.pdf)

---

## Conteúdo

### Página 1

Data Prepare

DATA PREPARE

### Página 2

Data Prepare

 Olá, cientista!
 Etapa do entendimento de negócio concluída com sucesso! Agora, seguindo
a metodologia do CRISP DM, entramos na etapa da preparação dos dados . Se a
Fase 1 te ajudou a pensar como cientista de dados, essa fase vai te ensinar a operar
dados no mundo real.
 Aqui começa a transição mais importante da formação: sair do cenário
idealizado de datasets prontos e limpos e entrar no território onde os dados são
grandes, distribuídos, inconsistentes, caros e, muitas vezes, caóticos. É exatamente
por isso que essa fase existe.

### Página 3

Data Prepare

Figura 1 - Relação engenharia de dados com ciência de dados.
Fonte: https://www.i2ai.org/content/blog/2021/6/engenharia-de-dados-para-todos/

 Por que um(a) cientista de dados precisa aprender tudo isso?
 Porque, na prática, você terá muitos outros desafios na sua carreira de
cientista de dados, além de modelagem preditiva, tal como a preparação dos
dados. Na maior parte dos projetos reais, o modelo é apenas a ponta do iceberg.
Antes dele existir, alguém precisava entender de onde os dados vêm, como são
gerados, quais regras de negócio os impactam, quais problemas de qualidade eles
carregam e como tudo isso pode ser organizado de forma confiável e escalável.

### Página 4

Data Prepare

 Além disso, os dados raramente chegam prontos para uso. Eles estão
espalhados em diferentes sistemas, formatos e tecnologias, exigindo que a pessoa
cientista de dados saiba consultar, integrar, transformar e validar informações de
maneira eficiente. Isso envolve dominar bancos de dados relacionais, compreender
quando e por que usar soluções NoSQL, lidar com grandes volumes de dados e
trabalhar com processamento distribuído.
 Outro ponto fundamental é a escala. Soluções que funcionam em um
notebook local muitas vezes não sobrevivem quando aplicadas a ambientes
corporativos, com milhões de registros, dados em tempo real e restrições de custo.
Entender arquitetura de dados, pipelines de ETL/ELT e ambientes de Cloud permite
que você construa soluções que não apenas funcionam, mas que funcionam de
forma sustentável ao longo do tempo.
 Nessa fase, você vai aprender disciplinas como:
 Arquitetura de Big Data:  você aprende a pensar estrategicamente sobre
onde os dados devem viver, como eles chegam até você e como escalam ao longo
do tempo. Entender Data Lake, Data Warehouse e conceitos como Data Mesh te tira
da posição de “consumidor passivo” de dados e te coloca como alguém capaz de
dialogar com engenheiros, arquitetos e times de negócio. Spark e processamento
distribuído entram exatamente aqui: quando os dados não cabem mais em uma
máquina, você precisa saber como pensar distribuído.
 Banco de dados relacionais para cientistas de dados:  Já os bancos de
dados relacionais seguem sendo uma das ferramentas mais importantes da área.
SQL avançado, agregações, subqueries, índices e partições não são apenas
detalhes técnicos, são o que separa uma análise lenta e frágil de uma análise
eficiente e confiável. Um cientista de dados que domina SQL consegue explorar
hipóteses mais rápido, validar ideias com agilidade e entender profundamente a
estrutura dos dados com os quais trabalha.
 NoSQL para ciência de dados:  Quando avançamos para NoSQL, o jogo
muda. Aqui você aprende que nem todo dado cabe em tabelas. Modelos chave -
valor, documentos, colunas e grafos ampliam seu repertório para lidar com logs,
eventos, dados semi -estruturados e aplicações modernas. A introdução aos bancos
vetoriais conecta diretamente essa fase com machine learning, IA generativa e

### Página 5

Data Prepare

sistemas de recomendação, mostrando como a forma de armazenar dados
influencia diretamente o tipo de solução que você consegue construir.
 ETL Pipelines : Os pipelines de ETL/ELT são, talvez, o ponto mais crítico
dessa fase. Eles representam a ponte entre o dado bruto e o dado pronto para
análise. Aqui você aprende a integrar múltiplas fontes, lidar com dados em tempo
real, trabalhar com ferramentas como Kafka e operar em ambientes de Cloud. Mais
do que isso: você passa a entender o custo da decisão técnica, explorando
conceitos de FinOps para equilibrar performance, escalabilidade e orçamento (algo
cada vez mais valorizado no mercado).
 Dentro do CRISP -DM, essa fase sustenta diretamente as etapas de Data
Understanding e Data Preparation, que são a base de todo o ciclo analítico. É aqui
que você:
● Entende a origem dos dados,
● Avalia sua qualidade,
● Identifica limitações,
● Realiza transformações,
● Integra diferentes fontes,
● Prepara o terreno para a modelagem.
 Sem essa base sólida, a fase de Modeling vira tentativa e erro, a Evaluation
perde confiabilidade e o Deployment se torna frágil ou inviável. Em outras palavras:
dados mal preparados comprometem todo o projeto, independentemente do quão
sofisticado seja o algoritmo.
 Aproveite para perguntar, explorar, errar e entender profundamente o “por
trás” dos dados. É esse conhecimento que vai sustentar tudo o que vem depois.
Espero que você aproveite muito essa jornada e aprenda mais sobre o mundo da
engenharia de dados nessa fase tão importante.

### Página 6

Data Prepare
