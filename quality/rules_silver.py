"""Regras de qualidade da Silver (join_match + desconhecido_count)."""
from __future__ import annotations

from dataclasses import dataclass

from google.cloud import bigquery

from quality.config import (
    DESCONHECIDO_LABEL_COLS,
    JOIN_MATCH_ENTITIES,
    JOIN_MATCH_THRESHOLD,
    SILVER_DATASET,
    SILVER_TABLES,
)
from quality.rules_bronze import RuleResult


@dataclass
class JoinMatchResult(RuleResult):
    linhas_esquerda: int = 0
    linhas_com_par: int = 0


def _table(project_id: str, entity: str) -> str:
    return f"`{project_id}.{SILVER_DATASET}.{entity}`"


def measure_join_match(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
) -> JoinMatchResult:
    sql = f"""
    SELECT
      COUNT(*) AS linhas_esquerda,
      COUNTIF(tem_meta) AS linhas_com_par,
      SAFE_DIVIDE(COUNTIF(tem_meta), COUNT(*)) AS taxa_match
    FROM {_table(project_id, entity)}
    """
    row = next(bq.query(sql).result())
    esquerda = int(row["linhas_esquerda"] or 0)
    com_par = int(row["linhas_com_par"] or 0)
    taxa = float(row["taxa_match"] if row["taxa_match"] is not None else 0.0)
    threshold = JOIN_MATCH_THRESHOLD
    status = "fail" if taxa < threshold else "pass"
    return JoinMatchResult(
        entity=entity,
        rule="join_match",
        rule_class="blocking",
        value=taxa,
        threshold=threshold,
        status=status,
        detail=f"linhas_esquerda={esquerda}; linhas_com_par={com_par}",
        linhas_esquerda=esquerda,
        linhas_com_par=com_par,
    )


def check_desconhecido_count(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
    label_cols: list[str],
) -> RuleResult:
    parts = " + ".join(f"COUNTIF({c} = 'desconhecido')" for c in label_cols)
    sql = f"""
    SELECT ({parts}) AS n_desconhecido
    FROM {_table(project_id, entity)}
    """
    n = float(next(bq.query(sql).result())["n_desconhecido"] or 0)
    # informative: status warn se > 0, pass se 0 (nao bloqueia)
    status = "warn" if n > 0 else "pass"
    return RuleResult(
        entity=entity,
        rule="desconhecido_count",
        rule_class="informative",
        value=n,
        threshold=0.0,
        status=status,
        detail=f"colunas={','.join(label_cols)}",
    )


def check_row_count_silver(
    bq: bigquery.Client,
    project_id: str,
    entity: str,
) -> RuleResult:
    sql = f"SELECT COUNT(*) AS n FROM {_table(project_id, entity)}"
    n = float(next(bq.query(sql).result())["n"] or 0)
    threshold = 1.0
    status = "fail" if n < threshold else "pass"
    return RuleResult(
        entity=entity,
        rule="row_count",
        rule_class="informative",
        value=n,
        threshold=threshold,
        status=status,
        detail="linhas na tabela silver",
    )


def run_desconhecido_counts(
    bq: bigquery.Client,
    project_id: str,
) -> list[RuleResult]:
    results: list[RuleResult] = []
    for entity, cols in DESCONHECIDO_LABEL_COLS.items():
        results.append(check_desconhecido_count(bq, project_id, entity, cols))
    return results


def run_all_silver_rules(
    bq: bigquery.Client,
    project_id: str,
) -> list[RuleResult]:
    results: list[RuleResult] = []
    for entity in JOIN_MATCH_ENTITIES:
        print(f"  rules: {entity}.join_match")
        results.append(measure_join_match(bq, project_id, entity))
    for entity in SILVER_TABLES:
        results.append(check_row_count_silver(bq, project_id, entity))
    results.extend(run_desconhecido_counts(bq, project_id))
    return results


def latest_silver_run_id(bq: bigquery.Client, project_id: str) -> str:
    """run_id_bronze da tabela silver.municipio (ou alunos)."""
    sql = f"""
    SELECT run_id_bronze
    FROM `{project_id}.{SILVER_DATASET}.municipio`
    GROUP BY run_id_bronze
    ORDER BY MAX(ano) DESC
    LIMIT 1
    """
    rows = list(bq.query(sql).result())
    if not rows:
        raise RuntimeError("Nenhum run_id_bronze em alfabetizacao_silver.municipio")
    return str(rows[0]["run_id_bronze"])
