# Atlas de Encargos: guia para quem vai continuar o desenvolvimento

Documento de passagem do projeto. Explica para que o sistema serve, como foi construído, onde está cada coisa, como rodar do zero e quais arquivos precisam ser entregues. Última atualização: 15/11/2026.

---

## 1. Para que serve (em um parágrafo)

O Atlas de Encargos é a parte de dados de uma tese de doutorado em Direito (UniCuritiba, autor: Thiago Garcia). A tese pergunta: **quando a União fixa obrigações iguais para todos os municípios e os municípios têm capacidade econômica desigual, quanto espaço real de escolha resta a cada um?** O sistema mede isso para os 5.570 municípios, de 2023 a 2027, com dados públicos. A medida central é a **margem de decisão**: a parte da receita livre que sobra depois das obrigações fixadas em norma nacional. Quem lê os resultados são o autor, o orientador (ainda a definir) e, depois, a banca. Por isso tudo precisa ser **conferível e repetível**: nenhum dado é corrigido à mão, cada requisição às fontes fica registrada com hash, e o que não fecha é marcado e não calculado.

Estado atual: o ano de **2023 está completo** (coleta nacional, cálculo, testes, protótipo). 2024 a 2027 ainda não foram coletados.

### Glossário mínimo

| Termo | Significado |
|---|---|
| MSC | Matriz de Saldos Contábeis, enviada pelos municípios ao Siconfi (Tesouro Nacional). É a fonte da execução linha a linha por fonte de recurso. |
| DCA | Declaração de Contas Anuais, também no Siconfi. Usada para **conferir** a MSC (receita e despesa liquidada). |
| RREO / RGF | Relatórios fiscais bimestrais e quadrimestrais (LRF). Dão a RCL e a despesa com pessoal. |
| RCL | Receita corrente líquida. Denominador dos percentuais. |
| Receita livre | Receita em fonte de recursos 1500 e 1501 (sem destino fixado). |
| Margem ampla | Receita livre − mínimos de educação e saúde − Legislativo − dívida − precatórios − contribuição patronal (decisão D68, 18/11/2026: o código agora desconta). |
| Margem estrita | Margem ampla − folha de pagamento paga com recurso livre. |
| Bloco I a IV | I = obrigação de origem nacional; II = estrutura e compromissos passados; III = margem; IV = pactuado (convênios, consórcios). |
| Quintil Q1 a Q5 | Cinco grupos de municípios pelo PIB por habitante (IBGE). Q1 = menor, Q5 = maior. |

---

## 2. Visão geral da arquitetura

```
FONTES PÚBLICAS                     CÓDIGO                         SAÍDAS
─────────────────                   ──────                         ──────
Siconfi (API do Tesouro) ─┐
SIOPS (Min. Saúde)        │   app_coleta/coletar*.py  ──►  dados/raw/*.json.gz + diario_extracao.csv
SIOPE (FNDE)              ├──►  (coleta, retomável)         (brutos, com SHA-256 por requisição)
IBGE (Censo 2022, PIB)    │
Portal da Transparência  ─┘
                                     │
                                     ▼
                         app_coleta/analisar.py  ──────►  resultado_2023.csv  (1 linha por município)
                         app_coleta/confianca.py ──────►  confianca_2023.json (testes de consistência)
                         app_coleta/comparar_siops.py ─►  comparacao_siops_2023.csv
                                     │
                                     ▼
                         analises/*.py  ───────────────►  catalogo/*.md e *.csv  (testes da tese)
                                     │
                                     ▼
                         prototipo/build_*.py  ────────►  prototipo/atlas_prototipo.html  (aplicativo)
```

Quatro peças, de trás para frente:

1. **`app_coleta/`**: o coletor e o calculador. Roda no computador do usuário, sem depender do Claude. É o coração do sistema.
2. **`analises/`**: scripts de pesquisa (testes das hipóteses H1 a H5, robustez, viés de cobertura, validações). Não fazem parte do aplicativo; servem à tese e à auditoria.
3. **`catalogo/`**: tudo que é **resultado e registro**: `resultado_2023.csv`, relatórios `.md`, `decisoes.md` (registro de 67 decisões, D1 a D67), diários de extração.
4. **`prototipo/`**: o aplicativo web de consulta, um único arquivo HTML.

Além do repositório existem **documentos de texto da tese** (seção metodológica, protocolo, roteiro, registro de decisões em versão Docs) e o **projeto de tese em PDF (66 páginas)**; ver seção 8.

---

## 3. Fontes de dados

| Fonte | O que traz | Onde no código |
|---|---|---|
| **Siconfi** (API `apidatalake.tesouro.gov.br/ords/siconfi/tt/`) | MSC (de dezembro e as 12 mensais), RREO (Anexos 01 e 03), RGF (Anexo 01), DCA (I-C, I-D, I-E), extrato de entregas | `app_coleta/coletar.py` |
| **SIOPS** (siops.datasus.gov.br) | Mínimo de saúde aplicado por município (conferência) | `app_coleta/coletar_siops.py`, `comparar_siops.py` |
| **SIOPE** (FNDE) | Indicadores e receita da educação | `scripts/siope_resume.py` |
| **IBGE** | População (Censo 2022) e PIB municipal (SIDRA, tabela 5938, variável 37) | `brutos/ibge/`, `catalogo/pib_2023.csv`, `analises/base_independente_2023.py` |
| **Portal da Transparência** | Transferências da União por programa e convênios (bloco P) | `app_coleta/transferencias.py`, `convenios.py` |
| **SIAI/TCE-RN** | Só para **validar** uma amostra do RN (conferência externa, nível 3) | `analises/siai_*.py`, `catalogo/auditoria_nivel3_2023.csv` |

Regras de coleta que valem para todo o código:

- Cada resposta da API é guardada **comprimida e sem alteração** (`.json.gz`), com SHA-256 e registro no `diario_extracao.csv` (data, URL, status, linhas, hash, arquivo).
- A coleta é **retomável**: roda de novo e continua de onde parou.
- No máximo **4 requisições simultâneas**, para não sobrecarregar a API do Tesouro.
- A coleta nacional completa leva cerca de **4 a 6 horas** e gera cerca de **2 GB** de brutos (por causa das 12 matrizes mensais da MSC).

---

## 4. Como a margem é calculada (`app_coleta/analisar.py`)

O código é a referência; o registro `catalogo/decisoes.md` explica o porquê de cada regra. Em resumo, por município:

1. **Escolha da MSC** (D19): usa a MSC de dezembro; se não fechar com a DCA (receita e despesa liquidada, **tolerância de 1%**), testa a soma das 12 matrizes mensais. Testa também as duas convenções de sinal (débito−crédito e crédito−débito).
2. **Receita livre**: receita da MSC em fonte 1500 e 1501 (bruta do Fundeb; o Fundeb entra como coluna informativa).
3. **Mínimos constitucionais** (D29): 25% da base de impostos (educação) e 15% da base **sem** as parcelas d e e do FPM (saúde). Desconta só o **mínimo exigido**, não o gasto efetivo (D25).
4. **Legislativo, dívida, precatórios**: despesa liquidada em fonte livre, classificada por poder/órgão, grupo de despesa e elemento 91.
5. **Contribuição patronal**: obrigação de origem nacional (bloco I).
6. **Consórcios e convênios**: pactuação (bloco IV), fora da margem (D37, corrigido em D43: modalidade de aplicação 71).
7. **Margem ampla** = receita livre − (mínimos + patronal) − (Câmara + dívida + precatórios). **Margem estrita** = ampla − folha paga com fonte livre.
8. **Percentuais**: sobre a RCL (denominador do RREO) e, nas análises da tese, sobre a receita total e por habitante.
9. **Não calcula (marca e explica)** quando: MSC ausente, incompleta ou divergente da DCA acima da tolerância; fonte livre codificada de forma atípica; RCL suspeita; receita por habitante acima de **R$ 40.000** (receita incompatível com a população, D50). **Nenhum dado é imputado ou corrigido.**
10. **Universo**: 5.568 municípios (sem DF e sem Fernando de Noronha, D49).

Níveis de confiança (D31): nível 1 = MSC fecha com a DCA; nível 2 = testes de consistência (`confianca.py`, testes T1 a T9); nível 3 = conferência externa por amostra (SIAI/TCE-RN e SIOPS). Resultado de 2023: **4.037 de 5.568 municípios calculados (72,5%)**.

**Dicionário de classificação**: o mapeamento fonte de recurso → bloco está em `analisar.py` (constante `LIVRE` e as regras acima) e descrito em `decisoes.md`. Mexer nele muda todos os resultados; toda mudança precisa de uma nova entrada em `decisoes.md`.

Colunas de `resultado_2023.csv` (uma linha por município): identificação (`cod_ibge, ente, uf, pop`), insumos (`rec_msc, dca_rec, liq_msc, dca_liq, rcl_rreo, rcl_ajustada, pessoal_rgf, base_impostos, fpm_parcela_de, minimos_exigidos, rec_livre, leg, divida, prec, folha_livre, consorcios`), conferências (`rec_dif, liq_dif, rcl_suspeita, flags`), resultado (`margem_ampla, margem_estrita, margem_ampla_pct_rcl, status`).

---

## 5. O aplicativo (`prototipo/atlas_prototipo.html`)

**O que é**: um único arquivo HTML (~2 MB), sem servidor e sem instalação. Abre direto no navegador. Todos os dados estão embutidos no próprio arquivo como constantes JavaScript. Também está publicado como página privada na plataforma do Claude (artefato).

**Telas** (menu superior): Início · 1 Coletar · 2 Conferir · 3 Classificar · 4 Resultados (Piloto, Hipóteses, Comparativo, Base própria, Validação) · 5 Município (ficha linha a linha) · Gráficos (comparar estados e municípios) · Metodologia.

**Dados embutidos** (constantes no HTML): `PILOTO` (um objeto por município: código, nome, UF, população, status, alertas, margem ampla `m`/`mp`, estrita `me`), `FICHA` (cálculo linha a linha por município), `COMP` (tabela por UF), `RD` (tabelas do Apêndice D e faixa de PIB por município), `TESE` (quintis por base própria), `DIARIO` e `VALID`.

**Como é montado**: os dados e as telas **não** estão em arquivos separados. Cada script `build_*.py` lê os CSV/MD de `catalogo/` e **insere ou substitui trechos no HTML** (por marcadores como `/*READ-START*/ … /*READ-END*/` ou por busca de texto). Ordem obrigatória, sempre da raiz do repositório:

```
python prototipo/build_prototipo_nacional.py catalogo     # PILOTO e VALID (resultado nacional)
python prototipo/build_tese_2023.py                       # TESE, tela Base própria, Gráficos originais
python prototipo/build_real_2023.py                       # Início, Coletar, Conferir, Ficha
python prototipo/build_comparativo_2023.py                # COMP e tela Comparativo (PIB, quintis)
python prototipo/build_readequacao_2023.py                # Hipóteses H1-H5, Comparativo = Apêndice D
python prototipo/build_graficos_comparar.py               # Gráficos: comparar estados e municípios
python prototipo/build_estrita.py                         # margem estrita ao lado da ampla
python prototipo/build_site_novo.py /caminho/br.json      # mapa, correspondência, busca (malha IBGE; ver cabeçalho do script)
```

Os scripts são idempotentes (rodar de novo não duplica). Depois de cada build o arquivo foi testado com Playwright (abrir cada tela e checar erros de console).

**Cuidado, ponto frágil.** Esse esquema de "remendar o HTML por texto" foi o jeito rápido de iterar com o Claude, mas é frágil: uma mudança no texto âncora quebra o build seguinte. **Recomendação para o programador:** tratar o HTML atual como protótipo e especificação visual, e refazer o front-end como projeto normal (por exemplo, dados em JSON/CSV separados + componentes), mantendo as mesmas telas e os mesmos números. O que **deve** ser preservado: os textos em linguagem simples, os avisos de cobertura e as regras de leitura (abaixo).

**Regras de leitura que o aplicativo aplica** (não são detalhe de interface; são decisões da pesquisa):

- UF fora das comparações se tiver menos de 40 municípios calculados ou cobertura abaixo de 40% (hoje: AC, AL, AP, PB, RO, RR). Aparecem em cinza com asterisco.
- 2023 é **exploratório**: os resultados não confirmam nem derrubam hipóteses.
- Município não calculado aparece com o motivo; nunca com número estimado.
- Margem ampla é a medida principal; estrita é a medida de robustez. As duas aparecem juntas.

---

## 6. Análises da tese (`analises/`)

Scripts de pesquisa. Alguns têm **caminhos fixos** da pasta de trabalho original e precisam de ajuste para rodar em outra máquina (ver `analises/LEIAME.md`). Os principais:

| Script | Produz |
|---|---|
| `testes_tese_2023.py` | `catalogo/testes_tese_2023.md`: testes da pergunta central |
| `base_independente_2023.py` | PIB por habitante (IBGE), quintis, relação com a margem |
| `comparativo_2023.py` | Comparação entre UFs e dentro da UF, modelo em dois níveis |
| `tabelas_projeto_2023.py` | `tabelas_projeto_2023.json`: tabelas 3 a 7 do Apêndice D do projeto |
| `testes_juridicos_2023.py` | Cobertura federal vinculada (art. 167, § 7º) e critério do art. 11 da LRF |
| `choque_pisos_2023.py` | Efeito do reajuste de 14,95% do piso do magistério |
| `robustez_2023.py`, `vies_cobertura_2023.py` | Robustez e viés da cobertura |
| `fpm_*.py`, `med_*.py`, `siops_lom.py` | Testes específicos de FPM/Fundeb, encargos e bloco P |

Bibliotecas usadas: `pandas`, `numpy`, `scipy`, `statsmodels`, `requests`.

---

## 7. Como rodar do zero

```bash
# 1) Ambiente (Python 3.9+)
pip install requests pandas numpy scipy statsmodels

# 2) Coleta nacional de 2023 (4-6 h, retomável; usa a pasta ./dados)
cd app_coleta
python atlas.py --pasta dados                       # todas as etapas
python atlas.py --pasta dados --uf RN               # só uma UF (teste)
python atlas.py --pasta dados --etapas analisar confianca comparar relatorio

# 3) Só recalcular, com brutos já coletados
python analisar.py --pasta dados      # gera dados/resultado_2023.csv
python confianca.py --pasta dados     # testes de consistência
```

`atlas.py` encadeia as etapas `siconfi, mscc, verificar, siops, transferencias, convenios, analisar, comparar, confianca, relatorio, empacotar`. Detalhes em `app_coleta/LEIAME.md`.

Para o ano seguinte basta `--ano 2024`, mas **atenção**: a classificação de fontes de recursos só é padronizada a partir de 2023; 2022 só serve como robustez, com cautela.

---

## 8. Estado do projeto e pendências

**Concluído (2023):** coleta nacional; cálculo (4.037 calculados); testes de consistência; validação externa em amostra (SIAI/SIOPS); PIB por habitante e quintis; análise entre estados e dentro da UF; testes jurídicos; protótipo com todas as telas; registro de decisões D1 a D67.

**Em aberto (técnico):**
1. Média do PIB por habitante 2021 a 2023 (o projeto prevê; o aplicativo usa só 2023).
2. Robustez: margem em R$/habitante, com e sem Fundeb, estrita por quintil de PIB, renda do Censo 2022.
3. Coleta de 2024 a 2027 e seletor de ano no aplicativo (hoje só 2023).
4. Tela **Classificar**: ainda é demonstração (dicionário somente de leitura).
5. Classificar as ações de transferência da União (obrigação legal / adesão / automática constitucional) em `catalogo/acoes_para_classificar_2023.*`.
6. Corrigir 20 nomes de municípios truncados e o texto do teste A3 em `testes_juridicos_2023.py`.
7. Municípios não calculados por problema de dados no Siconfi (exemplo: Guaratuba/PR, em que a despesa liquidada da MSC difere da DCA em mais de 800%): investigar se é falha de coleta ou do município.
8. Mover para o repositório os scripts de análise que ainda estão só no computador do usuário.

**Em aberto (jurídico/pesquisa, não é trabalho do programador, mas afeta o código):** texto oficial do art. 11 da LRF, Lei 11.738/2008, Lei 14.113/2020, lei do crédito do piso da enfermagem, portaria do Ministério da Saúde, Tema 1181 do STF, normas da ANEEL; **limiares numéricos das hipóteses** (a fixar com o orientador **antes** de abrir 2024).

**Decisão importante para não desfazer:** a RAIS (folha de pagamento) foi **retirada** do método e do sistema (D52). Não reintroduzir.

---

## 9. O que enviar ao programador e como

### A. Do repositório (já está no GitHub; tudo é leve, ~118 MB)

Repositório **privado**: `github.com/ze0803-arch/atlas-encargos-dados` (conta ze0803-arch).

**Como entregar (escolha um):**
1. **Convite no GitHub (melhor):** no repositório, *Settings → Collaborators → Add people*, digitar o usuário do GitHub do programador, permissão **Read** (ou Write, se for alterar). Ele recebe um e-mail e clona o repositório com todo o histórico.
2. **ZIP:** *Code → Download ZIP* (sem histórico), ou o arquivo `atlas-encargos-dados.zip` preparado junto com este guia.

Conteúdo: `app_coleta/` (coletor e calculador), `analises/`, `scripts/` (coleta do piloto), `catalogo/` (resultados e `decisoes.md`), `prototipo/` (aplicativo e scripts de montagem), `tese/`, `brutos/` (parte dos brutos: UFs do piloto, RN, IBGE e SIOPE).

### B. Do computador do usuário (o que **não** está no repositório)

| O que | Onde procurar | Observação |
|---|---|---|
| **Pasta `dados` da coleta nacional**: subpastas `raw/` (respostas originais `.json.gz`) e `pacotes/` (`UF_completo.tar`) e o arquivo `entes.json` | Pasta onde foi rodado `atlas.py` (`app_coleta/dados`) | ~2 GB. É o que permite recalcular tudo. **Enviar compactada**, por link de nuvem (Google Drive, OneDrive) ou, se for definitivo, pelo Zenodo. Sem `entes.json` o `analisar.py` não roda. |
| `diario_extracao.csv`, `diario_siops.csv` completos | `dados/` | Registro de cada requisição, com hash. Já há cópia em `catalogo/`; mandar a versão mais recente. |
| **Zips de transferências** (`2023MM_Transferencias.zip`) e `<ano>_Convenios.zip` | `dados/transferencias/` e pasta de download | Só se o programador for refazer o bloco P. |
| `Dados_Necessarios_Pesquisa.md` (versão mais recente) | Pasta "THIAGO GARCIA" na Área de Trabalho (OneDrive) | Lista dos dados da pesquisa, base do aplicativo. |
| **Projeto de tese em PDF (66 páginas)** | Anexo desta conversa | É a especificação do que o sistema deve mostrar (hipóteses, Quadro 7, Apêndice D). **Confidencial:** o projeto ainda será apresentado ao orientador. |
| Scripts de análise que ficaram só no PC | Pasta de trabalho do piloto | Se existirem arquivos `.py` fora do repositório, mandar também. |

### C. Documentos de texto (fora do repositório)

| Documento | Onde está | Para quê |
|---|---|---|
| Seção metodológica | Claude Docs (`PQB3e31bSQ4HjWTXWF4iKU`) | Método explicado em linguagem simples |
| Registro de decisões D13 a D63 | Claude Docs (`XFuWbdG9yTPhk7mSgoQZuz`) | Cópia em texto do registro; a versão completa e mais nova é `catalogo/decisoes.md` |
| Protocolo e Roteiro | Claude Docs | Passo a passo da pesquisa |
| Aplicativo publicado | Artefato `claude.ai/artifact/87zdg4b6PTAf2CyZwAuhfY` | **Privado**: para o programador ver, compartilhar pelo menu *Share* da página, ou enviar o arquivo `prototipo/atlas_prototipo.html` (basta abrir no navegador) |

### D. O que **não** enviar

- Senhas, tokens ou chaves de acesso (o repositório não contém nenhum; conferido).
- Dados pessoais de servidores (a pesquisa não coleta folha de pagamento).
- Qualquer arquivo da pasta do usuário que não seja da tese.

### E. Ordem sugerida para o primeiro contato

1. Enviar este guia + convite ao repositório + o PDF do projeto.
2. Pedir que ele abra `prototipo/atlas_prototipo.html` e navegue por todas as telas (15 minutos): é o resumo visual de tudo.
3. Enviar a pasta `dados` (2 GB) só quando ele confirmar que vai rodar a coleta/cálculo.
4. Primeira tarefa de verificação: rodar `python analisar.py --pasta dados` e conferir que o `resultado_2023.csv` gerado é **idêntico** ao de `catalogo/` (4.037 calculados). Se for, o ambiente dele está reproduzindo a pesquisa.

---

## 10. Sugestões para a próxima fase (a combinar com o programador)

1. **Reproduzir** o cálculo de 2023 em ambiente novo e documentar a instalação.
2. **Refazer o front-end** com dados separados do código (seção 5), mantendo telas e números.
3. **Coletar 2024** em um ou dois estados pequenos como teste, depois o país e, em seguida, 2025 a 2027.
4. **Automatizar o relatório de cobertura** por ano e por UF.
5. **Testes automáticos**: conferir `resultado_2023.csv` contra valores de referência (por exemplo, Caicó/RN, com margem ampla de 35,2% da RCL) e contra o SIOPS/SIAI.
6. **Publicação**: dados brutos e catálogo no Zenodo (DOI para citar na tese); aplicativo em endereço público somente depois da validação com o orientador.

---

*Qualquer decisão de método nova deve entrar em `catalogo/decisoes.md` com número, data e motivo. É o registro que a tese cita.*


## Atualização de 18/11/2026 (D68)
- A patronal passa a ser descontada na margem ampla (analisar.py). Os números do app ainda são anteriores; reprocesse com `python analisar.py --pasta dados` e rode a cadeia.
- Correções vindas da auditoria: paginação truncada (flag PAGINACAO_INCOMPLETA), arquivos duplicados (versão mais recente), coletar.py não grava município com página falha.
- Telas novas: Mapa, Correspondência, busca por nome (build_site_novo.py). Veja catalogo/decisoes.md, D68.
- Atenção: o repositório no GitHub está público. Considere torná-lo privado (Settings → Change visibility) e remover o e-mail pessoal de catalogo/decisoes.md (D16).
