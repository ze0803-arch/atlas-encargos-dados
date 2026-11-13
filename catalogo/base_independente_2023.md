# Testes com PIB por habitante (medida independente), 2023

Municípios calculados com PIB: 3891. Quintis do PIB por habitante.

## Por quintil de PIB por habitante (medianas)

| q          |   n |   pib_pc |   trib_pc |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|:-----------|----:|---------:|----------:|-----------------------:|-----------------------:|------------:|
| Q1 (menor) | 779 |  12689.3 |     175.9 |                   52.1 |                   24.4 |        52.8 |
| Q2         | 778 |  18647.8 |     264.2 |                   53.8 |                   29.3 |        44.9 |
| Q3         | 778 |  29620.8 |     472.3 |                   55.4 |                   33.6 |        39.6 |
| Q4         | 778 |  43889.2 |     675.2 |                   56.5 |                   36.3 |        35.4 |
| Q5 (maior) | 778 |  71998   |     913.1 |                   56.7 |                   38.3 |        32.2 |

## Efeito da base sobre a margem (efeitos fixos de UF, erro agrupado por UF, controle de população)

| desfecho                       | base                              |    n |   rho |   coef | ic95         |       p |
|:-------------------------------|:----------------------------------|-----:|------:|-------:|:-------------|--------:|
| margem % receita livre         | log do PIB por habitante          | 3891 | 0.372 |   1.14 | [0.82; 1.46] | 2.8e-12 |
| margem % receita livre         | log da base própria por habitante | 3891 | 0.356 |   1.17 | [0.73; 1.62] | 2.2e-07 |
| margem % receita total         | log do PIB por habitante          | 3891 | 0.554 |   4.19 | [3.57; 4.81] | 2.1e-40 |
| margem % receita total         | log da base própria por habitante | 3891 | 0.496 |   3.21 | [2.78; 3.64] | 5.9e-49 |
| parcela livre da receita total | log do PIB por habitante          | 3891 | 0.556 |   6.55 | [5.40; 7.69] | 3.6e-29 |
| parcela livre da receita total | log da base própria por habitante | 3891 | 0.488 |   4.79 | [4.23; 5.35] | 2.2e-63 |

Diferença entre Q5 e Q1 de PIB: margem sobre a receita livre +4.6 pontos; margem sobre a receita total +13.9 pontos; vinculada -20.6 pontos.

## Quintis de PIB por habitante dentro de cada UF

|   qu |   n |   margem_pct_rec_livre |   margem_pct_rec_total |   vinculada |
|-----:|----:|-----------------------:|-----------------------:|------------:|
|    1 | 782 |                   54.2 |                   30.7 |        43.4 |
|    2 | 772 |                   54.7 |                   31.9 |        41.7 |
|    3 | 768 |                   55.2 |                   32.7 |        40   |
|    4 | 772 |                   55.1 |                   32.9 |        40.3 |
|    5 | 776 |                   55.3 |                   35.2 |        36.4 |

Correlação (Spearman) entre PIB por habitante e margem sobre a receita total dentro da UF: mediana 0.21; positiva em 20 de 20 UFs.

## Art. 11 da LRF, com quintis de PIB por habitante (% do grupo abaixo do critério relativo)

| q          |   iptu_rel |   iss_rel |   itbi_rel |   algum |
|:-----------|-----------:|----------:|-----------:|--------:|
| Q1 (menor) |       15.6 |       0.7 |       15.9 |    25.3 |
| Q2         |        8.6 |       0.3 |        7.6 |    13.9 |
| Q3         |        2.7 |       0.3 |        1.6 |     3.8 |
| Q4         |        1.4 |       0.6 |        1.3 |     2.8 |
| Q5 (maior) |        1.8 |       0.4 |        1.8 |     3.6 |

Logit com efeitos fixos de UF: coeficiente do log do PIB por habitante = -1.05 (p = 8.6e-10).
