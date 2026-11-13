# Testes da pergunta central, 2023

Municípios calculados com receita tributária e população: 3891 (alta confiança: 3418). Medianas. "margem_pct" e os encargos são % da receita livre; "margem_rec_total" é % da receita total (o que resta do orçamento para a decisão local); "vinculada" é a % da receita total fora da receita livre.

## 1. Por quintil de receita tributária própria por habitante

| q          |   n |   trib_pc |   rec_pc |   margem_pct |   margem_rec_total |   minimos |   legislativo |   divida |   precatorios |   encargos |   margem_estrita |   vinculada |   margem_pc |
|:-----------|----:|----------:|---------:|-------------:|-------------------:|----------:|--------------:|---------:|--------------:|-----------:|-----------------:|------------:|------------:|
| Q1 (menor) | 779 |     154.7 |   5281.1 |         52.7 |               26.3 |      38.3 |           6   |      2.1 |           0.4 |       47.3 |             35.7 |        49.9 |      1334.1 |
| Q2         | 778 |     267.9 |   5697.3 |         53.3 |               28   |      38   |           5.7 |      2.3 |           0.4 |       46.7 |             36   |        47.2 |      1561.8 |
| Q3         | 778 |     450.1 |   6746   |         55.6 |               33.9 |      37.6 |           4.4 |      1.7 |           0.4 |       44.4 |             37.3 |        38.7 |      2189.3 |
| Q4         | 778 |     682.7 |   7286.5 |         56.6 |               36.6 |      37.2 |           3.5 |      1.7 |           0.4 |       43.4 |             39.2 |        34.9 |      2668.8 |
| Q5 (maior) | 778 |    1131.9 |   7403.2 |         56.8 |               37.6 |      36.8 |           3.3 |      2   |           0.5 |       43.2 |             40.5 |        33.7 |      2780.5 |

## 2. Por porte

| fx             |   n |   trib_pc |   rec_pc |   margem_pct |   margem_rec_total |   minimos |   legislativo |   divida |   precatorios |   encargos |   margem_estrita |   vinculada |   margem_pc |
|:---------------|----:|----------:|---------:|-------------:|-------------------:|----------:|--------------:|---------:|--------------:|-----------:|-----------------:|------------:|------------:|
| até 5 mil      | 917 |     484   |  10805.2 |         55.9 |               37.8 |      37.7 |           4.4 |      1.1 |           0.2 |       44.1 |             38.8 |        32.2 |      4034.1 |
| 5 a 10 mil     | 821 |     393.1 |   6715.8 |         54.8 |               33.2 |      37.9 |           4.7 |      1.7 |           0.3 |       45.2 |             37.6 |        39.3 |      2191   |
| 10 a 20 mil    | 931 |     344   |   5736.5 |         54.2 |               30.1 |      37.8 |           4.9 |      2.1 |           0.4 |       45.8 |             37.4 |        44.2 |      1661.9 |
| 20 a 50 mil    | 751 |     445.2 |   5177   |         54.3 |               28.3 |      37.4 |           4.9 |      2.6 |           0.5 |       45.7 |             36.7 |        47.2 |      1422.9 |
| 50 mil ou mais | 471 |     898.2 |   4833.3 |         54.2 |               30.3 |      36.6 |           4.1 |      3.4 |           0.9 |       45.8 |             36.4 |        44   |      1472.6 |

## 3. Testes

### 3a. Margem ampla como % da receita livre

|                 |    n |   rho_trib |   p_trib |   rho_pop |   p_pop |      kw |   kw_p |   med_Q1 |   med_Q5 |   dif_Q5_Q1 |   mw_p |   b_trib |   b_trib_p |   b_pop |   b_pop_p |     r2 |
|:----------------|-----:|-----------:|---------:|----------:|--------:|--------:|-------:|---------:|---------:|------------:|-------:|---------:|-----------:|--------:|----------:|-------:|
| todos           | 3891 |     0.3562 |        0 |   -0.1381 |       0 | 522.96  |      0 |  52.6917 |  56.7792 |      4.0874 |      0 |   1.1721 |          0 | -0.4334 |         0 | 0.2559 |
| alta confiança  | 3418 |     0.3653 |        0 |   -0.1724 |       0 | 490.761 |      0 |  52.6492 |  56.4529 |      3.8037 |      0 |   1.0094 |          0 | -0.4442 |         0 | 0.3848 |
| sem 1% extremos | 3813 |     0.3674 |        0 |   -0.1453 |       0 | 547.736 |      0 |  52.6908 |  56.7521 |      4.0613 |      0 |   1.0386 |          0 | -0.407  |         0 | 0.3713 |

### 3b. Margem ampla como % da receita total

|                 |    n |   rho_trib |   p_trib |   rho_pop |   p_pop |      kw |   kw_p |   med_Q1 |   med_Q5 |   dif_Q5_Q1 |   mw_p |   b_trib |   b_trib_p |   b_pop |   b_pop_p |     r2 |
|:----------------|-----:|-----------:|---------:|----------:|--------:|--------:|-------:|---------:|---------:|------------:|-------:|---------:|-----------:|--------:|----------:|-------:|
| todos           | 3891 |     0.4961 |        0 |   -0.352  |       0 | 992.246 |      0 |  26.3161 |  37.5977 |     11.2816 |      0 |   3.212  |          0 | -2.1637 |         0 | 0.5435 |
| alta confiança  | 3418 |     0.5098 |        0 |   -0.3981 |       0 | 920.603 |      0 |  26.3331 |  37.2855 |     10.9525 |      0 |   3.4193 |          0 | -2.3748 |         0 | 0.6534 |
| sem 1% extremos | 3813 |     0.5029 |        0 |   -0.3594 |       0 | 996.199 |      0 |  26.3441 |  37.5026 |     11.1585 |      0 |   3.2095 |          0 | -2.1455 |         0 | 0.5976 |

Legenda: rho_trib = Spearman entre receita tributária por habitante e a margem; rho_pop = com a população; kw = Kruskal-Wallis entre os 5 quintis; med_Q1/med_Q5 e dif_Q5_Q1 = medianas dos quintis extremos e a diferença (p.p.); b_trib e b_pop = coeficientes de uma regressão linear da margem (p.p.) sobre o log da receita tributária por habitante e o log da população, com efeitos fixos de UF e erros robustos (HC3).

## 4. De onde vem a diferença entre o quintil de maior e o de menor base (p.p. da receita livre)

|                  |   Q1 |   Q5 |   Q5 - Q1 |
|:-----------------|-----:|-----:|----------:|
| minimos          | 38.3 | 36.8 |      -1.5 |
| legislativo      |  6   |  3.3 |      -2.7 |
| divida           |  2.1 |  2   |      -0.1 |
| precatorios      |  0.4 |  0.5 |       0.1 |
| encargos         | 47.3 | 43.2 |      -4.1 |
| margem_pct       | 52.7 | 56.8 |       4.1 |
| margem_rec_total | 26.3 | 37.6 |      11.3 |
| vinculada        | 49.9 | 33.7 |     -16.2 |

## 5. Seleção: quem ficou fora do cálculo

| faixa          |   municipios |   calculados |   % |
|:---------------|-------------:|-------------:|----:|
| até 5 mil      |         1284 |          948 |  74 |
| 5 a 10 mil     |         1184 |          856 |  72 |
| 10 a 20 mil    |         1350 |          962 |  71 |
| 20 a 50 mil    |         1070 |          783 |  73 |
| 50 mil ou mais |          681 |          488 |  72 |

| calc   |   trib_pc_mediana |   rec_pc_mediana |   pop_mediana |
|:-------|------------------:|-----------------:|--------------:|
| False  |               414 |             6336 |         11602 |
| True   |               450 |             6369 |         11280 |

## 6. Transferências federais vinculadas por classe, % da receita total (mediana por quintil; FPM, royalties e CIDE ficam fora, pois entram na receita livre)

| q          |   u_adesao |   u_automatica_constitucional |   u_obrigacao_legal |   u_outra |
|:-----------|-----------:|------------------------------:|--------------------:|----------:|
| Q1 (menor) |        4.4 |                          16.1 |                 8.3 |       2   |
| Q2         |        3.7 |                          12.9 |                 7.2 |       1.7 |
| Q3         |        2.5 |                           3.5 |                 5.1 |       1.4 |
| Q4         |        1.9 |                           3   |                 4.1 |       1.1 |
| Q5 (maior) |        1.3 |                           3   |                 3.8 |       0.7 |

Obrigação legal e automática constitucional (Fundeb, salário-educação) formam o bloco heterônomo vinculado; adesão é pactuação (bloco P).
