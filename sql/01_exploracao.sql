-- Exploração analítica — basedosdados.br_inep_avaliacao_alfabetizacao
-- Passo 2 (extra): entender distribuição, gaps, cobertura e consistência

-- =============================================================================
-- 1) Volume e taxa simples por ano × rede (rótulo do dicionario)
-- =============================================================================

SELECT
  a.ano,
  a.rede,
  d.valor AS rede_rotulo,
  COUNT(*) AS n_alunos,
  COUNTIF(a.presenca = '1') AS n_presentes,
  COUNTIF(a.presenca = '1' AND a.alfabetizado = '1') AS n_alfabetizados_presentes,
  ROUND(
    SAFE_DIVIDE(
      COUNTIF(a.presenca = '1' AND a.alfabetizado = '1'),
      COUNTIF(a.presenca = '1')
    ) * 100,
    2
  ) AS taxa_alfabetizacao_simples_pct
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos` a
LEFT JOIN `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario` d
  ON d.id_tabela = 'alunos'
 AND d.nome_coluna = 'rede'
 AND d.chave = CAST(a.rede AS STRING)
GROUP BY 1, 2, 3
ORDER BY 1, 2;

-- =============================================================================
-- 2) Ranking de UF (rede pública = 5, série = 2) com delta YoY
-- =============================================================================

WITH base AS (
  SELECT ano, sigla_uf, taxa_alfabetizacao
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
  WHERE CAST(serie AS STRING) = '2'
    AND CAST(rede AS STRING) = '5'
)
SELECT
  COALESCE(t23.sigla_uf, t24.sigla_uf) AS sigla_uf,
  t23.taxa_alfabetizacao AS taxa_2023,
  t24.taxa_alfabetizacao AS taxa_2024,
  ROUND(t24.taxa_alfabetizacao - t23.taxa_alfabetizacao, 2) AS delta_yoy
FROM (SELECT * FROM base WHERE ano = 2023) t23
FULL OUTER JOIN (SELECT * FROM base WHERE ano = 2024) t24
  USING (sigla_uf)
ORDER BY taxa_2024 DESC NULLS LAST;

-- =============================================================================
-- 3) Gap até meta 2030 por UF (taxa - 80); NULLs (ex.: RR) ficam no topo
-- =============================================================================

SELECT
  ano,
  sigla_uf,
  rede,
  taxa_alfabetizacao,
  meta_alfabetizacao_2030,
  ROUND(taxa_alfabetizacao - meta_alfabetizacao_2030, 2) AS gap_vs_meta_2030,
  percentual_participacao
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
ORDER BY ano, gap_vs_meta_2030 ASC NULLS FIRST;

-- =============================================================================
-- 4) Presença × preenchimento × nulos de proficiencia/peso
-- =============================================================================

SELECT
  presenca,
  preenchimento_caderno,
  COUNT(*) AS n,
  COUNTIF(proficiencia IS NULL) AS null_proficiencia,
  COUNTIF(peso_aluno IS NULL) AS null_peso_aluno,
  COUNTIF(proficiencia IS NOT NULL) AS com_proficiencia
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
GROUP BY 1, 2
ORDER BY 1, 2;

-- =============================================================================
-- 5) Cobertura do join alunos → meta_municipio (só ano + id_municipio)
-- =============================================================================

WITH alunos_muni AS (
  SELECT DISTINCT ano, id_municipio
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
),
meta_muni AS (
  SELECT DISTINCT ano, id_municipio
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`
)
SELECT
  a.ano,
  COUNT(*) AS n_municipios_alunos,
  COUNTIF(m.id_municipio IS NOT NULL) AS n_com_meta,
  COUNTIF(m.id_municipio IS NULL) AS n_sem_meta,
  ROUND(SAFE_DIVIDE(COUNTIF(m.id_municipio IS NOT NULL), COUNT(*)) * 100, 2) AS cobertura_pct
FROM alunos_muni a
LEFT JOIN meta_muni m
  ON a.ano = m.ano
 AND a.id_municipio = m.id_municipio
GROUP BY 1
ORDER BY 1;

-- =============================================================================
-- 6) Consistência micro (alunos ponderado) vs agregado municipio (amostra)
-- =============================================================================

WITH micro AS (
  SELECT
    ano,
    id_municipio,
    rede,
    ROUND(
      SAFE_DIVIDE(
        SUM(IF(CAST(presenca AS STRING) = '1' AND CAST(alfabetizado AS STRING) = '1', peso_aluno, 0)),
        SUM(IF(CAST(presenca AS STRING) = '1', peso_aluno, 0))
      ) * 100,
      2
    ) AS taxa_micro_ponderada
  FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
  WHERE CAST(serie AS STRING) = '2'
    AND peso_aluno IS NOT NULL
  GROUP BY 1, 2, 3
),
amostra AS (
  SELECT *
  FROM micro
  WHERE CAST(rede AS STRING) = '3'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ano ORDER BY id_municipio) <= 20
)
SELECT
  a.ano,
  a.id_municipio,
  a.rede,
  a.taxa_micro_ponderada,
  m.taxa_alfabetizacao AS taxa_oficial_municipio,
  ROUND(a.taxa_micro_ponderada - m.taxa_alfabetizacao, 2) AS diff
FROM amostra a
INNER JOIN `basedosdados.br_inep_avaliacao_alfabetizacao.municipio` m
  ON a.ano = m.ano
 AND a.id_municipio = m.id_municipio
 AND CAST(a.rede AS STRING) = CAST(m.rede AS STRING)
 AND CAST(m.serie AS STRING) = '2'
ORDER BY a.ano, ABS(a.taxa_micro_ponderada - m.taxa_alfabetizacao) DESC;
