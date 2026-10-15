# Tech Challenge — Fase 2: Pipeline Híbrido de Dados (Alfabetização no Brasil)

**Pós-Graduação:** POSTECH — AI Scientist (IAST) | **FIAP**  
**Cloud:** Google Cloud Platform (GCP) — Always Free (`us-central1`)

Pipeline batch + streaming com arquitetura Medalhão (Bronze → Silver → Gold) sobre dados do INEP / Base dos Dados.

---

## Pré-requisitos

- **Python 3.10+** (`python --version` ou `python3 --version`)
- Conta no **Google Cloud** com um projeto ativo
- **Git** instalado
- (Opcional) [Google Cloud SDK](https://cloud.google.com/sdk) para gerar a chave da Service Account

---

## Instalação (qualquer computador)

### 1. Clonar o repositório

```bash
git clone https://github.com/<SEU_USUARIO>/tc-postech-fiap.git
cd tc-postech-fiap
```

> Substitua `<SEU_USUARIO>` pelo seu usuário do GitHub.

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

O prompt deve mostrar `(.venv)` no início da linha.

### 3. Instalar as dependências

Com a `.venv` ativa:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Edite o arquivo `.env` com os dados do **seu** projeto GCP:

```env
GCP_PROJECT_ID=seu-projeto-gcp
GCP_BUCKET_NAME=seu-bucket-datalake
GOOGLE_APPLICATION_CREDENTIALS=credentials/gcp-sa-key.json
GCP_LOCATION=us-central1
BIGQUERY_LOCATION=US
```

### 5. Credencial da Service Account

1. Crie (ou use) uma Service Account no GCP com permissões de Storage, BigQuery e Pub/Sub.
2. Baixe a chave JSON.
3. Salve como:

```text
credentials/gcp-sa-key.json
```

A pasta `credentials/` já existe no repositório (vazia no Git). Os arquivos `.env` e `credentials/*.json` **não** são versionados.

**Gerar chave via Cloud Shell (exemplo):**

```bash
gcloud iam service-accounts keys create ~/gcp-sa-key.json \
  --iam-account=sa-pipeline-educacao@SEU_PROJETO.iam.gserviceaccount.com

cloudshell download ~/gcp-sa-key.json
```

Mova o arquivo baixado para `credentials/gcp-sa-key.json`.

### 6. Testar a conexão com o GCP

Com a `.venv` ativa e o `.env` configurado:

```bash
python test_gcp_connection.py
```

Saída esperada: `[OK]` em Cloud Storage, BigQuery e Pub/Sub.

---

## Arquitetura (resumo)

| Camada | Serviço |
|--------|---------|
| Data Lake | Cloud Storage — Parquet particionado (Bronze / Silver / Gold) |
| Warehouse | BigQuery — dataset público `basedosdados.br_inep_avaliacao_alfabetizacao` |
| Streaming | Pub/Sub — tópico `alfabetizacao-stream-topic` |
| FinOps | Alerta de billing em R$ 1,00 |

Passo a passo de implementação: [docs/Tech_Challenge_Fase2_Passo_a_Passo.md](docs/Tech_Challenge_Fase2_Passo_a_Passo.md)

---

## Estrutura do projeto

```text
tc-postech-fiap/
├── .env.example                 # modelo de variáveis (versionado)
├── .env                         # suas credenciais locais (não versionado)
├── .venv/                       # ambiente local (não versionado)
├── credentials/                 # chave GCP local (não versionada)
├── requirements.txt
├── test_gcp_connection.py
├── docs/                        # aulas + passo a passo do challenge
├── bronze/  silver/  gold/      # pipelines (Medalhão)
├── quality/ streaming/ evidence/
```

---

## Troubleshooting rápido

| Problema | O que fazer |
|----------|-------------|
| `python` não encontrado | Use `python3` ou instale o Python 3.10+ e marque “Add to PATH” |
| Falha ao ativar `.venv` no PowerShell | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `[ERRO] Cloud Storage` / BigQuery | Confira `GCP_PROJECT_ID`, bucket e o caminho da chave no `.env` |
| Arquivo de chave não encontrado | Garanta que `credentials/gcp-sa-key.json` existe na raiz do projeto |
