# Robustez da pergunta central, 2023

## Coeficiente da base própria (log) sobre a margem, com efeitos fixos de UF e erro robusto (HC3), controlando pelo log da população

| desfecho               | amostra                                           |    n |   rho |   coef |       p |    r2 |
|:-----------------------|:--------------------------------------------------|-----:|------:|-------:|--------:|------:|
| margem % receita livre | principal (tol. 1%)                               | 4027 | 0.294 |   1.24 | 2.8e-16 | 0.196 |
| margem % receita total | principal (tol. 1%)                               | 4027 | 0.489 |   3.21 | 1.3e-58 | 0.515 |
| margem % receita livre | tolerância 3%                                     | 4239 | 0.291 |   1.24 | 4e-17   | 0.185 |
| margem % receita total | tolerância 3%                                     | 4239 | 0.482 |   3.18 | 1e-58   | 0.504 |
| margem % receita livre | base = IPTU+ISS+ITBI por habitante                | 3640 | 0.27  |   0.74 | 1.9e-05 | 0.193 |
| margem % receita total | base = IPTU+ISS+ITBI por habitante                | 3640 | 0.464 |   2.03 | 2e-14   | 0.503 |
| margem % receita livre | base = participação do tributo próprio na receita | 3640 | 0.173 |   9.58 | 3.3e-07 | 0.191 |
| margem % receita total | base = participação do tributo próprio na receita | 3640 | 0.295 |  27.94 | 1e-07   | 0.501 |
| margem % receita livre | só UFs com cobertura de 60% ou mais (20 UFs)      | 3643 | 0.282 |   1.35 | 1.9e-16 | 0.192 |
| margem % receita total | só UFs com cobertura de 60% ou mais (20 UFs)      | 3643 | 0.482 |   3.3  | 1.7e-58 | 0.521 |

UFs com cobertura abaixo de 60% (excluídas na linha 3): AC, AL, AP, BA, DF, MT, PB.

## Quintis dentro de cada UF (UFs com 15 ou mais municípios calculados)

|   qu |   n |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|-----:|----:|-----------------------:|-----------------------:|------------:|
|    1 | 808 |                   51.8 |                   29.7 |        42.2 |
|    2 | 800 |                   52   |                   30.6 |        40.9 |
|    3 | 793 |                   52.5 |                   30.9 |        40.2 |
|    4 | 800 |                   52.5 |                   30.8 |        40.6 |
|    5 | 805 |                   53   |                   32.8 |        38.4 |

Spearman entre o quintil dentro da UF e a margem sobre a receita total: rho = 0.077, p = 1.1e-06.

## Art. 11 da LRF com critério relativo (arrecadação abaixo de 10% da mediana da mesma UF e faixa de porte, % do grupo)

| q          |   iptu_rel |   iss_rel |   itbi_rel |   algum_rel |
|:-----------|-----------:|----------:|-----------:|------------:|
| Q1 (menor) |       16.6 |       0.7 |       15.2 |        25.4 |
| Q2         |        7.3 |       0.3 |        7.3 |        12.8 |
| Q3         |        3.6 |       0.3 |        2.6 |         5.6 |
| Q4         |        0.8 |       1.1 |        1.9 |         3   |
| Q5 (maior) |        1.4 |       0.3 |        1.1 |         2.2 |

Total com algum imposto abaixo do critério: 9.8% de 3640.