-- Exploracao v2: cada tabela + rotulos do dicionario (quando existirem)
-- Fonte: basedosdados.br_inep_avaliacao_alfabetizacao
--
-- O dicionario so tem id_tabela em: alunos, municipio, uf.
-- Metas usam rede textual (Publica / Municipal) — nao ha chave no dicionario.

-- =============================================================================
-- dicionario (apoio)
-- =============================================================================
select t1.id_tabela
     , t1.nome_coluna
     , t1.chave
     , t1.cobertura_temporal
     , t1.valor
  from basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t1
;

-- =============================================================================
-- alunos + dicionario (rede, serie, presenca, preenchimento_caderno, alfabetizado)
-- =============================================================================
select t1.ano
     , t1.id_municipio
     , t1.id_escola
     , t1.id_aluno
     , t1.caderno
     , t1.serie
     , t3.valor tx_serie
     , t1.rede
     , t2.valor tx_rede
     , t1.presenca
     , t4.valor tx_presenca
     , t1.preenchimento_caderno
     , t5.valor tx_preenchimento_caderno
     , t1.alfabetizado
     , t6.valor tx_alfabetizado
     , t1.proficiencia
     , t1.peso_aluno
  from basedosdados.br_inep_avaliacao_alfabetizacao.alunos t1
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t2
    on t2.id_tabela = 'alunos'
   and t2.nome_coluna = 'rede'
   and t2.chave = t1.rede
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t3
    on t3.id_tabela = 'alunos'
   and t3.nome_coluna = 'serie'
   and t3.chave = t1.serie
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t4
    on t4.id_tabela = 'alunos'
   and t4.nome_coluna = 'presenca'
   and t4.chave = t1.presenca
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t5
    on t5.id_tabela = 'alunos'
   and t5.nome_coluna = 'preenchimento_caderno'
   and t5.chave = t1.preenchimento_caderno
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t6
    on t6.id_tabela = 'alunos'
   and t6.nome_coluna = 'alfabetizado'
   and t6.chave = t1.alfabetizado
;

-- =============================================================================
-- municipio + dicionario (rede, serie)
-- =============================================================================
select t1.ano
     , t1.id_municipio
     , t1.serie
     , t3.valor tx_serie
     , t1.rede
     , t2.valor tx_rede
     , t1.taxa_alfabetizacao
     , t1.media_portugues
     , t1.proporcao_aluno_nivel_0
     , t1.proporcao_aluno_nivel_1
     , t1.proporcao_aluno_nivel_2
     , t1.proporcao_aluno_nivel_3
     , t1.proporcao_aluno_nivel_4
     , t1.proporcao_aluno_nivel_5
     , t1.proporcao_aluno_nivel_6
     , t1.proporcao_aluno_nivel_7
     , t1.proporcao_aluno_nivel_8
  from basedosdados.br_inep_avaliacao_alfabetizacao.municipio t1
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t2
    on t2.id_tabela = 'municipio'
   and t2.nome_coluna = 'rede'
   and t2.chave = t1.rede
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t3
    on t3.id_tabela = 'municipio'
   and t3.nome_coluna = 'serie'
   and t3.chave = t1.serie
;

-- =============================================================================
-- uf + dicionario (rede, serie)
-- =============================================================================
select t1.ano
     , t1.sigla_uf
     , t1.serie
     , t3.valor tx_serie
     , t1.rede
     , t2.valor tx_rede
     , t1.taxa_alfabetizacao
     , t1.media_portugues
     , t1.proporcao_aluno_nivel_0
     , t1.proporcao_aluno_nivel_1
     , t1.proporcao_aluno_nivel_2
     , t1.proporcao_aluno_nivel_3
     , t1.proporcao_aluno_nivel_4
     , t1.proporcao_aluno_nivel_5
     , t1.proporcao_aluno_nivel_6
     , t1.proporcao_aluno_nivel_7
     , t1.proporcao_aluno_nivel_8
  from basedosdados.br_inep_avaliacao_alfabetizacao.uf t1
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t2
    on t2.id_tabela = 'uf'
   and t2.nome_coluna = 'rede'
   and t2.chave = t1.rede
  left join basedosdados.br_inep_avaliacao_alfabetizacao.dicionario t3
    on t3.id_tabela = 'uf'
   and t3.nome_coluna = 'serie'
   and t3.chave = t1.serie
;

-- =============================================================================
-- meta_alfabetizacao_brasil
-- rede ja e rotulo textual (ex.: Publica) — sem entrada no dicionario
-- =============================================================================
select t1.ano
     , t1.rede
     , t1.taxa_alfabetizacao
     , t1.meta_alfabetizacao_2024
     , t1.meta_alfabetizacao_2025
     , t1.meta_alfabetizacao_2026
     , t1.meta_alfabetizacao_2027
     , t1.meta_alfabetizacao_2028
     , t1.meta_alfabetizacao_2029
     , t1.meta_alfabetizacao_2030
     , t1.percentual_participacao
  from basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil t1
;

-- =============================================================================
-- meta_alfabetizacao_uf
-- rede ja e rotulo textual (ex.: Publica) — sem entrada no dicionario
-- =============================================================================
select t1.ano
     , t1.sigla_uf
     , t1.rede
     , t1.taxa_alfabetizacao
     , t1.meta_alfabetizacao_2024
     , t1.meta_alfabetizacao_2025
     , t1.meta_alfabetizacao_2026
     , t1.meta_alfabetizacao_2027
     , t1.meta_alfabetizacao_2028
     , t1.meta_alfabetizacao_2029
     , t1.meta_alfabetizacao_2030
     , t1.percentual_participacao
  from basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf t1
;

-- =============================================================================
-- meta_alfabetizacao_municipio
-- rede ja e rotulo textual (ex.: Municipal) — sem entrada no dicionario
-- =============================================================================
select t1.ano
     , t1.id_municipio
     , t1.rede
     , t1.taxa_alfabetizacao
     , t1.meta_alfabetizacao_2024
     , t1.meta_alfabetizacao_2025
     , t1.meta_alfabetizacao_2026
     , t1.meta_alfabetizacao_2027
     , t1.meta_alfabetizacao_2028
     , t1.meta_alfabetizacao_2029
     , t1.meta_alfabetizacao_2030
     , t1.nivel_alfabetizacao
     , t1.percentual_participacao
  from basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio t1
;
