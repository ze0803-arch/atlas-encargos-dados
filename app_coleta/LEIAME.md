# Coletor e analisador do Atlas de Encargos

Dois programas em Python que fazem sozinhos a coleta do Siconfi e o cálculo, sem precisar do Claude.

## Instalação (uma vez)

1. Instale o Python 3.9 ou mais novo (python.org). No Windows, marque "Add Python to PATH".
2. Abra o terminal nesta pasta e rode: `pip install -r requirements.txt`

## Coletar

```
python coletar.py                    # todas as UFs, 2023, pasta ./dados (cerca de 4 a 6 horas)
python coletar.py --uf RN PB         # só algumas UFs
python coletar.py --uf RN --limite 3 # teste rápido com 3 municípios
```

- Pode ser interrompido (Ctrl+C) e rodado de novo: retoma de onde parou.
- Cada resposta da API é guardada comprimida em `dados/raw/` com hash SHA-256; tudo fica no `dados/diario_extracao.csv`.
- Ao concluir cada UF, gera `dados/pacotes/UF_completo.tar`.
- Use no máximo 4 requisições simultâneas (padrão), para não sobrecarregar a API do Tesouro.

Depois da coleta, rode uma vez para buscar as 12 matrizes mensais onde a de dezembro não fecha com a DCA:

```
python coletar.py --completar-mscc
```

## Analisar

```
python analisar.py --pasta dados
```

Gera `dados/resultado_2023.csv`: por município, conferência MSC × DCA, sinalizações e margem de decisão (ampla, estrita e % da RCL). Município com problema nos dados fica marcado e não calculado.

## Enviar ao GitHub

O destino dos dados é o repositório privado `ze0803-arch/atlas-encargos-dados`. Para o computador poder enviar:

1. Instale o Git para Windows (git-scm.com, instalação padrão).
2. No terminal: `git clone https://github.com/ze0803-arch/atlas-encargos-dados`. Na primeira vez abre uma janela do navegador para entrar na conta do GitHub.
3. Trabalhe dentro da pasta clonada: `cd atlas-encargos-dados\app_coleta`. Os comandos de coleta e análise são os mesmos; a pasta `dados` fica dentro do clone.
4. Rode a coleta com `python coletar.py --enviar`. A cada UF concluída ele envia os pacotes e o catálogo (nunca os arquivos soltos de `raw/`).
5. No fim, depois de `--completar-mscc` e de `analisar.py`, rode `python coletar.py --empacotar --enviar`. Isso refaz os pacotes com as matrizes mensais, em partes de até 80 MB, e envia junto o catálogo e o `resultado_2023.csv`.

## Regras de cálculo

Estão no registro de decisões: `catalogo/decisoes.md`.
