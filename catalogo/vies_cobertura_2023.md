# Viés de cobertura, 2023

Municípios com população: 5570; calculados: 4121 (74.0%).

## Principais flags entre os não calculados (um município pode ter mais de uma)

| flags                |   n |
|:---------------------|----:|
| LIQ_DIVERGE          | 949 |
| REC_DIVERGE          | 837 |
| FONTE_LIVRE_ATIPICA  | 258 |
| SEM_NATUREZA_RECEITA | 155 |
| RCL_SUSPEITA         | 108 |
| RREO3_VAZIO          |  37 |
| LEGISLATIVO_ATIPICO  |  19 |
| SEM_MSCE             |   3 |

## Cobertura por faixa de porte

| faixa           |    n |   cobertura_pct |
|:----------------|-----:|----------------:|
| até 5 mil       | 1285 |            75   |
| 5–10 mil        | 1183 |            73.9 |
| 10–20 mil       | 1350 |            72.6 |
| 20–50 mil       | 1070 |            75   |
| 50–100 mil      |  344 |            75   |
| 100–500 mil     |  290 |            70.7 |
| mais de 500 mil |   48 |            77.1 |

## Calculados × não calculados (mediana; Mann-Whitney)

| variavel                                 |   mediana_calculados |   mediana_nao_calculados |   n_c |   n_nc |      p |
|:-----------------------------------------|---------------------:|-------------------------:|------:|-------:|-------:|
| população                                |              11291   |                  11586   |  4121 |   1449 | 0.54   |
| receita por habitante (DCA)              |               6364.7 |                   6325.3 |  4121 |   1403 | 0.39   |
| receita tributária própria por habitante |                452.4 |                    414.6 |  4027 |   1413 | 0.0031 |

## Cobertura por quintil de base tributária própria

| q          |    n |   cobertura_pct |
|:-----------|-----:|----------------:|
| Q1 (menor) | 1088 |            71.1 |
| Q2         | 1088 |            73.8 |
| Q3         | 1088 |            72.2 |
| Q4         | 1088 |            76.4 |
| Q5 (maior) | 1088 |            76.6 |

## Logit: probabilidade de ser calculado (efeitos fixos de UF)

|    |   coef |     p |
|:---|-------:|------:|
| lp | -0.022 | 0.655 |
| lt |  0.052 | 0.473 |
| lr |  0.008 | 0.953 |

## Coeficiente da base própria, sem peso e ponderado pelo inverso da probabilidade de cobertura

| desfecho               |    n |   coef_sem_peso |   coef_ponderado |   p_ponderado |
|:-----------------------|-----:|----------------:|-----------------:|--------------:|
| margem % receita livre | 4027 |            1.24 |             1.23 |       2.1e-15 |
| margem % receita total | 4027 |            3.21 |             3.2  |       4e-51   |

Peso máximo usado: 20.0; mediana 1.24.