# Passo 10 — README, evidências e clone

O texto que a banca lê na raiz é [`README.md`](../../README.md).  
A comparação passo a passo com o enunciado é [`docs/avaliacao_conformidade.md`](../../docs/avaliacao_conformidade.md).  
Decisões por pasta: `DECISOES.md` em `bronze/`, `sql/`, `quality/`, `silver/`, `gold/`, `streaming/`, `ops/`.  
Leitura de cada evidência: `ANALISE.md` dentro de `passo_01/` … `passo_09/`.

## O que este passo alterou no repositório

| Peça | Antes | Agora |
|------|--------|--------|
| `requirements.txt` | mínimos com `>=` | pins `==` das versões que geraram as evidências |
| `test_gcp_connection.py` | erro de tópico ainda encerrava com sucesso | exit 1 se Storage, BigQuery ou `alfabetizacao-stream-topic` falharem; alerta do Passo 8 é aviso |
| README da raiz | só setup | contexto, diagrama, trade-offs, FinOps, vazamento, limitações, comandos até o evento |
| Análises | dumps e índices | `ANALISE.md` por passo, com leitura dos números |
| Consultas extras | — | [`insights_consultas.md`](insights_consultas.md) (corte 743 e distribuição da Gold) |

Segredos: `git check-ignore` confirma `.env` (regra `.env`) e `credentials/gcp-sa-key.json` (regra `*-sa-key.json`). Os dois ficam de fora do Git.

## Caminho de um clone limpo

Não foi aberto um segundo projeto GCP nesta etapa. O caminho abaixo é o que o README manda executar, conferido contra os argumentos reais dos scripts. A run já versionada (`20d3623d0430`) continua sendo a prova de que esse caminho produziu Gold e consumiu evento.

Pré-requisitos que o código **não** cria: projeto, bucket em `us-central1`, chave da service account, tópico `alfabetizacao-stream-topic`, subscription Pull `alfabetizacao-stream-sub`. O tópico `alfabetizacao-alertas` é criado no Passo 8.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# editar .env e salvar a chave em credentials/gcp-sa-key.json
python test_gcp_connection.py
python bronze/ingest_batch.py
python quality/validate.py --layer bronze
python silver/transform.py
python quality/validate.py --layer silver
python gold/build.py
python streaming/producer.py --n 20
python streaming/consumer.py
```

`python quality/prove_failure.py` e `python ops/prove_observability.py` terminam com exit 1. `python ops/finops_snapshot.py` regrava `evidence/passo_09/custo.md`.

Um clone gera um `run_id` novo. Os CSV desta pasta de evidências permanecem os da run `20d3623d0430`.

## Vídeo

Vídeo do Passo 11: https://youtu.be/xUfqOCZPeNk. O mesmo endereço está no README da raiz.
