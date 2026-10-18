"""Configuração das regras de qualidade (Bronze Passo 4 + Silver Passo 5 + Gold Passo 6)."""
from __future__ import annotations

BRONZE_DATASET = "alfabetizacao_bronze"
SILVER_DATASET = "alfabetizacao_silver"
GOLD_DATASET = "alfabetizacao_gold"
OPS_DATASET = "alfabetizacao_ops"
QUALITY_TABLE = "quality_checks"
FIXTURE_TABLE = "fixture_dup_keys"
PIPELINE_RUNS_TABLE = "pipeline_runs"
ALERT_TOPIC_ID = "alfabetizacao-alertas"

# Limiar: 0 códigos rede/serie ausentes no dicionario (perfil passo 2 = 0 orfaos).
ORPHAN_CODES_THRESHOLD = 0.0

# Cobertura geo Passo 2 ≈ 96–97%; limiar bloqueante justificado no contrato.
JOIN_MATCH_THRESHOLD = 0.95

# Entidades Bronze e chaves naturais (docs/contrato_dados.md).
ENTITY_KEYS: dict[str, list[str]] = {
    "alunos": ["ano", "id_municipio", "id_escola", "id_aluno", "serie", "rede"],
    "municipio": ["ano", "id_municipio", "serie", "rede"],
    "uf": ["ano", "sigla_uf", "serie", "rede"],
    "meta_alfabetizacao_brasil": ["ano", "rede"],
    "meta_alfabetizacao_uf": ["ano", "sigla_uf", "rede"],
    "meta_alfabetizacao_municipio": ["ano", "id_municipio", "rede"],
    "dicionario": ["id_tabela", "nome_coluna", "chave"],
}

# orphan_codes so em fato/agregado com codigo numerico (nao metas com rotulo).
ORPHAN_CODE_ENTITIES: dict[str, list[str]] = {
    "alunos": ["rede", "serie"],
    "municipio": ["rede", "serie"],
    "uf": ["rede", "serie"],
}

SILVER_TABLES: list[str] = [
    "dicionario",
    "alunos",
    "municipio",
    "uf",
    "meta_alfabetizacao_municipio",
    "meta_alfabetizacao_uf",
    "meta_alfabetizacao_brasil",
    "municipio_com_meta",
    "uf_com_meta",
    "brasil_com_meta",
]

JOIN_MATCH_ENTITIES: list[str] = [
    "municipio_com_meta",
    "uf_com_meta",
    "brasil_com_meta",
]

# Colunas *_label checadas para desconhecido_count (informative).
DESCONHECIDO_LABEL_COLS: dict[str, list[str]] = {
    "alunos": ["rede_label", "serie_label", "presenca_label", "alfabetizado_label"],
    "municipio": ["rede_label", "serie_label"],
    "uf": ["rede_label", "serie_label"],
}

GOLD_TABLES: list[str] = [
    "indicador_municipio",
    "indicador_uf",
    "meta_vs_resultado",
    "evolucao_temporal",
    "validacao_microdado",
]
