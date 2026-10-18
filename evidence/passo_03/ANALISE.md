# Passo 3 — análise das evidências

Run de referência: `20d3623d0430`. Run anterior, ainda no bucket: `f92c40cfe9a7`.

| Arquivo | O que é |
|---------|---------|
| `manifest_20d3623d0430.csv` e `manifest.csv` | Uma linha por entidade: job de export, job de contagem, linhas, bytes, URI, arquivos Parquet, external table |
| `manifest_f92c40cfe9a7.csv` | A primeira run, no mesmo dia, com outro `run_id` |
| `gcs_run_prefixes.txt` | Os dois prefixos de cada entidade |
| `README.md` | O mesmo manifesto em tabela |

## O que os números provam

As sete contagens são idênticas ao Passo 2. A coluna `n_linhas_external` repete `n_linhas`: o que saiu do BigQuery público voltou inteiro pela external table. Não houve filtro de negócio.

| Entidade | Linhas | Bytes processados no export | Arquivos |
|----------|--------|-----------------------------|----------|
| alunos | 3.867.999 | 268.545.240 | 11 |
| municipio | 23.995 | 1.832.061 | 1 |
| meta município | 10.704 | 1.151.232 | 1 |
| uf | 145 | 10.330 | 1 |
| meta UF | 81 | 7.374 | 1 |
| dicionário | 27 | 1.174 | 1 |
| meta Brasil | 3 | 270 | 1 |

O microdado é 99% dos bytes desta extração (268,5 MiB de 271,5 MiB). Os outros seis objetos são pequenos. É o argumento prático para não usar `SELECT *` e para não descer o aluno até o pandas: o custo e o risco estão nessa tabela, e ela já cabe num export Parquet particionado.

Os dois `run_id` aparecem lado a lado em `gcs_run_prefixes.txt`. A segunda execução não truncou a primeira. A external table aponta para `bronze/<entidade>/*`, então as duas runs ficam visíveis. A Silver tem de filtrar `run_id` — senão o país dobra.

O manifesto não altera `rede`. Código e rótulo seguem crus, como o contrato pediu.
