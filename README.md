# Atlas de Encargos: dados e scripts

Dados brutos e scripts da tese "Norma uniforme, autonomia desigual: encargos federativos, espaço de decisão orçamentária e o dever de correspondência entre encargo e fonte nos municípios brasileiros" (exercício 2023).

## Conteúdo

- `scripts/`: coleta (`coleta.py` piloto, `coleta_rn.py` RN, `coleta_br.py` nacional, `siope_resume.py`) e análise (`analise.py`).
- `catalogo/`: `diario_extracao.csv` (cada requisição, com hash SHA-256 e arquivo), `resultado_2023.csv` (cálculo por município), `amostra_piloto.csv` e `decisoes.md` (registro de decisões D1 a D16).
- `brutos/siconfi/2023/`: respostas originais da API do Siconfi, comprimidas (.json.gz), empacotadas em .tar por UF (piloto) ou em partes (RN).
- `brutos/siope/2023/`: respostas do SIOPE (Indicadores e Receita). Despesas e Remuneração incompletas e não incluídas.
- `brutos/ibge/2023/`: população (Censo 2022) e PIB municipal (SIDRA).

## Regras de cálculo

Ver `catalogo/decisoes.md`. Os arquivos brutos nunca são alterados; os hashes do diário permitem verificar a integridade.
