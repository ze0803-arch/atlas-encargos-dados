# Scripts de análise (piloto 2023)

Scripts usados nas conferências e medições do piloto. **Não fazem parte do aplicativo** (`app_coleta/`): rodam a partir da pasta de trabalho do piloto (`raw/siconfi/2023/`, `resultado_2023.csv`) e alguns têm caminhos fixos. Servem para reprodução e auditoria; cada decisão que usa um deles está em `catalogo/decisoes.md`.

| Script | O que faz | Decisão |
|---|---|---|
| `fpm_test.py`, `fpm_all.py` | Testa a hipótese FPM/Fundeb contra o SIOPS (natureza 17115111) | D42 |
| `siops_lom.py` | Identifica municípios que declaram % de saúde da Lei Orgânica | D41 |
| `med_enc.py`, `med_fundeb.py` | Medição de encargos (patronal, PASEP, assistência social) e Fundeb 70% | D35, D36 |
| `med_p.py` | Medição do bloco P (SUS, FNDE, convênios, FNAS) como teto | D38 |
| `conv_p.py` | Contrapartida de convênios da União (Portal da Transparência) | D39 |
| `teste_trib.py` | Teste de base tributária (natureza 17125101 = CFEM) | D30 |
| `siai_dados.py`, `siai_parse.py` | Dados e leitura dos anexos do SIAI/TCE-RN (RREO) | D27, D28 |
| `siai_nivel3_parse.sh` | Lê os Anexos 02 e 09 das contas de governo (SIAI) em PDF com `pdftotext` | D44 |

Os PDFs do SIAI têm camada de texto: `curl` direto em `siaiconsultas.tce.rn.gov.br/downloadanexoportalgestor/ContasDeGoverno/<PM...>/<ano>/<anexo>/<id>/<arquivo>.pdf` (Anexo 02 = categoria econômica consolidada; Anexo 09 = despesa por órgão e funções).
