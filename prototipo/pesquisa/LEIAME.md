# Versão de pesquisa do aplicativo

Anexo de dados e de conferência da tese. Público: orientador e banca. Não é produto para gestores.

- `app.html`: modelo da página (telas Início, Regras registradas, Como ler as margens, Mapa, H1 a H4, Cobertura e quem falta, Município, Coleta, Dados e fontes).
- `dados.json`: números agregados de 2023 que alimentam as telas (inclui `t6` e `h4itbi`).
- `municipios.json`: uma linha por município calculado (colunas em `IX` dentro de `app.html`).
- `mapa.json`: malha simplificada para o mapa.
- `build_pesquisa.py`: gera `atlas_pesquisa.html` a partir de `app.html` e `dados.json`.
- `calc_pesquisa.py`: gera `dados.json` e `municipios.json` a partir de `resultado_2023.csv` e do catálogo. Uso: `python calc_pesquisa.py ..\..\app_coleta\dados\resultado_2023.csv ..\..\catalogo`, depois `python build_pesquisa.py`.

Para abrir: dê dois cliques em `abrir_pesquisa.bat` (monta a página e abre no navegador).

Estado: 2023 exploratório, resultado após a recoleta dos 710 municípios (4.121 calculados); a tabela de projeto, a base jurídica e o teste de viés de cobertura dependem de `rodar_tudo.bat` completo. Depois de `rodar_tudo.bat`, rodar `calc_pesquisa.py` e `build_pesquisa.py`.
