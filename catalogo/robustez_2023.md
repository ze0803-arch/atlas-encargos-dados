# Robustez da pergunta central, 2023

## Coeficiente da base própria (log) sobre a margem, com efeitos fixos de UF e erro robusto (HC3), controlando pelo log da população

| desfecho               | amostra                                           |    n |   rho |   coef |       p |    r2 |
|:-----------------------|:--------------------------------------------------|-----:|------:|-------:|--------:|------:|
| margem % receita livre | principal (tol. 1%)                               | 3891 | 0.356 |   1.17 | 5.2e-16 | 0.256 |
| margem % receita total | principal (tol. 1%)                               | 3891 | 0.496 |   3.21 | 1.2e-54 | 0.543 |
| margem % receita livre | tolerância 3%                                     | 4103 | 0.351 |   1.19 | 3.9e-17 | 0.242 |
| margem % receita total | tolerância 3%                                     | 4103 | 0.489 |   3.19 | 6.2e-55 | 0.531 |
| margem % receita livre | base = IPTU+ISS+ITBI por habitante                | 3453 | 0.333 |   0.74 | 1.3e-05 | 0.262 |
| margem % receita total | base = IPTU+ISS+ITBI por habitante                | 3453 | 0.478 |   2.16 | 5.9e-15 | 0.541 |
| margem % receita livre | base = participação do tributo próprio na receita | 3453 | 0.218 |   9.35 | 2.1e-07 | 0.26  |
| margem % receita total | base = participação do tributo próprio na receita | 3453 | 0.3   |  28.23 | 2.4e-07 | 0.538 |
| margem % receita livre | só UFs com cobertura de 60% ou mais (19 UFs)      | 3389 | 0.35  |   1.28 | 3.4e-15 | 0.247 |
| margem % receita total | só UFs com cobertura de 60% ou mais (19 UFs)      | 3389 | 0.49  |   3.33 | 5.5e-52 | 0.547 |

UFs com cobertura abaixo de 60% (excluídas na linha 3): AC, AL, AP, BA, DF, GO, MT, PB.

## Quintis dentro de cada UF (UFs com 15 ou mais municípios calculados)

|   qu |   n |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|-----:|----:|-----------------------:|-----------------------:|------------:|
|    1 | 782 |                   54.4 |                   31.4 |        42   |
|    2 | 772 |                   54.6 |                   32.4 |        40.7 |
|    3 | 768 |                   55.1 |                   32.5 |        40.4 |
|    4 | 772 |                   55.1 |                   32.5 |        40.6 |
|    5 | 776 |                   55.3 |                   34.4 |        38.4 |

Spearman entre o quintil dentro da UF e a margem sobre a receita total: rho = 0.069, p = 1.7e-05.

## Art. 11 da LRF com critério relativo (arrecadação abaixo de 10% da mediana da mesma UF e faixa de porte, % do grupo)

| q          |   iptu_rel |   iss_rel |   itbi_rel |   algum_rel |
|:-----------|-----------:|----------:|-----------:|------------:|
| Q1 (menor) |       16.4 |       0.7 |       15.3 |        25.2 |
| Q2         |        7.5 |       0.3 |        7   |        12.8 |
| Q3         |        3.9 |       0.1 |        2.7 |         5.9 |
| Q4         |        0.9 |       0.9 |        1.9 |         3   |
| Q5 (maior) |        1.4 |       0.3 |        1.2 |         2.3 |

Total com algum imposto abaixo do critério: 9.8% de 3453.