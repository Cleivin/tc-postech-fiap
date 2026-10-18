"""Pub/Sub producer — eventos simulados de indicador municipal (Passo 7).

Uso:
  python streaming/producer.py
  python streaming/producer.py --n 20 --seed 42
"""
from __future__ import annotations

import argparse
import json
import os
import random
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import pubsub_v1

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "alfabetizacao-stream-topic"

SAMPLE_MUNICIPIOS = [
    "2304400",  # Fortaleza
    "3550308",  # Sao Paulo
    "3304557",  # Rio de Janeiro
    "3106200",  # Belo Horizonte
    "4106902",  # Curitiba
    "2927408",  # Salvador
    "2611606",  # Recife
    "1302603",  # Manaus
    "1501402",  # Belem
    "5208707",  # Goiania
]


def load_project() -> str:
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

    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise SystemExit("[ERRO] GCP_PROJECT_ID e obrigatorio no .env.")
    return project_id


def make_valid_skeleton(rng: random.Random) -> dict:
    """Evento valido sem produced_at (preenchido no publish)."""
    return {
        "event_id": str(uuid.uuid4()),
        "entidade": "municipio",
        "chave": {
            "id_municipio": rng.choice(SAMPLE_MUNICIPIOS),
            "ano": rng.choice([2023, 2024]),
            "rede": rng.choice(["3", "5"]),
            "serie": rng.choice(["2", "3"]),
        },
        "valor": round(rng.uniform(40.0, 95.0), 2),
        "origem": "simulado",
    }


def make_invalid_payload(rng: random.Random) -> bytes:
    kind = rng.choice(["missing_chave", "bad_valor", "broken_json"])
    if kind == "broken_json":
        return b'{"event_id":"broken","produced_at":"not-json"'
    if kind == "bad_valor":
        body = {
            "event_id": str(uuid.uuid4()),
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "entidade": "municipio",
            "chave": {
                "id_municipio": "2304400",
                "ano": 2024,
                "rede": "5",
                "serie": "2",
            },
            "valor": 150.0,
            "origem": "simulado",
        }
        return json.dumps(body, ensure_ascii=False).encode("utf-8")
    body = {
        "event_id": str(uuid.uuid4()),
        "produced_at": datetime.now(timezone.utc).isoformat(),
        "entidade": "municipio",
        "valor": 70.0,
        "origem": "simulado",
    }
    return json.dumps(body, ensure_ascii=False).encode("utf-8")


def plan_labels(n: int) -> list[str]:
    """Ordem fixa: valid_* → invalid → duplicate (duplicata sempre por ultimo)."""
    if n >= 3:
        return [f"valid_{i+1}" for i in range(n - 2)] + ["invalid", "duplicate"]
    if n == 2:
        return ["valid_1", "invalid"]
    return ["valid_1"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Publica eventos simulados no Pub/Sub")
    parser.add_argument("--n", type=int, default=20, help="Total de mensagens (default 20)")
    parser.add_argument("--seed", type=int, default=None, help="Seed para reprodutibilidade")
    args = parser.parse_args()

    if args.n < 1:
        raise SystemExit("[ERRO] --n deve ser >= 1")

    project_id = load_project()
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, TOPIC_ID)
    rng = random.Random(args.seed)

    labels = plan_labels(args.n)
    print(f"[INFO] projeto={project_id} topic={TOPIC_ID} n={len(labels)}")

    first_valid_payload: bytes | None = None
    published: list[dict] = []

    for label in labels:
        if label.startswith("valid"):
            event = make_valid_skeleton(rng)
            event["produced_at"] = datetime.now(timezone.utc).isoformat()
            payload = json.dumps(event, ensure_ascii=False).encode("utf-8")
            if first_valid_payload is None:
                first_valid_payload = payload
        elif label == "duplicate":
            if first_valid_payload is None:
                raise SystemExit("[ERRO] duplicata sem evento valido previo")
            payload = first_valid_payload
        else:
            payload = make_invalid_payload(rng)

        future = publisher.publish(topic_path, payload)
        msg_id = future.result(timeout=60)
        try:
            body = json.loads(payload.decode("utf-8"))
            event_id = body.get("event_id", "?")
        except json.JSONDecodeError:
            event_id = "(broken_json)"
        published.append({"label": label, "event_id": event_id, "pubsub_message_id": msg_id})
        print(f"  [OK] {label} event_id={event_id} message_id={msg_id}")

    n_valid = sum(1 for p in published if str(p["label"]).startswith("valid"))
    n_invalid = sum(1 for p in published if p["label"] == "invalid")
    n_dup = sum(1 for p in published if p["label"] == "duplicate")
    print(
        f"[OK] publicados={len(published)} "
        f"valid={n_valid} invalid={n_invalid} duplicate={n_dup}"
    )


if __name__ == "__main__":
    main()
