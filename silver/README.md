# Silver — o que foi criado, por quê, e o que o Challenge pede

Camada **Silver** do pipeline Medalhão (Passo 5).  
Fonte: Bronze (`alfabetizacao_bronze`). Destino: BigQuery `alfabetizacao_silver`.  
Evidência da run: [`evidence/passo_05/`](../evidence/passo_05/).

Este documento responde: **o que existe**, **por que existe** e **qual exigência do Tech Challenge / rubrica cada peça cobre**.

---

## 1. O que o Challenge cobra (e onde a Silver entra)

| Pts (rubrica) | Critério | Como a Silver contribui |
|---------------|----------|-------------------------|
| **15** | Arquitetura **Medalhão** (Bronze → Silver → Gold) | Dataset real `alfabetizacao_silver` com dados limpos/tipados/juntados — não só pasta vazia |
| **10** | **Qualidade** | Taxa de match do join (`join_match`) persistida em `quality_checks`, com limiar bloqueante justificado |
| (base) | **ELT** / warehouse | Transformação em **SQL no BigQuery**; Bronze permanece cru (Parquet + external tables) |
| (aula) | Spark / Medalhão (carga Silver) | Mesmo papel da aula: limpar, tipar, deduplicar conceito, deixar tabelas reutilizáveis — aqui sem cluster Spark |
| (guia) | SQL (chaves, `NULL`, CTE) + partição | Joins com tipos alinhados; `NULL` preservado; tabelas particionadas por `ano` |

O que a Silver **não** faz (fica para o Passo 6 — Gold):

- Produtos analíticos (`indicador_municipio`, `meta_vs_resultado`, `evolucao_temporal`, etc.)
- Responder as 3 perguntas do enunciado com agregações finais
- Export Parquet em `gs://.../gold/`

A Silver **prepara** o terreno: chaves certas, `rede` traduzida, fato×meta já juntados, qualidade de join auditável.

---

## 2. Fluxo operacional

```text
Bronze (run_id)
    → python silver/transform.py
        → sql/02_silver.sql  (10 CREATE TABLE)
        → calcula 3 join_match
        → APPEND em alfabetizacao_ops.quality_checks
        → exit 0 se todos ≥ 0.95; senão exit 1
    → python quality/validate.py --layer silver
        → recalcula regras (prova independente)
        → APPEND de novo + evidence/passo_05/
```

Comandos:

```powershell
python silver/transform.py
python silver/transform.py --run_id 20d3623d0430
python quality/validate.py --layer silver
```

---

## 3. Artefatos de código (arquivo a arquivo)

### 3.1 [`transform.py`](transform.py) — orquestrador

**O quê:** Script Python que:

1. Resolve `run_id` da Bronze (última por `MAX(ingestion_ts)`, ou `--run_id`).
2. Garante o dataset `alfabetizacao_silver` (US).
3. Lê e executa [`sql/02_silver.sql`](../sql/02_silver.sql) no BigQuery.
4. Conta linhas das 10 tabelas.
5. Mede `join_match` nos 3 joins, grava em `quality_checks`.
6. Registra `desconhecido_count` (informativo).
7. Escreve evidência em `evidence/passo_05/`.
8. Sai com **código ≠ 0** se algum `join_match` bloqueante falhar.

**Por quê:** O Challenge pede job reproduzível (não notebook manual). O gate `exit 1` cumpre a regra de qualidade: falha bloqueante **não publica** a camada seguinte (não avançar para Gold).

**Relação com o enunciado:** “pipeline batch” + “qualidade que interrompe” + evidência em pasta por passo.

---

### 3.2 [`../sql/02_silver.sql`](../sql/02_silver.sql) — transformação ELT

**O quê:** 10 statements `CREATE OR REPLACE TABLE` que tipam, traduzem códigos e materializam joins.

**Por quê:** Decisão de arquitetura do projeto = **ELT**: extrair cru na Bronze; transformar no warehouse (BigQuery). Evita trazer 3,8M de alunos para o pandas.

**Relação:** Medalhão “carga Silver” da aula (limpeza/tipagem) + aula de Cloud Data (SQL serverless, partição).

---

### 3.3 Pacote `quality/` (extensão Silver)

| Arquivo | Papel |
|---------|--------|
| [`../quality/config.py`](../quality/config.py) | `SILVER_DATASET`, `JOIN_MATCH_THRESHOLD = 0.95`, listas de tabelas/joins |
| [`../quality/rules_silver.py`](../quality/rules_silver.py) | `join_match`, `desconhecido_count`, `row_count` |
| [`../quality/validate.py`](../quality/validate.py) | Aceita `--layer bronze` **ou** `silver` |
| [`../quality/ops.py`](../quality/ops.py) | Já existia: `append` em `quality_checks` (reutilizado) |

**Por quê:** No Passo 4 a taxa de join foi **adiada de propósito** para o Passo 5. A rubrica de qualidade (10 pts) exige essa taxa persistida, não só log de terminal.

---

### 3.4 Documentação / contrato

| Arquivo | O que entrou no Passo 5 |
|---------|-------------------------|
| [`../docs/contrato_dados.md`](../docs/contrato_dados.md) | De-para `rede` + limiares Silver (`join_match ≥ 0.95`) |
| [`../README.md`](../README.md) | Linha com limiar 0.95 (critério de pronto do guia) |
| [`../docs/Tech_Challenge_Fase2_Passo_a_Passo.md`](../docs/Tech_Challenge_Fase2_Passo_a_Passo.md) | Passo 5 marcado como feito |
| [`../evidence/passo_05/`](../evidence/passo_05/) | Manifest, join_match, validate, README da run |

**Por quê:** A banca lê contrato + README + evidência. Limiar sem justificativa no contrato seria chute; a justificativa vem da cobertura medida no Passo 2 (~96–97%).

---

## 4. Dataset e tabelas BigQuery

**Dataset:** `alfabetizacao_silver` (padrão `alfabetizacao_<camada>` — proibido o invertido `silver_alfabetizacao`).

**Partição:** `RANGE_BUCKET(ano, …)` nas tabelas com `ano` (otimização / FinOps futuro: ler só partições usadas).

**Colunas técnicas comuns:** `origem = 'oficial'`, `run_id_bronze` (rastreio da partição Bronze).

### 4.1 Sete tabelas base (espelho limpo da fonte)

| Tabela | O que faz | Por quê o Challenge precisa |
|--------|-----------|-----------------------------|
| `dicionario` | Tipado; apoio à tradução | Traduzir códigos sem inventar rótulo |
| `alunos` | Tipado + `*_label` via dicionário; `proficiencia`/`peso` **sem** coalesce | Microdado tipado para validação cruzada futura (Gold); preservar NULL |
| `municipio` | Tipado + labels + `rede_para_meta` (`3`→`Municipal`) | Agregado oficial municipal pronto para join com meta |
| `uf` | Idem + `rede_para_meta` (`5`→`Pública`) | Agregado estadual |
| `meta_alfabetizacao_municipio` | Tipada; NULL preservado | Meta municipal (rótulo `Municipal`) |
| `meta_alfabetizacao_uf` | Tipada; NULL de RR preservado | Meta estadual (`Pública`) |
| `meta_alfabetizacao_brasil` | Tipada | Meta nacional 80 |

**Pedido do guia cumprido:**

- Padronizar nomes e tipos  
- Traduzir com `dicionario`; sem match → `desconhecido`  
- `NULL` continua `NULL` (não preencher meta/proficiência com 0)  
- `origem = 'oficial'` (separa depois o stream simulado do Passo 7)

### 4.2 Três tabelas de join (produto da Silver)

| Tabela | Join | Fórmula do match |
|--------|------|------------------|
| `municipio_com_meta` | `municipio` rede `3` ⟕ meta municipal em `ano` + `id_municipio` + `Municipal` | `COUNTIF(tem_meta) / COUNT(*)` |
| `uf_com_meta` | `uf` rede `5` ⟕ meta UF em `ano` + `sigla_uf` + `Pública` | idem |
| `brasil_com_meta` | `AVG` das UFs rede `5` ⟕ meta Brasil `Pública` | idem |

**Por quê LEFT JOIN:** município/UF sem meta deve aparecer com `tem_meta = false` e meta NULL — a lacuna fica visível e mensurável. INNER JOIN esconderia o problema e a qualidade mentiria.

**Por quê `brasil_com_meta` existe:** o guia pede “Brasil (agregado) × meta Brasil”. Não há tabela “Brasil” na fonte; agregamos UF pública. A coluna se chama `media_simples_ufs` de propósito (não fingir peso amostral nacional).

**Pedido do guia:** depois de **cada** join, calcular e persistir a taxa de match.

---

## 5. Anomalia de `rede` (de-para) — peça central

No Passo 2 descobriu-se que:

- Fato/agregado usa códigos (`"2"`, `"3"`, `"5"`, …)
- Metas usam rótulos (`Municipal`, `Pública`)

Join direto por `rede` → match ~0% → pipeline “passa” com dado errado ou trava sem motivo claro.

| Lado fato | Código | Rótulo na meta | Onde |
|-----------|--------|----------------|------|
| município | `3` | `Municipal` | `municipio_com_meta` |
| UF / Brasil agg | `5` | `Pública` | `uf_com_meta`, `brasil_com_meta` |

Isso está no [`contrato_dados.md`](../docs/contrato_dados.md). É o diferencial de entendimento da fonte (Data Understanding → Silver).

---

## 6. Qualidade: bloqueante vs informativa

Alinhado ao Passo 4 e ao enunciado interno:

| Classe | Regra Silver | Limiar | Se falhar |
|--------|--------------|--------|-----------|
| **Bloqueante** | `join_match` (3 joins) | **≥ 0.95** | Grava `status=fail` em `quality_checks` + **`sys.exit(1)`** — Silver não publicável |
| **Informativa** | `desconhecido_count` | só registra | Grava e segue |
| **Informativa** | `row_count` | ≥ 1 | Grava; não mata o job sozinho |

**Justificativa do 0.95:** cobertura geo medida no Passo 2 (`06_cobertura_join_meta.csv`) ≈ 96,37% / 96,97%. Exigir 100% seria irrealista (~170 municípios sem meta).

**O que a rubrica exige e nós fazemos:**

- Persistência em tabela (`alfabetizacao_ops.quality_checks`), não só print  
- Exit code ≠ 0 em falha bloqueante  
- Sem `except` que engole erro e devolve sucesso  

**Run real (evidência):**

| Join | taxa_match | Status |
|------|------------|--------|
| `municipio_com_meta` | ~0,978 | pass |
| `uf_com_meta` | 1,0 | pass |
| `brasil_com_meta` | 1,0 | pass |

---

## 7. Mapa pedido do guia → implementação

| Pedido do Passo 5 (guia) | Onde está |
|--------------------------|-----------|
| Ler última `run_id` (ou parâmetro) | `transform.py` + `latest_run_id` / `--run_id` |
| Padronizar nomes/tipos | `02_silver.sql` (`CAST`, `TRIM`) |
| Traduzir códigos; senão `desconhecido` | joins com `dicionario` + `COALESCE(..., 'desconhecido')` |
| Normalizar tipos antes do JOIN | `CAST(... AS STRING)` nos dois lados |
| De-para rede | `rede_para_meta` + filtro `rede IN ('3','5')` |
| `taxa_match` após cada join | `rules_silver.measure_join_match` + `append_check` |
| Limiar justificado no contrato | `contrato_dados.md` + README raiz |
| Bloqueante se abaixo do limiar | `exit(1)` em `transform.py` e `validate.py` |
| `NULL` preservado | sem `COALESCE`/`IFNULL` em taxa/meta/proficiência |
| `origem = oficial` | literal em todos os `SELECT` |
| Joins município / UF / Brasil × meta | tabelas `*_com_meta` |
| `alunos` tipados | tabela `alfabetizacao_silver.alunos` |
| Dataset `alfabetizacao_silver`, partição por ano | dataset + `PARTITION BY RANGE_BUCKET(ano, …)` |
| Evidência | `evidence/passo_05/` |

---

## 8. Relação com as aulas (repertório)

| Aula | Conceito aplicado aqui |
|------|------------------------|
| Medalhão / Spark | Camada Silver = limpar + tipar + juntar; Gold agrega depois |
| Lake vs Warehouse | Bronze no lake (Parquet); Silver no warehouse (BQ nativo) |
| ETL/ELT | Extração completa na Bronze; transformação na Silver via SQL |
| SQL relacional | Chaves `ano` + geo + rede mapeada; dicionário como dimensão |
| Otimização | Partição por `ano`; só colunas do contrato (sem `SELECT *` na origem Bronze) |
| Data Mesh / governança | Checagem (`join_match`) antes de considerar a camada publicável |

---

## 9. Contagens da run de referência

`run_id_bronze = 20d3623d0430` (ver detalhes e job ids em [`evidence/passo_05/README.md`](../evidence/passo_05/README.md)):

| Tabela | Linhas |
|--------|--------|
| dicionario | 27 |
| alunos | 3.867.999 |
| municipio | 23.995 |
| uf | 145 |
| meta_alfabetizacao_municipio | 10.704 |
| meta_alfabetizacao_uf | 81 |
| meta_alfabetizacao_brasil | 3 |
| municipio_com_meta | 10.896 |
| uf_com_meta | 49 |
| brasil_com_meta | 2 |

---

## 10. O que fica explícito para a banca (frase pronta)

> A Bronze guarda o histórico oficial cru no GCS. A Silver, no BigQuery (`alfabetizacao_silver`), tipa as seis entidades, traduz códigos pelo `dicionario`, resolve a anomalia de encoding de `rede` com de-para documentado (`3`↔Municipal, `5`↔Pública), materializa os joins fato×meta e só considera a camada publicável se a taxa de match de cada join for ≥ 95%, valor justificado pela cobertura medida no perfil e persistido em `alfabetizacao_ops.quality_checks`.

---

## 11. Fora deste passo

Decisões desta camada: [`DECISOES.md`](DECISOES.md).

- Gold — Passo 6 (`gold/DECISOES.md`, `evidence/passo_06/`)
- Streaming, observabilidade e FinOps — Passos 7–9
- Vídeo — Passo 11, ainda não gravado
- Alerta Pub/Sub em falha — Passo 8 (aqui o mínimo é persistir + exit ≠ 0)
