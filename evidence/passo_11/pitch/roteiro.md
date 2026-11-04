# Roteiro de narração — até 5 minutos

Cada linha é uma frase para gravar separada. A linha em branco é uma pausa curta, para respirar e recomeçar. O `···` marca uma pausa maior, quando a ideia muda.

Ritmo alvo: cerca de 4 min 40 s a 5 min. Se passar de 5 minutos no ensaio, corte a frase do painel de BI no slide 4.

---

## 0:00–0:10 · Slide 0 · Apresentação

Olá, eu sou o Cleivin, aluno do curso de Cientista de Dados com IA.

Esta é a Fase 2 do Tech Challenge, e aqui eu apresento um pipeline em arquitetura Medalhão para o Indicador Criança Alfabetizada.

## 0:10–0:42 · Slide 1 · O compromisso

Tudo começa com um compromisso do Brasil: que toda criança esteja alfabetizada até o fim do segundo ano do ensino fundamental.

Para medir isso, o Inep definiu um ponto de corte de 743 na escala do Saeb.

O indicador, então, é o percentual de estudantes que chegam a esse ponto.

···

E a régua que eu uso aqui é a meta pactuada para a rede pública: 80% até 2030.

Já o 100% é outra conta, e fica fora desta conversa.

## 0:42–1:32 · Slide 2 · Por que o dado importa

Só que o percentual nacional esconde o território.

···

Em 2024, na rede pública, o Ceará chegou a cerca de 85%, acima da meta.

A Bahia, por outro lado, ficou em cerca de 36%.

São quarenta e nove pontos percentuais de diferença entre os dois.

···

No país como um todo, a taxa subiu de quase 56%, em 2023, para quase 60%, em 2024.

Mesmo assim, ainda faltam cerca de 20 pontos para os 80% da meta.

···

E nos municípios, só cerca de um quinto bateu a meta em 2024: foram 1.141, contra 935 no ano anterior.

Ou seja, o dado mostra onde o resultado já chegou, onde a distância ainda é grande, e também onde a meta nem chegou a ser cadastrada.

## 1:32–2:24 · Slide 3 · Como a base foi organizada

Vale deixar claro: nesta fase eu não prevejo 2030 e não treino modelo.

O foco é organizar a base.

···

Na Bronze, entram os seis conjuntos oficiais, ainda crus: alunos, municípios, estados e as metas do país, tanto por UF quanto por município.

···

Na Silver, eu limpo esses dados e faço eles conversarem.

Traduzo os códigos com o dicionário oficial e cruzo o resultado de cada lugar com a meta daquele mesmo lugar.

Se menos de 95% desse cruzamento der certo, a publicação para.

E quando não existe meta, o campo fica em branco: eu não preencho esse vazio com nenhum número.

Depois, isso aparece como o status “sem meta”.

···

Por fim, na Gold ficam as tabelas prontas para análise, todas com origem oficial.

···

Além da carga oficial em lote, existe um fluxo de eventos simulado, só para mostrar a chegada contínua de dados.

Ele corre numa trilha separada e não entra na conta da taxa oficial, então os números da Gold não mudam.

## 2:24–3:22 · Slide 4 · Três leituras (Gold)

A camada Gold já entrega três leituras.

···

A primeira é o próprio resultado.

Em 2024, o Brasil tem quase 60% dos alunos alfabetizados, mas ainda não atingiu a meta de 80%.

O Ceará, com cerca de 85%, está acima dela e é a única UF da rede pública nesse patamar.

···

A segunda leitura é a lacuna de cadastro: os municípios sem meta.

Em 2024, são 96.

A taxa média deles passa de 50% de crianças alfabetizadas, cerca de 30 pontos abaixo da meta.

Mas atenção: tratar essas cidades como se tivessem falhado distorce a realidade, porque, sem meta publicada, não dá para julgar atingimento.

···

A terceira leitura é a trajetória, ainda sem previsão.

De 2023 para 2024, Minas Gerais subiu cerca de 12 pontos, e o Rio Grande do Sul caiu cerca de 18.

Essa evolução dá para ver por município, por estado e até do país.

E essas tabelas já estão prontas para um painel de BI, mas o BI em si não faz parte desta entrega.

## 3:22–3:42 · Slide 5 · Auditoria

Para conferir, eu recalculei a taxa com quase 4 milhões de registros de alunos e comparei com a taxa oficial.

A diferença é praticamente nula.

Ou seja, o dado bate, e o indicador publicado continua sendo o do Inep.

O projeto não reinventa o critério.

## 3:42–4:10 · Slide 6 · Próxima fase

Os modelos de IA ficam para a próxima fase; aqui, eles ainda não existem.

···

O que pode entrar no modelo é o passado: a taxa anterior, a variação, a rede, a série e os níveis de 2024.

O que fica de fora são as informações do mesmo ano: a taxa, a distância até a meta e o status.

Sem essa separação, o modelo só repetiria a conta.

E a projeção até 2030, vale reforçar, também não foi feita.

## 4:10–4:40 · Slide 7 · Fecho

Então, olhando a Gold agora: o Brasil está em quase 60%, com meta de 80%, e ainda não chegou lá.

O Ceará já passou, com cerca de 85%.

Em 2024, 96 municípios ficaram sem meta publicada.

E na trajetória, Minas Gerais subiu cerca de 12 pontos, enquanto o Rio Grande do Sul caiu cerca de 18.

···

Isso tudo é o passado organizado.

Para prever até 2030, é aí que entra a próxima fase, com machine learning e IA.
