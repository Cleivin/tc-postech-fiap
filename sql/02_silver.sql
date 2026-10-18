-- Passo 5 — Silver: tipar, traduzir dicionario, joins fato×meta.
-- Placeholders substituidos por silver/transform.py: {{project_id}}, {{run_id}}
-- Dataset saida: alfabetizacao_silver | fonte: alfabetizacao_bronze

-- ---------------------------------------------------------------------------
-- 1) dicionario (sem particao por ano)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.dicionario` AS
SELECT
  CAST(id_tabela AS STRING) AS id_tabela,
  CAST(nome_coluna AS STRING) AS nome_coluna,
  CAST(chave AS STRING) AS chave,
  CAST(cobertura_temporal AS STRING) AS cobertura_temporal,
  CAST(valor AS STRING) AS valor,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
WHERE run_id = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 2) alunos
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.alunos`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
WITH
dic_rede AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'alunos' AND nome_coluna = 'rede'
),
dic_serie AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'alunos' AND nome_coluna = 'serie'
),
dic_presenca AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'alunos' AND nome_coluna = 'presenca'
),
dic_alfabetizado AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'alunos' AND nome_coluna = 'alfabetizado'
),
base AS (
  SELECT *
  FROM `{{project_id}}.alfabetizacao_bronze.alunos`
  WHERE run_id = '{{run_id}}'
)
SELECT
  CAST(b.ano AS INT64) AS ano,
  TRIM(CAST(b.id_municipio AS STRING)) AS id_municipio,
  TRIM(CAST(b.id_escola AS STRING)) AS id_escola,
  TRIM(CAST(b.id_aluno AS STRING)) AS id_aluno,
  CAST(b.caderno AS STRING) AS caderno,
  CAST(b.serie AS STRING) AS serie,
  COALESCE(ds.valor, 'desconhecido') AS serie_label,
  CAST(b.rede AS STRING) AS rede,
  COALESCE(dr.valor, 'desconhecido') AS rede_label,
  CAST(b.presenca AS STRING) AS presenca,
  COALESCE(dp.valor, 'desconhecido') AS presenca_label,
  CAST(b.preenchimento_caderno AS STRING) AS preenchimento_caderno,
  CAST(b.alfabetizado AS STRING) AS alfabetizado,
  COALESCE(da.valor, 'desconhecido') AS alfabetizado_label,
  CAST(b.proficiencia AS FLOAT64) AS proficiencia,
  CAST(b.peso_aluno AS FLOAT64) AS peso_aluno,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM base b
LEFT JOIN dic_rede dr ON CAST(b.rede AS STRING) = dr.chave
LEFT JOIN dic_serie ds ON CAST(b.serie AS STRING) = ds.chave
LEFT JOIN dic_presenca dp ON CAST(b.presenca AS STRING) = dp.chave
LEFT JOIN dic_alfabetizado da ON CAST(b.alfabetizado AS STRING) = da.chave;

-- ---------------------------------------------------------------------------
-- 3) municipio
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.municipio`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
WITH
dic_rede AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'municipio' AND nome_coluna = 'rede'
),
dic_serie AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'municipio' AND nome_coluna = 'serie'
),
base AS (
  SELECT *
  FROM `{{project_id}}.alfabetizacao_bronze.municipio`
  WHERE run_id = '{{run_id}}'
)
SELECT
  CAST(b.ano AS INT64) AS ano,
  TRIM(CAST(b.id_municipio AS STRING)) AS id_municipio,
  CAST(b.serie AS STRING) AS serie,
  COALESCE(ds.valor, 'desconhecido') AS serie_label,
  CAST(b.rede AS STRING) AS rede,
  COALESCE(dr.valor, 'desconhecido') AS rede_label,
  CASE CAST(b.rede AS STRING)
    WHEN '3' THEN 'Municipal'
    ELSE NULL
  END AS rede_para_meta,
  CAST(b.taxa_alfabetizacao AS FLOAT64) AS taxa_alfabetizacao,
  CAST(b.media_portugues AS FLOAT64) AS media_portugues,
  CAST(b.proporcao_aluno_nivel_0 AS FLOAT64) AS proporcao_aluno_nivel_0,
  CAST(b.proporcao_aluno_nivel_1 AS FLOAT64) AS proporcao_aluno_nivel_1,
  CAST(b.proporcao_aluno_nivel_2 AS FLOAT64) AS proporcao_aluno_nivel_2,
  CAST(b.proporcao_aluno_nivel_3 AS FLOAT64) AS proporcao_aluno_nivel_3,
  CAST(b.proporcao_aluno_nivel_4 AS FLOAT64) AS proporcao_aluno_nivel_4,
  CAST(b.proporcao_aluno_nivel_5 AS FLOAT64) AS proporcao_aluno_nivel_5,
  CAST(b.proporcao_aluno_nivel_6 AS FLOAT64) AS proporcao_aluno_nivel_6,
  CAST(b.proporcao_aluno_nivel_7 AS FLOAT64) AS proporcao_aluno_nivel_7,
  CAST(b.proporcao_aluno_nivel_8 AS FLOAT64) AS proporcao_aluno_nivel_8,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM base b
LEFT JOIN dic_rede dr ON CAST(b.rede AS STRING) = dr.chave
LEFT JOIN dic_serie ds ON CAST(b.serie AS STRING) = ds.chave;

-- ---------------------------------------------------------------------------
-- 4) uf
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.uf`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
WITH
dic_rede AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'uf' AND nome_coluna = 'rede'
),
dic_serie AS (
  SELECT CAST(chave AS STRING) AS chave, valor
  FROM `{{project_id}}.alfabetizacao_bronze.dicionario`
  WHERE run_id = '{{run_id}}' AND id_tabela = 'uf' AND nome_coluna = 'serie'
),
base AS (
  SELECT *
  FROM `{{project_id}}.alfabetizacao_bronze.uf`
  WHERE run_id = '{{run_id}}'
)
SELECT
  CAST(b.ano AS INT64) AS ano,
  TRIM(CAST(b.sigla_uf AS STRING)) AS sigla_uf,
  CAST(b.serie AS STRING) AS serie,
  COALESCE(ds.valor, 'desconhecido') AS serie_label,
  CAST(b.rede AS STRING) AS rede,
  COALESCE(dr.valor, 'desconhecido') AS rede_label,
  CASE CAST(b.rede AS STRING)
    WHEN '5' THEN 'Pública'
    ELSE NULL
  END AS rede_para_meta,
  CAST(b.taxa_alfabetizacao AS FLOAT64) AS taxa_alfabetizacao,
  CAST(b.media_portugues AS FLOAT64) AS media_portugues,
  CAST(b.proporcao_aluno_nivel_0 AS FLOAT64) AS proporcao_aluno_nivel_0,
  CAST(b.proporcao_aluno_nivel_1 AS FLOAT64) AS proporcao_aluno_nivel_1,
  CAST(b.proporcao_aluno_nivel_2 AS FLOAT64) AS proporcao_aluno_nivel_2,
  CAST(b.proporcao_aluno_nivel_3 AS FLOAT64) AS proporcao_aluno_nivel_3,
  CAST(b.proporcao_aluno_nivel_4 AS FLOAT64) AS proporcao_aluno_nivel_4,
  CAST(b.proporcao_aluno_nivel_5 AS FLOAT64) AS proporcao_aluno_nivel_5,
  CAST(b.proporcao_aluno_nivel_6 AS FLOAT64) AS proporcao_aluno_nivel_6,
  CAST(b.proporcao_aluno_nivel_7 AS FLOAT64) AS proporcao_aluno_nivel_7,
  CAST(b.proporcao_aluno_nivel_8 AS FLOAT64) AS proporcao_aluno_nivel_8,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM base b
LEFT JOIN dic_rede dr ON CAST(b.rede AS STRING) = dr.chave
LEFT JOIN dic_serie ds ON CAST(b.serie AS STRING) = ds.chave;

-- ---------------------------------------------------------------------------
-- 5) meta_alfabetizacao_municipio
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_municipio`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
SELECT
  CAST(ano AS INT64) AS ano,
  TRIM(CAST(id_municipio AS STRING)) AS id_municipio,
  CAST(rede AS STRING) AS rede,
  CAST(taxa_alfabetizacao AS FLOAT64) AS taxa_alfabetizacao,
  CAST(meta_alfabetizacao_2024 AS FLOAT64) AS meta_alfabetizacao_2024,
  CAST(meta_alfabetizacao_2025 AS FLOAT64) AS meta_alfabetizacao_2025,
  CAST(meta_alfabetizacao_2026 AS FLOAT64) AS meta_alfabetizacao_2026,
  CAST(meta_alfabetizacao_2027 AS FLOAT64) AS meta_alfabetizacao_2027,
  CAST(meta_alfabetizacao_2028 AS FLOAT64) AS meta_alfabetizacao_2028,
  CAST(meta_alfabetizacao_2029 AS FLOAT64) AS meta_alfabetizacao_2029,
  CAST(meta_alfabetizacao_2030 AS FLOAT64) AS meta_alfabetizacao_2030,
  CAST(nivel_alfabetizacao AS STRING) AS nivel_alfabetizacao,
  CAST(percentual_participacao AS FLOAT64) AS percentual_participacao,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM `{{project_id}}.alfabetizacao_bronze.meta_alfabetizacao_municipio`
WHERE run_id = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 6) meta_alfabetizacao_uf
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_uf`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
SELECT
  CAST(ano AS INT64) AS ano,
  TRIM(CAST(sigla_uf AS STRING)) AS sigla_uf,
  CAST(rede AS STRING) AS rede,
  CAST(taxa_alfabetizacao AS FLOAT64) AS taxa_alfabetizacao,
  CAST(meta_alfabetizacao_2024 AS FLOAT64) AS meta_alfabetizacao_2024,
  CAST(meta_alfabetizacao_2025 AS FLOAT64) AS meta_alfabetizacao_2025,
  CAST(meta_alfabetizacao_2026 AS FLOAT64) AS meta_alfabetizacao_2026,
  CAST(meta_alfabetizacao_2027 AS FLOAT64) AS meta_alfabetizacao_2027,
  CAST(meta_alfabetizacao_2028 AS FLOAT64) AS meta_alfabetizacao_2028,
  CAST(meta_alfabetizacao_2029 AS FLOAT64) AS meta_alfabetizacao_2029,
  CAST(meta_alfabetizacao_2030 AS FLOAT64) AS meta_alfabetizacao_2030,
  CAST(percentual_participacao AS FLOAT64) AS percentual_participacao,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM `{{project_id}}.alfabetizacao_bronze.meta_alfabetizacao_uf`
WHERE run_id = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 7) meta_alfabetizacao_brasil
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_brasil`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
SELECT
  CAST(ano AS INT64) AS ano,
  CAST(rede AS STRING) AS rede,
  CAST(taxa_alfabetizacao AS FLOAT64) AS taxa_alfabetizacao,
  CAST(meta_alfabetizacao_2024 AS FLOAT64) AS meta_alfabetizacao_2024,
  CAST(meta_alfabetizacao_2025 AS FLOAT64) AS meta_alfabetizacao_2025,
  CAST(meta_alfabetizacao_2026 AS FLOAT64) AS meta_alfabetizacao_2026,
  CAST(meta_alfabetizacao_2027 AS FLOAT64) AS meta_alfabetizacao_2027,
  CAST(meta_alfabetizacao_2028 AS FLOAT64) AS meta_alfabetizacao_2028,
  CAST(meta_alfabetizacao_2029 AS FLOAT64) AS meta_alfabetizacao_2029,
  CAST(meta_alfabetizacao_2030 AS FLOAT64) AS meta_alfabetizacao_2030,
  CAST(percentual_participacao AS FLOAT64) AS percentual_participacao,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM `{{project_id}}.alfabetizacao_bronze.meta_alfabetizacao_brasil`
WHERE run_id = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 8) municipio_com_meta (rede 3 ↔ Municipal)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.municipio_com_meta`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
SELECT
  m.ano,
  m.id_municipio,
  m.serie,
  m.serie_label,
  m.rede,
  m.rede_label,
  m.taxa_alfabetizacao,
  m.media_portugues,
  m.proporcao_aluno_nivel_0,
  m.proporcao_aluno_nivel_1,
  m.proporcao_aluno_nivel_2,
  m.proporcao_aluno_nivel_3,
  m.proporcao_aluno_nivel_4,
  m.proporcao_aluno_nivel_5,
  m.proporcao_aluno_nivel_6,
  m.proporcao_aluno_nivel_7,
  m.proporcao_aluno_nivel_8,
  meta.taxa_alfabetizacao AS taxa_meta_fonte,
  meta.meta_alfabetizacao_2024,
  meta.meta_alfabetizacao_2025,
  meta.meta_alfabetizacao_2026,
  meta.meta_alfabetizacao_2027,
  meta.meta_alfabetizacao_2028,
  meta.meta_alfabetizacao_2029,
  meta.meta_alfabetizacao_2030,
  meta.rede AS meta_rede,
  meta.percentual_participacao,
  meta.id_municipio IS NOT NULL AS tem_meta,
  m.origem,
  m.run_id_bronze
FROM `{{project_id}}.alfabetizacao_silver.municipio` AS m
LEFT JOIN `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_municipio` AS meta
  ON m.ano = meta.ano
 AND m.id_municipio = meta.id_municipio
 AND m.rede_para_meta = meta.rede
WHERE m.rede = '3';

-- ---------------------------------------------------------------------------
-- 9) uf_com_meta (rede 5 ↔ Pública)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.uf_com_meta`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
SELECT
  u.ano,
  u.sigla_uf,
  u.serie,
  u.serie_label,
  u.rede,
  u.rede_label,
  u.taxa_alfabetizacao,
  u.media_portugues,
  u.proporcao_aluno_nivel_0,
  u.proporcao_aluno_nivel_1,
  u.proporcao_aluno_nivel_2,
  u.proporcao_aluno_nivel_3,
  u.proporcao_aluno_nivel_4,
  u.proporcao_aluno_nivel_5,
  u.proporcao_aluno_nivel_6,
  u.proporcao_aluno_nivel_7,
  u.proporcao_aluno_nivel_8,
  meta.taxa_alfabetizacao AS taxa_meta_fonte,
  meta.meta_alfabetizacao_2024,
  meta.meta_alfabetizacao_2025,
  meta.meta_alfabetizacao_2026,
  meta.meta_alfabetizacao_2027,
  meta.meta_alfabetizacao_2028,
  meta.meta_alfabetizacao_2029,
  meta.meta_alfabetizacao_2030,
  meta.rede AS meta_rede,
  meta.percentual_participacao,
  meta.sigla_uf IS NOT NULL AS tem_meta,
  u.origem,
  u.run_id_bronze
FROM `{{project_id}}.alfabetizacao_silver.uf` AS u
LEFT JOIN `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_uf` AS meta
  ON u.ano = meta.ano
 AND u.sigla_uf = meta.sigla_uf
 AND u.rede_para_meta = meta.rede
WHERE u.rede = '5';

-- ---------------------------------------------------------------------------
-- 10) brasil_com_meta (agg UF rede 5 × meta Pública)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_silver.brasil_com_meta`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036)) AS
WITH brasil_agg AS (
  SELECT
    ano,
    AVG(taxa_alfabetizacao) AS media_simples_ufs
  FROM `{{project_id}}.alfabetizacao_silver.uf`
  WHERE rede = '5'
  GROUP BY ano
)
SELECT
  b.ano,
  '5' AS rede,
  'Pública (Estadual e Municipal)' AS rede_label,
  b.media_simples_ufs,
  m.taxa_alfabetizacao AS taxa_oficial_meta_brasil,
  m.meta_alfabetizacao_2030,
  m.percentual_participacao,
  m.ano IS NOT NULL AS tem_meta,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM brasil_agg b
LEFT JOIN `{{project_id}}.alfabetizacao_silver.meta_alfabetizacao_brasil` m
  ON b.ano = m.ano AND m.rede = 'Pública';
