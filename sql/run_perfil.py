"""Executa as queries de sql/00_perfil.sql e grava CSVs em evidence/passo_02/."""
from __future__ import annotations

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "passo_02"
SQL_FILE = Path(__file__).with_name("00_perfil.sql")

NAMED_BLOCKS = [
    ("01_amostra_alunos", 0),
    ("01_amostra_municipio", 1),
    ("01_amostra_uf", 2),
    ("01_amostra_meta_brasil", 3),
    ("01_amostra_meta_uf", 4),
    ("01_amostra_meta_municipio", 5),
    ("01_dicionario_completo", 6),
    ("02_contagens_alunos", 7),
    ("02_contagens_municipio_uf", 8),
    ("02_contagens_metas", 9),
    ("03_meta_pactuada_brasil", 10),
    ("04_codigos_orfos_alunos", 11),
    ("04_codigos_orfos_municipio_uf", 12),
    ("05_anomalia_rede_encoding", 13),
    ("05_anomalia_meta_uf_nula", 14),
]


def split_statements(sql_text: str) -> list[str]:
    # Remove line comments, then split on ';' that end statements.
    lines = []
    for line in sql_text.splitlines():
        if line.strip().startswith("--"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    parts = [p.strip() for p in cleaned.split(";")]
    return [p for p in parts if p]


def main() -> None:
    load_dotenv(ROOT / ".env")
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds and not Path(creds).is_absolute():
        creds = str(ROOT / creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds or ""

    client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"), location="US")
    OUT.mkdir(parents=True, exist_ok=True)

    statements = split_statements(SQL_FILE.read_text(encoding="utf-8"))
    if len(statements) != len(NAMED_BLOCKS):
        raise SystemExit(
            f"Esperado {len(NAMED_BLOCKS)} statements, achei {len(statements)}. "
            "Ajuste NAMED_BLOCKS em run_perfil.py."
        )

    summary_lines = ["# Perfil BigQuery — evidência passo 2", ""]
    for name, idx in NAMED_BLOCKS:
        sql = statements[idx]
        print(f"Running {name}...")
        job = client.query(sql)
        df = job.to_dataframe()
        path = OUT / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  job={job.job_id} rows={len(df)} -> {path.relative_to(ROOT)}")
        summary_lines.append(f"## {name}")
        summary_lines.append(f"- job_id: `{job.job_id}`")
        summary_lines.append(f"- rows: {len(df)}")
        summary_lines.append(f"- file: `{path.relative_to(ROOT).as_posix()}`")
        summary_lines.append("")
        summary_lines.append("```")
        summary_lines.append(df.head(30).to_string(index=False))
        summary_lines.append("```")
        summary_lines.append("")

    (OUT / "README.md").write_text("\n".join(summary_lines), encoding="utf-8")
    print("DONE -> evidence/passo_02/")


if __name__ == "__main__":
    main()
