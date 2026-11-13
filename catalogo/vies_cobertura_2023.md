# Viés de cobertura, 2023

Municípios com população: 5570; calculados: 4037 (72.5%).

## Principais flags entre os não calculados (um município pode ter mais de uma)

| flags                |    n |
|:---------------------|-----:|
| LIQ_DIVERGE          | 1044 |
| REC_DIVERGE          |  908 |
| FONTE_LIVRE_ATIPICA  |  240 |
| RCL_SUSPEITA         |  178 |
| SEM_NATUREZA_RECEITA |  154 |
| RREO3_VAZIO          |  106 |
| LEGISLATIVO_ATIPICO  |   21 |
| SEM_MSCE             |    3 |

## Cobertura por faixa de porte

| faixa          |    n |   cobertura_pct |
|:---------------|-----:|----------------:|
| até 5 mil      | 1285 |            73.9 |
| 5–10 mil       | 1183 |            72.3 |
| 10–20 mil      | 1350 |            71.3 |
| 20–50 mil      | 1070 |            73.2 |
| mais de 50 mil |  682 |            71.6 |

## Calculados × não calculados (mediana; Mann-Whitney)

| variavel                                 |   mediana_calculados |   mediana_nao_calculados |   n_c |   n_nc |      p |
|:-----------------------------------------|---------------------:|-------------------------:|------:|-------:|-------:|
| população                                |              11280   |                  11617   |  4037 |   1533 | 0.32   |
| receita por habitante (DCA)              |               6367.8 |                   6310.1 |  4037 |   1481 | 0.22   |
| receita tributária própria por habitante |                450.1 |                    414.4 |  3891 |   1444 | 0.0024 |

## Cobertura por quintil de base tributária própria

| q          |    n |   cobertura_pct |
|:-----------|-----:|----------------:|
| Q1 (menor) | 1067 |            69.6 |
| Q2         | 1067 |            72.6 |
| Q3         | 1067 |            71.6 |
| Q4         | 1067 |            75.4 |
| Q5 (maior) | 1067 |            75.4 |

## Logit: probabilidade de ser calculado (efeitos fixos de UF)

|    |   coef |     p |
|:---|-------:|------:|
| lp | -0.016 | 0.737 |
| lt |  0.044 | 0.542 |
| lr |  0.035 | 0.798 |

## Coeficiente da base própria, sem peso e ponderado pelo inverso da probabilidade de cobertura

| desfecho               |    n |   coef_sem_peso |   coef_ponderado |   p_ponderado |
|:-----------------------|-----:|----------------:|-----------------:|--------------:|
| margem % receita livre | 3891 |            1.17 |             1.17 |       1.2e-15 |
| margem % receita total | 3891 |            3.21 |             3.19 |       9.4e-48 |

Peso máximo usado: 20.0; mediana 1.26.