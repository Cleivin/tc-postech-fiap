-- Passo 6 — Gold: produtos analiticos a partir da Silver.
-- Placeholders: {{project_id}}, {{run_id}}
-- Dataset saida: alfabetizacao_gold | fonte: alfabetizacao_silver

-- ---------------------------------------------------------------------------
-- 1) indicador_municipio
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_gold.indicador_municipio`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036))
CLUSTER BY id_municipio AS
SELECT
  ano,
  id_municipio,
  serie,
  serie_label,
  rede,
  rede_label,
  taxa_alfabetizacao,
  media_portugues,
  proporcao_aluno_nivel_0,
  proporcao_aluno_nivel_1,
  proporcao_aluno_nivel_2,
  proporcao_aluno_nivel_3,
  proporcao_aluno_nivel_4,
  proporcao_aluno_nivel_5,
  proporcao_aluno_nivel_6,
  proporcao_aluno_nivel_7,
  proporcao_aluno_nivel_8,
  'oficial' AS origem,
  run_id_bronze
FROM `{{project_id}}.alfabetizacao_silver.municipio`
WHERE run_id_bronze = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 2) indicador_uf
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_gold.indicador_uf`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036))
CLUSTER BY sigla_uf AS
SELECT
  ano,
  sigla_uf,
  serie,
  serie_label,
  rede,
  rede_label,
  taxa_alfabetizacao,
  media_portugues,
  proporcao_aluno_nivel_0,
  proporcao_aluno_nivel_1,
  proporcao_aluno_nivel_2,
  proporcao_aluno_nivel_3,
  proporcao_aluno_nivel_4,
  proporcao_aluno_nivel_5,
  proporcao_aluno_nivel_6,
  proporcao_aluno_nivel_7,
  proporcao_aluno_nivel_8,
  'oficial' AS origem,
  run_id_bronze
FROM `{{project_id}}.alfabetizacao_silver.uf`
WHERE run_id_bronze = '{{run_id}}';

-- ---------------------------------------------------------------------------
-- 3) meta_vs_resultado (municipio + uf + brasil)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_gold.meta_vs_resultado`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036))
CLUSTER BY nivel_geo AS
SELECT * FROM (
  SELECT
    'municipio' AS nivel_geo,
    CAST(id_municipio AS STRING) AS id_municipio,
    CAST(NULL AS STRING) AS sigla_uf,
    ano,
    serie,
    serie_label,
    rede,
    rede_label,
    taxa_alfabetizacao,
    meta_alfabetizacao_2030,
    taxa_alfabetizacao - meta_alfabetizacao_2030 AS gap_pp,
    CASE
      WHEN NOT tem_meta OR meta_alfabetizacao_2030 IS NULL THEN 'sem_meta'
      WHEN taxa_alfabetizacao IS NULL THEN 'sem_meta'
      WHEN taxa_alfabetizacao >= meta_alfabetizacao_2030 THEN 'atingiu'
      ELSE 'nao_atingiu'
    END AS status_meta,
    tem_meta,
    'oficial' AS origem,
    run_id_bronze
  FROM `{{project_id}}.alfabetizacao_silver.municipio_com_meta`
  WHERE run_id_bronze = '{{run_id}}'

  UNION ALL

  SELECT
    'uf' AS nivel_geo,
    CAST(NULL AS STRING) AS id_municipio,
    CAST(sigla_uf AS STRING) AS sigla_uf,
    ano,
    serie,
    serie_label,
    rede,
    rede_label,
    taxa_alfabetizacao,
    meta_alfabetizacao_2030,
    taxa_alfabetizacao - meta_alfabetizacao_2030 AS gap_pp,
    CASE
      WHEN NOT tem_meta OR meta_alfabetizacao_2030 IS NULL THEN 'sem_meta'
      WHEN taxa_alfabetizacao IS NULL THEN 'sem_meta'
      WHEN taxa_alfabetizacao >= meta_alfabetizacao_2030 THEN 'atingiu'
      ELSE 'nao_atingiu'
    END AS status_meta,
    tem_meta,
    'oficial' AS origem,
    run_id_bronze
  FROM `{{project_id}}.alfabetizacao_silver.uf_com_meta`
  WHERE run_id_bronze = '{{run_id}}'

  UNION ALL

  SELECT
    'brasil' AS nivel_geo,
    CAST(NULL AS STRING) AS id_municipio,
    CAST(NULL AS STRING) AS sigla_uf,
    ano,
    CAST(NULL AS STRING) AS serie,
    CAST(NULL AS STRING) AS serie_label,
    rede,
    rede_label,
    taxa_oficial_meta_brasil AS taxa_alfabetizacao,
    meta_alfabetizacao_2030,
    taxa_oficial_meta_brasil - meta_alfabetizacao_2030 AS gap_pp,
    CASE
      WHEN NOT tem_meta OR meta_alfabetizacao_2030 IS NULL THEN 'sem_meta'
      WHEN taxa_oficial_meta_brasil IS NULL THEN 'sem_meta'
      WHEN taxa_oficial_meta_brasil >= meta_alfabetizacao_2030 THEN 'atingiu'
      ELSE 'nao_atingiu'
    END AS status_meta,
    tem_meta,
    'oficial' AS origem,
    run_id_bronze
  FROM `{{project_id}}.alfabetizacao_silver.brasil_com_meta`
  WHERE run_id_bronze = '{{run_id}}'
);

-- ---------------------------------------------------------------------------
-- 4) evolucao_temporal (LAG por geo + rede + serie)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_gold.evolucao_temporal`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036))
CLUSTER BY nivel_geo AS
WITH base AS (
  SELECT
    'municipio' AS nivel_geo,
    CAST(id_municipio AS STRING) AS chave_geo,
    CAST(id_municipio AS STRING) AS id_municipio,
    CAST(NULL AS STRING) AS sigla_uf,
    ano,
    serie,
    serie_label,
    rede,
    rede_label,
    taxa_alfabetizacao,
    origem,
    run_id_bronze
  FROM `{{project_id}}.alfabetizacao_silver.municipio`
  WHERE run_id_bronze = '{{run_id}}'

  UNION ALL

  SELECT
    'uf' AS nivel_geo,
    CAST(sigla_uf AS STRING) AS chave_geo,
    CAST(NULL AS STRING) AS id_municipio,
    CAST(sigla_uf AS STRING) AS sigla_uf,
    ano,
    serie,
    serie_label,
    rede,
    rede_label,
    taxa_alfabetizacao,
    origem,
    run_id_bronze
  FROM `{{project_id}}.alfabetizacao_silver.uf`
  WHERE run_id_bronze = '{{run_id}}'
)
SELECT
  nivel_geo,
  chave_geo,
  id_municipio,
  sigla_uf,
  ano,
  serie,
  serie_label,
  rede,
  rede_label,
  taxa_alfabetizacao,
  LAG(taxa_alfabetizacao) OVER (
    PARTITION BY nivel_geo, chave_geo, rede, serie
    ORDER BY ano
  ) AS taxa_anterior,
  taxa_alfabetizacao - LAG(taxa_alfabetizacao) OVER (
    PARTITION BY nivel_geo, chave_geo, rede, serie
    ORDER BY ano
  ) AS delta_pp,
  'oficial' AS origem,
  run_id_bronze
FROM base;

-- ---------------------------------------------------------------------------
-- 5) validacao_microdado (taxa ponderada alunos vs municipio oficial)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE `{{project_id}}.alfabetizacao_gold.validacao_microdado`
PARTITION BY RANGE_BUCKET(ano, GENERATE_ARRAY(2020, 2036))
CLUSTER BY id_municipio AS
WITH micro AS (
  SELECT
    ano,
    id_municipio,
    serie,
    rede,
    SUM(CASE WHEN alfabetizado = '1' THEN peso_aluno ELSE 0 END) AS peso_alfabetizados,
    SUM(peso_aluno) AS peso_avaliados,
    SAFE_DIVIDE(
      SUM(CASE WHEN alfabetizado = '1' THEN peso_aluno ELSE 0 END),
      SUM(peso_aluno)
    ) * 100 AS taxa_micro
  FROM `{{project_id}}.alfabetizacao_silver.alunos`
  WHERE run_id_bronze = '{{run_id}}'
    AND presenca = '1'
    AND peso_aluno IS NOT NULL
  GROUP BY ano, id_municipio, serie, rede
)
SELECT
  m.ano,
  m.id_municipio,
  m.serie,
  mun.serie_label,
  m.rede,
  mun.rede_label,
  m.peso_avaliados,
  m.peso_alfabetizados,
  m.taxa_micro,
  mun.taxa_alfabetizacao AS taxa_oficial,
  m.taxa_micro - mun.taxa_alfabetizacao AS diff_pp,
  'oficial' AS origem,
  '{{run_id}}' AS run_id_bronze
FROM micro m
INNER JOIN `{{project_id}}.alfabetizacao_silver.municipio` mun
  ON m.ano = mun.ano
 AND m.id_municipio = mun.id_municipio
 AND m.serie = mun.serie
 AND m.rede = mun.rede
 AND mun.run_id_bronze = '{{run_id}}';
