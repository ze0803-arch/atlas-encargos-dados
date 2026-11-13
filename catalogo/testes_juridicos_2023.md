# Testes jurídicos, 2023

Municípios calculados com MSCE e dados de impostos: 3453. Medianas; quintis da receita tributária própria por habitante (Q1 = base menor).

## A. Art. 167, § 7º, da CF: o encargo vem com a fonte correspondente?

Por área, a despesa liquidada na função é separada pela fonte de recursos que a paga: transferência federal vinculada (SUS 1600/1601 e ACS 1604; FNAS 1660; FNDE 1550-1553 e 1569 e FUNDEB 1540-1543), fonte livre (1500/1501) e outras. "Descoberto" é a parte paga com fonte livre, isto é, o encargo que o município financia com a própria base.

### A1. Cobertura por fonte, mediana por quintil (% da despesa da função)

| area                           | q          |   n |   despesa_pc |   federal_vinculada_pct |   fonte_livre_pct |
|:-------------------------------|:-----------|----:|-------------:|------------------------:|------------------:|
| Saúde (função 10)              | Q1 (menor) | 691 |       1183.5 |                    42.6 |              44.5 |
| Saúde (função 10)              | Q2         | 688 |       1254.1 |                    35.1 |              48.6 |
| Saúde (função 10)              | Q3         | 679 |       1470.3 |                    22.2 |              58.6 |
| Saúde (função 10)              | Q4         | 661 |       1592.7 |                    18.4 |              66   |
| Saúde (função 10)              | Q5 (maior) | 672 |       1616.2 |                    16.4 |              68.3 |
| Assistência social (função 08) | Q1 (menor) | 679 |        164.7 |                    28.3 |              62.8 |
| Assistência social (função 08) | Q2         | 683 |        171   |                    22.2 |              65.5 |
| Assistência social (função 08) | Q3         | 676 |        223.5 |                    10.8 |              69.7 |
| Assistência social (função 08) | Q4         | 655 |        231.7 |                     7.7 |              75.3 |
| Assistência social (função 08) | Q5 (maior) | 668 |        223.1 |                     5.2 |              74.5 |
| Educação (função 12)           | Q1 (menor) | 691 |       1761.9 |                    80.3 |              15.5 |
| Educação (função 12)           | Q2         | 688 |       1771.9 |                    72.1 |              21.1 |
| Educação (função 12)           | Q3         | 678 |       1638   |                    53.6 |              33.9 |
| Educação (função 12)           | Q4         | 660 |       1689.6 |                    51   |              39.5 |
| Educação (função 12)           | Q5 (maior) | 672 |       1803.5 |                    49.8 |              41.3 |

### A2. Testes (Spearman com a receita tributária por habitante; Kruskal-Wallis entre quintis)

| area                           | medida                |    rho |   p_spearman |     p_kw |
|:-------------------------------|:----------------------|-------:|-------------:|---------:|
| Saúde (função 10)              | federal vinculada     | -0.542 |     4.4e-258 | 1.1e-217 |
| Saúde (função 10)              | fonte livre           |  0.481 |     4.4e-196 | 1.8e-174 |
| Saúde (função 10)              | despesa por habitante |  0.328 |     8.3e-86  | 9.2e-80  |
| Assistência social (função 08) | federal vinculada     | -0.597 |     0        | 1.7e-254 |
| Assistência social (função 08) | fonte livre           |  0.21  |     8.7e-35  | 4.3e-32  |
| Assistência social (função 08) | despesa por habitante |  0.212 |     1.3e-35  | 9.2e-39  |
| Educação (função 12)           | federal vinculada     | -0.491 |     2.4e-205 | 5.3e-179 |
| Educação (função 12)           | fonte livre           |  0.539 |     1.5e-254 | 1.2e-212 |
| Educação (função 12)           | despesa por habitante |  0.028 |     0.11     | 3.8e-07  |

### A1b. Quanto da parte paga com fonte livre (saúde e educação juntas) é o mínimo constitucional (25% e 15%) e quanto é excedente

O mínimo vem da CF (arts. 198 e 212), não de lei; o § 7º trata de encargo imposto por lei. Excedente = fonte livre gasta nas funções 10 e 12 acima do mínimo exigido calculado pelo sistema.

| q          |   minimo_pct_despesa |   excedente_pct_despesa |   municipios_com_excedente_acima_5pct |
|:-----------|---------------------:|------------------------:|--------------------------------------:|
| Q1 (menor) |                 34   |                       0 |                                   9.3 |
| Q2         |                 38.5 |                       0 |                                  11.2 |
| Q3         |                 50.9 |                       0 |                                  17.7 |
| Q4         |                 53.3 |                       0 |                                  28.1 |
| Q5 (maior) |                 52.7 |                       0 |                                  37.5 |

Excedente sobre o mínimo: rho com a base própria = 0.294, p = 1.2e-68; KW p = 5.3e-64

### A3. Pisos: o lado federal (o custo exige a RAIS e fica pendente)

Assistência federal ao piso da enfermagem (Lei 14.581/2023, Portaria GM/MS 1.135/2023) e vencimentos de ACS/ACE (fonte 1604), por habitante e como % da despesa de pessoal da função 10 (MSC):

| q          |   n |   enf_recebeu |   enf_pc |   enf_pct_pessoal_saude |   acs_pc |   acs_pct_pessoal_saude |
|:-----------|----:|--------------:|---------:|------------------------:|---------:|------------------------:|
| Q1 (menor) | 691 |          99.9 |     47.3 |                     8.4 |     43.6 |                     6.9 |
| Q2         | 690 |          98.8 |     40.3 |                     7   |     64.1 |                     8.7 |
| Q3         | 691 |          94.4 |     23.6 |                     3.5 |     41.5 |                     5.8 |
| Q4         | 690 |          91.3 |     13.4 |                     1.9 |     34.7 |                     5.6 |
| Q5 (maior) | 691 |          93.5 |     14.1 |                     2.2 |     21.5 |                     3.3 |

- enfermagem (R$/hab): rho = -0.482, p = 3e-200; Kruskal-Wallis p = 4.2e-185
- ACS/ACE (R$/hab): rho = -0.136, p = 9.1e-16; Kruskal-Wallis p = 4.1e-16
- enfermagem % pessoal saúde: rho = -0.544, p = 9.7e-258; Kruskal-Wallis p = 1.2e-226
- ACS % pessoal saúde: rho = -0.175, p = 1.4e-24; Kruskal-Wallis p = 8e-25

### A4. FUNDEB: pessoal (elementos 11, 13 e 16) sobre a despesa nas fontes 1540-1543 (aproximação do mínimo de 70%)

Mediana 82.8%; 70.7% dos 3333 com despesa nessas fontes estão em 70% ou mais. Por quintil (mediana): Q1 (menor) 72.6%; Q2 75.8%; Q3 86.0%; Q4 89.8%; Q5 (maior) 90.7%

### A5. Poder de investir (grupo de despesa 4)

| q          |   inv_pc |   inv_pct_despesa |   inv_pago_com_fonte_livre_pct |
|:-----------|---------:|------------------:|-------------------------------:|
| Q1 (menor) |    342.4 |               6.9 |                           20.5 |
| Q2         |    397   |               8   |                           18   |
| Q3         |    497.6 |               8.5 |                           22.4 |
| Q4         |    494   |               8   |                           28.5 |
| Q5 (maior) |    508.5 |               7.6 |                           32.7 |

- investimento por habitante: rho = 0.193, p = 3.2e-30; KW p = 8.6e-29
- investimento % da despesa: rho = 0.054, p = 0.0014; KW p = 2.2e-05
- % do investimento pago com fonte livre: rho = 0.214, p = 5.9e-36; KW p = 4e-37

## B. Art. 11 da LRF: efetiva arrecadação dos impostos municipais

Requisito: instituição, previsão e efetiva arrecadação de todos os tributos da competência do ente; o parágrafo único veda transferências voluntárias ao ente que não o cumpra quanto aos impostos. Teste operacional: receita realizada nas naturezas IPTU (1112.50), ITBI (1112.53) e ISS (1114.51) na MSC de dezembro de 2023. "Zero" = nenhuma arrecadação lançada; "baixa" = menos de R$ 10 por habitante.

### B1. Municípios sem arrecadação (% do grupo)

Por quintil de base própria:

| q          |   n |   IPTU_zero |   ITBI_zero |   ISS_zero |   algum_zero |   algum_baixa |
|:-----------|----:|------------:|------------:|-----------:|-------------:|--------------:|
| Q1 (menor) | 691 |         5.6 |         5.9 |        0.4 |          9   |          88.1 |
| Q2         | 690 |         2.8 |         3.2 |        0.1 |          5.7 |          56.4 |
| Q3         | 691 |         1.9 |         1.2 |        0.1 |          2.2 |          17.4 |
| Q4         | 690 |         0.6 |         1.4 |        0.4 |          1.9 |           6.8 |
| Q5 (maior) | 691 |         0.9 |         0.7 |        0.1 |          1.3 |           5.6 |

Por porte:

| fx             |   n |   IPTU_zero |   ITBI_zero |   ISS_zero |   algum_zero |   algum_baixa |
|:---------------|----:|------------:|------------:|-----------:|-------------:|--------------:|
| até 5 mil      | 818 |         2.7 |         3.8 |        0.1 |          5.5 |          28.7 |
| 5 a 10 mil     | 738 |         3.5 |         2   |        0   |          4.5 |          37.9 |
| 10 a 20 mil    | 822 |         2.2 |         3   |        0.6 |          4.4 |          44.3 |
| 20 a 50 mil    | 662 |         2.3 |         2.1 |        0.5 |          3.5 |          39.4 |
| 50 mil ou mais | 413 |         0   |         0.2 |        0   |          0.2 |          15.5 |

Total (3453): IPTU zero 2.3%; ITBI zero 2.5%; ISS zero 0.3%; algum dos três zero 4.0%; algum abaixo de R$ 10/hab 34.9%.

### B2. Associação com a base fiscal (logit simples com o log da receita tributária por habitante e da população, efeitos fixos de UF omitidos; o sinal indica a direção)

| desfecho      |   coef_log_trib_pc |       p |   coef_log_pop |   p_pop |
|:--------------|-------------------:|--------:|---------------:|--------:|
| iptu_zero     |             -1.009 | 1e-11   |         -0.381 | 0.0032  |
| itbi_zero     |             -1.049 | 5.2e-13 |         -0.434 | 0.00071 |
| iss_zero      |             -0.076 | 0.86    |          0.041 | 0.89    |
| qualquer_zero |             -0.993 | 2.5e-17 |         -0.412 | 4.1e-05 |

### B3. Exposição à sanção do parágrafo único: transferências voluntárias da União recebidas em 2023

- algum imposto com arrecadação zero: 138 municípios (4.0%); receberam R$ 1.26 bilhões em convênios e ações voluntárias específicas (3.8% do total do grupo analisado); mediana por habitante R$ 681 contra R$ 389 nos demais.
- algum imposto abaixo de R$ 10/hab: 1204 municípios (34.9%); receberam R$ 11.59 bilhões em convênios e ações voluntárias específicas (35.2% do total do grupo analisado); mediana por habitante R$ 522 contra R$ 334 nos demais.

Observação: "outras voluntárias específicas" inclui a assistência ao piso da enfermagem, que é obrigação legal; a soma é limite superior da exposição.