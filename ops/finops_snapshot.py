"""FinOps com quantidade medida (Passo 9).

Le do projeto real:
  - tamanho dos objetos no bucket GCS
  - bytes_processed + duration_seconds em alfabetizacao_ops.pipeline_runs
  - dry_run Gold (evidence/passo_06/dry_run_bytes.csv) quando existir
  - bytes de payload Pub/Sub (mesmo formato do producer, lote demo --n 20)

Escreve evidence/passo_09/ (CSVs + custo.md).

Uso:
  python ops/finops_snapshot.py
  python ops/finops_snapshot.py --batch-per-month 30 --events-per-day 1000
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from google.cloud import bigquery, storage

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quality.config import OPS_DATASET, PIPELINE_RUNS_TABLE
from quality.ops import load_env_and_client
from streaming.producer import make_invalid_payload, make_valid_skeleton, plan_labels

OUT = ROOT / "evidence" / "passo_09"
DRY_RUN_CSV = ROOT / "evidence" / "passo_06" / "dry_run_bytes.csv"
BRONZE_MANIFEST = ROOT / "evidence" / "passo_03" / "manifest_20d3623d0430.csv"
GOLD_EXPORT_CSV = ROOT / "evidence" / "passo_06" / "export_20d3623d0430.csv"
STREAM_STDOUT = ROOT / "evidence" / "passo_07" / "consumer_stdout.txt"

# Precos publicos GCP — consulta 2026-10-18 (paginas oficiais).
# GCS Standard regional (us-central1): ~$0.020/GiB-mes
#   (= $0.000027397 / GiB-hora * 730 h).
# BigQuery on-demand (US): $6.25 / TiB processado (1o TiB/mes free).
# Pub/Sub Message Delivery Basic: $40 / TiB (10 GiB/mes free).
PRICING_AS_OF = "2026-10-18"
PRICE_GCS_USD_PER_GIB_MONTH = 0.020
PRICE_BQ_USD_PER_TIB = 6.25
PRICE_PUBSUB_USD_PER_TIB = 40.0

FREE_GCS_GIB = 5.0
FREE_BQ_TIB = 1.0
FREE_PUBSUB_GIB = 10.0

BYTES_PER_GIB = 1024**3
BYTES_PER_TIB = 1024**4

PRICING_SOURCES = {
    "gcs": "https://cloud.google.com/storage/pricing",
    "bq": "https://cloud.google.com/bigquery/pricing",
    "pubsub": "https://cloud.google.com/pubsub/pricing",
    "free": "https://cloud.google.com/free",
}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def load_bucket_name() -> str:
    bucket = os.getenv("GCP_BUCKET_NAME")
    if not bucket:
        raise SystemExit("[ERRO] GCP_BUCKET_NAME e obrigatorio no .env.")
    return bucket


def measure_gcs(bucket_name: str) -> tuple[list[dict], dict]:
    """Lista objetos do bucket e agrega por prefixo de 1o nivel."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    by_prefix: dict[str, dict] = defaultdict(lambda: {"bytes": 0, "objects": 0})
    total_bytes = 0
    total_objects = 0
    detail_rows: list[dict] = []

    for blob in client.list_blobs(bucket_name):
        size = int(blob.size or 0)
        name = blob.name or ""
        prefix = name.split("/", 1)[0] if "/" in name else "(root)"
        by_prefix[prefix]["bytes"] += size
        by_prefix[prefix]["objects"] += 1
        total_bytes += size
        total_objects += 1

    for prefix in sorted(by_prefix):
        detail_rows.append(
            {
                "prefix": prefix,
                "objects": by_prefix[prefix]["objects"],
                "bytes": by_prefix[prefix]["bytes"],
                "gib": round(by_prefix[prefix]["bytes"] / BYTES_PER_GIB, 6),
            }
        )

    summary = {
        "bucket": bucket_name,
        "objects": total_objects,
        "bytes": total_bytes,
        "gib": total_bytes / BYTES_PER_GIB,
        "location_note": "us-central1 (GCP_LOCATION do projeto)",
    }
    print(
        f"[OK] GCS bucket={bucket_name} objects={total_objects} "
        f"bytes={total_bytes} gib={summary['gib']:.6f}"
    )
    return detail_rows, summary


def fetch_pipeline_runs(bq: bigquery.Client, project_id: str) -> list[dict]:
    table = f"{project_id}.{OPS_DATASET}.{PIPELINE_RUNS_TABLE}"
    sql = f"""
    SELECT
      run_id, etapa, started_at, finished_at, duration_seconds,
      rows_in, rows_out, status, bytes_processed,
      latency_min_s, latency_max_s, latency_avg_s, detail
    FROM `{table}`
    ORDER BY finished_at DESC
    LIMIT 200
    """
    rows = []
    for r in bq.query(sql).result():
        rows.append(
            {
                "run_id": r["run_id"],
                "etapa": r["etapa"],
                "started_at": r["started_at"].isoformat() if r["started_at"] else "",
                "finished_at": r["finished_at"].isoformat() if r["finished_at"] else "",
                "duration_seconds": float(r["duration_seconds"] or 0),
                "rows_in": r["rows_in"],
                "rows_out": r["rows_out"],
                "status": r["status"],
                "bytes_processed": int(r["bytes_processed"] or 0)
                if r["bytes_processed"] is not None
                else None,
                "latency_min_s": r["latency_min_s"],
                "latency_max_s": r["latency_max_s"],
                "latency_avg_s": r["latency_avg_s"],
                "detail": r["detail"],
            }
        )
    print(f"[OK] pipeline_runs lidas={len(rows)}")
    return rows


def _sum_csv_bytes(path: Path, col: str) -> int:
    if not path.exists():
        return 0
    total = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get(col) not in (None, ""):
                total += int(float(row[col]))
    return total


def _read_text_flexible(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    return raw.decode("utf-8", errors="replace")


def parse_stream_latency_from_evidence() -> float | None:
    """Extrai latency_avg do stdout do consumer (Passo 7) se pipeline_runs nao tiver stream."""
    if not STREAM_STDOUT.exists():
        return None
    text = _read_text_flexible(STREAM_STDOUT)
    for line in text.splitlines():
        if "latency_avg=" not in line:
            continue
        try:
            part = line.split("latency_avg=", 1)[1].split()[0]
            return float(part)
        except (IndexError, ValueError):
            continue
    return None


def enrich_from_evidence(
    latest_success: dict[str, dict], dry_run_gold_bytes: int
) -> dict[str, dict]:
    """Completa etapas ausentes em pipeline_runs com bytes medidos nas evidencias.

    Motivo: telemetria (Passo 8) foi ligada depois de algumas runs; os jobs
    reais ja deixaram bytes em evidence/passo_03 e passo_06.
    """
    filled = dict(latest_success)
    sources: dict[str, str] = {
        k: "pipeline_runs" for k in filled
    }

    if "bronze" not in filled:
        bronze_bytes = _sum_csv_bytes(BRONZE_MANIFEST, "bytes_processed")
        if bronze_bytes > 0:
            filled["bronze"] = {
                "run_id": "20d3623d0430",
                "etapa": "bronze",
                "duration_seconds": None,
                "bytes_processed": bronze_bytes,
                "status": "success",
                "detail": "bytes_processed somados de evidence/passo_03/manifest",
            }
            sources["bronze"] = "evidence/passo_03/manifest_20d3623d0430.csv"

    if "gold" not in filled:
        # Transform Gold = dry_run; export Parquet e job separado (menor).
        export_bytes = _sum_csv_bytes(GOLD_EXPORT_CSV, "bytes_processed")
        gold_bytes = dry_run_gold_bytes + export_bytes
        if gold_bytes > 0:
            filled["gold"] = {
                "run_id": "20d3623d0430",
                "etapa": "gold",
                "duration_seconds": None,
                "bytes_processed": gold_bytes,
                "status": "success",
                "detail": (
                    f"dry_run={dry_run_gold_bytes} + export={export_bytes} "
                    "(evidence/passo_06)"
                ),
            }
            sources["gold"] = "evidence/passo_06/dry_run_bytes.csv + export_*.csv"

    if "stream" not in filled:
        lat = parse_stream_latency_from_evidence()
        if lat is not None:
            filled["stream"] = {
                "run_id": "passo_07_demo",
                "etapa": "stream",
                "duration_seconds": None,
                "bytes_processed": 0,
                "status": "success",
                "latency_avg_s": lat,
                "detail": "latency_avg do consumer_stdout (Passo 7)",
            }
            sources["stream"] = "evidence/passo_07/consumer_stdout.txt"

    return {"latest_success": filled, "sources": sources}


def summarize_runs(runs: list[dict], dry_run_gold_bytes: int = 0) -> dict:
    """Ultima success por etapa + totais medidos (pipeline_runs + evidencias)."""
    latest_success: dict[str, dict] = {}
    for r in runs:
        if r["status"] != "success":
            continue
        etapa = r["etapa"]
        if etapa not in latest_success:
            latest_success[etapa] = r

    enriched = enrich_from_evidence(latest_success, dry_run_gold_bytes)
    latest_success = enriched["latest_success"]
    sources = enriched["sources"]

    batch_bytes = 0
    batch_duration = 0.0
    for etapa in ("bronze", "silver", "gold"):
        row = latest_success.get(etapa)
        if not row:
            continue
        batch_bytes += int(row.get("bytes_processed") or 0)
        dur = row.get("duration_seconds")
        if dur is not None:
            batch_duration += float(dur)

    stream = latest_success.get("stream")
    stream_duration = (
        float(stream["duration_seconds"])
        if stream and stream.get("duration_seconds") is not None
        else 0.0
    )
    stream_latency_avg = (
        float(stream["latency_avg_s"])
        if stream and stream.get("latency_avg_s") is not None
        else None
    )

    print(
        f"[OK] batch_bytes_one_run={batch_bytes} "
        f"(fontes={sources})"
    )
    return {
        "latest_success": latest_success,
        "sources": sources,
        "batch_bytes_one_run": batch_bytes,
        "batch_duration_s_one_run": batch_duration,
        "stream_duration_s_one_run": stream_duration,
        "stream_latency_avg_s": stream_latency_avg,
    }


def load_dry_run_gold() -> tuple[list[dict], int]:
    if not DRY_RUN_CSV.exists():
        print(f"[WARN] dry_run ausente: {DRY_RUN_CSV}")
        return [], 0
    rows = []
    total = 0
    with DRY_RUN_CSV.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            b = int(row["total_bytes_processed"])
            total += b
            rows.append(
                {
                    "step": row["step"],
                    "label": row["label"],
                    "total_bytes_processed": b,
                    "dry_run": row.get("dry_run", "True"),
                }
            )
    print(f"[OK] dry_run Gold steps={len(rows)} bytes={total}")
    return rows, total


def measure_pubsub_demo(n: int = 20, seed: int = 42) -> dict:
    """Mede bytes do lote demo (mesmo formato do producer), sem republicar."""
    rng = random.Random(seed)
    labels = plan_labels(n)
    payloads: list[bytes] = []
    first_valid: bytes | None = None

    for label in labels:
        if label.startswith("valid"):
            event = make_valid_skeleton(rng)
            event["produced_at"] = datetime.now(timezone.utc).isoformat()
            payload = json.dumps(event, ensure_ascii=False).encode("utf-8")
            if first_valid is None:
                first_valid = payload
        elif label == "duplicate":
            assert first_valid is not None
            payload = first_valid
        else:
            payload = make_invalid_payload(rng)
        payloads.append(payload)

    total = sum(len(p) for p in payloads)
    avg = total / len(payloads) if payloads else 0.0
    print(
        f"[OK] Pub/Sub demo n={len(payloads)} total_bytes={total} "
        f"avg_bytes={avg:.1f} (medido no payload; publish+subscribe ~2x no throughput)"
    )
    return {
        "n_messages": len(payloads),
        "total_payload_bytes": total,
        "avg_payload_bytes": avg,
        # Pub/Sub cobra publish + subscribe; estimativa conservadora 2x o payload.
        "throughput_bytes_estimate": total * 2,
        "seed": seed,
    }


def project_costs(
    *,
    gcs_gib: float,
    batch_bytes_one_run: int,
    dry_run_gold_bytes: int,
    pubsub_demo: dict,
    batch_per_month: int,
    events_per_day: int,
    batch_duration_s: float,
    stream_duration_s: float,
) -> list[dict]:
    """Projecao mensal: quantidade medida × cadencia (premissa) × preco publico."""
    # BigQuery: preferir soma real de pipeline_runs (bronze+silver+gold);
    # dry_run Gold entra como referencia analitica na mesma linha se runs faltarem.
    bq_bytes_one = batch_bytes_one_run if batch_bytes_one_run > 0 else dry_run_gold_bytes
    bq_bytes_month = bq_bytes_one * batch_per_month
    bq_tib_month = bq_bytes_month / BYTES_PER_TIB
    bq_billable_tib = max(0.0, bq_tib_month - FREE_BQ_TIB)
    bq_cost = bq_billable_tib * PRICE_BQ_USD_PER_TIB

    # Pub/Sub: media do payload demo × eventos/dia × 30 × 2 (publish+pull).
    avg = float(pubsub_demo["avg_payload_bytes"])
    pubsub_bytes_month = avg * events_per_day * 30 * 2
    pubsub_gib_month = pubsub_bytes_month / BYTES_PER_GIB
    pubsub_billable_gib = max(0.0, pubsub_gib_month - FREE_PUBSUB_GIB)
    pubsub_cost = (pubsub_billable_gib / 1024.0) * PRICE_PUBSUB_USD_PER_TIB

    gcs_billable = max(0.0, gcs_gib - FREE_GCS_GIB)
    gcs_cost = gcs_billable * PRICE_GCS_USD_PER_GIB_MONTH

    # Computacao: motor serverless (BQ slots on-demand + Pub/Sub). Sem VM 24/7.
    # Custo de query ja esta na linha BigQuery; aqui so documentamos duracao medida.
    compute_note = (
        f"duracao medida 1 batch (bronze+silver+gold)={batch_duration_s:.1f}s; "
        f"1 lote stream={stream_duration_s:.1f}s; "
        "sem GCE/GKE — custo embutido no BQ on-demand e Pub/Sub"
    )

    rows = [
        {
            "servico": "Cloud Storage",
            "unidade": "GiB-mes",
            "quantidade_medida": round(gcs_gib, 6),
            "preco_unitario_usd": PRICE_GCS_USD_PER_GIB_MONTH,
            "custo_mensal_projetado_usd": round(gcs_cost, 4),
            "como_mediu": "soma size dos objetos via Storage API (list_blobs)",
            "premissa_cadencia": "estoque atual do lake (nao escala com cadencia)",
            "always_free": f"primeiros {FREE_GCS_GIB} GiB-mes free (us-central1)",
        },
        {
            "servico": "BigQuery",
            "unidade": "TiB processados/mes",
            "quantidade_medida": round(bq_tib_month, 6),
            "preco_unitario_usd": PRICE_BQ_USD_PER_TIB,
            "custo_mensal_projetado_usd": round(bq_cost, 4),
            "como_mediu": (
                f"soma bronze+silver+gold = {bq_bytes_one} B/batch "
                f"(pipeline_runs e/ou evidence; dry_run Gold transform={dry_run_gold_bytes} B)"
            ),
            "premissa_cadencia": f"{batch_per_month} batch/mes (≈1/dia)",
            "always_free": f"primeiros {FREE_BQ_TIB} TiB/mes de query free",
        },
        {
            "servico": "Pub/Sub",
            "unidade": "GiB mensagens/mes",
            "quantidade_medida": round(pubsub_gib_month, 6),
            "preco_unitario_usd": PRICE_PUBSUB_USD_PER_TIB,
            "custo_mensal_projetado_usd": round(pubsub_cost, 4),
            "como_mediu": (
                f"payload medio demo n={pubsub_demo['n_messages']} "
                f"= {avg:.1f} B; throughput≈2× (publish+subscribe)"
            ),
            "premissa_cadencia": f"{events_per_day} eventos/dia × 30 dias",
            "always_free": f"primeiros {FREE_PUBSUB_GIB} GiB/mes free",
        },
        {
            "servico": "Computacao do job",
            "unidade": "segundos (serverless)",
            "quantidade_medida": round(batch_duration_s + stream_duration_s, 3),
            "preco_unitario_usd": 0.0,
            "custo_mensal_projetado_usd": 0.0,
            "como_mediu": compute_note,
            "premissa_cadencia": (
                f"{batch_per_month} batch/mes + consumer sob demanda "
                "(sem cluster Kafka/Spark ligado 24/7)"
            ),
            "always_free": "N/A — custo coberto nas linhas BQ/Pub/Sub",
        },
    ]
    return rows


def fmt_money(v: float) -> str:
    if abs(v) < 0.0001:
        return "$0.00"
    if abs(v) < 0.01:
        return f"${v:.4f}"
    return f"${v:.2f}"


def write_custo_md(
    path: Path,
    *,
    gcs: dict,
    gcs_detail: list[dict],
    run_summary: dict,
    dry_run_total: int,
    pubsub_demo: dict,
    cost_rows: list[dict],
    batch_per_month: int,
    events_per_day: int,
) -> None:
    latest = run_summary["latest_success"]
    today = date.today().isoformat()
    total_proj = sum(float(r["custo_mensal_projetado_usd"]) for r in cost_rows)
    within_free = total_proj < 0.01

    lines: list[str] = []
    lines.append("# FinOps — custo medido (Passo 9)")
    lines.append("")
    lines.append(f"**Data do snapshot:** {today}  ")
    lines.append(f"**Precos publicos consultados em:** {PRICING_AS_OF}  ")
    lines.append(
        f"**Fontes:** [GCS]({PRICING_SOURCES['gcs']}) · "
        f"[BigQuery]({PRICING_SOURCES['bq']}) · "
        f"[Pub/Sub]({PRICING_SOURCES['pubsub']}) · "
        f"[Always Free]({PRICING_SOURCES['free']})"
    )
    lines.append("")
    lines.append("## Premissa de cadencia (projecao)")
    lines.append("")
    lines.append(
        "Os **bytes** e as **duracoes** abaixo vieram de API/log do projeto. "
        "A **cadencia** e premissa hipotetica de producao — nao e o que roda hoje:"
    )
    lines.append("")
    lines.append(f"- **Batch:** {batch_per_month} execucao(oes)/mes (≈ 1 batch/dia)")
    lines.append(f"- **Stream:** {events_per_day} eventos/dia")
    lines.append(
        "- A execucao atual do challenge (poucas runs manuais + demo de 20 eventos) "
        "**cabe no Always Free**. A coluna da direita e o custo **se** essa cadencia "
        "rodasse de forma continua **fora da cota gratuita** (apos descontar o free tier)."
    )
    lines.append("")
    lines.append("## Tabela de custo")
    lines.append("")
    lines.append(
        "| Servico | Unidade | Quantidade medida | Preco unitario | "
        "Custo mensal projetado |"
    )
    lines.append(
        "|---------|---------|-------------------|----------------|------------------------|"
    )
    for r in cost_rows:
        q = r["quantidade_medida"]
        if r["servico"] == "BigQuery":
            q_s = f"{q:.6f} TiB/mes"
            price_s = f"${r['preco_unitario_usd']:.2f}/TiB"
        elif r["servico"] == "Pub/Sub":
            q_s = f"{q:.6f} GiB/mes"
            price_s = f"${r['preco_unitario_usd']:.0f}/TiB"
        elif r["servico"] == "Cloud Storage":
            q_s = f"{q:.6f} GiB"
            price_s = f"${r['preco_unitario_usd']:.3f}/GiB-mes"
        else:
            q_s = f"{q:.1f} s (ref. 1 ciclo)"
            price_s = "embutido (serverless)"
        lines.append(
            f"| {r['servico']} | {r['unidade']} | {q_s} | {price_s} | "
            f"{fmt_money(float(r['custo_mensal_projetado_usd']))} |"
        )
    lines.append(
        f"| **Total projetado (apos free tier)** | | | | **{fmt_money(total_proj)}** |"
    )
    lines.append("")
    if within_free:
        lines.append(
            "> **Leitura:** com a cadencia acima, o uso estimado ainda fica "
            "**dentro do Always Free** (custo projetado ≈ $0 apos o free tier). "
            "O valor didatico da tabela e mostrar a conta com quantidade real, "
            "nao inventar fatura."
        )
    else:
        lines.append(
            f"> **Leitura:** custo mensal projetado ≈ **{fmt_money(total_proj)}** "
            "apos o free tier, se a cadencia de producao fosse sustentada."
        )
    lines.append("")
    lines.append("## De onde veio cada quantidade")
    lines.append("")
    lines.append("### Cloud Storage (tamanho real do bucket)")
    lines.append("")
    lines.append(f"- Bucket: `{gcs['bucket']}`")
    lines.append(f"- Objetos: **{gcs['objects']}**")
    lines.append(
        f"- Bytes: **{gcs['bytes']}** ({gcs['gib']:.6f} GiB)"
    )
    lines.append("")
    lines.append("| prefixo | objetos | bytes | GiB |")
    lines.append("|---------|---------|-------|-----|")
    for d in gcs_detail:
        lines.append(
            f"| `{d['prefix']}` | {d['objects']} | {d['bytes']} | {d['gib']:.6f} |"
        )
    lines.append("")
    lines.append("### BigQuery (`pipeline_runs` + dry_run Gold)")
    lines.append("")
    lines.append(
        "Bytes/duracao por etapa — `pipeline_runs` quando existir; senao evidencias "
        "dos passos anteriores (mesmos jobs, sem chute):"
    )
    lines.append("")
    lines.append("| etapa | run_id | duration_s | bytes_processed | fonte |")
    lines.append("|-------|--------|------------|-----------------|-------|")
    sources = run_summary.get("sources") or {}
    for etapa in ("bronze", "silver", "gold", "stream"):
        row = latest.get(etapa)
        src = sources.get(etapa, "—")
        if not row:
            lines.append(f"| {etapa} | — | — | — | — |")
            continue
        bp = row.get("bytes_processed")
        bp_s = str(bp) if bp is not None else "null"
        dur = row.get("duration_seconds")
        dur_s = f"{float(dur):.3f}" if dur is not None else "n/d"
        lines.append(
            f"| {etapa} | `{row['run_id']}` | {dur_s} | {bp_s} | `{src}` |"
        )
    lines.append("")
    lines.append(
        f"- Soma batch (bronze+silver+gold) por execucao: "
        f"**{run_summary['batch_bytes_one_run']}** bytes"
    )
    lines.append(
        f"- Dry-run Gold (`evidence/passo_06/dry_run_bytes.csv`): "
        f"**{dry_run_total}** bytes"
    )
    lines.append(
        f"- Duracao batch medida: "
        f"**{run_summary['batch_duration_s_one_run']:.1f}** s"
    )
    if run_summary.get("stream_latency_avg_s") is not None:
        lines.append(
            f"- Latencia media stream (Passo 7/8): "
            f"**{run_summary['stream_latency_avg_s']:.3f}** s"
        )
    lines.append("")
    lines.append("### Pub/Sub (bytes do teste)")
    lines.append("")
    lines.append(
        f"- Lote demo igual ao producer (`n={pubsub_demo['n_messages']}`, "
        f"seed={pubsub_demo['seed']}): "
        f"**{pubsub_demo['total_payload_bytes']}** bytes de payload"
    )
    lines.append(
        f"- Media por mensagem: **{pubsub_demo['avg_payload_bytes']:.1f}** B"
    )
    lines.append(
        f"- Throughput estimado (publish + subscribe ≈ 2×): "
        f"**{pubsub_demo['throughput_bytes_estimate']}** B no lote de teste"
    )
    lines.append(
        f"- Projecao: media × {events_per_day} eventos/dia × 30 × 2"
    )
    lines.append("")
    lines.append("## Decisoes de arquitetura que a aula de FinOps pede")
    lines.append("")
    lines.append(
        "| Decisao | Por que baixa o custo neste projeto |"
    )
    lines.append("|---------|-------------------------------------|")
    lines.append(
        "| **Parquet comprimido** no lake | Menos GiB no GCS e menos bytes lidos "
        "quando o BigQuery varre external/export |"
    )
    lines.append(
        "| **Particao** por `ingestion_date`/`run_id` (Bronze) e por `ano` "
        "(Silver/Gold) | Evita full scan; dry_run do Passo 6 mostra o volume "
        "real por statement |"
    )
    lines.append(
        "| **Colunas explicitas** (sem `SELECT *` na extracao) | Menos "
        "`bytes_processed` no EXPORT e nas transforms |"
    )
    lines.append(
        "| **GCS `us-central1` + BigQuery `US`** | Mesma area geografica; "
        "sem cobranca de transferencia desnecessaria lake→warehouse |"
    )
    lines.append(
        "| **Pub/Sub + consumer sob demanda** (sem cluster Kafka 24/7) | "
        "Paga so pelo throughput do evento; aula trata cluster ligado o tempo "
        "todo como custo continuo |"
    )
    lines.append(
        "| **SQL serverless no BigQuery** (sem Spark/GKE) | Job liga e "
        "desliga; a linha de computacao nao tem VM ociosa |"
    )
    lines.append(
        "| **Alerta de billing R$ 1,00** (Passo 1) | Freio financeiro antes "
        "do uso sair do free tier |"
    )
    lines.append("")
    lines.append("## Como reproduzir")
    lines.append("")
    lines.append("```powershell")
    lines.append("python ops/finops_snapshot.py")
    lines.append(
        "python ops/finops_snapshot.py --batch-per-month 30 --events-per-day 1000"
    )
    lines.append("```")
    lines.append("")
    lines.append(
        "Artefatos: `gcs_objects_by_prefix.csv`, `pipeline_runs_snapshot.csv`, "
        "`cost_projection.csv`, `pubsub_payload_sample.csv`, este `custo.md`."
    )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] escrito {path}")


def write_readme(path: Path, *, within_free: bool, total_proj: float) -> None:
    status = "dentro do Always Free" if within_free else f"≈ {fmt_money(total_proj)}/mes"
    text = f"""# Passo 9 — FinOps com numero medido

- comando: `python ops/finops_snapshot.py`
- saida principal: [`custo.md`](custo.md)
- precos publicos GCP consultados em: **{PRICING_AS_OF}**
- cadencia de projecao (premissa): **1 batch/dia** + **1000 eventos/dia**
- leitura: execucao atual do challenge cabe no Always Free; projecao com cadencia = **{status}**

## Criterio de pronto

| check | resultado |
|-------|-----------|
| quantidade GCS via API | `gcs_objects_by_prefix.csv` |
| bytes/duracao de `pipeline_runs` | `pipeline_runs_snapshot.csv` |
| dry_run Gold (Passo 6) | referenciado em `custo.md` |
| bytes Pub/Sub do lote demo | `pubsub_payload_sample.csv` |
| tabela custo + premissa na mesma pagina | `custo.md` |

## Artefatos

| arquivo | o que prova |
|---------|-------------|
| `custo.md` | tabela + premissas + decisoes FinOps |
| `cost_projection.csv` | mesma tabela em CSV |
| `gcs_objects_by_prefix.csv` | tamanho real do bucket |
| `pipeline_runs_snapshot.csv` | bytes e duracao medidos |
| `pubsub_payload_sample.csv` | bytes do payload do teste |
"""
    path.write_text(text, encoding="utf-8")
    print(f"[OK] escrito {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot FinOps (Passo 9)")
    parser.add_argument(
        "--batch-per-month",
        type=int,
        default=30,
        help="Cadencia hipotetica de batch/mes (default 30 ≈ 1/dia)",
    )
    parser.add_argument(
        "--events-per-day",
        type=int,
        default=1000,
        help="Cadencia hipotetica de eventos Pub/Sub por dia (default 1000)",
    )
    parser.add_argument(
        "--pubsub-n",
        type=int,
        default=20,
        help="Tamanho do lote demo para medir payload (default 20)",
    )
    args = parser.parse_args()

    project_id, bq = load_env_and_client(ROOT)
    bucket_name = load_bucket_name()
    print(f"[INFO] projeto={project_id} bucket={bucket_name}")

    gcs_detail, gcs = measure_gcs(bucket_name)
    runs = fetch_pipeline_runs(bq, project_id)
    dry_rows, dry_total = load_dry_run_gold()
    run_summary = summarize_runs(runs, dry_run_gold_bytes=dry_total)
    pubsub_demo = measure_pubsub_demo(n=args.pubsub_n, seed=42)

    cost_rows = project_costs(
        gcs_gib=float(gcs["gib"]),
        batch_bytes_one_run=int(run_summary["batch_bytes_one_run"]),
        dry_run_gold_bytes=dry_total,
        pubsub_demo=pubsub_demo,
        batch_per_month=args.batch_per_month,
        events_per_day=args.events_per_day,
        batch_duration_s=float(run_summary["batch_duration_s_one_run"]),
        stream_duration_s=float(run_summary["stream_duration_s_one_run"]),
    )
    total_proj = sum(float(r["custo_mensal_projetado_usd"]) for r in cost_rows)
    within_free = total_proj < 0.01

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "gcs_objects_by_prefix.csv", gcs_detail)
    write_csv(OUT / "pipeline_runs_snapshot.csv", runs)
    write_csv(OUT / "cost_projection.csv", cost_rows)
    if dry_rows:
        write_csv(OUT / "dry_run_gold_ref.csv", dry_rows)
    write_csv(
        OUT / "pubsub_payload_sample.csv",
        [
            {
                "n_messages": pubsub_demo["n_messages"],
                "total_payload_bytes": pubsub_demo["total_payload_bytes"],
                "avg_payload_bytes": round(pubsub_demo["avg_payload_bytes"], 2),
                "throughput_bytes_estimate": pubsub_demo["throughput_bytes_estimate"],
                "seed": pubsub_demo["seed"],
            }
        ],
    )

    write_custo_md(
        OUT / "custo.md",
        gcs=gcs,
        gcs_detail=gcs_detail,
        run_summary=run_summary,
        dry_run_total=dry_total,
        pubsub_demo=pubsub_demo,
        cost_rows=cost_rows,
        batch_per_month=args.batch_per_month,
        events_per_day=args.events_per_day,
    )
    write_readme(OUT / "README.md", within_free=within_free, total_proj=total_proj)

    print(
        f"[OK] Passo 9 concluido -> {OUT} | "
        f"custo_projetado_usd={total_proj:.4f} within_always_free={within_free}"
    )


if __name__ == "__main__":
    main()
