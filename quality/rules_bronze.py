"""Regras SQL de qualidade sobre alfabetizacao_bronze (ultima run_id)."""
from __future__ import annotations

from dataclasses import dataclass

from google.cloud import bigquery

from quality.config import (
    BRONZE_DATASET,
    ENTITY_KEYS,
    ORPHAN_CODE_ENTITIES,
    ORPHAN_CODES_THRESHOLD,
)


@dataclass
class RuleResult:
    entity: str
    rule: str
    rule_class: str  # blocking | informative
    value: float
    threshold: float
    status: str  # pass | fail
    detail: str = ""


def latest_run_id(bq: bigquery.Client, project_id: str) -> str:
    # Preferir ingestion_ts (coluna tecnica do Parquet); run_id hex nao e cronologico.
    sql = f"""
    SELECT run_id
    FROM `{project_id}.{BRONZE_DATASET}.alunos`
    GROUP BY run_id
    ORDER BY MAX(ingestion_ts) DESC
    LIMIT 1
    """
    rows = list(bq.query(sql).result())
    if not rows:
        raise RuntimeError("Nenhuma run_id em alfabetizacao_bronze.alunos")
    return str(rows[0]["run_id"])


def _table(project_id: str, entity: str) -> str:
    return f"`{project_id}.{BRONZE_DATASET}.{entity}`"


def check_null_keys(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    run_id: str,
) -> RuleResult:
    keys = ENTITY_KEYS[entity]
    null_expr = " + ".join(f"COUNTIF({k} IS NULL)" for k in keys)
    sql = f"""
    SELECT ({null_expr}) AS n_null
    FROM {_table(project_id, entity)}
    WHERE run_id = @run_id
    """
    job = bq.query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("run_id", "STRING", run_id)]
        ),
    )
    n_null = float(next(job.result())["n_null"] or 0)
    threshold = 0.0
    status = "fail" if n_null > threshold else "pass"
    return RuleResult(
        entity=entity,
        rule="null_keys",
        rule_class="blocking",
        value=n_null,
        threshold=threshold,
        status=status,
        detail=f"chaves={','.join(keys)}",
    )


def check_duplicate_keys(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    run_id: str,
    *,
    table_fqn: str | None = None,
    filter_run_id: bool = True,
) -> RuleResult:
    keys = ENTITY_KEYS[entity]
    table = table_fqn or _table(project_id, entity)
    key_list = ", ".join(keys)
    where = "WHERE run_id = @run_id" if filter_run_id else ""
    # Extra rows beyond unique key grain (BQ nao aceita COUNT DISTINCT STRUCT).
    sql = f"""
    SELECT IFNULL(SUM(cnt - 1), 0) AS n_dup
    FROM (
      SELECT COUNT(*) AS cnt
      FROM {table}
      {where}
      GROUP BY {key_list}
      HAVING COUNT(*) > 1
    )
    """
    params = []
    if filter_run_id:
        params.append(bigquery.ScalarQueryParameter("run_id", "STRING", run_id))
    job = bq.query(
        sql,
        job_config=bigquery.QueryJobConfig(query_parameters=params),
    )
    n_dup = float(next(job.result())["n_dup"] or 0)
    threshold = 0.0
    status = "fail" if n_dup > threshold else "pass"
    return RuleResult(
        entity=entity,
        rule="duplicate_keys",
        rule_class="blocking",
        value=n_dup,
        threshold=threshold,
        status=status,
        detail=f"chaves={key_list}",
    )


def check_orphan_codes(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    run_id: str,
) -> RuleResult | None:
    cols = ORPHAN_CODE_ENTITIES.get(entity)
    if not cols:
        return None

    unions = []
    for col in cols:
        unions.append(
            f"""
            SELECT '{col}' AS nome_coluna, CAST({col} AS STRING) AS chave
            FROM {_table(project_id, entity)}
            WHERE run_id = @run_id AND {col} IS NOT NULL
            GROUP BY 1, 2
            """
        )
    codes_sql = " UNION ALL ".join(unions)
    sql = f"""
    WITH codes AS (
      {codes_sql}
    ),
    dic AS (
      SELECT nome_coluna, CAST(chave AS STRING) AS chave
      FROM {_table(project_id, "dicionario")}
      WHERE run_id = @run_id AND id_tabela = @id_tabela
    )
    SELECT COUNT(*) AS n_orphan
    FROM codes c
    LEFT JOIN dic d
      ON c.nome_coluna = d.nome_coluna AND c.chave = d.chave
    WHERE d.chave IS NULL
    """
    job = bq.query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("run_id", "STRING", run_id),
                bigquery.ScalarQueryParameter("id_tabela", "STRING", entity),
            ]
        ),
    )
    n_orphan = float(next(job.result())["n_orphan"] or 0)
    threshold = ORPHAN_CODES_THRESHOLD
    status = "fail" if n_orphan > threshold else "pass"
    return RuleResult(
        entity=entity,
        rule="orphan_codes",
        rule_class="blocking",
        value=n_orphan,
        threshold=threshold,
        status=status,
        detail=f"colunas={','.join(cols)} limiar={threshold}",
    )


def check_row_count(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    run_id: str,
) -> RuleResult:
    sql = f"""
    SELECT COUNT(*) AS n
    FROM {_table(project_id, entity)}
    WHERE run_id = @run_id
    """
    job = bq.query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("run_id", "STRING", run_id)]
        ),
    )
    n = float(next(job.result())["n"] or 0)
    threshold = 1.0
    # informative: status fail se 0, mas validate nao aborta so por isso
    status = "fail" if n < threshold else "pass"
    return RuleResult(
        entity=entity,
        rule="row_count",
        rule_class="informative",
        value=n,
        threshold=threshold,
        status=status,
        detail="linhas na run",
    )


def run_all_bronze_rules(
    bq: bigquery.Client,
    project_id: str,
    run_id: str,
) -> list[RuleResult]:
    results: list[RuleResult] = []
    for entity in ENTITY_KEYS:
        print(f"  rules: {entity}")
        results.append(check_null_keys(bq, project_id, entity, run_id))
        results.append(check_duplicate_keys(bq, project_id, entity, run_id))
        orphan = check_orphan_codes(bq, project_id, entity, run_id)
        if orphan is not None:
            results.append(orphan)
        results.append(check_row_count(bq, project_id, entity, run_id))
    return results
