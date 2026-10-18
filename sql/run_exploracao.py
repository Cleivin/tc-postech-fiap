"""Executa sql/01_exploracao.sql e grava CSVs 06_* em evidence/passo_02/."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "passo_02"
SQL_FILE = Path(__file__).with_name("01_exploracao.sql")
README = OUT / "README.md"

NAMED_BLOCKS = [
    ("06_distribuicao_rede_alunos", 0),
    ("06_taxa_uf_ranking", 1),
    ("06_gap_meta_uf", 2),
    ("06_presenca_vs_proficiencia", 3),
    ("06_cobertura_join_meta", 4),
    ("06_consistencia_micro_vs_muni", 5),
]

MARKER = "# Exploração BigQuery — passo 2 (extra)"


def split_statements(sql_text: str) -> list[str]:
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

    if not creds or not Path(creds).exists():
        raise SystemExit(
            "[ERRO] Credencial GCP nao encontrada. "
            "Salve credentials/gcp-sa-key.json e confira GOOGLE_APPLICATION_CREDENTIALS no .env."
        )

    client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"), location="US")
    OUT.mkdir(parents=True, exist_ok=True)

    statements = split_statements(SQL_FILE.read_text(encoding="utf-8"))
    if len(statements) != len(NAMED_BLOCKS):
        raise SystemExit(
            f"Esperado {len(NAMED_BLOCKS)} statements, achei {len(statements)}. "
            "Ajuste NAMED_BLOCKS em run_exploracao.py."
        )

    summary_lines = [MARKER, ""]
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

    existing = README.read_text(encoding="utf-8") if README.exists() else ""
    if MARKER in existing:
        existing = existing.split(MARKER)[0].rstrip() + "\n\n"

    README.write_text(existing + "\n".join(summary_lines), encoding="utf-8")
    print("DONE -> evidence/passo_02/ (06_*.csv)")


if __name__ == "__main__":
    main()
