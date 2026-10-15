# Consultas em NoSQL: operadores, filtros e agregações

**NoSQL para Ciência de Dados** · Aula 3 · Fase 2 — Data Prepare

Consultas, filtros e pipelines de agregação em bancos NoSQL.

**Tópicos:** `operadores` · `filtros` · `agregações` · `MongoDB`

📄 [PDF da aula](./aula_03_consultas_em_nosql_operadores_filtros_e_agregacoes.pdf)

---

## Conteúdo

### Página 1

Consultas em NoSQL: operadores, filtros e agregações

CONSULTAS EM NOSQL:
OPERADORES, FILTROS
E AGREGAÇÕES

### Página 2

Consultas em NoSQL: operadores, filtros e agregações

### Página 3

Consultas em NoSQL: operadores, filtros e agregações

À medida que os dados se tornam cada vez mais volumosos, distribuídos e
heterogêneos, as consultas em bancos NoSQL deixam de ser apenas um mecanismo
de recuperação e passam a ocupar um papel estratégico na geração de valor para o
negócio. Operadores de consulta, filtros avançados e agregações complexas evoluem
para atender cenários de tempo real , alta concorrência  e análises analíticas
diretamente sobre dados operacionais, reduzindo a dependência de pipelines longos
e custosos.
Nesta aula,  exploraremos como diferentes tecnologias NoSQL — como
MongoDB, Apache Cassandra e Redis — estão ampliando suas capacidades de
consulta com agregações distribuídas , indexação inteligente , consultas vetoriais  e
integração nativa com analytics e machine learning. A proposta é conectar a teoria às
práticas que o mercado já adota, te preparando para desenhar consultas mais
eficientes, escaláveis e alinhadas às arquiteturas modernas de dados.

### Página 4

Consultas em NoSQL: operadores, filtros e agregações

Consultas em NoSQL: operadores, filtros e agregações
Você irá acessar ambientes reais de bancos NoSQL  e executar consultas
utilizando operadores, filtros e agregações conforme o modelo de dados. O objetivo é
consolidar o entendimento de que cada modelo NoSQL responde perguntas
diferentes, e que a forma de consulta está diretamente ligada à sua arquitetura e à
modelagem adotada.
A atividade está organizada por modelo NoSQL. Em cada um deles, você
primeiro acessará o ambiente do banco e, em seguida, executará os comandos
propostos.
Banco Chave-Valor – Redis
Acesso ao ambiente
Utilizaremos o serviço gerenciado do Redis Cloud . Link de acesso:
https://redis.io/cloud/
Passo a passo para acesso:
• Acesse o site do Redis Cloud pelo link indicado;
• Crie uma conta gratuita;
• No painel principal, crie um banco utilizando o plano gratuito;
• Após a criação, clique em Open Redis Insight (Web);
• Selecione o banco criado e acesse o CLI disponível na interface.

Execução dos comandos
Inserção de dados (Hash)
HSET cliente:1001 nome "Ana" cidade "SP" idade 34
HSET cliente:1002 nome "Carlos" cidade "RJ" idade 41
Código-fonte 1 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

### Página 5

Consultas em NoSQL: operadores, filtros e agregações

Consulta direta por chave
HGETALL cliente:1001
Código-fonte 2 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Simulação de filtro com estrutura auxiliar (Set)
SADD clientes:cidade:SP 1001
SADD clientes:cidade:RJ 1002
SMEMBERS clientes:cidade:SP
Código-fonte 3 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Banco Orientado a Documentos – MongoDB
Acesso ao ambiente
Utilizaremos o MongoDB Atlas . Link de acesso:
https://www.mongodb.com/atlas
Passo a passo para acesso:
• Acesse o MongoDB Atlas pelo link indicado;
• Crie uma conta gratuita;
• Crie um cluster do tipo Free Tier (M0);
• Após o provisionamento, clique em Browse Collections;
• Crie um banco chamado loja e uma coleção chamada pedidos.

Execução dos comandos

### Página 6

Consultas em NoSQL: operadores, filtros e agregações

Inserção de documentos

{
  "cliente": "Ana",
  "status": "FINALIZADO",
  "valor": 300
}
Código-fonte 4 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Consulta com filtro
{ "status": "FINALIZADO" }
Código-fonte 5 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Agregação com pipeline
[
  { "$match": { "status": "FINALIZADO" } },
  {
    "$group": {
      "_id": "$cliente",

### Página 7

Consultas em NoSQL: operadores, filtros e agregações

      "total_gasto": { "$sum": "$valor" }
    }
  }
]
Código-fonte 6 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Banco Orientado a Grafos – Neo4j
Acesso ao ambiente
Utilizaremos o Neo4j Aura . Link de acesso:
https://neo4j.com/cloud/aura/

Passo a passo para acesso
• Acesse o Neo4j Aura pelo link indicado;
• Crie uma conta gratuita;
• Crie uma instância Aura Free;
• Após a criação, clique em Open with Neo4j Browser;
• Aguarde a abertura do console Cypher no navegador.
Execução dos comandos
Criação de nós e relacionamentos
CREATE (a:Cliente {nome:"Ana"})
CREATE (c:Cliente {nome:"Carlos"})
CREATE (p:Produto {nome:"Notebook"})

### Página 8

Consultas em NoSQL: operadores, filtros e agregações

CREATE (a)-[:COMPROU]->(p)
CREATE (c)-[:COMPROU]->(:Produto {nome:"Mouse"})
Código-fonte 7 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Consulta de relacionamento
MATCH (c:Cliente)-[:COMPROU]->(p:Produto)
RETURN c.nome, p.nome;
Código-fonte 8 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Banco Colunar – Cassandra
Acesso ao ambiente
Utilizaremos o DataStax Astra DB . Link de acesso:
https://www.datastax.com/products/datastax-astra-db
Passo a passo para acesso
• Acesse o Astra DB pelo link indicado;
• Crie uma conta gratuita;
• Crie um banco do tipo Serverless (Cassandra);
• Após a criação, clique em CQL Console para abrir o editor no navegador;
• Execução dos comandos.

Criação da estrutura
CREATE KEYSPACE loja

### Página 9

Consultas em NoSQL: operadores, filtros e agregações

WITH replication =
{'class':'SimpleStrategy','replication_factor':1};

USE loja;

CREATE TABLE vendas (
  cliente TEXT,
  data DATE,
  valor DECIMAL,
  PRIMARY KEY (cliente, data)
);
Código-fonte 9 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Inserção e consulta
INSERT INTO vendas (cliente, data, valor)
VALUES ('Ana', '2025-03-01', 300);

SELECT * FROM vendas WHERE cliente = 'Ana';
Código-fonte 10 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

### Página 10

Consultas em NoSQL: operadores, filtros e agregações

Neste hands on, você acessou diferentes bancos NoSQL e executou consultas
práticas, observando como operadores, filtros e agregações  se comportam de
acordo com cada modelo de dados. A atividade reforça que a escolha do banco
NoSQL é uma decisão arquitetural , diretamente ligada aos padrões de acesso, à
escalabilidade e aos objetivos analíticos da solução — uma competência essencial
para atuação em projetos avançados de dados.

### Página 11

Consultas em NoSQL: operadores, filtros e agregações

Modelagem de Dados em NoSQL: Conceitos, Estratégias e Exemplos
Nesta seção, aprofundamos os conceitos centrais da aula Consultas em
NoSQL: operadores, filtros e agregações, conectando explicações conceituais a
exemplos práticos  semelhantes aos trabalhados no hands on. O objetivo é
consolidar o entendimento de que, em NoSQL, a forma de consultar dados é
consequência direta do modelo de dados escolhido , impactando desempenho,
escalabilidade e decisões arquiteturais.

Consultas em NoSQL: o papel dos operadores, filtros e agregações
Em bancos relacionais, operadores, filtros e agregações são abstraídos por
uma linguagem única (SQL), aplicável a qualquer tabela. Já nos bancos NoSQL,
esses mecanismos não são padronizados, pois cada modelo foi criado para resolver
problemas específicos de armazenamento e acesso.
Isso significa que:
• Operadores definem como comparar ou navegar pelos dados;
• Filtros determinam quais dados são relevantes para a consulta;
• Agregações sintetizam informações a partir de múltiplos registros.
Em NoSQL, esses três elementos não existem de forma genérica , mas sim
adaptados ao modelo de dados, o que exige um raciocínio diferente do tradicional.

Modelo Chave-Valor: operadores mínimos e filtros antecipados
No modelo chave-valor, representado por soluções como o Redis, a consulta
é baseada quase exclusivamente no operador de acesso à chave . Não existem
operadores de comparação nem filtros condicionais aplicados no momento da leitura.
Exemplo prático
Pergunta: Quais clientes pertencem à cidade de São Paulo?

### Página 12

Consultas em NoSQL: operadores, filtros e agregações

Em um banco chave -valor, essa pergunta só pode ser respondida se a
modelagem já tiver criado uma estrutura específica para isso, como um conjunto de
clientes por cidade.
SADD clientes:cidade:SP 1001
SADD clientes:cidade:SP 1003
Código-fonte 11 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Consulta:
SMEMBERS clientes:cidade:SP
Código-fonte 12 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Nesse caso:
• O filtro (cidade) foi definido na modelagem;
• A consulta apenas acessa o conjunto já preparado;
• Não há agregação dinâmica, apenas leitura direta.
Esse modelo é ideal para cenários como cache, sessões, contadores e
rankings, onde previsibilidade e latência mínima  são mais importantes que
flexibilidade.

Modelo Orientado a Documentos: filtros declarativos e agregações ricas
Nos bancos orientados a documentos, como o MongoDB, os dados são
armazenados como documentos semiestruturados, permitindo o uso de operadores
de comparação, operadores lógicos e filtros compostos.
Exemplo prático de filtro:

### Página 13

Consultas em NoSQL: operadores, filtros e agregações

Pergunta: Quais pedidos estão finalizados e possuem valor acima de 200?
db.pedidos.find({
  status: "FINALIZADO",
  valor: { $gt: 200 }
})
Código-fonte 13 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

 Aqui, o filtro é aplicado diretamente sobre os campos do documento, sem
necessidade de modelagem prévia específica para essa pergunta.
Exemplo prático de agregação
Pergunta: quanto cada cliente gastou no total?
db.pedidos.aggregate([
  { $match: { status: "FINALIZADO" } },
  {
    $group: {
      _id: "$cliente",
      total_gasto: { $sum: "$valor" }
    }
  }
])
Código-fonte 14 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

### Página 14

Consultas em NoSQL: operadores, filtros e agregações

Nesse pipeline:
• $match atua como filtro;
• $group realiza a agregação;
• O resultado já retorna uma visão consolidada.
Esse modelo é amplamente utilizado em APIs, microsserviços, logs e eventos,
pois combina flexibilidade estrutural com capacidade analítica.

Modelo Orientado a Grafos: filtros por padrão de relacionamento
Nos bancos orientados a grafos, como o Neo4j, filtros não são baseados
apenas em valores, mas em padrões de relacionamento entre entidades.
Exemplo prático
Pergunta: quais clientes compraram o mesmo produto que Ana?
MATCH (a:Cliente {nome:"Ana"}) -[:COMPROU]->(p)<-
[:COMPROU]-(c:Cliente)
RETURN c.nome
Código-fonte 15 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Nesse caso:
• O “filtro” é o padrão de navegação no grafo;
• A consulta percorre relacionamentos, não tabelas;
• Não há joins explícitos, pois as relações já fazem parte do modelo.

Agregação em grafos
Pergunta: quantos produtos cada cliente comprou?
MATCH (c:Cliente)-[:COMPROU]->(p)

### Página 15

Consultas em NoSQL: operadores, filtros e agregações

RETURN c.nome, COUNT(p) AS total_compras
Código-fonte 16 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Esse modelo é especialmente eficiente para redes sociais, recomendações,
fraude e análise de dependências.

Modelo Colunar: filtros restritos e agregações previsíveis
Nos bancos colunares distribuídos, como o Apache Cassandra , filtros e
agregações são fortemente condicionados à chave de partição, definida no momento
da modelagem.
Exemplo prático de filtro
Pergunta: quais vendas pertencem à cliente Ana?
SELECT *
FROM vendas
WHERE cliente = 'Ana';
Código-fonte 17 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Essa consulta só é válida porque cliente foi definido como chave de partição.
Exemplo prático de agregação
SELECT cliente, SUM(valor)
FROM vendas
WHERE cliente = 'Ana';

### Página 16

Consultas em NoSQL: operadores, filtros e agregações

Código-fonte 18 – Exemplo de linha de comando
Fonte: Elaborado pelo autor (2026)

Nesse modelo:
• Não é possível filtrar livremente qualquer coluna;
• As agregações são eficientes dentro da partição;
• O desempenho é previsível mesmo em grandes volumes.
Esse tipo de banco é indicado para séries temporais, eventos e sistemas que
exigem alta disponibilidade e escalabilidade horizontal.

Comparando os modelos a partir das consultas
Observando os exemplos práticos, fica claro que cada modelo NoSQL
responde melhor a um tipo específico de pergunta:
Chave-Valor → acesso direto e resultados previamente preparados.
Documentos → filtros flexíveis e agregações dinâmicas.
Grafos → exploração eficiente de relacionamentos.
Colunar → consultas previsíveis em larga escala.
Essa diversidade explica a adoção de arquiteturas poliglotas , nas quais
diferentes bancos NoSQL coexistem para atender necessidades distintas dentro do
mesmo sistema.

Conectando teoria e prática
Os exemplos apresentados nesta aula mostram que consultar dados em
NoSQL é uma decisão arquitetural , e não apenas sintática. Entender como
operadores, filtros e agregações funcionam em cada modelo permite projetar soluções
mais eficientes, escaláveis e alinhadas aos objetivos do negócio.
Ao dominar esses conceitos, você estará mais preparado(a) para atuar em
projetos de engenharia de dados, arquitetura de sistemas e analytics em escala,

### Página 17

Consultas em NoSQL: operadores, filtros e agregações

escolhendo conscientemente o modelo NoSQL mais adequado para cada tipo de
pergunta que o sistema precisa responder.

### Página 18

Consultas em NoSQL: operadores, filtros e agregações

O uso de bancos de dados NoSQL consolidou -se no mercado como uma
resposta direta às limitações dos modelos relacionais tradicionais diante de cenários
que exigem alta escalabilidade, baixa latência e flexibilidade de esquema .
Atualmente, organizações de diferentes setores adotam bancos NoSQL não como
substitutos absolutos do SQL, mas como componentes complementares em
arquiteturas poliglotas , nas quais cada tecnologia é escolhida de acordo com o
padrão de consulta e o tipo de dado envolvido.
Do ponto de vista de mercado, observa-se uma convivência madura entre SQL
e NoSQL. Relatórios e análises recentes indicam que sistemas modernos utilizam
bancos relacionais para dados altamente estruturados e transacionais, enquanto
bancos NoSQL são emprega dos para consultas em larga escala, dados
semiestruturados, eventos, logs, grafos de relacionamento e workloads em tempo
real.
Uma análise atual sobre esse cenário pode ser encontrada no artigo “SQL vs
NoSQL em 2025: Quais Tecnologias Vão Dominar os Bancos de Dados?”, disponível
em: https://medium.com/ai-analytics-diaries/sql-vs-nosql-in-2025-what-you-should-
really-be-using-a21a7c2bd73c
No contexto de consultas, o mercado tem valorizado soluções NoSQL que
oferecem mecanismos cada vez mais expressivos de filtros e agregações, sem
comprometer a escalabilidade. Bancos orientados a documentos, como o MongoDB,
evoluíram significativamente seus pipelines de agregação, permitindo análises
diretamente sobre dados operacionais. Esse movimento reduz a necessidade de
múltiplas camadas de processamento em cenários de média escala e acelera a
geração de insights em aplicações digitais, APIs e plataformas de dados.
Em paralelo, bancos chave-valor, como o Redis, continuam sendo
amplamente utilizados em sistemas que exigem respostas em tempo real. No
mercado, seu uso está fortemente associado a caches distribuídos, controle de
sessões, contadores e rankings. Nesses cenários, a ausência de filtros e agregações
dinâmicas não é vista como limitação, mas como uma decisão arquitetural que garante
previsibilidade e desempenho extremo.

### Página 19

Consultas em NoSQL: operadores, filtros e agregações

Os bancos orientados a grafos , com destaque para o Neo4j, ganharam
relevância em casos onde as consultas envolvem múltiplos níveis de relacionamento.
Empresas que atuam com redes sociais, sistemas de recomendação, prevenção a
fraudes e grafos de conhecimento utilizam esse modelo para responder perguntas que
seriam complexas ou ineficientes em bancos relacionais. O diferencial competitivo
está na capacidade de realizar filtros baseados em padrões de relacionamento e
agregações sobre conexões, algo alinhado à s demandas atuais de análise de
comportamento e contexto.
Já os bancos colunares distribuídos , como o Apache Cassandra ,
permanecem como referência em cenários de grande volume de dados e alta taxa de
escrita. No mercado, são amplamente adotados em sistemas de telemetria, Internet
das Coisas, eventos e séries temporais. A limitação deliberada de filtros e agregações
fora da chave de partição é compreendida como um trade-off necessário para garantir
disponibilidade, tolerância a falhas e escalabilidade horizontal.
Do ponto de vista de tendências, três movimentos se destacam. O primeiro é
a consolidação de bancos NoSQL como serviços gerenciados em nuvem, reduzindo
o esforço operacional e permitindo que equipes foquem mais em modelagem e
consultas do que em infraestrutura. O segundo é a integração cada vez maior entre
bancos NoSQL e ferramentas analíticas, incluindo processamento em tempo real e
machine learning. O terceiro é o fortalecimento do ensino e da pesquisa acadêmica
sobre NoSQL, com estudos comparativos que a nalisam desempenho, padrões de
consulta e adequação dos modelos a diferentes tipos de aplicações.
Um panorama sobre tendências e inovações em bancos de dados pode ser
consultado no artigo “O Futuro dos Bancos de Dados: Tendências e Inovações ”,
disponível em: https://horusinfo.com.br/o-futuro-dos-bancos-de-dados-tendencias-e-
inovacoes/
Do ponto de vista acadêmico e comparativo, estudos têm demonstrado que
diferentes bancos NoSQL apresentam vantagens claras dependendo do tipo de
consulta e do padrão de acesso. Um exemplo é o artigo “NoSQL Databases in Real-
Time Systems: Performance Analysis ”, que compara Redis, MongoDB, Cassandra e
Neo4j em cenários distintos de uso, disponível em:
https://ijdim.com/journal/index.php/ijdim/article/download/272/246/621

### Página 20

Consultas em NoSQL: operadores, filtros e agregações

Outro estudo relevante é “Comparative Study on Oracle, Neo4J, Cassandra,
Redis and MongoDB ”, que analisa características, desempenho e adequação de
bancos relacionais e NoSQL para diferentes aplicações, disponível em:
https://www.researchgate.net/publication/388444167_Comparative_Study_on_Oracl
e_Neo4J_Cassandra_Redis_and_MongoDB
Além de artigos e estudos, alguns livros tornaram-se referências fundamentais
para compreender o uso de NoSQL no mercado. Designing Data -Intensive
Applications, de Martin Kleppmann, aprofunda os princípios de sistemas distribuídos
e a escolha entre diferentes modelos de dados. NoSQL Distilled , de Pramod J.
Sadalage e Martin Fowler, oferece uma visão prática sobre quando e por que utilizar
bancos NoSQL. Já Graph Databases, de Ian Robinson, Jim Webber e Emil Eifrem,
explora em profundidade a modelagem e as consultas em bancos orientados a grafos.
Em síntese, o mercado demonstra que consultas em NoSQL são uma
decisão estratégica, diretamente ligada ao tipo de dado, ao padrão de acesso e aos
requisitos de escala. A compreensão de operadores, filtros e agregações em cada
modelo não apenas amplia a capacidade técnica do(a) profissional, mas também o
prepara para tomar decisões arqui teturais alinhadas às demandas reais das
organizações modernas.

### Página 21

Consultas em NoSQL: operadores, filtros e agregações

Nesta aula, você compreendeu como consultas em bancos NoSQL  são
diretamente influenciadas pelo modelo de dados adotado , e por que operadores,
filtros e agregações não podem ser tratados de forma padronizada, como ocorre nos
bancos relacionais tradicionais. A partir dessa perspectiva, ficou evidente que
consultar dados em NoSQL é, acima de tudo, uma decisão arquitetural , e não
apenas a aplicação de comandos específicos.
Você analisou, de forma comparativa, como os principais modelos NoSQL —
chave-valor, documentos, grafos e colunar  — lidam com consultas. Nos bancos
chave-valor, o foco está no acesso direto à chave e na previsibilidade, com filtros e
agregações antecipados na modelagem. Nos bancos orientados a documentos,
explorou filtros expressivos e pipelines de agregação capazes de gerar visões
analíticas diretamente sobre dados operacionais. Nos bancos orientados a grafos,
entendeu como as consultas são baseadas em pad rões de relacionamento e
travessias, permitindo responder perguntas complexas sobre conexões. Já nos
bancos colunares, observou como a restrição dos filtros à chave de partição garante
desempenho previsível e escalabilidade em ambientes distribuídos.
Por meio dos exemplos práticos e das discussões conceituais, você consolidou
a compreensão de que não existe um modelo NoSQL superior , mas sim modelos
mais adequados a determinados tipos de perguntas e padrões de acesso. Esse
entendimento é fundamental para projetar soluções modernas de dados, capazes de
equilibrar flexibilidade, desempenho e escalabilidade de acordo com as necessidades
reais do negócio.

### Página 22

Consultas em NoSQL: operadores, filtros e agregações

APACHE CASSANDRA. Cassandra Query Language (CQL) documentation.
Disponível em: https://cassandra.apache.org/doc/latest/cassandra/cql/.
Acesso em: 27 mar. 2026.
KLEPPMANN, M. Designing data-intensive applications. Sebastopol: O’Reilly Media,
2017.
MONGODB. Aggregation framework documentation.
Disponível em:  https://www.mongodb.com/docs/manual/aggregation/.
Acesso em: 27 mar. 2026.
NEO4J. Cypher query language manual.
Disponível em:  https://neo4j.com/docs/cypher-manual/current/.
Acesso em: 27 mar. 2026.
REDIS. Redis data types documentation.
Disponível em: https://redis.io/docs/data -types/.
Acesso em: 27 mar. 2026.
ROBINSON, I.; WEBBER, J.; EIFREM, E. Graph databases.  2. ed. Sebastopol:
O’Reilly Media, 2015.
SADALAGE, P. J.; FOWLER, M. NoSQL distilled: a brief guide to the emerging world
of polyglot persistence. Boston: Addison-Wesley, 2013.

### Página 23

Consultas em NoSQL: operadores, filtros e agregações

PALAVRAS-CHAVE
Arquitetura De Dados, Consultas Distribuídas, Escalabilidade De Sistemas.

### Página 24

Consultas em NoSQL: operadores, filtros e agregações
