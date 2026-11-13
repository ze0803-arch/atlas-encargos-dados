# Gerar o pacote do Tocantins (2023)

O catálogo já tem os 138 municípios do TO (89 calculados), mas a pasta `dados/pacotes` do seu PC não tem `TO_completo_p01.tar`. Os brutos do TO provavelmente estão em `dados/raw/siconfi/2023`. Passos, no terminal dentro de `app_coleta`:

1. Conferir se os brutos existem: `dir dados\raw\siconfi\2023\msce\*_17*` (deve listar arquivos com código começando em 17).
2. Gerar o pacote: `python coletar.py --pasta dados --ano 2023 --uf TO --empacotar`
3. Se disser que o TO não está concluído, completar e tentar de novo:
   `python coletar.py --pasta dados --ano 2023 --uf TO --verificar` e depois o passo 2.
4. Se não houver brutos do TO (lista do passo 1 vazia), coletar do zero (cerca de 15 a 25 min): `python coletar.py --pasta dados --ano 2023 --uf TO --enviar` e depois o passo 2.
5. Conferir: deve existir `dados\pacotes\TO_completo_p01.tar`. Avise-me e eu copio.
