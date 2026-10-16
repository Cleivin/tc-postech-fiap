-- Perfil das entidades — basedosdados.br_inep_avaliacao_alfabetizacao
-- Passo 2: Data Understanding (Tech Challenge Fase 2)

-- =============================================================================
-- 1) Amostra + lista de colunas (não inventar nomes)
-- =============================================================================

-- alunos: ano, id_municipio, id_escola, id_aluno, caderno, serie, rede,
--         presenca, preenchimento_caderno, alfabetizado, proficiencia, peso_aluno
SELECT
  ano, id_municipio, id_escola, id_aluno, caderno, serie, rede,
  presenca, preenchimento_caderno, alfabetizado, proficiencia, peso_aluno
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
LIMIT 5;

-- municipio: ano, id_municipio, serie, rede, taxa_alfabetizacao, media_portugues,
--            proporcao_aluno_nivel_0..8
SELECT
  ano, id_municipio, serie, rede, taxa_alfabetizacao, media_portugues,
  proporcao_aluno_nivel_0, proporcao_aluno_nivel_1, proporcao_aluno_nivel_2,
  proporcao_aluno_nivel_3, proporcao_aluno_nivel_4, proporcao_aluno_nivel_5,
  proporcao_aluno_nivel_6, proporcao_aluno_nivel_7, proporcao_aluno_nivel_8
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
LIMIT 5;

-- uf: ano, sigla_uf, serie, rede, taxa_alfabetizacao, media_portugues,
--     proporcao_aluno_nivel_0..8
SELECT
  ano, sigla_uf, serie, rede, taxa_alfabetizacao, media_portugues,
  proporcao_aluno_nivel_0, proporcao_aluno_nivel_1, proporcao_aluno_nivel_2,
  proporcao_aluno_nivel_3, proporcao_aluno_nivel_4, proporcao_aluno_nivel_5,
  proporcao_aluno_nivel_6, proporcao_aluno_nivel_7, proporcao_aluno_nivel_8
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
LIMIT 5;

-- meta_alfabetizacao_brasil
SELECT
  ano, rede, taxa_alfabetizacao,
  meta_alfabetizacao_2024, meta_alfabetizacao_2025, meta_alfabetizacao_2026,
  meta_alfabetizacao_2027, meta_alfabetizacao_2028, meta_alfabetizacao_2029,
  meta_alfabetizacao_2030, percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
LIMIT 5;

-- meta_alfabetizacao_uf
SELECT
  ano, sigla_uf, rede, taxa_alfabetizacao,
  meta_alfabetizacao_2024, meta_alfabetizacao_2025, meta_alfabetizacao_2026,
  meta_alfabetizacao_2027, meta_alfabetizacao_2028, meta_alfabetizacao_2029,
  meta_alfabetizacao_2030, percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
LIMIT 5;

-- meta_alfabetizacao_municipio
SELECT
  ano, id_municipio, rede, taxa_alfabetizacao,
  meta_alfabetizacao_2024, meta_alfabetizacao_2025, meta_alfabetizacao_2026,
  meta_alfabetizacao_2027, meta_alfabetizacao_2028, meta_alfabetizacao_2029,
  meta_alfabetizacao_2030, nivel_alfabetizacao, percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`
LIMIT 5;

-- dicionario (apoio)
SELECT id_tabela, nome_coluna, chave, cobertura_temporal, valor
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
ORDER BY id_tabela, nome_coluna, chave;

-- =============================================================================
-- 2) Contagens, anos, nulos nas chaves
-- =============================================================================

SELECT
  COUNT(*) AS n_linhas,
  COUNT(DISTINCT ano) AS n_anos,
  MIN(ano) AS ano_min,
  MAX(ano) AS ano_max,
  COUNTIF(ano IS NULL) AS null_ano,
  COUNTIF(id_municipio IS NULL) AS null_id_municipio,
  COUNTIF(id_escola IS NULL) AS null_id_escola,
  COUNTIF(id_aluno IS NULL) AS null_id_aluno,
  COUNTIF(serie IS NULL) AS null_serie,
  COUNTIF(rede IS NULL) AS null_rede,
  COUNTIF(presenca IS NULL) AS null_presenca,
  COUNTIF(alfabetizado IS NULL) AS null_alfabetizado,
  COUNTIF(proficiencia IS NULL) AS null_proficiencia,
  COUNTIF(peso_aluno IS NULL) AS null_peso_aluno
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`;

SELECT
  'municipio' AS tabela,
  COUNT(*) AS n_linhas,
  COUNT(DISTINCT ano) AS n_anos,
  MIN(ano) AS ano_min,
  MAX(ano) AS ano_max,
  COUNTIF(ano IS NULL) AS null_ano,
  COUNTIF(id_municipio IS NULL) AS null_geo,
  COUNTIF(serie IS NULL) AS null_serie,
  COUNTIF(rede IS NULL) AS null_rede,
  COUNTIF(taxa_alfabetizacao IS NULL) AS null_taxa
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
UNION ALL
SELECT
  'uf',
  COUNT(*),
  COUNT(DISTINCT ano),
  MIN(ano),
  MAX(ano),
  COUNTIF(ano IS NULL),
  COUNTIF(sigla_uf IS NULL),
  COUNTIF(serie IS NULL),
  COUNTIF(rede IS NULL),
  COUNTIF(taxa_alfabetizacao IS NULL)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`;

SELECT
  'meta_brasil' AS tabela,
  COUNT(*) AS n_linhas,
  COUNT(DISTINCT ano) AS n_anos,
  COUNTIF(meta_alfabetizacao_2030 IS NULL) AS null_meta_2030,
  COUNTIF(meta_alfabetizacao_2030 = 80) AS meta_2030_eq_80,
  COUNTIF(meta_alfabetizacao_2030 != 80) AS meta_2030_neq_80
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
UNION ALL
SELECT
  'meta_uf',
  COUNT(*),
  COUNT(DISTINCT ano),
  COUNTIF(meta_alfabetizacao_2030 IS NULL),
  COUNTIF(meta_alfabetizacao_2030 = 80),
  COUNTIF(meta_alfabetizacao_2030 != 80)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
UNION ALL
SELECT
  'meta_municipio',
  COUNT(*),
  COUNT(DISTINCT ano),
  COUNTIF(meta_alfabetizacao_2030 IS NULL),
  COUNTIF(meta_alfabetizacao_2030 = 80),
  COUNTIF(meta_alfabetizacao_2030 != 80)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`;

-- =============================================================================
-- 3) Meta pactuada: rede pública, meta_alfabetizacao_2030 = 80
-- =============================================================================

SELECT ano, rede, taxa_alfabetizacao, meta_alfabetizacao_2030, percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
ORDER BY ano;

-- =============================================================================
-- 4) Códigos em alunos que não existem no dicionario
-- =============================================================================

WITH codigos AS (
  SELECT 'rede' AS nome_coluna, rede AS chave, COUNT(*) AS n
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  GROUP BY 1, 2
  UNION ALL
  SELECT 'serie', serie, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  GROUP BY 1, 2
  UNION ALL
  SELECT 'alfabetizado', alfabetizado, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  GROUP BY 1, 2
  UNION ALL
  SELECT 'presenca', presenca, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  GROUP BY 1, 2
  UNION ALL
  SELECT 'preenchimento_caderno', preenchimento_caderno, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  GROUP BY 1, 2
),
dic AS (
  SELECT nome_coluna, chave
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
  WHERE id_tabela = 'alunos'
)
SELECT
  c.nome_coluna,
  c.chave,
  c.n,
  CASE WHEN d.chave IS NULL THEN 'ORFAO' ELSE 'OK' END AS status_dicionario
FROM codigos c
LEFT JOIN dic d
  USING (nome_coluna, chave)
ORDER BY status_dicionario DESC, nome_coluna, chave;

-- municipio / uf vs dicionario
WITH codigos AS (
  SELECT 'municipio' AS tabela, 'rede' AS nome_coluna, rede AS chave, COUNT(*) AS n
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
  GROUP BY 1, 2, 3
  UNION ALL
  SELECT 'municipio', 'serie', serie, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
  GROUP BY 1, 2, 3
  UNION ALL
  SELECT 'uf', 'rede', rede, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
  GROUP BY 1, 2, 3
  UNION ALL
  SELECT 'uf', 'serie', serie, COUNT(*)
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
  GROUP BY 1, 2, 3
),
dic AS (
  SELECT nome_coluna, chave
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
  WHERE id_tabela IN ('alunos', 'municipio', 'uf')
)
SELECT
  c.*,
  CASE WHEN d.chave IS NULL THEN 'ORFAO' ELSE 'OK' END AS status_dicionario
FROM codigos c
LEFT JOIN dic d
  USING (nome_coluna, chave)
ORDER BY status_dicionario DESC, tabela, nome_coluna, chave;

-- =============================================================================
-- 5) Anomalia: encoding de rede diverge (código numérico x rótulo textual)
-- =============================================================================

SELECT 'alunos' AS fonte, ARRAY_AGG(DISTINCT rede ORDER BY rede) AS valores_rede
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
UNION ALL
SELECT 'municipio', ARRAY_AGG(DISTINCT rede ORDER BY rede)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
UNION ALL
SELECT 'uf', ARRAY_AGG(DISTINCT rede ORDER BY rede)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
UNION ALL
SELECT 'meta_brasil', ARRAY_AGG(DISTINCT rede ORDER BY rede)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
UNION ALL
SELECT 'meta_uf', ARRAY_AGG(DISTINCT rede ORDER BY rede)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
UNION ALL
SELECT 'meta_municipio', ARRAY_AGG(DISTINCT rede ORDER BY rede)
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`;

-- UF com meta_2030 nula (ex.: RR)
SELECT ano, sigla_uf, rede, taxa_alfabetizacao, meta_alfabetizacao_2030, percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
WHERE meta_alfabetizacao_2030 IS NULL
ORDER BY sigla_uf, ano;
