# Gold — o que foi criado, por quê, e o que o Challenge pede

Camada **Gold** do pipeline Medalhão (Passo 6).  
Fonte: Silver (`alfabetizacao_silver`). Destino: BigQuery `alfabetizacao_gold` + Parquet em `gs://…/gold/`.  
Evidência da run: [`evidence/passo_06/`](../evidence/passo_06/).

Este documento responde: **o que existe**, **por que existe** e **qual exigência do Tech Challenge / rubrica cada peça cobre**.

---

## 1. O que o Challenge cobra (e onde a Gold entra)

| Pts (rubrica) | Critério | Como a Gold contribui |
|---------------|----------|-------------------------|
| **15** | Arquitetura **Medalhão** | Produtos analíticos em `alfabetizacao_gold` + export Parquet no lake |
| (base) | Três perguntas do enunciado | `indicador_municipio`, `meta_vs_resultado`, `evolucao_temporal` |
| (aula) | Agregações / CTE / window | `LAG` em `evolucao_temporal`; CTEs em `meta_vs_resultado` e microdado |
| (aula) | Data Mesh | Cada tabela = produto com schema no contrato e descrição de uma linha |
| (aula) | Otimização / FinOps | Partição por `ano`, cluster geo, `dry_run` com `total_bytes_processed` |

Decisões desta camada: [`DECISOES.md`](DECISOES.md).

O que a Gold **não** faz (passos seguintes, já entregues à parte):

- Streaming simulado (`origem = simulado`) — Passo 7 (`streaming/`, `eventos_stream`)
- `pipeline_runs` / alertas — Passo 8 (`ops/`)
- Tabela FinOps projetada — Passo 9

Gate: **só publica se o `join_match` bloqueante da Silver passou** (re-medido no início de `build.py`).

---

## 2. Fluxo operacional

```text
Silver (run_id) + join_match OK
    → python gold/build.py
        → gate Silver (3 join_match)
        → dry_run de cada statement (bytes)
        → sql/03_gold.sql  (5 CREATE TABLE)
        → EXPORT DATA Parquet → gs://…/gold/<produto>/…
        → SELECT de conferencia (CE 2024; Brasil 2024)
        → evidence/passo_06/
        → exit 0 se conferencia OK
```

Comandos:

```powershell
python gold/build.py
python gold/build.py --run_id 20d3623d0430
```

---

## 3. Artefatos de código

| Arquivo | Papel |
|---------|--------|
| [`build.py`](build.py) | Orquestrador: gate, dry_run, SQL, export, conferencia, evidência |
| [`../sql/03_gold.sql`](../sql/03_gold.sql) | 5 produtos `CREATE OR REPLACE TABLE` |
| [`../quality/config.py`](../quality/config.py) | `GOLD_DATASET`, `GOLD_TABLES` |

---

## 4. Dataset e produtos

**Dataset:** `alfabetizacao_gold` (padrão `alfabetizacao_<camada>`).

**Partição:** `RANGE_BUCKET(ano, …)`. **Cluster:** `id_municipio` / `sigla_uf` / `nivel_geo` conforme o grain.

**Coluna técnica:** `origem = 'oficial'`, `run_id_bronze`.

| Produto | Uma linha é | Uso |
|---------|-------------|-----|
| `indicador_municipio` | município + ano + rede + série | painel e Fase 3 |
| `indicador_uf` | UF + ano + rede + série | comparação estadual |
| `meta_vs_resultado` | geo + ano (+ série no mun/UF) × meta pactuada | distância até a meta 80; status `atingiu` / `nao_atingiu` / `sem_meta` |
| `evolucao_temporal` | mesma chave no tempo + `LAG` | trajetória (`delta_pp`), não previsão |
| `validacao_microdado` | mun×ano×rede×série | taxa ponderada dos `alunos` vs taxa oficial |

### Regras de cálculo

- Meta × resultado na **mesma** rede (já alinhada na Silver: `3`↔Municipal, `5`↔Pública).
- Meta ausente / `NULL` → `sem_meta` (terceiro estado).
- `NULL` de taxa (ex.: RR) permanece `NULL`; não vira 0.
- Microdado: denominador = presentes com `peso_aluno`; numerador = alfabetizados presentes (`presenca='1'`, `alfabetizado='1'`).

### Fase 3 / ML (vazamento)

- **Alvo típico:** `taxa_alfabetizacao` futura ou `status_meta` / `gap_pp`.
- **Não usar como feature do mesmo ano-alvo:** a própria `taxa_alfabetizacao`, `meta_alfabetizacao_2030` do mesmo ano, nem `status_meta` derivado deles.
- Colunas candidatas a feature (exemplos): histórico (`taxa_anterior`, `delta_pp` de anos anteriores), composição de níveis, presença/participação — nunca o rótulo que o modelo tentaria prever.

---

## 5. Conferência (critério de pronto)

| Check | Esperado (perfil Passo 2) | Resultado da run |
|-------|---------------------------|------------------|
| UF `CE`, 2024, rede `5` | taxa ≈ 85,31 | bate |
| Brasil 2024 (meta pública) | taxa 59,2 / meta 80 | bate (`nao_atingiu`) |

Evidência: [`evidence/passo_06/conferencia.csv`](../evidence/passo_06/conferencia.csv).

---

## 6. Relação com o enunciado

| Pedido do guia | Onde |
|----------------|------|
| Indicador por município | `indicador_municipio` |
| Meta × resultado | `meta_vs_resultado` |
| Evolução temporal | `evolucao_temporal` |
| Validação cruzada microdado | `validacao_microdado` |
| Guardar Gold no lake | `EXPORT DATA` → `gs://…/gold/` |
| dry_run / bytes | `evidence/passo_06/dry_run_bytes.csv` |
