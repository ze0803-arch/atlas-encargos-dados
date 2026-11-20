Fonte: Tesouro Transparente (CKAN) — "Transferências constitucionais para municípios", arquivos mensais 2023 (transferenciamensalmunicipios2023NN.csv).
Os 12 arquivos mensais (~55 MB) não estão no repositório; os hashes SHA-256 de cada um estão em HASHES_transferencia_mensal_municipios.txt.
Atenção: o campo "Mês" do arquivo está defasado em relação ao nome (arquivo 202304 traz mês 3; arquivo 202312 traz mês 11; mês 12 vem do segundo arquivo 202312). Usamos o campo Mês.
Agregado: catalogo/fpm_fundeb_2023.csv (FPM cota-parte, desconto Fundeb, complementação VAAF/VAAT da União por município; casamento por nome+UF, 2 aliases manuais).

Definição do FPM (D76, conferida contra a MSC): "FPM/FPM" é a cota líquida da dedução do Fundeb; o FPM bruto é FPM/FPM + DEDU/FUNDEB (coluna fpm_bruto_est). O item "FPM/FUNDEB" é outra coisa (não é a dedução) e não deve ser somado à cota. Contra a soma das naturezas 17115* da MSCE em 179 municípios: mediana 1,002; 77% a menos de 2%, 87% a menos de 5%. A cota líquida sozinha fica 22% abaixo.
