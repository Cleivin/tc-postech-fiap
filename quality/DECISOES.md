# Qualidade — decisões

Passos 4 e 5. Código: [`validate.py`](validate.py), [`prove_failure.py`](prove_failure.py), [`rules_bronze.py`](rules_bronze.py), [`rules_silver.py`](rules_silver.py), [`config.py`](config.py).  
Evidência: [`evidence/passo_04/`](../evidence/passo_04/) e a parte de `join_match` em [`evidence/passo_05/`](../evidence/passo_05/).

## O que o challenge pede

Regra bloqueante interrompe o job (exit ≠ 0) e não publica a camada seguinte. Regra informativa grava e segue. O resultado vai para `alfabetizacao_ops.quality_checks` em append. É obrigatória uma falha provocada, sem alterar o Parquet do lake. A taxa de match do join é bloqueante a partir da Silver, com limiar justificado no contrato.

## Decisões

| Decisão | Alternativa recusada | Motivo |
|---------|----------------------|--------|
| Limiar `orphan_codes` = 0 em `rede` e `série` de alunos, município e UF | Limiar folgado “para não travar” | O perfil mediu zero órfãos. O guia diz que 0 é um bom começo quando o perfil confirma. |
| Metas fora de `orphan_codes` | Exigir que `Pública` exista como chave do dicionário | A meta usa rótulo, não código. Tratar isso como órfão reprovaria toda carga saudável. O de-para mora na Silver. |
| `null_keys` e `duplicate_keys` bloqueantes, limiar 0 | Só alertar | Chave nula ou repetida quebra o grain. Nesta run as sete entidades passaram com valor 0. |
| `row_count` informativo, limiar ≥ 1 | Bloquear por volume “esperado” | Serve para pegar partição vazia. O volume oficial pode mudar de ano; o grain é que não pode duplicar. |
| Falha provocada numa fixture `alfabetizacao_ops.fixture_dup_keys` | Duplicar uma linha no Parquet do GCS | O guia pede a prova sem alterar o lake. Uma linha de UF copiada basta para `duplicate_keys = 1`. Exit 1. |
| `join_match` ≥ 0,95, bloqueante, só na Silver | Exigir 1,0 ou deixar a taxa só no log | A cobertura medida no Passo 2 fica em 96–97%. Exigir 100% reprovaria a carga por ~170 municípios sem meta. 0,95 fica abaixo do medido e ainda dispara se o de-para de `rede` quebrar. |
| Match = linhas com par / linhas do lado esquerdo, no recorte da rede do de-para | Match sobre as 23.995 linhas de município, misturando redes | A meta municipal só conversa com `rede = 3`. Incluir estadual no denominador derrubaria a taxa por desenho, não por falha. |
| `desconhecido_count` informativo | Bloquear qualquer `desconhecido` | Nesta run deu 0. Se um código novo aparecer, o job registra e a Gold ainda pode sair; o bloqueio de código conhecido continua sendo o `orphan_codes` da Bronze. |
| `except` não converte falha em sucesso | Capturar erro e devolver exit 0 | O guia anula o critério se o script “engolir” a falha. `prove_failure` termina em 1. |

## Resultado da run de referência

Bronze `20d3623d0430`: 0 falhas bloqueantes. Alunos 3.867.999, município 23.995, UF 145, metas 3 / 81 / 10.704, dicionário 27.

Silver: `municipio_com_meta` 10.654 / 10.896 = 0,9778; `uf_com_meta` 49 / 49; `brasil_com_meta` 2 / 2.

A Gold só publica se esse gate passa de novo no início de `gold/build.py`.
