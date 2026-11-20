# Testes da pergunta central, 2023

Municípios calculados com receita tributária e população: 4027 (alta confiança: 3558). Medianas. "margem_pct" e os encargos são % da receita livre; "margem_rec_total" é % da receita total (o que resta do orçamento para a decisão local); "vinculada" é a % da receita total fora da receita livre.

## 1. Por quintil de receita tributária própria por habitante

| q          |   n |   trib_pc |   rec_pc |   margem_pct |   margem_rec_total |   minimos |   legislativo |   divida |   precatorios |   encargos |   margem_estrita |   vinculada |   margem_pc |
|:-----------|----:|----------:|---------:|-------------:|-------------------:|----------:|--------------:|---------:|--------------:|-----------:|-----------------:|------------:|------------:|
| Q1 (menor) | 806 |     154.6 |   5272.7 |         50.5 |               25.2 |      38.3 |           6   |      2.1 |           0.4 |       47.3 |             35.8 |        50.2 |      1277.1 |
| Q2         | 805 |     268   |   5715.5 |         50.9 |               27   |      38   |           5.7 |      2.3 |           0.4 |       46.6 |             36   |        47.3 |      1498.9 |
| Q3         | 805 |     452.4 |   6742   |         52.7 |               32.1 |      37.6 |           4.4 |      1.7 |           0.4 |       44.5 |             37.3 |        38.9 |      2077.9 |
| Q4         | 805 |     686.9 |   7253.9 |         53.7 |               34.8 |      37.1 |           3.5 |      1.7 |           0.4 |       43.4 |             39.3 |        34.9 |      2533.9 |
| Q5 (maior) | 806 |    1131.5 |   7370.2 |         54   |               36   |      36.8 |           3.3 |      2   |           0.5 |       43.2 |             40.6 |        33.7 |      2637.7 |

## 2. Por porte

| fx              |   n |   trib_pc |   rec_pc |   margem_pct |   margem_rec_total |   minimos |   legislativo |   divida |   precatorios |   encargos |   margem_estrita |   vinculada |   margem_pc |
|:----------------|----:|----------:|---------:|-------------:|-------------------:|----------:|--------------:|---------:|--------------:|-----------:|-----------------:|------------:|------------:|
| até 5 mil       | 941 |     485.4 |  10773.7 |         53.2 |               36   |      37.7 |           4.4 |      1.1 |           0.2 |       44.1 |             38.8 |        32.2 |      3789.2 |
| 5 a 10 mil      | 849 |     393.1 |   6714   |         52.2 |               31.3 |      37.9 |           4.7 |      1.7 |           0.3 |       45.1 |             37.8 |        39.3 |      2067.8 |
| 10 a 20 mil     | 959 |     344   |   5736.5 |         51.8 |               28.6 |      37.8 |           4.9 |      2.1 |           0.4 |       45.9 |             37.4 |        44.2 |      1583.6 |
| 20 a 50 mil     | 780 |     442   |   5169.8 |         52   |               27   |      37.4 |           4.9 |      2.6 |           0.5 |       45.7 |             36.7 |        47.3 |      1347   |
| 50 a 100 mil    | 257 |     673.4 |   4822.8 |         51.6 |               27.3 |      36.8 |           4.7 |      2.8 |           0.7 |       46.1 |             36.7 |        46.6 |      1294.7 |
| 100 a 500 mil   | 204 |     993.6 |   4814.2 |         52.7 |               29.7 |      36.3 |           3.7 |      3.4 |           1.1 |       45.2 |             36.7 |        41.9 |      1454.3 |
| mais de 500 mil |  37 |    1520.4 |   5233.6 |         50   |               28.7 |      36.7 |           3.4 |      5.2 |           1.2 |       46.5 |             35.2 |        41   |      1508.5 |

## 3. Testes

### 3a. Margem ampla como % da receita livre

|                 |    n |   rho_trib |   p_trib |   rho_pop |   p_pop |      kw |   kw_p |   med_Q1 |   med_Q5 |   dif_Q5_Q1 |   mw_p |   b_trib |   b_trib_p |   b_pop |   b_pop_p |     r2 |
|:----------------|-----:|-----------:|---------:|----------:|--------:|--------:|-------:|---------:|---------:|------------:|-------:|---------:|-----------:|--------:|----------:|-------:|
| todos           | 4027 |     0.2944 |        0 |   -0.1051 |       0 | 363.68  |      0 |  50.4916 |  54.0465 |      3.5549 |      0 |   1.2374 |          0 | -0.4704 |         0 | 0.196  |
| alta confiança  | 3558 |     0.3012 |        0 |   -0.1366 |       0 | 340.221 |      0 |  50.3857 |  53.8676 |      3.4819 |      0 |   1.1033 |          0 | -0.5043 |         0 | 0.2883 |
| sem 1% extremos | 3945 |     0.3034 |        0 |   -0.1111 |       0 | 379.684 |      0 |  50.4767 |  54.014  |      3.5373 |      0 |   1.151  |          0 | -0.4745 |         0 | 0.2829 |

### 3b. Margem ampla como % da receita total

|                 |    n |   rho_trib |   p_trib |   rho_pop |   p_pop |      kw |   kw_p |   med_Q1 |   med_Q5 |   dif_Q5_Q1 |   mw_p |   b_trib |   b_trib_p |   b_pop |   b_pop_p |     r2 |
|:----------------|-----:|-----------:|---------:|----------:|--------:|--------:|-------:|---------:|---------:|------------:|-------:|---------:|-----------:|--------:|----------:|-------:|
| todos           | 4027 |     0.4886 |        0 |   -0.3396 |       0 | 985.26  |      0 |  25.2111 |  36.0171 |     10.806  |      0 |   3.2119 |          0 | -2.0928 |         0 | 0.5148 |
| alta confiança  | 3558 |     0.5047 |        0 |   -0.3856 |       0 | 926.709 |      0 |  25.2087 |  35.6724 |     10.4637 |      0 |   3.4163 |          0 | -2.3039 |         0 | 0.6282 |
| sem 1% extremos | 3945 |     0.4963 |        0 |   -0.3459 |       0 | 990.269 |      0 |  25.2207 |  35.9297 |     10.709  |      0 |   3.215  |          0 | -2.0674 |         0 | 0.5741 |

Legenda: rho_trib = Spearman entre receita tributária por habitante e a margem; rho_pop = com a população; kw = Kruskal-Wallis entre os 5 quintis; med_Q1/med_Q5 e dif_Q5_Q1 = medianas dos quintis extremos e a diferença (p.p.); b_trib e b_pop = coeficientes de uma regressão linear da margem (p.p.) sobre o log da receita tributária por habitante e o log da população, com efeitos fixos de UF e erros robustos (HC3).

## 4. De onde vem a diferença entre o quintil de maior e o de menor base (p.p. da receita livre)

|                  |   Q1 |   Q5 |   Q5 - Q1 |
|:-----------------|-----:|-----:|----------:|
| minimos          | 38.3 | 36.8 |      -1.5 |
| legislativo      |  6   |  3.3 |      -2.7 |
| divida           |  2.1 |  2   |      -0.1 |
| precatorios      |  0.4 |  0.5 |       0.1 |
| encargos         | 47.3 | 43.2 |      -4.1 |
| margem_pct       | 50.5 | 54   |       3.5 |
| margem_rec_total | 25.2 | 36   |      10.8 |
| vinculada        | 50.2 | 33.7 |     -16.5 |

## 5. Seleção: quem ficou fora do cálculo

| faixa           |   municipios |   calculados |   % |
|:----------------|-------------:|-------------:|----:|
| até 5 mil       |         1284 |          963 |  75 |
| 5 a 10 mil      |         1184 |          875 |  74 |
| 10 a 20 mil     |         1350 |          980 |  73 |
| 20 a 50 mil     |         1070 |          803 |  75 |
| 50 a 100 mil    |          344 |          258 |  75 |
| 100 a 500 mil   |          290 |          205 |  71 |
| mais de 500 mil |           47 |           37 |  79 |

| calc   |   trib_pc_mediana |   rec_pc_mediana |   pop_mediana |
|:-------|------------------:|-----------------:|--------------:|
| False  |               415 |             6311 |         11579 |
| True   |               452 |             6366 |         11291 |

## 6. Transferências federais vinculadas por classe, % da receita total (mediana por quintil; FPM, royalties e CIDE ficam fora, pois entram na receita livre)

| q          |   u_adesao |   u_automatica_constitucional |   u_obrigacao_legal |   u_outra |
|:-----------|-----------:|------------------------------:|--------------------:|----------:|
| Q1 (menor) |        4.4 |                          16.2 |                 8.3 |       2   |
| Q2         |        3.6 |                          12.8 |                 7.2 |       1.7 |
| Q3         |        2.5 |                           3.5 |                 5.2 |       1.4 |
| Q4         |        1.9 |                           3   |                 4.1 |       1.1 |
| Q5 (maior) |        1.3 |                           3   |                 3.8 |       0.7 |

Obrigação legal e automática constitucional (Fundeb, salário-educação) formam o bloco heterônomo vinculado; adesão é pactuação (bloco P).
