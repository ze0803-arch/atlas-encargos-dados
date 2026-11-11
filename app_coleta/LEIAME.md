# Coletor e analisador do Atlas de Encargos

Dois programas em Python que fazem sozinhos a coleta do Siconfi e o cálculo, sem precisar do Claude.

## Instalação (uma vez)

1. Instale o Python 3.9 ou mais novo (python.org). No Windows, marque "Add Python to PATH".
2. Abra o terminal nesta pasta e rode: `pip install -r requirements.txt`

## Jeito mais simples: um comando só (`atlas.py`)

```
python atlas.py --pasta dados                 # todas as etapas, 2023
python atlas.py --pasta dados --uf RN         # coleta só algumas UFs
python atlas.py --pasta dados --etapas analisar confianca comparar relatorio   # só estas etapas
python atlas.py --pasta dados --ano 2024
```

Etapas, em ordem: `siconfi`, `mscc`, `verificar`, `siops`, `analisar`, `comparar`, `confianca`, `relatorio`, `empacotar`. Cada uma é retomável; se uma falhar, o programa para e diz qual. No fim grava `dados/relatorio_<ano>.md` (cobertura por UF e porte, motivos dos não calculados, comparação com o SIOPS, maiores diferenças).

Programas que o `atlas.py` chama: `coletar.py` (Siconfi; `--verificar` refaz meses vazios), `coletar_siops.py` (SIOPS, mínimo de saúde), `analisar.py`, `confianca.py` (testes de consistência), `comparar_siops.py`.

## Convênios da União (bloco P)

Baixe `<ano>_Convenios.zip` em portaldatransparencia.gov.br/download-de-dados/convenios/<ano>, descompacte e rode `python convenios.py --pasta dados --csvs pasta_dos_csv --ano 2023`. Gera `dados/convenios_<ano>.csv` com repasse e contrapartida por município.

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

## Onde ficam os dados

- **GitHub** (repositório privado `ze0803-arch/atlas-encargos-dados`): scripts, catálogo (`diario_extracao.csv`, `resultado_2023.csv`) e registro de decisões. É leve.
- **Zenodo**: os pacotes de brutos de `dados/pacotes` (cerca de 2 GB no país), com DOI para citar na tese. Envio pelo navegador, em zenodo.org (Novo envio, arrastar os arquivos .tar).

### Enviar o catálogo ao GitHub

1. Instale o Git para Windows (git-scm.com, instalação padrão).
2. No terminal: `git clone https://github.com/ze0803-arch/atlas-encargos-dados`. Na primeira vez abre o navegador para entrar na conta do GitHub.
3. Trabalhe dentro da pasta clonada: `cd atlas-encargos-dados\app_coleta`. A pasta `dados` fica dentro do clone (os arquivos pesados de `dados/` são ignorados pelo Git).
4. Rode a coleta com `python coletar.py --enviar`. A cada UF concluída ele envia só o catálogo.
5. No fim, depois de `--completar-mscc` e de `analisar.py`, rode `python coletar.py --empacotar --enviar`. Refaz os pacotes com as matrizes mensais (em partes de até 80 MB) e envia o catálogo e o `resultado_2023.csv`. Os pacotes ficam em `dados/pacotes` para você subir ao Zenodo.

## Regras de cálculo

Estão no registro de decisões: `catalogo/decisoes.md`.
