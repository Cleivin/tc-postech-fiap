# Consultas de leitura da Gold e do corte de 743

Feitas em **2026-10-18** contra o projeto `tc-postech-fiap`, location `US`, em cima da run já publicada (`alfabetizacao_silver.alunos` e `alfabetizacao_gold`). Não republicam tabela. Servem para a análise dos passos 2, 6 e 10 não afirmar um número que não esteja neste arquivo.

## Corte de 743 no microdado

Bytes processados: 50.045.282.

```sql
SELECT alfabetizado, presenca, COUNT(*) AS n,
  COUNTIF(proficiencia IS NULL) AS prof_null,
  ROUND(MIN(proficiencia), 2) AS min_p,
  ROUND(MAX(proficiencia), 2) AS max_p,
  COUNTIF(proficiencia >= 743) AS ge_743,
  COUNTIF(proficiencia < 743) AS lt_743
FROM `tc-postech-fiap.alfabetizacao_silver.alunos`
GROUP BY alfabetizado, presenca
ORDER BY presenca, alfabetizado
```

| alfabetizado | presenca | n | prof_null | min_p | max_p | ge_743 | lt_743 |
|--------------|----------|---|-----------|-------|-------|--------|--------|
| 0 | 0 | 512153 | 512153 | | | 0 | 0 |
| 0 | 1 | 1371300 | 1185 | 578.46 | 743.00 | 0 | 1370115 |
| 1 | 1 | 1984546 | 0 | 743.00 | 904.38 | 1984546 | 0 |

512.153 + 1.371.300 + 1.984.546 = 3.867.999. Flag 1 implica proficiência ≥ 743, sem nulo. Flag 0 com nota preenchida tem contagem `>= 743` igual a zero (o máximo impresso com duas casas arredonda para 743,00). Ausente não tem nota.

## Produtos Gold

**Níveis municipais.** 2023: 11.547 linhas, todas com `proporcao_aluno_nivel_0` nula. 2024: 12.448 linhas, zero nulos. 11.547 + 12.448 = 23.995.

**Status em `meta_vs_resultado`.**

| nível | status | n | média da taxa | média do gap |
|-------|--------|---|----------------|--------------|
| brasil | nao_atingiu | 2 | 57,55 | −22,45 |
| municipio | atingiu | 2076 | 88,54 | 8,54 |
| municipio | nao_atingiu | 8578 | 55,23 | −24,77 |
| municipio | sem_meta | 242 | 53,69 | nulo |
| uf | atingiu | 2 | 84,88 | 4,88 |
| uf | nao_atingiu | 47 | 54,20 | −25,80 |

Sem meta no município: 146 em 2023 e 96 em 2024. Por ano, o grain municipal da meta tem 5.448 linhas (935 atingiram em 2023; 1.141 em 2024).

**UF com taxa ≥ 80 e rede 5:** só CE, 84,46 (2023) e 85,31 (2024). Rede 5 tem 24 UFs em 2023 e 25 em 2024, nenhuma com taxa nula. `indicador_uf` não tem linha de RR.

**Brasil no produto:** 2023 → 55,9 / meta 80 / gap −24,1. 2024 → 59,2 / 80 / −20,8. Os dois `nao_atingiu`. Não há linha 2025.

**`validacao_microdado`:** 12.408 linhas; média absoluta do `diff_pp` 0,0376; mediana 0,0037; p95 0,0456; máximo 36,061; 57 linhas com diferença absoluta acima de 1 pp.

Maiores diferenças absolutas acima de 5 pp:

| ano | id_municipio | rede | taxa_micro | taxa_oficial | diff_pp | peso |
|-----|--------------|------|------------|--------------|---------|------|
| 2023 | 2305100 | 3 | 55,61 | 91,67 | −36,06 | 72,0 |
| 2023 | 5105622 | 2 | 46,45 | 19,85 | 26,60 | 190,8 |
| 2024 | 5103908 | 2 | 36,67 | 59,62 | −22,95 | 51,9 |
| 2024 | 5107040 | 2 | 56,52 | 33,91 | 22,61 | 29,9 |
| 2024 | 2506905 | 2 | 33,33 | 50,57 | −17,24 | 14,0 |
| 2023 | 1304005 | 3 | 52,54 | 35,75 | 16,79 | 126,4 |
| 2023 | 2304905 | 3 | 83,11 | 99,15 | −16,04 | 120,0 |
| 2024 | 2506806 | 3 | 47,24 | 37,97 | 9,27 | 158,0 |
| 2023 | 1300607 | 3 | 44,00 | 38,02 | 5,98 | 504,4 |

O caso extremo combina diferença grande e peso pequeno. A mediana perto de zero é o comportamento do restante da tabela.
