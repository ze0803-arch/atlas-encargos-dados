# Testes jurídicos, 2023

Municípios calculados com MSCE e dados de impostos: 3640. Medianas; quintis da receita tributária própria por habitante (Q1 = base menor).

## A. Art. 167, § 7º, da CF: o encargo vem com a fonte correspondente?

Por área, a despesa liquidada na função é separada pela fonte de recursos que a paga: transferência federal vinculada (SUS 1600/1601 e ACS 1604; FNAS 1660; FNDE 1550-1553 e 1569 e FUNDEB 1540-1543), fonte livre (1500/1501) e outras. "Descoberto" é a parte paga com fonte livre, isto é, o encargo que o município financia com a própria base.

### A1. Cobertura por fonte, mediana por quintil (% da despesa da função)

| area                           | q          |   n |   despesa_pc |   federal_vinculada_pct |   fonte_livre_pct |
|:-------------------------------|:-----------|----:|-------------:|------------------------:|------------------:|
| Saúde (função 10)              | Q1 (menor) | 728 |       1196.3 |                    42.6 |              44.5 |
| Saúde (função 10)              | Q2         | 726 |       1274.9 |                    34.8 |              49   |
| Saúde (função 10)              | Q3         | 714 |       1487.2 |                    22.2 |              58.8 |
| Saúde (função 10)              | Q4         | 697 |       1627.1 |                    18.4 |              66.2 |
| Saúde (função 10)              | Q5 (maior) | 707 |       1658   |                    16.2 |              68.1 |
| Assistência social (função 08) | Q1 (menor) | 716 |        168.2 |                    28.3 |              62.7 |
| Assistência social (função 08) | Q2         | 721 |        174.6 |                    22   |              65.6 |
| Assistência social (função 08) | Q3         | 711 |        227.2 |                    10.8 |              69.8 |
| Assistência social (função 08) | Q4         | 690 |        241.7 |                     7.7 |              75.2 |
| Assistência social (função 08) | Q5 (maior) | 703 |        229   |                     5.1 |              74.6 |
| Educação (função 12)           | Q1 (menor) | 728 |       1785   |                    80.3 |              15.5 |
| Educação (função 12)           | Q2         | 726 |       1782   |                    71.5 |              21.1 |
| Educação (função 12)           | Q3         | 713 |       1679.1 |                    53.3 |              34.4 |
| Educação (função 12)           | Q4         | 696 |       1721.8 |                    51   |              39.7 |
| Educação (função 12)           | Q5 (maior) | 707 |       1855   |                    49.9 |              41.3 |

### A2. Testes (Spearman com a receita tributária por habitante; Kruskal-Wallis entre quintis)

| area                           | medida                |    rho |   p_spearman |     p_kw |
|:-------------------------------|:----------------------|-------:|-------------:|---------:|
| Saúde (função 10)              | federal vinculada     | -0.547 |     8.1e-278 | 3.3e-231 |
| Saúde (função 10)              | fonte livre           |  0.478 |     8.8e-204 | 1.7e-180 |
| Saúde (função 10)              | despesa por habitante |  0.326 |     5.4e-89  | 2.3e-81  |
| Assistência social (função 08) | federal vinculada     | -0.6   |     0        | 6.8e-271 |
| Assistência social (função 08) | fonte livre           |  0.203 |     2.2e-34  | 8.6e-32  |
| Assistência social (função 08) | despesa por habitante |  0.214 |     5.2e-38  | 3.2e-40  |
| Educação (função 12)           | federal vinculada     | -0.492 |     1.7e-217 | 6.4e-188 |
| Educação (função 12)           | fonte livre           |  0.534 |     6.5e-262 | 5.4e-219 |
| Educação (função 12)           | despesa por habitante |  0.035 |     0.035    | 1.4e-06  |

### A1b. Quanto da parte paga com fonte livre (saúde e educação juntas) é o mínimo constitucional (25% e 15%) e quanto é excedente

O mínimo vem da CF (arts. 198 e 212), não de lei; o § 7º trata de encargo imposto por lei. Excedente = fonte livre gasta nas funções 10 e 12 acima do mínimo exigido calculado pelo sistema.

| q          |   minimo_pct_despesa |   excedente_pct_despesa |   municipios_com_excedente_acima_5pct |
|:-----------|---------------------:|------------------------:|--------------------------------------:|
| Q1 (menor) |                 33.7 |                       0 |                                  11.5 |
| Q2         |                 37.8 |                       0 |                                  13.3 |
| Q3         |                 50.3 |                       0 |                                  21.6 |
| Q4         |                 52.7 |                       0 |                                  31.4 |
| Q5 (maior) |                 52.4 |                       0 |                                  39   |

Excedente sobre o mínimo: rho com a base própria = 0.281, p = 5.3e-66; KW p = 1.8e-59

### A3. Pisos: o lado federal (o custo é tratado no teto de exposição, D54)

Assistência federal ao piso da enfermagem (Lei 14.581/2023, Portaria GM/MS 1.135/2023) e vencimentos de ACS/ACE (fonte 1604), por habitante e como % da despesa de pessoal da função 10 (MSC):

| q          |   n |   enf_recebeu |   enf_pc |   enf_pct_pessoal_saude |   acs_pc |   acs_pct_pessoal_saude |
|:-----------|----:|--------------:|---------:|------------------------:|---------:|------------------------:|
| Q1 (menor) | 728 |          99.9 |     47.3 |                     8.3 |     45.7 |                     6.8 |
| Q2         | 728 |          98.6 |     40.3 |                     6.9 |     64.5 |                     8.8 |
| Q3         | 728 |          94.2 |     23.3 |                     3.3 |     41.3 |                     5.4 |
| Q4         | 728 |          91.5 |     13.9 |                     1.9 |     33.4 |                     5.5 |
| Q5 (maior) | 728 |          93.3 |     13.9 |                     2   |     21.9 |                     3.4 |

- enfermagem (R$/hab): rho = -0.484, p = 1.8e-213; Kruskal-Wallis p = 1.9e-195
- ACS/ACE (R$/hab): rho = -0.128, p = 7.2e-15; Kruskal-Wallis p = 3.8e-16
- enfermagem % pessoal saúde: rho = -0.543, p = 1.3e-270; Kruskal-Wallis p = 3.2e-236
- ACS % pessoal saúde: rho = -0.174, p = 2.5e-25; Kruskal-Wallis p = 1.5e-26

### A4. FUNDEB: pessoal (elementos 11, 13 e 16) sobre a despesa nas fontes 1540-1543 (aproximação do mínimo de 70%)

Mediana 82.9%; 70.5% dos 3508 com despesa nessas fontes estão em 70% ou mais. Por quintil (mediana): Q1 (menor) 72.6%; Q2 75.5%; Q3 86.3%; Q4 89.8%; Q5 (maior) 90.6%

### A5. Poder de investir (grupo de despesa 4)

| q          |   inv_pc |   inv_pct_despesa |   inv_pago_com_fonte_livre_pct |
|:-----------|---------:|------------------:|-------------------------------:|
| Q1 (menor) |    345.9 |               6.8 |                           20.5 |
| Q2         |    406.3 |               8   |                           18.3 |
| Q3         |    501.6 |               8.5 |                           22.7 |
| Q4         |    502   |               7.9 |                           28.4 |
| Q5 (maior) |    521   |               7.6 |                           32.4 |

- investimento por habitante: rho = 0.194, p = 3.2e-32; KW p = 5e-30
- investimento % da despesa: rho = 0.052, p = 0.0017; KW p = 4e-05
- % do investimento pago com fonte livre: rho = 0.209, p = 3.4e-36; KW p = 3e-37

## B. Art. 11 da LRF: efetiva arrecadação dos impostos municipais

Requisito: instituição, previsão e efetiva arrecadação de todos os tributos da competência do ente; o parágrafo único veda transferências voluntárias ao ente que não o cumpra quanto aos impostos. Teste operacional: receita realizada nas naturezas IPTU (1112.50), ITBI (1112.53) e ISS (1114.51) na MSC de dezembro de 2023. "Zero" = nenhuma arrecadação lançada; "baixa" = menos de R$ 10 por habitante.

### B1. Municípios sem arrecadação (% do grupo)

Por quintil de base própria:

| q          |   n |   IPTU_zero |   ITBI_zero |   ISS_zero |   algum_zero |   algum_baixa |
|:-----------|----:|------------:|------------:|-----------:|-------------:|--------------:|
| Q1 (menor) | 728 |         5.5 |         5.8 |        0.4 |          8.7 |          87.8 |
| Q2         | 728 |         2.9 |         3.2 |        0.1 |          5.6 |          55.5 |
| Q3         | 728 |         1.9 |         1.1 |        0.3 |          2.3 |          16.5 |
| Q4         | 728 |         0.7 |         1.5 |        0.7 |          2.1 |           6.9 |
| Q5 (maior) | 728 |         0.7 |         0.8 |        0.1 |          1.2 |           5.8 |

Por porte:

| fx              |   n |   IPTU_zero |   ITBI_zero |   ISS_zero |   algum_zero |   algum_baixa |
|:----------------|----:|------------:|------------:|-----------:|-------------:|--------------:|
| até 5 mil       | 863 |         2.9 |         3.9 |        0.5 |          5.9 |          28.9 |
| 5 a 10 mil      | 774 |         3.4 |         1.9 |        0   |          4.3 |          37.3 |
| 10 a 20 mil     | 864 |         2.1 |         2.9 |        0.6 |          4.2 |          43.6 |
| 20 a 50 mil     | 703 |         2.3 |         2.1 |        0.4 |          3.4 |          39.1 |
| 50 a 100 mil    | 221 |         0   |         0.5 |        0   |          0.5 |          24.9 |
| 100 a 500 mil   | 183 |         0   |         0   |        0   |          0   |           5.5 |
| mais de 500 mil |  32 |         0   |         0   |        0   |          0   |           0   |

Total (3640): IPTU zero 2.3%; ITBI zero 2.5%; ISS zero 0.3%; algum dos três zero 4.0%; algum abaixo de R$ 10/hab 34.5%.

### B2. Associação com a base fiscal (logit simples com o log da receita tributária por habitante e da população, efeitos fixos de UF omitidos; o sinal indica a direção)

| desfecho      |   coef_log_trib_pc |       p |   coef_log_pop |   p_pop |
|:--------------|-------------------:|--------:|---------------:|--------:|
| iptu_zero     |             -1.007 | 3.6e-12 |         -0.398 | 0.0017  |
| itbi_zero     |             -1.027 | 4.2e-13 |         -0.448 | 0.00036 |
| iss_zero      |              0.118 | 0.75    |         -0.248 | 0.36    |
| qualquer_zero |             -0.961 | 3.7e-17 |         -0.446 | 6.4e-06 |

### B3. Exposição à sanção do parágrafo único: transferências voluntárias da União recebidas em 2023

- algum imposto com arrecadação zero: 145 municípios (4.0%); receberam R$ 1.30 bilhões em convênios e ações voluntárias específicas (3.8% do total do grupo analisado); mediana por habitante R$ 679 contra R$ 390 nos demais.
- algum imposto abaixo de R$ 10/hab: 1255 municípios (34.5%); receberam R$ 11.99 bilhões em convênios e ações voluntárias específicas (34.7% do total do grupo analisado); mediana por habitante R$ 524 contra R$ 334 nos demais.

Observação: "outras voluntárias específicas" inclui a assistência ao piso da enfermagem, que é obrigação legal; a soma é limite superior da exposição.