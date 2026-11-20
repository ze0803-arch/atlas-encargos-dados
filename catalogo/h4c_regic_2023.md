# H4c, base fora do território (REGIC 2018)

Base: 4336 municípios calculados; hierarquia (grupos 1 a 5): {1: 163, 2: 246, 3: 395, 4: 336, 5: 3196}. Razão = mediana dos dependentes ÷ mediana dos centros, dentro de células faixa de população × quintil de PIB por habitante (células com 5 ou mais em cada grupo), média ponderada em escala log.

| teste                                                | variavel                             |   celulas |   n_dep |   n_cen |   razao |   celulas_abaixo_85 |   celulas_abaixo_100 |
|:-----------------------------------------------------|:-------------------------------------|----------:|--------:|--------:|--------:|--------------------:|---------------------:|
| Principal: dependentes (4 e 5) x centros (1 a 3)     | VA dos serviços por habitante (2021) |        22 |    3022 |     541 |   0.825 |                  12 |                   18 |
| Principal: dependentes (4 e 5) x centros (1 a 3)     | ISS realizado por habitante (2023)   |        21 |    2341 |     457 |   0.735 |                  14 |                   19 |
| Sensibilidade: só Centro Local (5) x centros (1 a 4) | VA dos serviços por habitante (2021) |        22 |    2883 |     803 |   0.817 |                  14 |                   21 |
| Sensibilidade: só Centro Local (5) x centros (1 a 4) | ISS realizado por habitante (2023)   |        21 |    2473 |     640 |   0.834 |                  11 |                   17 |

Critério provisório: dependentes pelo menos 15% abaixo dos centros (razão ≤ 0,85). Limites: classificação de 2018 contra receita de 2023; VA dos serviços de 2021; o quintil de PIB por habitante usa o valor adicionado, então a comparação é em parte circular.
