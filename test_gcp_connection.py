import os
import sys

from dotenv import load_dotenv
from google.cloud import storage, bigquery, pubsub_v1

# Carrega as variáveis do .env
load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
bucket_name = os.getenv("GCP_BUCKET_NAME")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Define a variável de ambiente para que as bibliotecas achem automaticamente
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

print("=" * 60)
print(f"TESTANDO CONEXÃO COM O GCP - PROJETO: {project_id}")
print("=" * 60)

failures: list[str] = []

# 1. Cloud Storage
try:
    gcs_client = storage.Client(project=project_id)
    bucket = gcs_client.get_bucket(bucket_name)
    print(f"[OK] Cloud Storage: Bucket '{bucket.name}' ativo na região '{bucket.location}'.")
except Exception as e:
    failures.append(f"Cloud Storage: {e}")
    print(f"[ERRO] Cloud Storage: {e}")

# 2. BigQuery (Consulta pública na Base dos Dados)
try:
    bq_client = bigquery.Client(project=project_id, location="US")
    query = """
        SELECT nome_coluna, chave, cobertura_temporal
        FROM `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
        LIMIT 5
    """
    df = bq_client.query(query).to_dataframe()
    print(f"[OK] BigQuery: Conexão bem-sucedida! {len(df)} linhas retornadas da Base dos Dados.")
    print("\nAmostra do dicionário:")
    print(df.to_string(index=False))
except Exception as e:
    failures.append(f"BigQuery: {e}")
    print(f"[ERRO] BigQuery: {e}")

# 3. Pub/Sub — get_topic falha se o tópico de streaming não existir
publisher = pubsub_v1.PublisherClient()
try:
    topic_path = publisher.topic_path(project_id, "alfabetizacao-stream-topic")
    topic = publisher.get_topic(request={"topic": topic_path})
    print(f"\n[OK] Pub/Sub: Tópico '{topic.name}' existe e respondeu ao get_topic.")
except Exception as e:
    failures.append(f"Pub/Sub stream: {e}")
    print(f"[ERRO] Pub/Sub: tópico alfabetizacao-stream-topic não encontrado. {e}")

# O tópico de alerta nasce no Passo 8 (ops/telemetry.ensure_alert_topic).
# Ausência aqui não derruba o teste de ambiente.
try:
    alert_path = publisher.topic_path(project_id, "alfabetizacao-alertas")
    alert_topic = publisher.get_topic(request={"topic": alert_path})
    print(f"[OK] Pub/Sub: Tópico de alerta '{alert_topic.name}' respondeu ao get_topic.")
except Exception:
    print(
        "[AVISO] Tópico alfabetizacao-alertas ainda não existe. "
        "O Passo 8 cria esse tópico na primeira falha bloqueante."
    )

print("=" * 60)
if failures:
    print(f"[FALHA] {len(failures)} checagem(ns) obrigatória(s) falharam.")
    print("=" * 60)
    sys.exit(1)

print("Ambiente configurado: Storage, BigQuery e o tópico de streaming responderam.")
print("=" * 60)
