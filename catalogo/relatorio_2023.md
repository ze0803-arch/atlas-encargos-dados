# Atlas de Encargos 2023: relatório da execução

- Municípios: **5569** · calculados: **4038** (73%) · alta confiança: **3451** (85% dos calculados)
- Margem ampla mediana: **40.3%** da RCL

## Cobertura por UF

| UF | Municípios | Calculados | % | Alta confiança | Margem mediana (% RCL) |
|---|---|---|---|---|---|
| AC | 22 | 1 | 5% | 1 | 49.7% |
| AL | 102 | 35 | 34% | 30 | 24.9% |
| AM | 62 | 51 | 82% | 37 | 26.0% |
| AP | 16 | 7 | 44% | 3 | 23.2% |
| BA | 417 | 225 | 54% | 195 | 29.9% |
| CE | 184 | 165 | 90% | 155 | 22.1% |
| DF | 1 | 0 | 0% | 0 | — |
| ES | 78 | 69 | 88% | 66 | 37.7% |
| GO | 246 | 141 | 57% | 118 | 47.0% |
| MA | 217 | 172 | 79% | 137 | 23.8% |
| MG | 853 | 670 | 79% | 625 | 42.3% |
| MS | 79 | 50 | 63% | 46 | 40.8% |
| MT | 142 | 70 | 49% | 64 | 44.8% |
| PA | 144 | 129 | 90% | 96 | 19.2% |
| PB | 223 | 41 | 18% | 39 | 33.1% |
| PE | 184 | 141 | 77% | 105 | 34.0% |
| PI | 224 | 212 | 95% | 185 | 29.0% |
| PR | 399 | 272 | 68% | 181 | 45.8% |
| RJ | 92 | 57 | 62% | 41 | 28.9% |
| RN | 167 | 153 | 92% | 133 | 35.5% |
| RO | 52 | 35 | 67% | 33 | 40.0% |
| RR | 15 | 13 | 87% | 11 | 26.6% |
| RS | 497 | 407 | 82% | 372 | 46.5% |
| SC | 295 | 264 | 89% | 245 | 46.6% |
| SE | 75 | 46 | 61% | 41 | 30.4% |
| SP | 645 | 523 | 81% | 421 | 50.8% |
| TO | 138 | 89 | 64% | 71 | 37.9% |

## Por porte

| Faixa | Municípios | Calculados | % | Margem mediana (% RCL) |
|---|---|---|---|---|
| até 5 mil | 1283 | 948 | 74% | 48.2% |
| 5 a 10 mil | 1184 | 856 | 72% | 41.6% |
| 10 a 20 mil | 1350 | 962 | 71% | 36.6% |
| 20 a 50 mil | 1070 | 783 | 73% | 34.5% |
| 50 mil ou mais | 682 | 489 | 72% | 35.8% |

## Motivos dos não calculados

LIQ_DIVERGE (1043) · REC_DIVERGE (907) · FONTE_LIVRE_ATIPICA (240) · RCL_SUSPEITA (177) · SEM_NATUREZA_RECEITA (154) · RREO3_VAZIO (106) · LEGISLATIVO_ATIPICO (21) · SEM_MSCE (3)

## Mínimo de saúde × SIOPS (|diferença| %)

| Grupo | n | Mediana | p90 | ≤1% | ≤10% |
|---|---|---|---|---|---|
| Calculados | 4034 | 0.08 | 2.9 | 78% | 97% |
| Todos | 5456 | 0.17 | 8.7 | 70% | 91% |

Maiores diferenças (a investigar): Varginha/MG +1408%; Lagoa da Canoa/AL +216%; Atibaia/SP -200%; Cordeirópolis/SP -200%; Major Gercino/SC -200%; Porto do Mangue/RN -198%; Baía da Traição/PB -189%; Casserengue/PB -173%; Borborema/PB -171%; Jiquiriçá/BA +166%

## Bloco P (pactuação), medido à parte da margem

| Item | Calculados com dado | Mediana (% da receita livre) | p90 |
|---|---|---|---|
| Consórcios (modalidade 71) | 2582 | 0.12% | 1.48% |
| Contrapartida de convênios da União | 2802 | 0.03% | 0.72% |
| SUS atenção primária (recebido) | 4022 | 3.37% | 7.42% |
| SUS média e alta complexidade (recebido) | 3430 | 0.88% | 5.98% |
| SUS agentes de saúde (recebido) | 3991 | 1.88% | 4.53% |

## Próximos passos

1. Subir os pacotes de `dados/pacotes` ao Zenodo (navegador).
2. Enviar ao GitHub o catálogo: `diario_extracao.csv`, `diario_siops.csv`, `resultado_2023.csv`, `confianca_2023.json`, `siops_2023.csv`, `comparacao_siops_2023.csv`, `convenios_2023.csv`, `transferencias_2023.csv`.
3. Levar este relatório ao Claude para investigar as exceções.