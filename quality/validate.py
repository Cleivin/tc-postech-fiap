"""Valida qualidade Bronze ou Silver.

Uso:
  python quality/validate.py --layer bronze
  python quality/validate.py --layer silver
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quality.ops import append_check, ensure_quality_table, load_env_and_client
from quality.rules_bronze import latest_run_id, run_all_bronze_rules
from quality.rules_silver import latest_silver_run_id, run_all_silver_rules


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def update_readme_bronze(run_id: str, rows: list[dict], blocking_fails: int) -> None:
    out = ROOT / "evidence" / "passo_04"
    out.mkdir(parents=True, exist_ok=True)
    readme = out / "README.md"
    section = [
        "# Passo 4 — Qualidade da Bronze",
        "",
        "Escopo: somente Bronze (sem join / Silver).",
        "",
        "## Validate limpo",
        "",
        f"- comando: `python quality/validate.py --layer bronze`",
        f"- run_id: `{run_id}`",
        f"- blocking fails: **{blocking_fails}**",
        f"- exit esperado: `0` se blocking fails = 0",
        f"- snapshot: `evidence/passo_04/validate_bronze_{run_id}.csv`",
        "",
        "| entity | rule | class | status | value | threshold |",
        "|--------|------|-------|--------|-------|-----------|",
    ]
    for r in rows:
        section.append(
            f"| {r['entity']} | {r['rule']} | {r['class']} | {r['status']} | "
            f"{r['value']} | {r['threshold']} |"
        )
    section.extend(["", "---", ""])

    old = readme.read_text(encoding="utf-8") if readme.exists() else ""
    marker = "## Prove failure"
    if marker in old:
        section.append(old[old.index(marker) :])
    else:
        section.append(
            "## Prove failure\n\n_(rode `python quality/prove_failure.py`)_\n"
        )

    readme.write_text("\n".join(section), encoding="utf-8")


def update_readme_silver(run_id: str, rows: list[dict], blocking_fails: int) -> None:
    out = ROOT / "evidence" / "passo_05"
    out.mkdir(parents=True, exist_ok=True)
    readme = out / "README.md"
    old = readme.read_text(encoding="utf-8") if readme.exists() else ""

    validate_block = [
        "## Validate Silver",
        "",
        f"- comando: `python quality/validate.py --layer silver`",
        f"- run_id_bronze: `{run_id}`",
        f"- blocking fails: **{blocking_fails}**",
        f"- exit esperado: `0` se blocking fails = 0",
        f"- snapshot: `evidence/passo_05/validate_silver_{run_id}.csv`",
        "",
        "| entity | rule | class | status | value | threshold |",
        "|--------|------|-------|--------|-------|-----------|",
    ]
    for r in rows:
        validate_block.append(
            f"| {r['entity']} | {r['rule']} | {r['class']} | {r['status']} | "
            f"{r['value']} | {r['threshold']} |"
        )
    validate_block.append("")

    marker = "## Validate Silver"
    if marker in old:
        # preserve transform section (everything before Validate Silver)
        head = old[: old.index(marker)].rstrip() + "\n\n"
        readme.write_text(head + "\n".join(validate_block), encoding="utf-8")
    elif old.strip():
        readme.write_text(old.rstrip() + "\n\n" + "\n".join(validate_block), encoding="utf-8")
    else:
        readme.write_text(
            "# Passo 5 — Silver\n\n" + "\n".join(validate_block),
            encoding="utf-8",
        )


def persist_results(
    bq,
    project_id: str,
    run_id: str,
    layer: str,
    results,
) -> tuple[list[dict], int]:
    persisted: list[dict] = []
    blocking_fails = 0
    for r in results:
        row = append_check(
            bq,
            project_id,
            run_id=run_id,
            layer=layer,
            entity=r.entity,
            rule=r.rule,
            rule_class=r.rule_class,
            status=r.status,
            value=r.value,
            threshold=r.threshold,
            detail=r.detail,
        )
        persisted.append(row)
        flag = "FAIL" if r.status == "fail" else ("WARN" if r.status == "warn" else "OK")
        print(
            f"  [{flag}] {r.entity}.{r.rule} class={r.rule_class} "
            f"value={r.value} threshold={r.threshold}"
        )
        if r.rule_class == "blocking" and r.status == "fail":
            blocking_fails += 1
    return persisted, blocking_fails


def main() -> None:
    parser = argparse.ArgumentParser(description="Qualidade Bronze / Silver")
    parser.add_argument(
        "--layer",
        required=True,
        choices=["bronze", "silver"],
        help="Camada a validar",
    )
    args = parser.parse_args()

    project_id, bq = load_env_and_client(ROOT)
    ensure_quality_table(bq, project_id)

    print("=" * 60)
    print(f"QUALITY validate | layer={args.layer} project={project_id}")
    print("=" * 60)

    if args.layer == "bronze":
        run_id = latest_run_id(bq, project_id)
        print(f"run_id alvo: {run_id}")
        results = run_all_bronze_rules(bq, project_id, run_id)
        persisted, blocking_fails = persist_results(
            bq, project_id, run_id, "bronze", results
        )
        out = ROOT / "evidence" / "passo_04"
        csv_path = out / f"validate_bronze_{run_id}.csv"
        write_csv(persisted, csv_path)
        write_csv(persisted, out / "validate_bronze_latest.csv")
        update_readme_bronze(run_id, persisted, blocking_fails)
    else:
        run_id = latest_silver_run_id(bq, project_id)
        print(f"run_id_bronze alvo: {run_id}")
        results = run_all_silver_rules(bq, project_id)
        persisted, blocking_fails = persist_results(
            bq, project_id, run_id, "silver", results
        )
        out = ROOT / "evidence" / "passo_05"
        csv_path = out / f"validate_silver_{run_id}.csv"
        write_csv(persisted, csv_path)
        write_csv(persisted, out / "validate_silver_latest.csv")
        update_readme_silver(run_id, persisted, blocking_fails)

    print("=" * 60)
    print("checks gravados em alfabetizacao_ops.quality_checks")
    print(f"evidencia: {csv_path.relative_to(ROOT).as_posix()}")
    if blocking_fails:
        print(f"[ERRO] {blocking_fails} regra(s) bloqueante(s) falharam")
        sys.exit(1)
    print(f"[OK] qualidade {args.layer} OK (exit 0)")
    sys.exit(0)


if __name__ == "__main__":
    main()
