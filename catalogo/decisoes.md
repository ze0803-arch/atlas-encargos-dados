# Registro de decisões (autonomia delegada em 10/11/2026 19:19)
D1. Receita MSCE = conta 621200000, apenas natureza_receita iniciada em 1 ou 2 (exclui intra-orçamentárias 7/8 e linhas sem natureza); escolhida entre variantes A (só débitos) e B (débito−crédito) a que mais se aproxima da DCA — variante registrada por município.
D2. Despesa liquidada MSCE = líquido (débito−crédito) de 622130400 + 622130700.
D3. Conferência RCL RREO×RGF removida (RGF traz só RCL ajustada).
D4. Brutos do Siconfi no Drive em tar por UF (<3 MB, limite do conector). Opção 3 (Zenodo/OSF/GitHub) fica para a coleta completa.
D5. Município com SEM_MSCE, MSCE_INCOMPLETA (≤30 linhas) ou divergência >1% vs DCA: marcado e não calculado.
D6. Mínimos (educação/saúde): mantida aproximação = despesa liquidada em fonte livre (1500/1501) nas funções 10 e 12. Teto pelo mínimo legal (25%/15%) ADIADO: exige base de impostos (RREO Anexos 8/12, ausentes na API). Achado: algumas entes (ex.: Sorocaba) executam MDE/ASPS em fontes vinculadas (1550/1600/1659), então "mínimos" nas fontes livres fica subestimado; margem desses entes é limite superior.
D7. Fontes livres confirmadas empiricamente: FPM/impostos aparecem em 1500 (Extremoz) ou 1501 (Sorocaba); 1540-1544=Fundeb, 1600/1659=SUS, 1550=educação vinculada. Livre = 1500 e 1501.
D8. Divergências MSCE×DCA (16): ocorrem por (a) MSCE de dez só com movimento do mês (Barra do Garças: receita 20,8 mi vs DCA 385 mi; meses 1–11 vazios na API) ou (b) enviada incompleta. Teste com id_tv=ending_balance: fecha receita e despesa só em João Pessoa; recupera só a receita em Acari, Florânia, Taquari, Apiacás, Duque de Caxias. Decisão: NÃO usar ending_balance como regra geral; manter "marcar e não calcular". Fallback ending_balance só se receita e despesa baterem ≤1% (a implementar na coleta completa).
D9. Coleta completa começa pelo RN (167 municípios), pulando os 9 já coletados no piloto.
D10. Despesa liquidada MSCE = líquido (D−C) de 622130300 (liquidada a pagar) + 622130400 (paga) + 622130700. Testado em 190 municípios: fecha com a DCA (≤1%) em 173 (91%); a regra anterior (400+700) fechava 153; 300+400 só 81. Os 17 restantes ficam marcados (diferenças de −1,5% a −6% em RN: provável inscrição de RP processados que o ente não lançou na MSC).
D11. Mínimos de educação e saúde na margem ampla: passam a ser o mínimo LEGAL aproximado = 40% (25% educação + 15% saúde) da base de impostos e transferências constitucionais calculada na MSCE (naturezas 111*, 1711*, 1721*). Substitui a regra por função/fonte (que subestimava onde MDE/ASPS são executados em fontes vinculadas). Validação parcial com SIOPE (indicador 24, % aplicado em MDE): mediana de 28,6% no RN e 161 dos 166 municípios do RN com ≥25%. Pendente: saúde (SIOPS) e patronal. A regra por função fica na coluna minimos_funcao, só para comparação.
D12. Resultado do piloto: margem ampla (% RCL) mediana 35% (percentis 10/90: 25% e 48%) nos 167 calculados com RCL; nenhuma negativa. Valores ainda preliminares.
D13. SIOPE completo (Indicadores, Receita, Despesas, Remuneração) é grande (>34 MB só até aqui). Fica no ambiente de trabalho e vai para repositório (opção 3), não para o Drive via conector.
D14. Coleta SIOPE: Indicadores (17 UFs, 4.883 municípios) e Receita (17 UFs) completas. Despesas_Siope e Remuneracao_Siope interrompidas: cada página de 50 mil linhas leva 2–4 min, o volume é de horas e nenhuma é necessária para a margem. Despesas ficaram parciais (10 arquivos, só algumas UFs; marcar como INCOMPLETO no catálogo) e voltam na coleta completa com execução noturna.
D15. Coleta nacional iniciada (coleta_br.py): todos os municípios ainda sem extrato, por UF, 4 requisições simultâneas, retomável (pula quem já tem extrato).
D16. Destino dos brutos: GitHub, conta ze0803@gmail.com (decisão do usuário em 11/11). Repositório privado ainda não criado: a conta GitHub não está conectada ao Claude. Coleta nacional reiniciada após parar às 23:04 UTC com 308 municípios.
D17. Repositório privado ze0803-arch/atlas-encargos-dados criado pelo usuário; Claude sem permissão de criar repositórios. Enviados: scripts, catálogo, brutos do Siconfi (piloto + RN), SIOPE (Indicadores e Receita) e IBGE. Brutos nacionais entram por UF quando a coleta terminar.
D18. Coleta nacional em etapas (supervisor.sh): coletor e etapa.py a cada 15 min empacotam por UF completa (UF_completo.tar), atualizam o catálogo e enviam ao GitHub. Retomada usa dca_IE como critério de município concluído.
D19. MSC por município (analisar.py): usa a MSCE de dezembro; se não fecha com a DCA (1%) testa a soma das 12 matrizes mensais (MSCC, classe 6, period_change). Testa ainda as convenções de sinal (D−C e C−D) e "só débitos" na receita, escolhendo a que mais se aproxima da DCA. Achado: em muitos entes (AL, BA, GO, CE) a MSCE de dezembro traz só o movimento do mês e a receita anual só fecha somando as 12 mensais (Água Branca/AL: R$ 112,15 mi contra R$ 112,15 mi da DCA). Efeito nos 1.250 municípios das 9 UFs coletadas: calculados 708 → 861 (69%); sem MSC 192 → 2; RN 145 → 159 de 167 (95%).
D20. Receita sem natureza na MSC (21 de 22 municípios do AC, entre outros): receita fecha com a DCA, mas não há como calcular a base de impostos para o mínimo legal. Ficam marcados (SEM_NATUREZA_RECEITA, 44 casos). Alternativa futura: obter a base pelo SIOPE.
D21. Divergências restantes (359 municípios, 29%) são heterogêneas, não sistemáticas: despesa liquidada com contas 6221 ausentes na MSCC (liq_dif vazio), diferenças de 2% a 60% em despesa e de 1% a 30% em receita. Seguem marcados e não calculados.
D22. Coleta nacional passa a ser feita pelo aplicativo independente (app_coleta/coletar.py), rodado pelo próprio usuário no computador, com envio ao GitHub; pacotes em partes de até 80 MB. A coleta rodando na sessão do Claude foi pausada em 11/11 com 9 UFs completas (RN, AC, AP, AL, AM, BA, CE, DF, ES).
D23. Brutos de Siconfi/SIOPE em escala nacional (~2 GB) vão para o Zenodo; GitHub fica com scripts, catálogo e resultados. O --enviar do coletor envia só o catálogo; dados/raw e dados/pacotes são ignorados pelo Git. (Decisão do usuário em 11/11.)

## D24 · Conferência de Caicó e correção do % de pessoal (11/11/2026)
- Validação externa (RGF/RREO de Caicó informados pelo usuário): RCL 202.863.507,54 confere; DTP do Executivo 122.101.866,86 (61,50% da RCL **ajustada** de 198.532.923,54, não da RCL) confere; receita do RREO Anexo 1 (216.535.235,53) = receita bruta da DCA I-C (234.960.908,29) − dedução FUNDEB (18.425.672,76).
- Correção: o resultado passa a trazer `rcl_ajustada`, `dtp_leg`, `dtp_exec_pct_rcla` (como publicado no RGF), `dtp_total_pct_rcla` (Executivo + Legislativo), `deducao_fundeb` e `rec_liquida_fundeb`. O "pessoal/RCL" mostrado antes usava a RCL (não a ajustada) e só o Executivo.
- `receita` do sistema = bruta (antes da dedução do FUNDEB), por construção, para fechar com a DCA I-C. Margens não mudaram (nenhuma das 1.250 linhas).

## D25 · Método da margem confirmado pelo pesquisador (11/11/2026)
Respostas do questionário de validação:
- Mínimos de saúde e educação: descontar **só o exigido** (40% da base de impostos). O que o município executa acima disso é escolha do gestor e conta como espaço de decisão exercido (a coluna `minimos_funcao` fica só como informação).
- FUNDEB: receita livre **bruta**; a receita líquida (`rec_liquida_fundeb`) e a dedução (`deducao_fundeb`) ficam como colunas informativas.
- Margem estrita: desconta **apenas a folha** paga com fonte livre (sem serviços essenciais, restos a pagar ou contrapartidas).
- Fonte livre: continua 1500/1501; município com codificação diferente (ex.: BA com receita livre ~0) fica **marcado e não calculado** (regra D5).

## D26 · Casos fora da curva: três flags novas (11/11/2026)
Investigação dos 7 municípios com margem negativa e dos 7 com margem acima de 100% da RCL:
- **Margem negativa (6 na BA + Silves/AM):** nos municípios da BA a fonte 1500 recebe lançamentos positivos e negativos de mesma natureza (reclassificação de FPM/ICMS/IPTU da fonte 1500 para outras, como 1540/1542/1715), e o líquido da fonte livre fica irreal (ex.: Boa Nova 54,3 positivos e −47,8 negativos). Encruzilhada lança 98% da receita na fonte 1001 (codificação antiga). Regra nova: `FONTE_LIVRE_ATIPICA` quando rec_livre/base_impostos < 0,6 ou > 1,5 (mediana 1,03; p1 = 0,69) → marcado e não calculado (D5). Pegou 42 municípios.
- **Silves/AM:** R$ 25,3 mi de despesa do órgão 20231 (Legislativo) em fonte livre, contra teto constitucional de ~7% da base (R$ 2,3 mi); o órgão está codificado errado. Regra nova: `LEGISLATIVO_ATIPICO` quando leg/base_impostos > 0,12 (p99 = 0,078) → marcado e não calculado.
- **Margem acima de 100% da RCL (7 municípios):** a margem em R$ está coerente; o erro é a RCL, que aparece de 5 a 27 mi para receitas de 35 a 214 mi (o RGF desses entes não traz RCL). Regra nova: `RCL_SUSPEITA` quando RCL do RREO 3 / receita líquida do FUNDEB fora de 0,6–1,10 → o percentual da RCL fica vazio; a margem em R$ continua calculada. Pegou 56 municípios.

## D27 · Primeira validação externa da margem: Serra Negra do Norte contra o SIAI/TCE-RN (11/11/2026)
Fonte: SIAI Consultas (TCE/RN), dados abertos, RREO 6º bimestre 2023, Anexos 11 (MDE) e 12 (ASPS), arquivados em `brutos/siai/2023/`.
- Base de impostos: SIAI R$ 22.163.597,09 × sistema R$ 22.163.733,83 (diferença de R$ 136,74). FPM R$ 15.727.904,95 e ICMS R$ 4.075.013,67 batem com as naturezas 171151 e 172150.
- Mínimos exigidos: SIAI MDE R$ 5.540.899,27 + ASPS R$ 3.112.501,01 = R$ 8,65 mi × sistema (40% da base) R$ 8,87 mi (+2,5%).
- Executado em saúde e educação com recursos de impostos: SIAI MDE R$ 5,85 mi + ASPS R$ 5,25 mi = R$ 11,10 mi × sistema (funções 10 e 12 em fonte livre) R$ 11,40 mi (+2,7%). Excesso sobre o mínimo: SIAI R$ 2,45 mi × sistema R$ 2,53 mi.
- O SIAI conta a contribuição ao FUNDEB (R$ 3,80 mi) como aplicação em MDE, o que confirma a neutralidade da receita bruta na margem (D25).
- Em aberto: natureza 171251 (R$ 5,11 mi na fonte livre, fora da base de impostos); Timbaúba dos Batistas (SIAI fora do ar durante a coleta); SIOPS (endereço `carregarDadosLC141.php` devolveu página malformada com zeros).

## D28 · Validação em 12 municípios do RN contra o SIAI/TCE-RN (11/11/2026)
Amostra: Serra Negra do Norte e Timbaúba dos Batistas (indicados) + 10 sorteados (semente 20261111) entre os 157 calculados do RN: Tibau, Lagoa de Velhos, Ouro Branco, Fernando Pedroza, Santana do Seridó, Montanhas, Triunfo Potiguar, Cerro Corá, Grossos e Brejinho. Fonte: RREO 6º bimestre 2023, anexos 11 (MDE) e 12 (ASPS) do SIAI Consultas (dados abertos), lidos pelo navegador do pesquisador. Resultado completo em `catalogo/validacao_siai_2023.csv`.
- **Base de impostos:** diferença absoluta mediana de 0,01% e máxima de 0,17% (confirmada).
- **Mínimos exigidos:** o sistema (40% da base) fica de 1,3% a 4,4% acima do SIAI (MDE 25% + ASPS 15%), mediana +2,2%. Causa: a base da saúde exclui parcelas do FPM (art. 159, I, d/e) e outras transferências, e a do ensino não. Efeito na margem: cerca de 1 a 2%. Refinamento possível: 25% da base + 15% da base sem as parcelas d/e.
- **Executado em saúde e educação com impostos** (coluna informativa, fora da margem): diferença mediana de 2,3%, com casos de −17% a +7% (classificação por função e fonte versus apuração do TCE). Não afeta a margem (D25).
- **Timbaúba:** o mínimo é cumprido com a contribuição ao FUNDEB (MDE com impostos R$ 2,26 mi + FUNDEB = R$ 5,56 mi, 29,85% contra 25%), o que é coerente com a receita bruta (D25).
- Todos os 12 cumprem 25% em MDE e 15% em ASPS.
- Em aberto: a receita livre (fontes 1500/1501) não tem equivalente nos anexos 11 e 12; falta conferi-la, por exemplo, pelo Anexo 1 (balanço orçamentário) e a natureza 171251 de Serra Negra do Norte.

## D29 — Refinamento do mínimo constitucional (25% ensino + 15% saúde sem FPM d/e)
- Mínimos exigidos = 25% × base de impostos (MDE) + 15% × (base − parcelas FPM art. 159, I, "d" e "e": naturezas 17115121/17115122) (ASPS), conforme critério do TCE/RN.
- Validação externa (SIAI/TCE-RN, RREO 6º bim. 2023, 12 municípios do RN): regra antiga (40% da base) +2,2% de erro mediano; regra refinada |Δ| mediana 0,08%, máximo 1,8% (Triunfo Potiguar).
- Resultado: 850 municípios calculados; mediana margem ampla/RCL 31,89%. Ex.: Caicó 34,9→35,2%; Serra Negra do Norte 50,8→51,4%; Timbaúba dos Batistas 50,9→51,3%.
- Limitações: 56 municípios calculados sem parcela d/e identificada (GO 23, BA 11, RN 7, ES 7…) — mínimo da saúde pode ficar levemente superestimado; mínimo da saúde fora do RN sem conferência externa (SIOPS inacessível por script).
- Receita livre (fontes 1500/1501) não tem equivalente nos anexos 11/12; o RREO Anexo 1 é agregado por categoria e não mostra a natureza 17125101 (R$ 5,11 mi em Serra Negra do Norte), classificada como transferência da União fora da base de impostos (compensação financeira), corretamente excluída da base de mínimos e mantida como receita livre.

## D30 — Teste de fontes automáticas de validação (Tesouro Transparente e DCA)
- DCA (Siconfi) só publica I-AB, I-C, I-D, I-E, I-F, I-G e I-HI: não há Balanço Financeiro por fonte de recurso; a receita livre (1500/1501) segue sem conferência externa.
- Tesouro Transparente: o portal web ficou em manutenção (503), mas a API CKAN (/ckan/api/3/action/package_show?id=af4e7c47-2132-4d9a-bd7c-34e28a210b03) entrega CSV mensal por município (FPM, FUNDEB, ICMS, royalties ANP/CFEM/FEP…). Cuidados: arquivos com nome de mês trocado/duplicado (ler a coluna Mês e deduplicar por chave), codificação latin-1, nome do município sem código IBGE.
- Natureza 17125101 = CFEM: Serra Negra do Norte R$ 5.108.936,19 (Tesouro) = MSC, exato; Caicó R$ 8.657,44 (Tesouro) = DCA 1.7.1.2.51.
- FPM: Tesouro difere da MSC/DCA (só 3% dos municípios dentro de 1%); 4 municípios do RN de mesmo coeficiente têm FPM idêntico na MSC (R$ 15.727.905) e valores distintos no Tesouro (hipótese: valor líquido de retenções, não confirmada). Tesouro não separa as alíneas d/e, logo não valida a parcela d/e; em Caicó a cota mensal da MSC (alínea b) bate com o Tesouro (−0,1%).

## D31 — Testes de consistência interna (nível 2 de confiança)
- Sem fonte nacional independente por fonte de recurso (D30), a receita livre e as despesas em fonte livre são validadas por consistência interna. Testes sobre os 850 calculados: T1 receita livre/base 0,8–1,3 (99,1%); T2 Legislativo ≤7% da base (96,1%); T3 folha livre ≤ DTP Executivo do RGF (100%); T4 dívida+precatórios ≤15% da receita livre (99,6%); T5 margem ampla entre 0 e receita livre (100%); T7 margem/RCL entre 0 e 80% (100%); T8 RCL consistente (97,9%).
- 791 municípios (93%) sem nenhuma falha ("alta confiança"; mediana margem/RCL 32,05%); 56 com 1 falha; 3 com 2. Detalhe por município em catalogo/confianca_2023.json.
- Ressalva: T3, T5, T6 e T7 discriminam pouco (T5/T7 em parte circulares com os filtros D26; T3 compara total com parte). Os discriminantes reais são T1, T2, T4 e T8.

## D32 — Recoleta com verificação (resultado: nada recuperado) e SIOPS
- `coletar.py --verificar` compara cada município concluído com o extrato de entregas e refaz meses entregues que vieram vazios (3 tentativas) e a MSCE. Rodado sobre 1.229 municípios: 20 tinham lacunas reais de MSC mensal (AL 11, BA 5, GO 3, RN 1); **0 recuperados** (a API devolve vazio apesar de constar como entregue); MSCE vazia na API em 194. A cobertura segue 850 calculados / 400 não calculados.
- **Correção de erro de análise:** a estimativa anterior de ~100 municípios recuperáveis estava errada: contei meses ausentes no bruto também em municípios para os quais a MSC mensal nunca foi coletada porque a MSCE já fechava com a DCA (e o município estava sem cálculo por outro motivo).
- SIOPS: o endpoint de cálculo LC 141 (`carregarDadosLC141.php?valor=<IBGE6>&ano=&periodo=&g=0`) devolve dados reais até 2019; de 2020 em diante devolve página malformada de ~630 MB com zeros. Formulário (cmbAno, cmbUF, cmbPeriodo, cmbMunicipio) é automatizável; a página `consleirespfiscal.php` (Demonstrativo da Saúde do RREO) não foi concluída.

## D33 — SIOPS 2023 coletado e mínimo de saúde conferido em 1.294 municípios
- Coleta: `app_coleta/coletar_siops.py` (POST em `rel_LRF.php`, mesmo envio do formulário "Consulta de Lei de Responsabilidade Fiscal"; o endpoint `carregarDadosLC141.php` só traz dados até 2019). 1.294 municípios (AC, AL, AM, AP, BA, CE, ES, GO, RN), todos com o Demonstrativo da Saúde (RREO Anexo 12) de 2023, 6º bimestre. Catálogo: `catalogo/siops_2023.csv` e `catalogo/diario_siops.csv`; HTML originais com hash vão ao Zenodo.
- Comparação do mínimo de saúde (15% × (base de impostos − FPM d/e), do sistema) com a Despesa Mínima em ASPS (XVII) declarada no SIOPS: nos 827 calculados, diferença absoluta mediana de 0,03%; 80% dentro de 1%, 86% dentro de 3%, 96% dentro de 10%. Em todos os 1.174 comparáveis: mediana 0,20%; 66% dentro de 1%.
- Por UF (|Δ| mediana): CE 0,01%, RN 0,01%, GO 0,13%, AM 0,31%, ES 0,35%, BA 0,95%, AL 0,97%, AP 1,14%. BA e AL têm mais casos distantes (p90 acima de 20%).
- Sem parcela d/e identificada (118 casos): |Δ| mediana 1,85% (45% dentro de 1%); com d/e: 0,16%. Confirma que a parcela d/e ausente explica parte da diferença.
- O selo de confiança (D31) discrimina pouco: >10% de diferença em 3,9% dos de alta confiança e 7,1% dos com ressalva.
- Extremos (acima de 100%) em poucos municípios (Lagoa da Canoa/AL, Jiquiriçá/BA, Ribeira do Amparo/BA, Esplanada/BA, Tapiramutá/BA, Ipu/CE): possível diferença de base declarada no SIOPS ou erro na MSC; a investigar.

## D34. Exceções do SIOPS e teste T9 (11/11/2026)

- Das 827 prefeituras calculadas com SIOPS, 34 (4%) divergem mais de 10% do mínimo de saúde (BA 19, GO 5, CE 3, RN 3, AM 2, ES 1, AL 1). Entre as 347 não calculadas com SIOPS, 121 divergem: a divergência acompanha os problemas já sinalizados.
- Causa identificada em parte dos casos extremos (Jiquiriçá, Ribeira do Amparo, Laje, Ituaçu, Santa Rita de Cássia, Barra do Choça, BA; Lagoa da Canoa, AL): a prefeitura lançou praticamente toda a receita, inclusive transferências, sob uma natureza de imposto (11125001) na MSC. A receita total fecha com a DCA, mas a "base de impostos" vira a receita total. Os testes de receita não detectam isso.
- Detector próprio (natureza 111* contra a receita tributária do RREO) tem falsos positivos demais; foi descartado.
- Decisão: o SIOPS passa a ser o teste T9 de confiança (|diferença| ≤ 10%). Município calculado que falha em T9 perde o selo de alta confiança (não deixa de ser calculado). No `atlas.py`, a etapa `comparar` passa a rodar antes de `confianca`.
- Efeito no piloto: alta confiança de 90% dos calculados (761 de 850); 34 falharam em T9.
- Limite: T9 só vale onde o SIOPS existe. O mínimo de saúde conferido não prova a receita livre nem as despesas por fonte.

## D35. Matriz de encargos e primeira medição (11/11/2026)

- Planilha "Matriz de encargos do Atlas" (artefato) lista 24 encargos por bloco (H heterônoma, L autovinculação, P pactuada), com norma, se entra na margem e se é mensurável na MSC. Normas e artigos a conferir no texto oficial antes de citar na tese.
- Códigos de fonte confirmados na Tabela Padrão de Fontes (TCE-RN, V3, baseada na Portaria Conjunta STN/SOF 20/2021): 1500 não vinculados de impostos; 1501 outros não vinculados; 1540 a 1543 FUNDEB (impostos, VAAF, VAAT, VAAR); 1544 precatórios do FUNDEF; 1550 a 1553 e 1569 FNDE; 1600/1601 SUS; 1604 vencimento de ACS/ACE; 1660 FNAS; 1700 convênios da União; 1751 COSIP.
- FUNDEB 70% (696 municípios com MSCE, convenção liq+): pessoal é 70% ou mais da despesa nas fontes do FUNDEB em 634 de 692 (92%); mediana 88,5%. Aproximação, porque a regra incide sobre a receita do Fundo. Não é encargo adicional: a dedução do FUNDEB já conta como aplicação em educação (D-anterior sobre receita bruta).
- Precatórios: elemento 91 em qualquer fonte; 609 de 696 com valor, mediana 0,4% da base. Não existe fonte própria de precatórios municipais. Elemento 91 pode incluir outras sentenças judiciais.
- COSIP (fonte 1751): receita em 467 de 696; despesa paga com ela cobre em mediana 86% da receita. O custo acima da COSIP sai de outra fonte e não se separa.
- Limite: a medição cobre só os 696 municípios calculados com MSCE na convenção liq+; os 153 por soma de MSCC mensais ficaram de fora.

## D36. Segunda medição de encargos (11/11/2026)

Mesma base da D35 (696 municípios calculados, MSCE, liq+). Medianas sobre a despesa liquidada total ou a receita livre:
- Elemento 13 (obrigações patronais): 6,1% da despesa (4,7% da receita livre). Já dentro da folha livre; não somar de novo.
- Elemento 47 (obrigações tributárias e contributivas, inclui PASEP): 0,84% da despesa. Compatível com 1% do PASEP, mas o elemento mistura outros tributos.
- Função 08 (assistência social): 3,5% da despesa (3,9% da receita livre); fonte FNAS (1660) cobre 20% em mediana. Sem gasto mínimo em lei.
- Elemento 71 (consórcios, contrato de rateio): 637 de 696 têm o gasto; 2,4% da despesa (2,0% da receita livre; máx. 12,6%). Ainda fora da margem; decidir se entra no bloco P.
