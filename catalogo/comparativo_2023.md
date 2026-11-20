# Análise comparativa entre UFs e municípios, 2023

Cuidado de cobertura: cada resultado traz o número de municípios calculados; UFs com menos de 40 municípios calculados ou cobertura abaixo de 40% ficam fora dos resultados por UF e marcadas.

## Tabela por UF (medianas dos municípios calculados)

| uf   |   n |   trib_pc |   pib_pc |   margem_rt |   margem_livre |   vinc |   cobertura_% | leitura                |
|:-----|----:|----------:|---------:|------------:|---------------:|-------:|--------------:|:-----------------------|
| PA   | 125 |     279.5 |  20090.9 |        15.9 |           43.9 |   63.3 |            87 | ok                     |
| RR   |  13 |     301.9 |  27593.9 |        16.1 |           51.2 |   66.9 |            87 | cobertura insuficiente |
| AP   |   7 |     456.9 |  27061.3 |        16.7 |           44.2 |   65.6 |            44 | cobertura insuficiente |
| CE   | 166 |     210.7 |  14233.2 |        18.1 |           42.8 |   57.8 |            90 | ok                     |
| AL   |  35 |     207.5 |  24061.9 |        21   |           47.6 |   56.2 |            34 | cobertura insuficiente |
| MA   | 177 |     180.2 |  12098.8 |        21.5 |           52.9 |   60.3 |            82 | ok                     |
| AM   |  51 |     147.7 |  13919.8 |        21.9 |           54.1 |   60   |            82 | ok                     |
| RJ   |  54 |     709.6 |  36383.8 |        23.4 |           49.2 |   52.8 |            59 | ok                     |
| PI   | 209 |     211.4 |  13440.4 |        24.4 |           50.6 |   51.5 |            93 | ok                     |
| BA   | 224 |     265   |  15169.4 |        25.9 |           49.9 |   48.3 |            54 | ok                     |
| PB   |  45 |     210.3 |  14436.2 |        26.2 |           50   |   45.3 |            20 | cobertura insuficiente |
| PE   | 138 |     202.5 |  14716.9 |        26.9 |           51.7 |   48   |            75 | ok                     |
| SE   |  45 |     345.2 |  20115.5 |        26.9 |           50.7 |   47   |            60 | ok                     |
| ES   |  74 |     409.5 |  30506.5 |        28.2 |           53   |   45.4 |            95 | ok                     |
| RO   |  34 |     485.2 |  39756.5 |        29   |           53.3 |   44.4 |            65 | cobertura insuficiente |
| RN   | 154 |     242.9 |  16961.2 |        29.4 |           50.4 |   41.4 |            92 | ok                     |
| TO   |  85 |     408.9 |  31042.6 |        29.4 |           51.2 |   42   |            61 | ok                     |
| MS   |  50 |    1033.8 |  67900.2 |        31.1 |           51.6 |   37.8 |            63 | ok                     |
| MG   | 668 |     319.3 |  23197.7 |        32.7 |           52.8 |   38.4 |            78 | ok                     |
| MT   |  72 |     917.2 |  54313.2 |        33.2 |           54.2 |   37.8 |            51 | ok                     |
| RS   | 401 |     700.5 |  45687.6 |        33.6 |           53.2 |   36.9 |            81 | ok                     |
| PR   | 267 |     597.5 |  46207.5 |        33.8 |           53.6 |   36.2 |            67 | ok                     |
| GO   | 144 |     623.6 |  37768.9 |        35   |           51.7 |   32.5 |            59 | ok                     |
| SC   | 264 |     735.1 |  50833.1 |        35.6 |           54.1 |   34.3 |            89 | ok                     |
| AC   |   1 |     701.4 |  33318.6 |        36.6 |           52.2 |   29.8 |             5 | cobertura insuficiente |
| SP   | 524 |     826.2 |  44978.1 |        40.8 |           55.7 |   26.8 |            81 | ok                     |

## Quintis de base própria por habitante dentro de cada UF, depois juntados

|   qu |   n |   margem_rt |   margem_livre |   vinc |
|-----:|----:|------------:|---------------:|-------:|
|    1 | 785 |        29.9 |           51.8 |   41.9 |
|    2 | 777 |        30.7 |           52.1 |   40.5 |
|    3 | 771 |        31.1 |           52.6 |   39.6 |
|    4 | 777 |        31.2 |           52.6 |   40.5 |
|    5 | 782 |        32.8 |           53   |   38.3 |

Teste de Kruskal-Wallis na margem sobre a receita total: p = 1.4e-05.

## Quintis de PIB por habitante dentro de cada UF, depois juntados

|   qu |   n |   margem_rt |   margem_livre |   vinc |
|-----:|----:|------------:|---------------:|-------:|
|    1 | 785 |        29.3 |           51.5 |   43.1 |
|    2 | 777 |        30.5 |           52.2 |   41.5 |
|    3 | 771 |        31.2 |           52.6 |   39.6 |
|    4 | 777 |        31.4 |           52.7 |   40.2 |
|    5 | 782 |        33.6 |           52.8 |   36.1 |

Teste de Kruskal-Wallis na margem sobre a receita total: p = 4.1e-19.

## Pares de mesma UF e mesmo porte: terço de maior PIB por habitante menos terço de menor (margem sobre a receita total, pontos)

Grupos comparáveis: 94. Mediana da diferença: 3.3 pontos; positiva em 87% dos grupos.

## Modelo em dois níveis (município dentro de UF)

- Parcela da variação da margem que está entre UFs (sem variáveis): 30%.
- Efeito médio do log do PIB por habitante (intercepto aleatório): 4.25 (erro 0.21).
- Com inclinação aleatória: efeito médio 4.08; desvio-padrão da inclinação entre UFs 0.95.

Inclinação por UF (UFs com 40+ municípios): mínima -0.1, mediana 3.0, máxima 5.7; positiva em 19 de 20.

Sensibilidade (peso inverso da cobertura da UF, com efeitos fixos de UF): efeito do log do PIB por habitante 4.14 (IC95% 3.71 a 4.57).
