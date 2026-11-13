# Análise comparativa entre UFs e municípios, 2023

Cuidado de cobertura: cada resultado traz o número de municípios calculados; UFs com menos de 40 municípios calculados ou cobertura abaixo de 40% ficam fora dos resultados por UF e marcadas.

## Tabela por UF (medianas dos municípios calculados)

| uf   |   n |   trib_pc |   pib_pc |   margem_rt |   margem_livre |   vinc |   cobertura_% | leitura                |
|:-----|----:|----------:|---------:|------------:|---------------:|-------:|--------------:|:-----------------------|
| RR   |  13 |     301.9 |  27593.9 |        16.4 |           52   |   66.9 |            87 | cobertura insuficiente |
| PA   | 121 |     282.6 |  20090.9 |        17.1 |           45.7 |   63.3 |            84 | ok                     |
| AP   |   7 |     456.9 |  27061.3 |        17.9 |           50.6 |   65.6 |            44 | cobertura insuficiente |
| CE   | 164 |     210.3 |  14133.5 |        18.9 |           45.2 |   57.7 |            89 | ok                     |
| MA   | 163 |     180.2 |  12098.8 |        21.6 |           53.6 |   60.9 |            75 | ok                     |
| AM   |  51 |     147.7 |  13919.8 |        22   |           55.3 |   60   |            82 | ok                     |
| AL   |  34 |     216   |  25387   |        22.4 |           49.2 |   56   |            33 | cobertura insuficiente |
| RJ   |  55 |     716.5 |  36548.5 |        25   |           53.4 |   52.9 |            60 | ok                     |
| PI   | 200 |     211.4 |  13403.2 |        25.2 |           52.3 |   51.4 |            89 | ok                     |
| BA   | 219 |     266.1 |  15142.3 |        26.3 |           51   |   48.2 |            53 | ok                     |
| SE   |  45 |     345.2 |  20115.5 |        27.3 |           51.6 |   47   |            60 | ok                     |
| PE   | 136 |     202.5 |  14627.2 |        28.4 |           54.5 |   48   |            74 | ok                     |
| PB   |  39 |     211.8 |  14849   |        28.4 |           53.1 |   45   |            17 | cobertura insuficiente |
| ES   |  69 |     401.6 |  29212.3 |        30.3 |           56.6 |   45.3 |            88 | ok                     |
| RN   | 148 |     242.9 |  16961.2 |        30.5 |           52.3 |   41.7 |            89 | ok                     |
| RO   |  33 |     484.2 |  39368.2 |        30.8 |           56.4 |   44.2 |            63 | cobertura insuficiente |
| TO   |  85 |     408.9 |  31042.6 |        30.9 |           54.3 |   42.3 |            61 | ok                     |
| MS   |  50 |    1033.8 |  67900.2 |        33.6 |           54.3 |   37.8 |            63 | ok                     |
| MG   | 651 |     317.9 |  23057.1 |        34.1 |           55.4 |   38.5 |            76 | ok                     |
| MT   |  69 |     925.7 |  56441.9 |        35   |           56.6 |   37.5 |            49 | ok                     |
| RS   | 389 |     700.5 |  45654.3 |        35.8 |           56.6 |   36.8 |            78 | ok                     |
| PR   | 259 |     590.8 |  46167.3 |        35.9 |           56.2 |   36.2 |            65 | ok                     |
| GO   | 133 |     616.7 |  38017.4 |        37.5 |           54.7 |   32.1 |            54 | ok                     |
| SC   | 256 |     735.1 |  51053   |        37.7 |           57   |   34.2 |            87 | ok                     |
| AC   |   1 |     701.4 |  33318.6 |        38.9 |           55.4 |   29.8 |             5 | cobertura insuficiente |
| SP   | 501 |     812.5 |  44933.9 |        42.7 |           58.5 |   27   |            78 | ok                     |

## Quintis de base própria por habitante dentro de cada UF, depois juntados

|   qu |   n |   margem_rt |   margem_livre |   vinc |
|-----:|----:|------------:|---------------:|-------:|
|    1 | 760 |        31.6 |           54.5 |   41.8 |
|    2 | 751 |        32.5 |           54.6 |   40.4 |
|    3 | 748 |        32.6 |           55.1 |   39.8 |
|    4 | 751 |        32.7 |           55.1 |   40.5 |
|    5 | 754 |        34.4 |           55.3 |   38.3 |

Teste de Kruskal-Wallis na margem sobre a receita total: p = 7.5e-05.

## Quintis de PIB por habitante dentro de cada UF, depois juntados

|   qu |   n |   margem_rt |   margem_livre |   vinc |
|-----:|----:|------------:|---------------:|-------:|
|    1 | 760 |        30.8 |           54.2 |   43.2 |
|    2 | 751 |        32.1 |           54.7 |   41.4 |
|    3 | 748 |        32.8 |           55.2 |   39.8 |
|    4 | 751 |        33   |           55.2 |   40.2 |
|    5 | 754 |        35.4 |           55.3 |   36   |

Teste de Kruskal-Wallis na margem sobre a receita total: p = 3.9e-18.

## Pares de mesma UF e mesmo porte: terço de maior PIB por habitante menos terço de menor (margem sobre a receita total, pontos)

Grupos comparáveis: 87. Mediana da diferença: 3.4 pontos; positiva em 87% dos grupos.

## Modelo em dois níveis (município dentro de UF)

- Parcela da variação da margem que está entre UFs (sem variáveis): 33%.
- Efeito médio do log do PIB por habitante (intercepto aleatório): 4.28 (erro 0.21).
- Com inclinação aleatória: efeito médio 4.15; desvio-padrão da inclinação entre UFs 1.28.

Inclinação por UF (UFs com 40+ municípios): mínima -1.2, mediana 3.3, máxima 6.1; positiva em 19 de 20.

Sensibilidade (peso inverso da cobertura da UF, com efeitos fixos de UF): efeito do log do PIB por habitante 4.16 (IC95% 3.71 a 4.61).
