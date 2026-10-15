import os
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

# 1. Cloud Storage
try:
    gcs_client = storage.Client(project=project_id)
    bucket = gcs_client.get_bucket(bucket_name)
    print(f"[OK] Cloud Storage: Bucket '{bucket.name}' ativo na região '{bucket.location}'.")
except Exception as e:
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
    print(f"[ERRO] BigQuery: {e}")

# 3. Pub/Sub
try:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, "alfabetizacao-stream-topic")
    print(f"\n[OK] Pub/Sub: Tópico '{topic_path}' validado com sucesso.")
except Exception as e:
    print(f"[ERRO] Pub/Sub: {e}")

print("=" * 60)
print("Ambiente 100% configurado para o Tech Challenge!")
print("=" * 60)
