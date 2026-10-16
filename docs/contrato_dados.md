# Contrato de dados — Avaliação da Alfabetização (INEP / Base dos Dados)

Fonte: `basedosdados.br_inep_avaliacao_alfabetizacao`  
Evidência: `evidence/passo_02/` (gerada por `sql/00_perfil.sql` via `sql/run_perfil.py`).

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
