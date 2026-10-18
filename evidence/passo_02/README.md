# Passo 2 — Perfil BigQuery (Data Understanding)

## 01_amostra_alunos
- job_id: `601f73ff-cb47-4329-af29-e3dd287286df`
- rows: 5
- file: `evidence/passo_02/01_amostra_alunos.csv`

```
 ano id_municipio id_escola id_aluno caderno serie rede presenca preenchimento_caderno alfabetizado  proficiencia  peso_aluno
2023      1100122  60000113 11021655       1     2    2        0                     0            0           NaN         NaN
2023      1302603  60000679 13049233       1     2    2        0                     0            0           NaN         NaN
2023      1302603  60001009 13049495       1     2    2        0                     0            0           NaN         NaN
2023      1302603  60001116 13036026       1     2    3        0                     0            0           NaN         NaN
2023      1504703  60002885 15060189       1     2    3        0                     0            0           NaN         NaN
```

## 01_amostra_municipio
- job_id: `d604f5b5-c21f-4b87-9851-4f8461d40b73`
- rows: 5
- file: `evidence/passo_02/01_amostra_municipio.csv`

```
 ano id_municipio serie rede  taxa_alfabetizacao  media_portugues  proporcao_aluno_nivel_0  proporcao_aluno_nivel_1  proporcao_aluno_nivel_2  proporcao_aluno_nivel_3  proporcao_aluno_nivel_4  proporcao_aluno_nivel_5  proporcao_aluno_nivel_6  proporcao_aluno_nivel_7  proporcao_aluno_nivel_8
2023      1100031     2    3               69.10         767.8763                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023      1100072     2    3               58.20         747.8918                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023      1100189     2    5               69.73         762.4062                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023      1101609     2    3               50.70         745.6802                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023      1101807     2    3               55.69         752.3724                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
```

## 01_amostra_uf
- job_id: `728640db-a126-4588-b1dd-08a0f350530a`
- rows: 5
- file: `evidence/passo_02/01_amostra_uf.csv`

```
 ano sigla_uf serie rede  taxa_alfabetizacao  media_portugues  proporcao_aluno_nivel_0  proporcao_aluno_nivel_1  proporcao_aluno_nivel_2  proporcao_aluno_nivel_3  proporcao_aluno_nivel_4  proporcao_aluno_nivel_5  proporcao_aluno_nivel_6  proporcao_aluno_nivel_7  proporcao_aluno_nivel_8
2023       AM     2    3               49.20         733.6637                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023       PB     2    2               55.23         744.8152                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023       PR     2    5               73.12         757.2146                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023       AP     2    3               41.87         732.7858                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023       PE     2    5               58.95         747.4522                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
```

## 01_amostra_meta_brasil
- job_id: `9ec38ffc-787e-43ec-8524-733e60856113`
- rows: 3
- file: `evidence/passo_02/01_amostra_meta_brasil.csv`

```
 ano    rede  taxa_alfabetizacao  meta_alfabetizacao_2024  meta_alfabetizacao_2025  meta_alfabetizacao_2026  meta_alfabetizacao_2027  meta_alfabetizacao_2028  meta_alfabetizacao_2029  meta_alfabetizacao_2030  percentual_participacao
2025 PÃºblica                66.0                     60.0                    64.00                    67.00                    71.00                    74.00                    77.00                     80.0                    88.00
2024 PÃºblica                59.2                     59.9                    63.77                    67.47                    70.97                    74.23                    77.24                     80.0                    87.37
2023 PÃºblica                55.9                     59.9                    63.77                    67.47                    70.97                    74.23                    77.24                     80.0                    86.00
```

## 01_amostra_meta_uf
- job_id: `a472f15a-0e4e-4028-b58c-e3f48f53d7ed`
- rows: 5
- file: `evidence/passo_02/01_amostra_meta_uf.csv`

```
 ano sigla_uf    rede  taxa_alfabetizacao  meta_alfabetizacao_2024  meta_alfabetizacao_2025  meta_alfabetizacao_2026  meta_alfabetizacao_2027  meta_alfabetizacao_2028  meta_alfabetizacao_2029  meta_alfabetizacao_2030  percentual_participacao
2024       RR PÃºblica                 NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2023       RR PÃºblica                 NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN                      NaN
2024       SE PÃºblica               38.39                     38.3                     45.9                     53.6                     61.2                     68.3                     74.6                     80.0                    92.84
2023       SE PÃºblica               31.30                     38.3                     45.9                     53.6                     61.2                     68.3                     74.6                     80.0                    88.34
2025       SE PÃºblica               50.00                     38.0                     46.0                     54.0                     61.0                     68.0                     75.0                     80.0                    87.00
```

## 01_amostra_meta_municipio
- job_id: `afc0f061-d942-4f3f-9553-149f354894c3`
- rows: 5
- file: `evidence/passo_02/01_amostra_meta_municipio.csv`

```
 ano id_municipio      rede  taxa_alfabetizacao  meta_alfabetizacao_2024  meta_alfabetizacao_2025  meta_alfabetizacao_2026  meta_alfabetizacao_2027  meta_alfabetizacao_2028  meta_alfabetizacao_2029  meta_alfabetizacao_2030  nivel_alfabetizacao  percentual_participacao
2023      4301750 Municipal                 NaN                      NaN                    14.05                    23.65                    37.00                    52.68                    67.85                     80.0                 <NA>                      NaN
2024      4301750 Municipal                4.40                      NaN                    14.05                    23.65                    37.00                    52.68                    67.85                     80.0                    0                    92.59
2024      2406908 Municipal               42.86                     7.94                    14.05                    23.65                    37.00                    52.68                    67.85                     80.0                    1                    84.00
2023      2406908 Municipal                4.40                     7.94                    14.05                    23.65                    37.00                    52.68                    67.85                     80.0                    0                    82.14
2023      1718501 Municipal                4.60                     8.25                    14.48                    24.16                    37.49                    53.03                    68.00                     80.0                    0                    95.65
```

## 01_dicionario_completo
- job_id: `5634f504-453e-4a67-8d96-327f2400cee8`
- rows: 27
- file: `evidence/passo_02/01_dicionario_completo.csv`

```
id_tabela           nome_coluna chave cobertura_temporal                                          valor
   alunos          alfabetizado     0                (1)                                            NÃ£o
   alunos          alfabetizado     1                (1)                                            Sim
   alunos preenchimento_caderno     0                (1)                           Prova nÃ£o preenchida
   alunos preenchimento_caderno     1                (1)                               Prova preenchida
   alunos              presenca     0                (1)                                        Ausente
   alunos              presenca     1                (1)                                       Presente
   alunos                  rede     1                (1)                                        Federal
   alunos                  rede     2                (1)                                       Estadual
   alunos                  rede     3                (1)                                      Municipal
   alunos                  rede     4                (1)                                        Privada
   alunos                 serie     2                (1)                   2Â° ano do Ensino Fundamental
municipio                  rede     0                (1) Total (Federal, Estadual, Municipal e Privada)
municipio                  rede     1                (1)                                        Federal
municipio                  rede     2                (1)                                       Estadual
municipio                  rede     3                (1)                                      Municipal
municipio                  rede     4                (1)                                        Privada
municipio                  rede     5                (1)                 PÃºblica (Estadual e Municipal)
municipio                  rede     6                (1)        PÃºblica (Federal, Estadual e Municipal)
municipio                 serie     2                (1)                   2Â° ano do Ensino Fundamental
       uf                  rede     0                (1) Total (Federal, Estadual, Municipal e Privada)
       uf                  rede     1                (1)                                        Federal
       uf                  rede     2                (1)                                       Estadual
       uf                  rede     3                (1)                                      Municipal
       uf                  rede     4                (1)                                        Privada
       uf                  rede     5                (1)                 PÃºblica (Estadual e Municipal)
       uf                  rede     6                (1)        PÃºblica (Federal, Estadual e Municipal)
       uf                 serie     2                (1)                   2Â° ano do Ensino Fundamental
```

## 02_contagens_alunos
- job_id: `d92312a0-b73f-4224-9de3-f5ece1c47b41`
- rows: 1
- file: `evidence/passo_02/02_contagens_alunos.csv`

```
 n_linhas  n_anos  ano_min  ano_max  null_ano  null_id_municipio  null_id_escola  null_id_aluno  null_serie  null_rede  null_presenca  null_alfabetizado  null_proficiencia  null_peso_aluno
  3867999       2     2023     2024         0                  0               0              0           0          0              0                  0             513338           513338
```

## 02_contagens_municipio_uf
- job_id: `0e5406ed-7e64-4ac7-ba31-29a2f7780f98`
- rows: 2
- file: `evidence/passo_02/02_contagens_municipio_uf.csv`

```
   tabela  n_linhas  n_anos  ano_min  ano_max  null_ano  null_geo  null_serie  null_rede  null_taxa
municipio     23995       2     2023     2024         0         0           0          0          0
       uf       145       2     2023     2024         0         0           0          0          0
```

## 02_contagens_metas
- job_id: `693cc6be-eb9b-48a1-94e2-2252d2443279`
- rows: 3
- file: `evidence/passo_02/02_contagens_metas.csv`

```
        tabela  n_linhas  n_anos  null_meta_2030  meta_2030_eq_80  meta_2030_neq_80
   meta_brasil         3       3               0                3                 0
       meta_uf        81       3               2               79                 0
meta_municipio     10704       2               0            10704                 0
```

## 03_meta_pactuada_brasil
- job_id: `b1416346-4c80-4589-8a3a-bcc05c1df992`
- rows: 3
- file: `evidence/passo_02/03_meta_pactuada_brasil.csv`

```
 ano    rede  taxa_alfabetizacao  meta_alfabetizacao_2030  percentual_participacao
2023 PÃºblica                55.9                     80.0                    86.00
2024 PÃºblica                59.2                     80.0                    87.37
2025 PÃºblica                66.0                     80.0                    88.00
```

## 04_codigos_orfos_alunos
- job_id: `c378961f-2d4d-42a1-812f-1e78c19f1dad`
- rows: 10
- file: `evidence/passo_02/04_codigos_orfos_alunos.csv`

```
          nome_coluna chave       n status_dicionario
         alfabetizado     0 1883453                OK
         alfabetizado     1 1984546                OK
preenchimento_caderno     0  513338                OK
preenchimento_caderno     1 3354661                OK
             presenca     0  512153                OK
             presenca     1 3355846                OK
                 rede     2  435398                OK
                 rede     3 3432576                OK
                 rede     4      25                OK
                serie     2 3867999                OK
```

## 04_codigos_orfos_municipio_uf
- job_id: `6fadf2b7-cd83-47f9-bab3-81e91a87f37e`
- rows: 26
- file: `evidence/passo_02/04_codigos_orfos_municipio_uf.csv`

```
   tabela nome_coluna chave     n status_dicionario
municipio        rede     0   398                OK
municipio        rede     0   398                OK
municipio        rede     2  2235                OK
municipio        rede     2  2235                OK
municipio        rede     2  2235                OK
municipio        rede     3 10896                OK
municipio        rede     3 10896                OK
municipio        rede     3 10896                OK
municipio        rede     5 10466                OK
municipio        rede     5 10466                OK
municipio       serie     2 23995                OK
municipio       serie     2 23995                OK
municipio       serie     2 23995                OK
       uf        rede     0     1                OK
       uf        rede     0     1                OK
       uf        rede     2    46                OK
       uf        rede     2    46                OK
       uf        rede     2    46                OK
       uf        rede     3    49                OK
       uf        rede     3    49                OK
       uf        rede     3    49                OK
       uf        rede     5    49                OK
       uf        rede     5    49                OK
       uf       serie     2   145                OK
       uf       serie     2   145                OK
       uf       serie     2   145                OK
```

## 05_anomalia_rede_encoding
- job_id: `e6c1174b-9bfa-4924-bf78-36ded459246c`
- rows: 6
- file: `evidence/passo_02/05_anomalia_rede_encoding.csv`

```
         fonte valores_rede
        alunos    [2, 3, 4]
            uf [0, 2, 3, 5]
       meta_uf    [PÃºblica]
   meta_brasil    [PÃºblica]
     municipio [0, 2, 3, 5]
meta_municipio  [Municipal]
```

## 05_anomalia_meta_uf_nula
- job_id: `676383dd-b166-418a-9060-80143c9a8a34`
- rows: 2
- file: `evidence/passo_02/05_anomalia_meta_uf_nula.csv`

```
 ano sigla_uf    rede  taxa_alfabetizacao  meta_alfabetizacao_2030  percentual_participacao
2023       RR PÃºblica                 NaN                      NaN                      NaN
2024       RR PÃºblica                 NaN                      NaN                      NaN
```

# Exploração BigQuery — passo 2 (extra)

## 06_distribuicao_rede_alunos
- job_id: `6208127d-e63a-451a-97a8-f97e5e7e145d`
- rows: 5
- file: `evidence/passo_02/06_distribuicao_rede_alunos.csv`

```
 ano rede rede_rotulo  n_alunos  n_presentes  n_alfabetizados_presentes  taxa_alfabetizacao_simples_pct
2023    2    Estadual    155140       131526                      80662                           61.33
2023    3   Municipal   1592299      1371532                     796765                           58.09
2024    2    Estadual    280258       241173                     150760                           62.51
2024    3   Municipal   1840277      1611591                     956343                           59.34
2024    4     Privada        25           24                         16                           66.67
```

## 06_taxa_uf_ranking
- job_id: `b3bb5793-7aa3-487b-b4c1-2c7fa359faad`
- rows: 25
- file: `evidence/passo_02/06_taxa_uf_ranking.csv`

```
sigla_uf  taxa_2023  taxa_2024  delta_yoy
      CE      84.46      85.31       0.85
      GO      66.74      72.74       6.00
      MG      59.81      72.07      12.26
      ES      67.93      71.69       3.76
      PR      73.12      70.42      -2.70
      RO      64.60      62.62      -1.98
      SC      61.38      62.02       0.64
      PE      58.95      60.79       1.84
      MT      55.03      60.59       5.56
      PI      52.48      59.82       7.34
      MA      56.43      59.64       3.21
      SP      51.91      58.13       6.22
      PB      51.12      55.96       4.84
      MS      47.45      55.87       8.42
      RJ      52.13      55.25       3.12
      AC        NaN      51.38        NaN
      TO      43.72      50.07       6.35
      AM      52.20      49.17      -3.03
      AL      43.88      48.63       4.75
      PA      48.38      48.20      -0.18
      AP      41.56      46.62       5.06
      RS      63.43      44.67     -18.76
      RN      37.24      39.29       2.05
      SE      31.30      38.39       7.09
      BA      36.78      35.96      -0.82
```

## 06_gap_meta_uf
- job_id: `f09ae77b-fb1b-4065-8d7c-47db16c3f3f8`
- rows: 81
- file: `evidence/passo_02/06_gap_meta_uf.csv`

```
 ano sigla_uf    rede  taxa_alfabetizacao  meta_alfabetizacao_2030  gap_vs_meta_2030  percentual_participacao
2023       AC Pública                 NaN                     80.0               NaN                      NaN
2023       RR Pública                 NaN                      NaN               NaN                      NaN
2023       DF Pública                 NaN                     80.0               NaN                      NaN
2023       SE Pública               31.30                     80.0            -48.70                    88.34
2023       BA Pública               36.80                     80.0            -43.20                    84.53
2023       RN Pública               37.24                     80.0            -42.76                    78.55
2023       AP Pública               41.56                     80.0            -38.44                    89.68
2023       TO Pública               43.72                     80.0            -36.28                    83.91
2023       AL Pública               43.88                     80.0            -36.12                    92.36
2023       MS Pública               47.45                     80.0            -32.55                    87.95
2023       PA Pública               48.40                     80.0            -31.60                    80.55
2023       PB Pública               51.12                     80.0            -28.88                    88.22
2023       SP Pública               51.91                     80.0            -28.09                    88.75
2023       RJ Pública               52.13                     80.0            -27.87                    81.21
2023       AM Pública               52.20                     80.0            -27.80                    76.14
2023       PI Pública               52.48                     80.0            -27.52                    93.37
2023       MT Pública               55.06                     80.0            -24.94                    87.47
2023       MA Pública               56.43                     80.0            -23.57                    89.11
2023       PE Pública               59.00                     80.0            -21.00                    91.93
2023       MG Pública               59.81                     80.0            -20.19                    89.59
2023       SC Pública               61.38                     80.0            -18.62                    78.60
2023       RS Pública               63.40                     80.0            -16.60                    81.44
2023       RO Pública               64.60                     80.0            -15.40                    88.10
2023       GO Pública               66.70                     80.0            -13.30                    87.03
2023       ES Pública               67.93                     80.0            -12.07                    88.40
2023       PR Pública               73.12                     80.0             -6.88                    86.18
2023       CE Pública               84.50                     80.0              4.50                    95.22
2024       RR Pública                 NaN                      NaN               NaN                      NaN
2024       BA Pública               35.96                     80.0            -44.04                    90.04
2024       SE Pública               38.39                     80.0            -41.61                    92.84
```

## 06_presenca_vs_proficiencia
- job_id: `2daa1cf8-01f1-4439-9990-d06926663206`
- rows: 3
- file: `evidence/passo_02/06_presenca_vs_proficiencia.csv`

```
presenca preenchimento_caderno       n  null_proficiencia  null_peso_aluno  com_proficiencia
       0                     0  512153             512153           512153                 0
       1                     0    1185               1185             1185                 0
       1                     1 3354661                  0                0           3354661
```

## 06_cobertura_join_meta
- job_id: `611cce4d-3e2e-4d7c-a5eb-90bbbdcf1a4a`
- rows: 2
- file: `evidence/passo_02/06_cobertura_join_meta.csv`

```
 ano  n_municipios_alunos  n_com_meta  n_sem_meta  cobertura_pct
2023                 4873        4696         177          96.37
2024                 5519        5352         167          96.97
```

## 06_consistencia_micro_vs_muni
- job_id: `2884dd89-e207-45c1-8d68-3d310ed37a86`
- rows: 40
- file: `evidence/passo_02/06_consistencia_micro_vs_muni.csv`

```
 ano id_municipio rede  taxa_micro_ponderada  taxa_oficial_municipio  diff
2023      1100080    3                 80.70                   80.68  0.02
2023      1100130    3                 51.38                   51.40 -0.02
2023      1100072    3                 58.19                   58.20 -0.01
2023      1100098    3                 85.32                   85.33 -0.01
2023      1100189    3                 69.72                   69.73 -0.01
2023      1100015    3                 64.55                   64.55  0.00
2023      1100023    3                 62.30                   62.30  0.00
2023      1100031    3                 69.10                   69.10  0.00
2023      1100049    3                 62.51                   62.51  0.00
2023      1100056    3                 58.53                   58.53  0.00
2023      1100064    3                 62.85                   62.85  0.00
2023      1100106    3                 41.76                   41.76  0.00
2023      1100114    3                 62.82                   62.82  0.00
2023      1100122    3                 81.83                   81.83  0.00
2023      1100148    3                 74.81                   74.81  0.00
2023      1100155    3                 72.39                   72.39  0.00
2023      1100205    3                 65.06                   65.06  0.00
2023      1100254    3                 62.41                   62.41  0.00
2023      1100262    3                 83.84                   83.84  0.00
2023      1100288    3                 68.81                   68.81  0.00
2024      1100049    3                 65.88                   65.81  0.07
2024      1100064    3                 71.72                   71.69  0.03
2024      1100031    3                 75.90                   75.88  0.02
2024      1100114    3                 64.01                   63.99  0.02
2024      1100015    3                 67.81                   67.79  0.02
2024      1100130    3                 64.77                   64.75  0.02
2024      1100072    3                 72.67                   72.68 -0.01
2024      1100098    3                 71.17                   71.16  0.01
2024      1100254    3                 71.13                   71.14 -0.01
2024      1100080    3                 59.64                   59.63  0.01
```
