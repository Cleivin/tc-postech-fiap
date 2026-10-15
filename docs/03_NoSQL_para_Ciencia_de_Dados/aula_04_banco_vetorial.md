# Banco Vetorial

**NoSQL para Ciência de Dados** · Aula 4 · Fase 2 — Data Prepare

Bancos vetoriais, embeddings e busca por similaridade para IA generativa/RAG.

**Tópicos:** `embeddings` · `similaridade` · `RAG` · `vector DB`

📄 [PDF da aula](./aula_04_banco_vetorial.pdf)

---

## Conteúdo

### Página 1

Banco Vetorial

BANCO VETORIAL

### Página 2

Banco Vetorial

### Página 3

Banco Vetorial

Se até aqui você trabalhou com dados estruturados, consultas exatas e
modelos bem definidos, prepare -se para dar um salto conceitual. Bancos Vetoriais
surgem como resposta direta a um mundo onde dados não estruturados — textos,
imagens, áudios e embeddings gerados por modelos de IA — passam a ser o principal
ativo. Em vez de buscar “igualdade”, esses bancos permitem encontrar similaridade,
abrindo espaço para perguntas muito mais próximas da forma como humanos pensam
e se comunicam.
Você vai entender como Bancos Vetoriais se conectam ao avanço da
Inteligência Artificial, especialmente em aplicações como busca semântica,
recomendação inteligente e arquiteturas modernas de IA generativa. Vamos explorar
por que esse tipo de banco deixou de s er tendência para se tornar peça central em
soluções data -driven, e como ele muda completamente a forma de armazenar,
consultar e extrair valor dos dados. Aqui começa a transição do query tradicional para
o pensar por proximidade.

### Página 4

Banco Vetorial

Neste hands on, você vai construir um mini pipeline de Banco Vetorial usando
Python, indo da criação dos embeddings até a busca por similaridade semântica. O
objetivo é entender o que acontece em cada etapa, não apenas rodar código.

Preparando o ambiente
Vamos assumir um ambiente local ou notebook (Jupyter/Colab). As bibliotecas
abaixo são amplamente usadas em projetos reais.
pip install sentence-transformers faiss-cpu pandas

Aqui usamos:
• sentence-transformers para gerar embeddings de texto;
• faiss para indexação e busca vetorial;
• pandas apenas para organizar os dados.

Criando um conjunto de dados simples
Imagine que você tem pequenas descrições, como FAQs, produtos ou
documentos internos.
import pandas as pd

dados = [
    "Banco vetorial permite busca por similaridade semântica",
    "SQL é usado para consultas estruturadas em bancos
relacionais",
    "Embeddings transformam texto em vetores numéricos",
    "Bancos NoSQL escalam grandes volumes de dados",

### Página 5

Banco Vetorial

    "Busca semântica vai além da correspondência exata de
palavras"
]

df = pd.DataFrame(dados, columns=["texto"])
df
Código fonte1 – Exemplo de código fonte python
Fonte: Elaborado pelo autor (2026)
Ponto-chave: até aqui, os dados ainda são texto puro. Bancos Vetoriais
não operam diretamente sobre strings, mas sobre vetores.

Gerando embeddings (o coração do processo)
Agora vamos transformar cada texto em um vetor numérico usando um modelo
pré-treinado.
from sentence_transformers import SentenceTransformer
modelo = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = modelo.encode(df["texto"].tolist())
Código fonte2 – Exemplo de código fonte python
Fonte: Elaborado pelo autor (2026)
Cada linha agora virou um vetor de centenas de dimensões.
Esses vetores posicionam os textos em um espaço semântico, onde textos parecidos
ficam próximos.

Criando o índice vetorial
Aqui entra o papel do Banco Vetorial. Vamos usar FAISS, muito comum em
protótipos e sistemas de recomendação.

### Página 6

Banco Vetorial

import faiss
import numpy as np

dimensao = embeddings.shape[1]
index = faiss.IndexFlatL2(dimensao)

index.add(np.array(embeddings))
print("Total de vetores indexados:", index.ntotal)
Código fonte3 – Exemplo de código fonte python
Fonte: Elaborado pelo autor (2026)
Reflexão importante:
• Não há tabelas;
• Não há chaves primárias;
• Há apenas vetores e uma métrica de distância.

Realizando uma busca semântica
Agora vem a mágica. Vamos buscar textos semanticamente parecidos, mesmo
sem repetir as mesmas palavras.
consulta = "Como funciona pesquisa por significado em textos?"
consulta_embedding = modelo.encode([consulta])

distancias, indices = index.search(
    np.array(consulta_embedding),
    k=2
)

### Página 7

Banco Vetorial

Código fonte4 – Exemplo de código fonte python
Fonte: Elaborado pelo autor (2026)
Interpretando o resultado
for i in indices[0]:
    print("-", df.iloc[i]["texto"])
Código fonte5 – Exemplo de código fonte python
Fonte: Elaborado pelo autor (2026)
Você deve notar que os textos retornados fazem sentido conceitual, mesmo
que não tenham as mesmas palavras da consulta.
Aqui está o grande diferencial do Banco Vetorial: a busca é feita por
proximidade semântica, não por igualdade.

Conectando com o mundo real
Esse mesmo fluxo é usado em:
• Buscas inteligentes em portais corporativos;
• Sistemas de recomendação;
• Chatbots com recuperação de contexto;
• Arquiteturas de IA generativa com RAG (Retrieval -Augmented
Generation).
Em ambientes produtivos, o FAISS pode ser substituído por soluções
gerenciadas como Pinecone, Weaviate ou Chroma, mas o conceito central é
exatamente o mesmo.

### Página 8

Banco Vetorial

Os Bancos Vetoriais surgem como resposta direta à transformação do tipo de
dado que as organizações passaram a produzir e consumir. Em um cenário dominado
por textos livres, imagens, áudios, vídeos e informações contextuais, torna -se cada
vez mais limitada  a capacidade dos bancos de dados tradicionais de representar e
consultar significado. Bancos Vetoriais partem de um princípio distinto: dados não
precisam ser apenas armazenados, mas compreendidos matematicamente.
Diferentemente de modelos baseados em igualdade ou ordenação, Bancos
Vetoriais operam sobre proximidade semântica. Isso significa que o valor de um
dado não está apenas em seu conteúdo literal, mas na relação que ele mantém com
outros dados. Essa mudança de paradigma impacta diretamente a forma como
sistemas de busca, recomendação, análise de contexto e Inteligência Artificial são
construídos.

Figura 1 – Representação de dados
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)
Nesse contexto, o dado deixa de ser visto como um registro isolado e passa a
ser interpretado como um ponto em um espaço matemático de alta dimensionalidade.
Quanto mais próximos dois pontos estão nesse espaço, maior é a similaridade

### Página 9

Banco Vetorial

semântica entre os dados que eles representam. Essa ideia é fundamental para
entender por que Bancos Vetoriais são especialmente adequados para problemas
onde o significado é subjetivo, contextual e aproximado.

Embeddings: a base matemática do significado
O conceito de embedding é o alicerce técnico dos Bancos Vetoriais. Um
embedding é uma representação vetorial densa, geralmente gerada por modelos de
aprendizado profundo, capaz de capturar relações semânticas complexas presentes
nos dados. Em vez de trabalhar com palavras, pixel s ou sons de forma direta, esses
modelos aprendem a projetar informações em vetores numéricos que preservam
significado.
No caso de textos, embeddings conseguem representar sinônimos, intenções
e contextos semelhantes de forma próxima no espaço vetorial, mesmo quando as
palavras utilizadas são diferentes. Esse comportamento é resultado do treinamento
desses modelos em grande s volumes de dados, onde padrões estatísticos e
semânticos são aprendidos de forma distribuída ao longo das dimensões do vetor.

Figura 2 – Embeddings
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)

### Página 10

Banco Vetorial

Uma característica importante dos embeddings é que nenhuma dimensão
isolada possui significado explícito. O sentido emerge da combinação de todas as
dimensões, o que torna essas representações extremamente expressivas, porém
menos interpretáveis. Essa opac idade exige novos cuidados em projetos de dados,
especialmente quando embeddings passam a representar documentos sensíveis ou
decisões críticas de negócio.
Além disso, embeddings permitem uma abordagem multimodal. Textos,
imagens e áudios podem ser convertidos para o mesmo espaço vetorial, possibilitando
consultas cruzadas, como buscar imagens a partir de descrições textuais ou recuperar
documentos com base em perguntas feitas em linguagem natural.

Métricas de similaridade e o conceito de proximidade
Uma vez que os dados são representados como vetores, o próximo desafio é
medir quão próximos eles estão entre si. Bancos Vetoriais utilizam métricas de
similaridade, que substituem os operadores tradicionais de igualdade utilizados em
SQL. Entre as métricas mais comuns estão a similaridade do cosseno, a distância
euclidiana e o produto interno.
A similaridade do cosseno mede o ângulo entre dois vetores e é amplamente
utilizada em aplicações de processamento de linguagem natural, pois foca no
alinhamento semântico entre os dados. Já a distância euclidiana considera a distância
geométrica direta no espaço vetorial, sendo útil quando a magnitude do vetor também
carrega informação relevante. A escolha da métrica impacta diretamente a experiência
do usuário e a qualidade percebida dos resultados.

### Página 11

Banco Vetorial

Figura 3 – Comparação entre métricas de similaridade em espaços vetoriais
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)
Esse modelo de busca introduz um novo paradigma: os resultados deixam de
ser exatos e passam a ser ordenados por relevância. Isso exige uma mudança de
mentalidade tanto no desenvolvimento de sistemas quanto na forma como usuários
interagem com dados, aceitando que respostas são probabilísticas e contextuais.
Indexação vetorial e busca aproximada
Buscar similaridade em espaços de alta dimensionalidade é
computacionalmente custoso. Uma busca exaustiva, comparando cada vetor com
todos os outros, rapidamente se torna inviável à medida que o volume de dados
cresce. Para resolver esse problema, Bancos V etoriais utilizam técnicas conhecidas
como Approximate Nearest Neighbors (ANN).
Essas técnicas constroem estruturas de índice que permitem localizar vetores
próximos de forma eficiente, sacrificando uma pequena parcela de precisão em troca
de ganhos significativos de desempenho. Métodos como IVF particionam o espaço
vetorial, enquanto  abordagens baseadas em grafos, como HNSW, criam redes de
conexões entre vetores semanticamente próximos.

### Página 12

Banco Vetorial

Figura 4 – Estruturas de indexação vetorial
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)
Bibliotecas como FAISS tornaram essas técnicas acessíveis para pesquisa e
indústria, enquanto soluções gerenciadas como Pinecone, Weaviate e Chroma
abstraem a complexidade operacional, permitindo escalar Bancos Vetoriais em
ambientes produtivos.
Bancos Vetoriais e IA Generativa (RAG)
O crescimento recente dos Bancos Vetoriais está profundamente ligado à
evolução da Inteligência Artificial Generativa. Em arquiteturas modernas,
especialmente no padrão conhecido como Retrieval-Augmented Generation (RAG),
o Banco Vetorial atua como uma memória semântica externa. Antes de gerar uma
resposta, o modelo consulta o Banco Vetorial para recuperar informações relevantes,
que são então utilizadas como contexto.

### Página 13

Banco Vetorial

Figura 5 – Arquitetura Retrieval-Augmented Generation (RAG)
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)
Esse padrão reduz significativamente problemas como alucinação e falta de
contextualização, permitindo que modelos respondam com base em dados
atualizados e específicos da organização. Assim, o Banco Vetorial deixa de ser
apenas um mecanismo de busca e pas sa a desempenhar um papel estratégico na
arquitetura de dados corporativa.
Convivência com bancos tradicionais e persistência poliglota
Bancos Vetoriais não substituem bancos relacionais ou NoSQL. Eles fazem
parte de uma arquitetura de persistência poliglota, onde cada tecnologia é utilizada
de acordo com sua vocação. Bancos relacionais continuam sendo essenciais para
transações e integridade, enquanto Bancos Vetoriais lidam com contexto, similaridade
e significado.

### Página 14

Banco Vetorial

Figura 6 – Arquitetura poliglota
Fonte: Elaborado pelo autor via Inteligência Artificial (2026)
Essa convivência exige novos cuidados arquiteturais, como sincronização entre
dados estruturados e embeddings, além de mecanismos de governança para garantir
segurança, qualidade semântica e conformidade regulatória.
Desafios, governança e qualidade semântica
Apesar de suas vantagens, Bancos Vetoriais introduzem desafios relevantes.
Embeddings podem reproduzir vieses dos dados de treinamento, e sua natureza
opaca dificulta auditorias tradicionais. Além disso, avaliar qualidade deixa de ser
apenas medir performa nce técnica e passa a envolver critérios subjetivos, como
relevância percebida.
Nesse sentido, a adoção de Bancos Vetoriais exige maturidade organizacional,
colaboração entre áreas técnicas e de negócio e uma nova forma de pensar
governança de dados. Mais do que uma inovação tecnológica, eles representam uma
mudança cultural na forma de tratar informação.

### Página 15

Banco Vetorial

A consolidação dos Bancos Vetoriais no mercado está diretamente associada
ao avanço da Inteligência Artificial e, sobretudo, à adoção em larga escala de modelos
de linguagem. O crescimento de aplicações baseadas em busca semântica,
recomendação contextual e IA generativa fez com que organizações passassem a
enxergar o Banco Vetorial como infraestrutura essencial, e não apenas como um
componente experimental.
Esse movimento é bem descrito em materiais introdutórios do próprio mercado,
como o artigo What is a Vector Database? publicado pela Pinecone, que contextualiza
o papel dessas bases como camada fundamental para aplicações orientadas a
significado (https://www.pinecone.io/learn/vector-database/).
Na prática, empresas vêm adotando Bancos Vetoriais como complemento às
suas plataformas analíticas tradicionais. Data Lakes e Data Warehouses continuam
sendo o núcleo da persistência de dados estruturados, enquanto as bases vetoriais
assumem a responsabilidade de lidar com contexto, linguagem natural e similaridade.
Esse desenho arquitetural dialoga diretamente com os princípios apresentados por
Martin Kleppmann em Designing Data -Intensive Applications  (O’Reilly, 2017), obra
amplamente reconhecida por discu tir como diferentes modelos de armazenamento
coexistem em arquiteturas modernas e escaláveis.
Um dos cases mais relevantes do mercado está no uso de Bancos Vetoriais
em arquiteturas de Retrieval-Augmented Generation (RAG) . Nesse padrão,
documentos corporativos são transformados em embeddings e armazenados em uma
base vetorial, que passa a ser consultada antes da geração de respostas por um
modelo de linguagem. Essa abordagem foi formalizada no artigo Retrieval-Augmented
Generation for Knowledge -Intensive NLP Tasks , publicado pela Meta AI, que
demonstra como a recuperação semântica melhora significat ivamente a qualidade e
a confiabilidade das respostas geradas por modelos de NLP
(https://ai.facebook.com/blog/retrieval-augmented-generation-streamlining-the-
creation-of-intelligent-natural-language-processing-models/).
No ecossistema de fornecedores, observa -se uma rápida especialização das
soluções. Plataformas como Pinecone (https://www.pinecone.io), Weaviate

### Página 16

Banco Vetorial

(https://weaviate.io) e Chroma (https://www.trychroma.com) oferecem Bancos
Vetoriais gerenciados, com foco em escalabilidade, baixa latência e integração direta
com frameworks de IA. Em paralelo, soluções open source como FAISS
(https://github.com/facebookresearch/faiss) continuam sendo amplamente utilizadas
em ambientes acadêmicos e corporativos, especialmente em cenários que demandam
maior controle sobre a indexação e a infraestrutura.
Outra tendência clara é a aproximação entre Bancos Vetoriais e práticas
consolidadas de engenharia de machine learning. O livro Designing Machine Learning
Systems, de Saleema Amershi et al. (O’Reilly, 2022), discute como sistemas de ML
em produção exigem pipelines robustos, observabilidade e integração contínua com
dados — contexto no qual Bancos Vetoriais passam a atuar como camada estratégica
para recuperação de conhecimento e contextualização de modelos.
Além disso, cresce o interesse por buscas multimodais , nas quais textos,
imagens e áudios coexistem no mesmo espaço vetorial. Essa tendência amplia
significativamente as possibilidades de negócio, permitindo, por exemplo, pesquisar
imagens a partir de descrições textuais ou recuperar documentos técnicos a partir de
perguntas em linguagem natural. Conteúdos educacionais, como o vídeo Vector
Databases Explained , publicado pelo time do Weaviate no YouTube
(https://www.youtube.com/watch?v=klTvEwg3oJ4), ajudam a visualizar como essas
arquiteturas estão sendo aplicadas em cenários reais.
Por fim, o mercado passa a discutir com mais profundidade temas como
governança semântica, viés e qualidade de resultados . À medida que Bancos
Vetoriais passam a influenciar decisões automatizadas e experiências do usuário,
torna-se essencial avaliar não apenas desempenho técnico, mas também relevância,
explicabilidade e aderência ao contexto de negócio. Essa discussão apont a para um
futuro em que Bancos Vetoriais deixam de ser apenas uma inovação tecnológica e se
consolidam como um pilar das arquiteturas modernas de dados e Inteligência Artificial.

### Página 17

Banco Vetorial

Nesta aula, você compreendeu como os Bancos Vetoriais  surgem como
resposta às limitações dos modelos tradicionais de armazenamento e consulta
quando o foco passa a ser significado, contexto e similaridade . Foi possível
perceber que, diferentemente dos bancos relacionais e NoSQL clássicos, essas bases
operam sobre representações vetoriais de dados não estruturados, permitindo buscas
semânticas e análises baseadas em proximidade.
Você também explorou o conceito de embeddings como elemento central
desse modelo, entendendo como textos, imagens e outros tipos de dados podem ser
transformados em vetores numéricos e posicionados em espaços semânticos de alta
dimensionalidade. A aula destacou ainda o papel das métricas de similarid ade e das
técnicas de indexação vetorial, que viabilizam buscas eficientes mesmo em grandes
volumes de dados.
Por fim, foram discutidas aplicações práticas e tendências de mercado, como o
uso de Bancos Vetoriais em arquiteturas de IA generativa e Retrieval -Augmented
Generation (RAG), além de sua convivência com bancos tradicionais em arquiteturas
de persistência poliglota. Esse conjunto de conceitos reforça a importância dos
Bancos Vetoriais como componente estratégico nas arquiteturas modernas de dados
e Inteligência Artificial.

### Página 18

Banco Vetorial

AMERSHI, Saleema; BEGEL, Andrew; BIRD, Christian et al. Designing Machine
Learning Systems. Sebastopol: O’Reilly Media, 2022.
CHROMA. Chroma Documentation . Chroma DB, 2024. Disponível em:
https://docs.trychroma.com/. Acesso em: 09 abr. 2026.
JOHNSON, Jeff; DOUZE, Matthijs; JÉGOU, Hervé. Billion-scale similarity search
with GPUs. IEEE Transactions on Big Data , v. 7, n. 3, p. 535 –547, 2021.
(Base conceitual do FAISS e técnicas de busca aproximada por vizinhança).
KLEPPMANN, Martin. Designing Data -Intensive Applications: The Big Ideas
Behind Reliable, Scalable, and Maintainable Systems. Sebastopol: O’Reilly Media,
2017.
LEWIS, Patrick; OGAZIO, Ethan; GRAVE, Edouard; RIEDEL, Sebastian. Retrieval-
Augmented Generation for Knowledge-Intensive NLP Tasks. Meta AI Research,
2020. Disponível em:  https://ai.facebook.com/blog/retrieval-augmented-generation-
streamlining-the-creation-of-intelligent-natural-language-processing-models/. Acesso
em: 09 abr. 2026.
META AI. FAISS: A Library for Efficient Similarity Search. GitHub, 2023. Disponível
em: https://github.com/facebookresearch/faiss. Acesso em: 09 abr. 2026.
PINECONE. What is a Vector Database?  Pinecone Learn, 2023. Disponível em:
https://www.pinecone.io/learn/vector-database/. Acesso em: 09 abr. 2026.
WEAVIATE. Vector Databases Explained . YouTube, 2023. Disponível em:
https://www.youtube.com/watch?v=klTvEwg3oJ4. Acesso em: 09 abr. 2026.
WEAVIATE. Vector Search Explained . Weaviate Documentation, 2024. Disponível
em: https://weaviate.io/blog/vector-search-explained. Acesso em: 09 abr. 2026.

### Página 19

Banco Vetorial

PALAVRAS-CHAVE
Busca Semântica. Bancos Vetoriais. Representações Vetoriais.

### Página 20

Banco Vetorial
