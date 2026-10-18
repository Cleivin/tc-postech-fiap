# Contrato de dados — Avaliação da Alfabetização (INEP / Base dos Dados)

Fonte: `basedosdados.br_inep_avaliacao_alfabetizacao`  
Evidência: `evidence/passo_02/` (gerada por `sql/00_perfil.sql` via `sql/run_perfil.py`).

Warehouse (BigQuery): datasets no padrão `alfabetizacao_<camada>`. Dataset canônico da Bronze = `alfabetizacao_bronze` (external tables do Passo 3). Não criar `bronze_alfabetizacao` / `silver_alfabetizacao` / `gold_alfabetizacao`.

Nenhuma coluna abaixo foi inventada: nomes e tipos vêm do schema real + amostra.

---

## Mapa rápido de colunas (nomes reais)

| Conceito | Nome real | Onde aparece |
|----------|-----------|--------------|
| Ano | `ano` (INTEGER) | todas as 6 entidades |
| Município | `id_municipio` (STRING) | `alunos`, `municipio`, `meta_alfabetizacao_municipio` |
| UF | `sigla_uf` (STRING) | `uf`, `meta_alfabetizacao_uf` |
| Rede | `rede` (STRING) | todas — **encoding diverge** (ver anomalia) |
| Série | `serie` (STRING) | `alunos`, `municipio`, `uf` (valor observado: `2` = 2º ano EF) |
| Taxa | `taxa_alfabetizacao` (FLOAT) | `municipio`, `uf`, metas |
| Proficiência | `proficiencia` (FLOAT) | `alunos` |
| Presença | `presenca` (STRING, código) | `alunos` → `dicionario` |
| Peso | `peso_aluno` (FLOAT) | `alunos` |
| Meta 2030 pactuada | `meta_alfabetizacao_2030` (FLOAT) | metas; rede pública = **80** |
| Universalização / participação | `percentual_participacao` (FLOAT) | metas — **não** é a meta 80 |

---

## Grain (o que é uma linha)

| Tabela | Grain | Linhas / anos (medido) |
|--------|-------|-------------------------|
| `alunos` | 1 aluno × escola × ano × série × rede (microdado) | 3.867.999 · anos 2023–2024 |
| `municipio` | 1 município × ano × série × rede (agregado) | 23.995 · anos 2023–2024 |
| `uf` | 1 UF × ano × série × rede (agregado) | 145 · anos 2023–2024 |
| `meta_alfabetizacao_brasil` | 1 ano × rede (rótulo textual) | 3 · anos 2023–2025 |
| `meta_alfabetizacao_uf` | 1 UF × ano × rede | 81 · anos 2023–2025 |
| `meta_alfabetizacao_municipio` | 1 município × ano × rede | 10.704 · anos 2023–2024 |
| `dicionario` | 1 código (`id_tabela` + `nome_coluna` + `chave`) | 27 (apoio) |

Chaves naturais (sem nulos nas contagens de perfil):

- `alunos`: `ano`, `id_municipio`, `id_escola`, `id_aluno`, `serie`, `rede`
- `municipio`: `ano`, `id_municipio`, `serie`, `rede`
- `uf`: `ano`, `sigla_uf`, `serie`, `rede`
- `meta_brasil`: `ano`, `rede`
- `meta_uf`: `ano`, `sigla_uf`, `rede`
- `meta_municipio`: `ano`, `id_municipio`, `rede`

Nulos relevantes em `alunos`: `proficiencia` e `peso_aluno` = **513.338** cada (alinhado a caderno não preenchido / ausência).

---

## Chaves de join (tipos nos dois lados)

| Join | Lado A | Tipo | Lado B | Tipo | Observação |
|------|--------|------|--------|------|------------|
| Município (fato → agregado) | `alunos.id_municipio` | STRING | `municipio.id_municipio` | STRING | + `ano`, `serie`, `rede` (código) |
| Município (fato → meta) | `alunos.id_municipio` | STRING | `meta_alfabetizacao_municipio.id_municipio` | STRING | + `ano`; **`rede` não casa direto** |
| UF (agregado → meta) | `uf.sigla_uf` | STRING | `meta_alfabetizacao_uf.sigla_uf` | STRING | + `ano`; **`rede` não casa direto** |
| Brasil (meta) | — | — | `meta_alfabetizacao_brasil` | — | grain nacional; join por `ano` após filtrar rede pública |
| Código → rótulo | `*.rede` / `serie` / flags | STRING | `dicionario.chave` | STRING | filtrar `id_tabela` + `nome_coluna` |

Códigos de `alunos` / `municipio` / `uf` encontrados no perfil **existem** no `dicionario` (sem órfãos nas colunas checadas).

---

## Meta pactuada (confirmada)

Em `meta_alfabetizacao_brasil`, rede `Pública`:

| ano | taxa_alfabetizacao | meta_alfabetizacao_2030 |
|-----|--------------------|-------------------------|
| 2023 | 55.9 | **80.0** |
| 2024 | 59.2 | **80.0** |
| 2025 | 66.0 | **80.0** |

Nas UFs com meta preenchida e em todos os municípios do perfil, `meta_alfabetizacao_2030 = 80`.  
`percentual_participacao` é outro indicador (cenário de universalização/participação), não substitui a meta 80.

---

## Anomalia real (limitação do pipeline)

**`rede` usa dois encodings incompatíveis.**

- Microdado / agregados oficiais (`alunos`, `municipio`, `uf`): códigos numéricos em STRING (`"2"`, `"3"`, `"5"`, …) traduzíveis pelo `dicionario`.
- Metas (`meta_alfabetizacao_*`): rótulos textuais — `Pública` (Brasil/UF) e `Municipal` (município).

Exemplo medido: `alunos.rede ∈ {2,3,4}` vs `meta_brasil.rede = Pública` vs `meta_municipio.rede = Municipal`.

Consequência: join direto por `rede` entre fato e meta **quebra**. A Silver precisa de de-para explícito (ex.: código `5` / composição estadual+municipal ↔ rótulo `Pública`; código `3` ↔ `Municipal`), documentado e testado — não assumir igualdade de string.

Anomalia complementar: UF `RR` (2023 e 2024) com `taxa_alfabetizacao` e `meta_alfabetizacao_2030` nulos na meta estadual — preservar `NULL` nas médias da Gold.

---

## Exploração (entendimento analítico)

Consultas em [`sql/01_exploracao.sql`](../sql/01_exploracao.sql) → CSVs `06_*` em `evidence/passo_02/` (`python sql/run_exploracao.py`).

**Achados medidos**

- **Rede:** microdado é quase só Municipal (`3`) + Estadual (`2`); Privada irrelevante (25 linhas em 2024). Taxa simples entre presentes ~58–62%.
- **Ranking UF (rede pública `5`, 2024):** CE lidera (85,31, já acima da meta 80); BA na cauda (35,96). Maior alta YoY: MG (+12,26); maior queda: RS (−18,76).
- **Gap vs meta 80:** em 2024 só CE tem gap positivo (+5,31); SE/BA/RN ficam ~40+ pp abaixo. RR 2023–2024 sem taxa/meta (gap nulo); em 2025 RR já aparece com taxa 57.
- **Presença × proficiência:** os 513.338 nulos de `proficiencia`/`peso` = ausentes (`0,0`) + 1.185 presentes com caderno vazio; quem preencheu caderno tem 0 nulos.
- **Cobertura join meta (só `ano`+`id_municipio`):** 96,37% (2023) e 96,97% (2024) — ~170 municípios do microdado sem linha na meta.
- **Consistência micro→município:** na amostra rede `3`, `diff` ≈ 0 (arredondamento) — o agregado oficial bate com a taxa ponderada dos alunos.

Interpretação Silver/Gold: taxa oficial vem de `municipio`/`uf`; microdado para composição/qualidade; join com meta exige de-para de `rede`; preservar `NULL` de RR nas médias.

---

## Limiares de qualidade (Bronze — Passo 4)

Checks em `alfabetizacao_ops.quality_checks` via `python quality/validate.py --layer bronze`.

| Regra | Classe | Limiar | Justificativa |
|-------|--------|--------|---------------|
| `null_keys` | blocking | 0 | Chaves naturais do grain acima; nulo quebra grain |
| `duplicate_keys` | blocking | 0 | Grain único por entidade |
| `orphan_codes` (`rede`/`serie` em `alunos`/`municipio`/`uf`) | blocking | **0** | Perfil Passo 2 (`04_codigos_orfos_*`) = zero órfãos; guia: “0 é um bom começo” |
| `row_count` | informative | ≥ 1 | Detecta partição vazia |

Metas **não** entram em `orphan_codes`: `rede` é rótulo textual (anomalia acima), não código do `dicionario`.

---

## De-para `rede` (Silver — Passo 5)

Join fato/agregado × meta **não** usa igualdade direta de `rede` (ver anomalia). De-para canônico:

| Lado fato / agregado | Código `rede` | Rótulo na meta (`rede_para_meta`) | Join |
|----------------------|---------------|-----------------------------------|------|
| `municipio` | `3` | `Municipal` | `municipio_com_meta` |
| `uf` | `5` | `Pública` | `uf_com_meta` |
| agregado UF (`rede=5`) | `5` | `Pública` | `brasil_com_meta` |

Metas **não têm** `serie`: o join é `ano` + geo + `rede` mapeada; `serie` permanece só no lado do fato.

---

## Limiares de qualidade (Silver — Passo 5)

Checks em `alfabetizacao_ops.quality_checks` via `python silver/transform.py` e `python quality/validate.py --layer silver`.

| Regra | Classe | Limiar | Justificativa |
|-------|--------|--------|---------------|
| `join_match` (`municipio_com_meta`, `uf_com_meta`, `brasil_com_meta`) | blocking | **≥ 0.95** | Cobertura geo medida no Passo 2 (`06_cobertura_join_meta.csv`): 96,37% (2023) e 96,97% (2024); 0.95 deixa margem para ~170 municípios sem meta |
| `desconhecido_count` (labels via `dicionario`) | informative | — (só registra) | Código sem tradução vira `desconhecido`; não bloqueia sozinho |
| `row_count` (tabelas Silver) | informative | ≥ 1 | Detecta tabela vazia |

Fórmula: `taxa_match = linhas_com_par / linhas_do_lado_esquerdo` (recorte já filtrado por rede do de-para). Se qualquer `join_match` falhar → exit ≠ 0 (Silver não publicável; não avançar para a camada seguinte).

---

## Produtos Gold (Passo 6)

Dataset: `alfabetizacao_gold`. Fonte: Silver do mesmo `run_id_bronze`. Publicação só se `join_match` Silver passou. Export Parquet: `gs://<bucket>/gold/<produto>/ingestion_date=…/run_id=…/`.

| Produto | Grain (uma linha) | Colunas-chave |
|---------|-------------------|---------------|
| `indicador_municipio` | município × ano × rede × série | `id_municipio`, `ano`, `rede`, `serie`, `taxa_alfabetizacao`, níveis 0–8, `origem` |
| `indicador_uf` | UF × ano × rede × série | `sigla_uf`, `ano`, `rede`, `serie`, `taxa_alfabetizacao`, … |
| `meta_vs_resultado` | geo × ano (+ série no mun/UF) | `nivel_geo`, chaves geo, `taxa_alfabetizacao`, `meta_alfabetizacao_2030`, `gap_pp`, `status_meta` ∈ {`atingiu`,`nao_atingiu`,`sem_meta`} |
| `evolucao_temporal` | mesma chave no tempo | `taxa_alfabetizacao`, `taxa_anterior` (`LAG`), `delta_pp` |
| `validacao_microdado` | município × ano × rede × série | `taxa_micro` (peso amostral), `taxa_oficial`, `diff_pp` |

Regras: comparar meta e resultado na mesma rede (de-para Silver); `NULL` de taxa/meta permanece `NULL`; `origem = 'oficial'`.

**Fase 3 / vazamento de alvo:** não usar como feature do mesmo ano a própria `taxa_alfabetizacao`, a `meta_alfabetizacao_2030` nem o `status_meta` derivado — são o alvo (ou função direta dele).

---

## Eventos de streaming (Passo 7)

Tabela: `alfabetizacao_gold.eventos_stream`. **Não** altera os produtos oficiais acima.

| Campo | Tipo | Papel |
|-------|------|--------|
| `event_id` | STRING | Chave lógica (dedupe / MERGE) |
| `produced_at` | TIMESTAMP | Relógio no publish (producer) |
| `ingested_at` | TIMESTAMP | Relógio na ingestão (consumer) |
| `latency_seconds` | FLOAT64 | `ingested_at - produced_at` |
| `entidade` | STRING | Ex.: `municipio` |
| `id_municipio`, `ano`, `rede`, `serie` | chave do indicador | |
| `valor` | FLOAT64 | Taxa simulada em \[0, 100\] |
| `origem` | STRING | Sempre `simulado` nesta tabela |
| `ingestion_date` | DATE | Partição lógica do dia da ingestão |

**Grain:** uma linha = um `event_id` aceito (documento JSON do Pub/Sub).

**Regra de consulta:** indicadores oficiais (Passo 6) filtram `origem = 'oficial'`. Eventos simulados ficam só em `eventos_stream` e no prefixo GCS `bronze/stream/` (inválidos em `bronze/stream_quarentena/`).
