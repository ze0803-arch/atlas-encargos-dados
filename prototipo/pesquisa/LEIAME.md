# Versão de pesquisa do aplicativo

Anexo de dados e de conferência da tese. Público: orientador e banca. Não é produto para gestores.

- `app.html`: modelo da página (telas Início, Regras registradas, Como ler as margens, Mapa, H1 a H4, Cobertura e quem falta, Município, Coleta, Dados e fontes).
- `dados.json`: números agregados de 2023 que alimentam as telas (inclui `t6` e `h4itbi`).
- `municipios.json`: uma linha por município calculado (colunas em `IX` dentro de `app.html`).
- `mapa.json`: malha simplificada para o mapa.
- `build_pesquisa.py`: gera `atlas_pesquisa.html` a partir de `app.html` e `dados.json`.
- `calc_dados.py`: calcula `dados.json` e `municipios.json` a partir de `resultado_2023.csv` e do catálogo (caminhos de entrada ajustáveis no topo).
- `calc_h4itbi.py`: ITBI e IPTU por habitante por quintil (D72).

Para abrir: `python build_pesquisa.py` e depois `python -m http.server` nesta pasta, com `atlas_pesquisa.html` no navegador (ele busca `municipios.json` e `mapa.json`).

Estado: 2023 exploratório, base anterior à recoleta dos 710 municípios. Refazer `calc_dados.py` e `calc_h4itbi.py` depois de `rodar_tudo.bat`.
