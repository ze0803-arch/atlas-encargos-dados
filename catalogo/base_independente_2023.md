# Testes com PIB por habitante (medida independente), 2023

Municípios calculados com PIB: 4027. Quintis do PIB por habitante.

## Por quintil de PIB por habitante (medianas)

| q          |   n |   pib_pc |   trib_pc |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|:-----------|----:|---------:|----------:|-----------------------:|-----------------------:|------------:|
| Q1 (menor) | 806 |  12684.4 |     175.8 |                   50.2 |                   23.6 |        52.9 |
| Q2         | 805 |  18627   |     264.1 |                   51.3 |                   27.9 |        45.1 |
| Q3         | 805 |  29638.3 |     474.9 |                   52.6 |                   31.9 |        39.6 |
| Q4         | 805 |  43893.4 |     676.4 |                   53.8 |                   34.3 |        35.4 |
| Q5 (maior) | 806 |  72243.9 |     914   |                   53.9 |                   36.4 |        32.3 |

## Efeito da base sobre a margem (efeitos fixos de UF, erro agrupado por UF, controle de população)

| desfecho                       | base                              |    n |   rho |   coef | ic95         |       p |
|:-------------------------------|:----------------------------------|-----:|------:|-------:|:-------------|--------:|
| margem % receita livre         | log do PIB por habitante          | 4027 | 0.295 |   1.18 | [0.78; 1.58] | 9.4e-09 |
| margem % receita livre         | log da base própria por habitante | 4027 | 0.294 |   1.24 | [0.71; 1.76] | 4.2e-06 |
| margem % receita total         | log do PIB por habitante          | 4027 | 0.54  |   4.17 | [3.64; 4.71] | 8e-53   |
| margem % receita total         | log da base própria por habitante | 4027 | 0.489 |   3.21 | [2.76; 3.67] | 9.7e-44 |
| parcela livre da receita total | log do PIB por habitante          | 4027 | 0.559 |   6.7  | [5.67; 7.72] | 1.6e-37 |
| parcela livre da receita total | log da base própria por habitante | 4027 | 0.494 |   4.91 | [4.36; 5.46] | 2.7e-68 |

Diferença entre Q5 e Q1 de PIB: margem sobre a receita livre +3.7 pontos; margem sobre a receita total +12.8 pontos; vinculada -20.6 pontos.

## Quintis de PIB por habitante dentro de cada UF

|   qu |   n |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|-----:|----:|-----------------------:|-----------------------:|------------:|
|    1 | 808 |                   51.5 |                   29   |        43.6 |
|    2 | 800 |                   52.2 |                   30.4 |        41.8 |
|    3 | 793 |                   52.6 |                   31   |        40   |
|    4 | 800 |                   52.6 |                   31.2 |        40.3 |
|    5 | 805 |                   52.8 |                   33.5 |        36.4 |

Correlação (Spearman) entre PIB por habitante e margem sobre a receita total dentro da UF: mediana 0.20; positiva em 21 de 21 UFs.

## Art. 11 da LRF, com quintis de PIB por habitante (% do grupo abaixo do critério relativo)

| q          |   iptu_rel |   iss_rel |   itbi_rel |   algum |
|:-----------|-----------:|----------:|-----------:|--------:|
| Q1 (menor) |       15.7 |       0.7 |       16.5 |    25.7 |
| Q2         |        8.4 |       0.3 |        7.3 |    13.4 |
| Q3         |        2.6 |       0.3 |        1.5 |     3.6 |
| Q4         |        1.5 |       0.8 |        1.6 |     3.1 |
| Q5 (maior) |        1.8 |       0.6 |        1.5 |     3.5 |

Logit com efeitos fixos de UF: coeficiente do log do PIB por habitante = -1.04 (p = 4.2e-10).
