# Passo 5 — análise das evidências

Run Bronze lida: `20d3623d0430`. Dataset `alfabetizacao_silver`.

| Arquivo | O que contém |
|---------|----------------|
| `manifest_20d3623d0430.csv` / `manifest_latest.csv` | Contagem das 10 tabelas Silver |
| `join_match_20d3623d0430.csv` / `join_match_latest.csv` | As três taxas, com numerador e denominador |
| `validate_silver_*.csv` | A mesma conta refeita por `quality/validate.py`, mais `row_count` e `desconhecido_count` |
| `README.md` | Resumo da run |

## Match

| Join | Esquerda | Com par | Taxa | Limiar |
|------|----------|---------|------|--------|
| `municipio_com_meta` | 10.896 | 10.654 | 0,9778 | 0,95 |
| `uf_com_meta` | 49 | 49 | 1,0 | 0,95 |
| `brasil_com_meta` | 2 | 2 | 1,0 | 0,95 |

10.896 é o recorte `rede = 3` do agregado municipal (5.448 × dois anos), não as 23.995 linhas de todas as redes. 242 linhas ficam sem meta: 10.896 − 10.654. A taxa passa o limiar com folga de cerca de 2,8 pp. Se o de-para `3 → Municipal` estivesse errado, essa taxa cairia perto de zero e o job sairia com código 1.

O denominador não é o do Passo 2. Lá a cobertura era “município distinto no microdado × meta”, 96–97%. Aqui é “linha do agregado de rede municipal × meta”. Os dois medem a mesma lacuna por caminhos diferentes e os dois ficam acima de 0,95. Por isso o limiar não foi copiado de um percentual redondo.

UF rede pública: 49/49. Não há UF desse recorte sem linha de meta. Isso **não** significa que RR tenha taxa. RR não está entre essas 49 linhas, porque o agregado `uf` não tem RR em `rede = 5`. A meta nula de RR continua na tabela de meta; ela não fabrica uma linha de fato.

Brasil: 2 linhas, 2023 e 2024. A taxa 66,0 de 2025 fica de fora porque o lado esquerdo (anos da UF) não tem 2025.

## O que mais a validação registra

`desconhecido_count = 0` em alunos, município e UF. Todo código traduziu. A categoria `desconhecido` não foi usada nesta carga; a regra informativa existe para a próxima.

As contagens-espelho repetem a Bronze (3.867.999 alunos, 27 códigos no dicionário, etc.). Tipar e traduzir não dropou linha. Proficiência nula do ausente continua nula — não há, nestes CSV, uma coluna zerada no lugar dela.

Há dois horários de `join_match` (por volta de 18:29 e de 19:54 UTC). São a validação e a transformação gravando a mesma taxa de novo, em append. O valor não muda.
