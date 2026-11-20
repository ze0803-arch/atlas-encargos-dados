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

## D37. Consórcios públicos como bloco P (11/11/2026)

- Decisão do autor: a adesão a consórcio público (contrato de rateio, elemento de despesa 71, em fonte livre, fora do Legislativo) é pactuação (bloco P), não autovinculação.
- `analisar.py` ganhou a coluna `consorcios` e a coluna `margem_ampla_p` (margem ampla menos consórcios). A margem ampla e a estrita não mudam, para manter a série comparável; o bloco P entra à parte.
- Piloto 2023 (850 calculados): 785 têm gasto com consórcio; mediana de 2,1% da receita livre. A mediana da margem ampla sobre a receita livre cai de 52,3% para 49,8% após o bloco P. Nenhum município fica negativo por causa dele.
- Conferência de 12/11/2026 (resultado_2023.csv do piloto): sobre os 850 calculados, a mediana é 2,09% (p90 5,9%; máx. 12,6%); entre os 785 que têm gasto, 2,35% (p90 6,0%). Os dois números estão certos e medem coisas diferentes (com e sem os zeros). Padrão de citação: "2,1% sobre os 850 calculados; 2,3% entre os 785 com gasto". O protótipo havia usado 787 e 2,34% por contagem anterior.
- Pendente: decidir quais outros itens da matriz entram no bloco P (contrapartidas de convênios, programas com adesão) e se a margem principal passa a descontá-lo.

### Correção da D37 (11/11/2026)

- Conferido o mapeamento de 3.1.3: H = bloco I, L = bloco II, margem = bloco III, P = bloco IV. Portanto o bloco P não é desconto da margem: é medido à parte. Contrapartidas de convênios e programas com adesão também são P (confirmado pelo autor).
- `margem_ampla_p` fica como sensibilidade (quanto a margem cairia se o bloco P fosse tratado como desconto), não como margem principal. A margem ampla e a estrita não mudam.

## D38. Bloco P: receita federal vinculada e acesso ao Transferegov (11/11/2026)

- Receita por fonte vinculada de transferência da União, sobre a receita total, nos 696 calculados com MSCE (medianas): SUS 1600-1604 8,1%; FNDE 1550-1553 e 1569 1,5%; convênios 1570 e 1700 0,8%; FNAS 1660 0,7%. Soma: 11,8% da receita (p10 7,1%; p90 19,4%; máx. 35,6%).
- Leitura: é o tamanho do que a União financia com recurso vinculado, não o encargo líquido do município. Limite de classificação: parte dessas fontes não depende de adesão (salário-educação 1550 e transferências SUS fundo a fundo têm base legal); a soma é teto do bloco P, não medida dele.
- Contrapartida não aparece separada na MSC. A fonte possível é o Transferegov (convênios). Do ambiente do Claude o site não abre (403/502; o endereço antigo do repositório siconv.zip retorna 404). Qualquer coleta precisa rodar no computador do autor, e o endereço correto do conjunto de dados abertos deve ser confirmado por ele na página do portal.

## D39. Contrapartida de convênios da União, 2023 (11/11/2026)

- Fonte: Portal da Transparência, arquivo 20261023_Convenios.zip (Convenios.csv e Convenios_OrdensBancarias.csv; dados do SIAFI e do SICONV até 23/10/2026), enviado pelo autor. Do ambiente do Claude o servidor de download retorna 403. O endereço do portal `download-de-dados/convenios/<ano>` redireciona para `dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/convenios/<ano>_Convenios.zip`.
- O arquivo tem a coluna VALOR CONTRAPARTIDA. VALOR CONVÊNIO é o repasse da União (liberado/convênio tem mediana 1,0). Contrapartida total tem mediana de 5% do repasse.
- Método (`app_coleta/convenios.py`): liga a prefeitura pelo CNPJ de `entes.json` (429.283 de 431.429 convênios de municípios ligaram); contrapartida de 2023 = contrapartida total x (liberado em 2023 pelas ordens bancárias / valor do convênio), teto 1. É um rateio proporcional, não o gasto efetivo de contrapartida em 2023.
- Resultado nos 850 calculados: 633 têm repasse liberado em 2023. Repasse liberado = 1,2% da receita livre em mediana (p90 7,5%; máx. 85%). Contrapartida = 0,01% da receita livre em mediana (p90 0,45%; máx. 3,0%); contrapartida/liberado = 5,9%.
- Leitura: a contrapartida de convênios da União pesa pouco na margem; o bloco P relevante em valor é consórcios (2,0%) e a receita vinculada da União (11,8%, teto). Cobre só convênios; não cobre SUS fundo a fundo nem FNDE.
- Saída em `catalogo/convenios_2023.csv` (4.107 municípios, todos os que tiveram liberação em 2023).

## D40. Transferências da União por programa, Portal da Transparência "Recursos Transferidos" (11/11/2026)

- Arquivo `<ano><mês>_Transferencias.zip` (portaldatransparencia.gov.br/download-de-dados/transferencias/<ano><mês>), testado com janeiro de 2023 (enviado pelo autor). Traz tipo de transferência, favorecido, município (código SIAFI), função, órgão, ação e valor.
- Os repasses fundo a fundo do SUS aparecem com favorecido "Administração Pública" (fundos municipais) e por ação: Piso de Atenção Primária, Média e Alta Complexidade, vencimentos de ACS e ACE, assistência farmacêutica. O cofinanciamento do FNAS também. Constitucionais, FUNDEB e salário-educação estão como favorecido municipal. PNAE, PNATE e PDDE não apareceram em janeiro; podem estar em outros meses (a conferir com o ano completo).
- Ligação com o IBGE por UF e nome normalizado: 5.549 de 5.569 municípios (20 com nome truncado no arquivo, ex.: Itapajé/CE).
- `app_coleta/transferencias.py` baixa os 12 meses (precisa de internet, no computador do autor), classifica por grupo e grava `transferencias_<ano>.csv` e `transferencias_<ano>_por_acao.csv`.
- Pendente: rodar com os 12 meses, comparar com as fontes da MSC (1600, 1604, 1660, 1550) e decidir quais ações entram no bloco P (adesão) e quais são transferência legal.

## D41. Diferenças de 10% ou mais com o SIOPS: causas e correção do extrator (11/11/2026)

- Dos 34 calculados acima de 10% (D34), 3 eram falso positivo: Acaraú, Boquira e Itamari usam percentual da Lei Orgânica Municipal (XVII sem o rótulo de 15%). O extrator lia o número da linha seguinte quando a linha de 15% vinha N/A. Corrigido em `coletar_siops.py` (campos `minimo_lom` e `base_realizada_III`) e em `comparar_siops.py` (para município com Lei Orgânica compara a base: 15% x receita realizada do SIOPS). Resultado: Acaraú 5,3%, Boquira 0,01%, Itamari 0,12%. Restam 31 acima de 10%; alta confiança passa de 761 para 764 de 850.
- Conferido em 1.171 municípios: o XVII de 15% é exatamente 15% da receita realizada (coluna b) do item III. A coluna `base_calculo_III` guarda a previsão, não a realizada; para comparar bases usar `base_realizada_III`.
- Levantamento por componente da base (MSCE contra o Anexo 12): 8 casos em que a receita de impostos próprios da MSC difere do SIOPS (Santa Rita de Cássia, Ribeira do Amparo, Jiquiriçá, Barra do Choça, Ituaçu, Laje: outras receitas lançadas sob natureza de imposto, como em D34; Umburanas e Mascote: impostos ausentes ou com sinal negativo na MSC). 17 casos em que só a linha do FPM difere: a natureza 17115111 (FPM) da MSC é maior que o FPM do SIOPS em 1,5 a 7,6 milhões em 12 deles, parte da dedução do Fundeb (a diferença equivale a 29% a 86% dela; Guaçuí tem diferença exata de R$ 7.600.000,00); em Érico Cardoso o SIOPS não separa a parcela d/e que o sistema separa (diferença de R$ 6 mil); em Taipu, Araguapaz e Itapiranga o SIOPS tem FPM maior que a MSC. 4 casos pela cota de ICMS, IPVA e IPI (Itatira, Paulo Afonso, Caculé, Divinópolis de Goiás). Lagoa da Canoa e Gouvelândia não reconstituídos (base vem da soma de MSC mensais).
- Leitura: nenhum dos 31 indica erro do método; são lançamentos diferentes entre MSC e SIOPS. A causa do FPM é hipótese (SIOPS líquido de parte do Fundeb), não confirmada. Esses municípios seguem calculados, sem o selo de alta confiança.
- Achado para a tese: só 3 de 1.171 municípios do SIOPS declaram percentual de saúde da Lei Orgânica acima de 15% (Acaraú 20%, Boquira 22,4%, Itamari 17,8%). É autovinculação (bloco L), mas rara; o mínimo do Atlas continua 15% e o excedente aparece como gasto livre.
- Efeito colateral do levantamento: a execução do extrator sem restrição de UF baixou também páginas do SIOPS de outras UFs no ambiente de trabalho (211 arquivos, fora do catálogo); não entram nos resultados.

## D42. Teste da hipótese do FPM e do Fundeb (11/11/2026)

- Método: para os 1.174 municípios com SIOPS, comparou-se a linha "Cota-Parte FPM" do Anexo 12 com a natureza 17115111 (FPM) da MSCE de dezembro. 926 têm as duas; 248 não têm a natureza 17115111 na MSC.
- Resultado: em 639 (69%) o FPM do SIOPS é igual à natureza 17115111 (±0,3%), sem a parcela d/e, que está na natureza 17115121; confirma que o sistema trata o FPM como o SIOPS na regra geral. Em 21 o SIOPS inclui a parcela d/e.
- Padrão do Fundeb: em 34 municípios (quase todos da Bahia) o FPM do SIOPS está abaixo do da MSC por um valor igual a 20% do FPM: em 13 a diferença é 20% do FPM da MSC (MSC x 0,8 = SIOPS; ex.: Guaçuí, Jaguaribara, Campinaçu) e em 21 é 20% do FPM do SIOPS (MSC = 1,2 x SIOPS; ex.: Serrolândia, Mutuípe, Sítio do Quinto). Entre os 31 calculados acima de 10% (D41), 11 se encaixam nesse padrão (Guaçuí, Jaguaribara, Caculé, Campinaçu, Serrolândia, Sítio do Quinto, Mundo Novo, Mutuípe, Nova Itarana, Cardeal da Silva, Ituaçu).
- A dedução do Fundeb não aparece como natureza de receita na MSC desses municípios (nenhuma natureza iniciada em 9 na conta 621200000); por isso não deu para conferir pelo valor da dedução da MSC. A comparação com a dedução total da DCA não é estável (29% a 86%), porque ela inclui ICMS, IPVA e ITR.
- Leitura: é compatível com municípios que informaram o FPM líquido do Fundeb no SIOPS. A base legal da saúde não deduz o Fundeb, então o sistema (FPM bruto da MSC) segue como está. É indício, não prova: faltaria o demonstrativo do município. Os outros 20 dos 31 têm causas diversas (D41); 232 dos 926 comparáveis têm diferença no FPM sem padrão identificado.
- Consequência para o selo: nenhuma mudança. Os 11 continuam sem alta confiança por T9; se a hipótese for aceita, poderiam ser reclassificados em "diferença explicada pelo SIOPS", sem mudar o cálculo.

## D43. Correção do cálculo de consórcios: modalidade 71, não elemento 71 (12/11/2026)

- Erro: a D37 somava como consórcio o elemento de despesa 71 (`nd[4:6] == '71'`). Esse elemento é o principal da dívida contratual resgatado (ex.: natureza 46907101 em Pureza/RN). Os consórcios ficam na modalidade de aplicação 71 (`nd[2:4] == '71'`, contrato de rateio). A coluna `consorcios` do piloto media, na prática, a amortização da dívida: em 468 dos 850 calculados ela era igual à dívida da margem.
- Achado ao conferir a amostra do nível 3 (SIAI); a conferência da D37 de 12/11 (2,1% e 2,3%) só tinha reconferido a contagem, não o conceito.
- Correção em `analisar.py` e no rótulo do relatório. Margem ampla, estrita, status e selos não mudam (conferido nos 1.250 do piloto); só mudam `consorcios` e `margem_ampla_p`.
- Piloto 2023 (850 calculados) depois da correção: 619 têm gasto com consórcio em fonte livre; mediana de 0,31% da receita livre sobre os 850 (0,52% entre os 619); p90 1,6%; máximo 5,0%. A margem ampla mediana vai de 52,3% para 51,8% (sensibilidade do bloco P); antes aparecia 49,8%. Ninguém fica negativo.
- Substitui os números de consórcios das D37 (2,1% e 785), da D37 corrigida, da Matriz (linha 25), do protótipo e da seção metodológica da tese. Quem rodou o `analisar.py` antes desta correção precisa rodar de novo (só a etapa analisar).

## D44 — Auditoria por amostra (nível 3), SIAI/TCE-RN, exercício 2023 (12/11/2026)
- Amostra: 5 municípios do RN, um por faixa de porte (Paraú, Pureza, Lagoa Nova, Parelhas, Ceará-Mirim). Fonte: Anexo 02 (despesa por categoria econômica, consolidada) e Anexo 09 (despesa por órgão e funções) das contas de governo no SIAI Consultas (público; os PDFs têm camada de texto).
- Itens comparados: Legislativo (órgão Câmara), dívida (3.2 juros + 4.6 amortização) e sentenças judiciais (elemento 91, todas as categorias). 15 comparações; arquivo `auditoria_nivel3_2023.csv`.
- Resultado: 9 de 15 conferem a menos de 0,1%; 3 ficam entre 98% e 99,6% do SIAI; 3 ficam entre 64% e 89% (Legislativo de Lagoa Nova e de Parelhas; dívida de Ceará-Mirim). Em nenhuma comparação o Atlas excede o SIAI.
- Leitura: o Atlas usa só despesa liquidada em fonte livre (1500/1501), e os anexos somam todas as fontes. Atlas ≤ SIAI é o esperado, e a igualdade em oito casos mostra que nesses a despesa é toda de fonte livre. Os três desvios maiores são compatíveis com parte do gasto em outras fontes, mas os anexos não trazem fonte de recurso e a hipótese não está provada.
- Limites: amostra de 5 (não permite taxa de acerto nacional); só RN; só 2023; Anexo 09 pode refletir empenhado e não liquidado (não verificado). Para fechar os três desvios é preciso o XML das contas de governo ou a MSC por órgão e fonte (pedido ao TCE-RN, opcional).
- Efeito: o selo de nível 3 pode ser declarado "auditado por amostra, com ressalva" para esses cinco; os resultados dos demais municípios não mudam.

## D45 — Execução nacional de 2023: cobertura, tolerância e universo (13/11/2026)
- Resultado: 5.569 entes, 4.038 calculados (73%; 4.038 de 5.568 se o DF sair do universo, 72,5%) e 3.451 com alta confiança (85% dos calculados). Relatório em `relatorio_2023.md`.
- Cobertura desigual por UF: AC 5%, PB 18%, AL 34%, AP 44%, MT 49%, BA 54%, GO 57%; PI 95%, RN 92%, CE e PA 90%.
- Acre: 21 dos 22 municípios sem natureza da receita na MSC (`SEM_NATUREZA_RECEITA`); limitação do dado de origem, sem imputação. Demais UF de baixa cobertura: divergência MSC × DCA (`REC_DIVERGE`, `LIQ_DIVERGE`).
- Tolerância MSC × DCA mantida em 1% como regra principal. Entre os 1.350 com divergência, 1.011 têm só esse motivo; com tolerância de 2%, 3% e 5% voltariam 228, 325 e 484. A divergência mediana desses 1.011 é de 2,6% (receita) e 3,5% (despesa liquidada), o que indica diferença sistemática de classificação, não ruído. A sensibilidade a 3% é análise separada: `python analisar.py --pasta dados --tol 0.03` grava `resultado_2023_tol3.csv` (a regra principal não muda).
- Universo: o DF não é município e sai do denominador municipal. Fernando de Noronha (2605459) não aparece na lista de entes; é distrito estadual de Pernambuco; decisão pendente (incluir ou declarar a exclusão).
- Margem ampla mediana nacional: 40,3% da RCL (não comparável com os 51,8% da receita livre do piloto do RN; bases diferentes).
- Nas tabelas do bloco P, as linhas de SUS mostram o recebido em % da receita livre, não encargo; são apresentadas à parte.

## D46 — Correspondência de nomes do Portal da Transparência com o IBGE (13/11/2026)
- O arquivo de transferências ligava município por UF e nome normalizado; 20 municípios ficaram sem ligação por grafia diferente (nome antigo, ortografia antiga ou sufixo), por exemplo Parati (RJ, IBGE: Paraty), Iguaraci (PE, IBGE: Iguaracy), Seridó (PB, IBGE: São Vicente do Seridó), Januário Cicco (RN, IBGE: Boa Saúde).
- Corrigido em `transferencias.py` com tabela `ALIAS` (20 pares, conferida contra o arquivo de janeiro de 2023). Boa Esperança do Norte (MT) não aparece no Portal em janeiro; fica sem transferências. Rodar de novo a etapa `transferencias`.

## D47 — Casos extremos de receita e de mínimo de saúde (nov/2026)
Varginha (MG): MSC e DCA trazem receita de R$ 12,7 bi para 144 mil habitantes (RCL do RREO R$ 107 mi); o erro está na fonte, não no método. O município continua "calculado" mas sem selo de alta confiança (T3, T8, T9). Proposta: regra de exclusão quando a receita da MSC for maior que 10 vezes a RCL; pendente de decisão.
Lagoa da Canoa (AL), Jiquiriçá e Ribeira do Amparo (BA): toda a receita, inclusive transferências, lançada sob natureza de imposto (receita livre = base = receita total); o mínimo de saúde do sistema fica 2 a 3 vezes o do SIOPS. T9 já tira o selo.

## D48 — Bloco P nacional (nov/2026)
Receita federal vinculada (SUS, FNAS, FNDE, convênios) sobre a receita total, em 3.522 municípios calculados com MSCE e convenção liq+: mediana 9,5%, p90 16,6% (piloto de 9 UFs: 11,8%). Script: analises/med_p.py. Pendente em nível nacional: teste do FPM contra o SIOPS (precisa de raw/siops).

## D49 — Decisões do formulário de 2023 (13/11/2026)
- PNAE: fora do bloco P (obrigação legal).
- Fernando de Noronha (2605459): excluído do universo municipal, como o DF; a exclusão é registrada.
- Sensibilidade de 3% entre MSC e DCA: só em apêndice metodológico, com ressalva; o resultado oficial é o de 1%.
- Classificação das ações da União (catalogo/classificacao_acoes_2023.csv): as 40 maiores ações (99,3% do valor) foram classificadas pelo formulário, aceitando todas as propostas; as demais pela proposta, ou adesão a revisar (0,4% do valor). Participação no total transferido (R$ 391,9 bi): automática constitucional 69,1%; obrigação legal 21,4%; adesão 6,3%; outra 3,2%.

## D50 — Receita incompatível com a população (13/11/2026)
Município cuja receita na MSC passa de R$ 40.000 por habitante fica "marcado, não calculado" (flag RECEITA_INCOMPATIVEL). Mediana nacional: R$ 6.370 por habitante; p99: R$ 19.557. Efeito em 2023: só Varginha (MG, R$ 88.495 por habitante, receita de R$ 12,7 bi); nenhum falso positivo entre os calculados. Medianas e cobertura não mudam; o total nacional de receita cai R$ 12,7 bi. Rejeitada a regra "receita maior que 10 vezes a RCL" (excluiria Paiçandu/PR, cuja RCL é que está errada, e não se aplica aos 143 calculados sem RCL).

## D51 — Teste do FPM nacional (13/11/2026)
Cota-Parte FPM do SIOPS contra a natureza 17115111 da MSCE (analises/fpm_nacional.py), 3.685 calculados com os dois valores: igual até 1% em 3.180; cerca de 20% abaixo (padrão da dedução do Fundeb) em 51; entre as 88 exceções de saúde acima de 10%, 36 têm esse padrão. Indício, não prova; o cálculo não muda.

## D52 — RAIS retirada do método, dos cálculos e do sistema (13/11/2026)
- Decisão final do pesquisador, depois de uma ida e volta no mesmo dia: os arquivos da RAIS são grandes demais e a pergunta da tese pode ser respondida sem eles. A RAIS não entra na margem, nos testes de assimetria, nos testes jurídicos nem na coleta.
- O custo dos pisos salariais, que a RAIS permitiria medir por cargo, é substituído pela exposição a um choque uniforme (D54).
- Efeito: RAIS removida do Protocolo, do Roteiro de coleta, do protótipo e dos scripts; o quesito 8 do Protocolo (obtenção da RAIS) ficou como retirado.

## D53 — Testes jurídicos de 2023 (13/11/2026)
- Art. 167, § 7º da CF: correspondência encargo-fonte medida pela fonte que paga a despesa nas funções 10, 08 e 12 (transferência federal vinculada × fonte livre), pelo excedente da fonte livre sobre o mínimo constitucional e, nos pisos, só pelo lado federal (assistência da enfermagem, fonte 1604). Pisos: ver D54.
- Art. 11 da LRF: "efetiva arrecadação" operacionalizada como receita realizada de IPTU, ITBI e ISS na MSC; critério principal = zero; sensibilidade = menos de R$ 10 por habitante (limiar arbitrário, só sensibilidade). Exposição à sanção = convênios e ações voluntárias da União de 2023.
- 3.453 municípios calculados com MSCE. Resultados em catalogo/testes_juridicos_2023.md; extração em analises/extrai_juridico.py (base catalogo/juridico_base_2023.csv); testes em analises/testes_juridicos_2023.py.

## D54 — Pisos: choque uniforme sobre a folha da função (13/11/2026)
- Sem a folha por cargo, os pisos passam a ser medidos pela exposição de cada município a um mesmo reajuste nacional: índice x despesa de pessoal da função (MSC). Magistério: 14,95% (piso de jan/2023). É teto do custo, não o custo.
- Resultado e script: catalogo/choque_pisos_2023.md, analises/choque_pisos_2023.py. O custo efetivo (folha abaixo do piso por cargo) fica como limitação declarada.

## D55 — Robustez dos testes de 2023 e critério relativo do art. 11 (2023)
- Teste de robustez em analises/robustez_2023.py (saída: catalogo/robustez_2023.md).
- A relação entre base tributária própria por habitante e margem decisória se mantém com tolerância MSC×DCA de 3% (n = 4.103), com base alternativa (IPTU+ISS+ITBI por habitante; participação do tributo próprio na receita) e excluindo as 8 UFs com cobertura abaixo de 60% (AC, AL, AP, BA, DF, GO, MT, PB). Sinal e significância não mudam (coeficiente sobre a receita total entre 2,2 e 3,3 pontos por log de base; p < 1e-5 em todas).
- Dentro da mesma UF a diferença cai: margem sobre a receita livre quase não varia entre quintis (54,4 a 55,3%); sobre a receita total vai de 31,4 a 34,4% (rho = 0,069). Parte relevante da assimetria de 2023 é entre UFs e faixas de porte, não só entre municípios vizinhos. Registrar como limite da conclusão.
- Art. 11 da LRF: critério relativo substitui o limite de R$ 10 por habitante. Considera-se baixa arrecadação a receita de IPTU, ISS ou ITBI abaixo de 10% da mediana da mesma UF e faixa de porte. Resultado: 25,2% dos municípios do quintil de menor base têm algum imposto abaixo do critério, contra 2,3% no quintil de maior base (9,8% do total).

## D56 — Conclusões de 2023 e conferência de normas
- Consolidação em catalogo/conclusoes_2023.md. A conclusão central é afirmada com o limite de que a assimetria dentro da mesma UF é pequena.
- Normas com texto oficial integral ainda por conferir antes de citação na tese: art. 11 da LRF, Lei 11.738, Lei 14.113, número da lei do crédito do piso da enfermagem, Portaria GM/MS 1.135/2023 (provável confusão com a 597/2023), Tema 1181 e resoluções ANEEL.

## D57 — Viés de cobertura de 2023
- 4.037 de 5.570 municípios calculados (72,5%). Principais motivos entre os não calculados: divergência MSC×DCA na liquidação (1.044) e na receita (908), fonte livre atípica (240), RCL suspeita (178), sem natureza da receita (154).
- A cobertura não varia com o porte (71% a 74%) nem com a população ou a receita por habitante (p > 0,2). Varia pouco com a base própria: 69,6% no quintil menor e 75,4% nos dois maiores; no logit com efeito fixo de UF a base não prediz cobertura (p = 0,54).
- Coeficiente ponderado pelo inverso da probabilidade de cobertura é igual ao sem peso (1,17 sobre a receita livre; 3,19 contra 3,21 sobre a receita total). Sem evidência de viés em variáveis observadas; viés em não observadas não é descartável. Arquivo: catalogo/vies_cobertura_2023.md

## D58 — Correções no protótipo e sincronização do catálogo
- Os alertas de cada município no protótipo saíam como "Flags(allows_duplicate_labels=True)" (x.flags é atributo do pandas; corrigido para x['flags'] em build_prototipo_nacional.py). A lista de alertas por município agora mostra os códigos reais (REC_DIVERGE, LIQ_DIVERGE etc.).
- catalogo/ tinha siops_2023.csv, comparacao_siops_2023.csv, confianca_2023.json e convenios_2023.csv de 9 UFs; substituídos pelas versões nacionais. Reconstruir o protótipo com os arquivos antigos reduziria a validação nacional (5.456 comparações) a 1.174.
- O script de reconstrução passa a ser idempotente nos textos.
- Novo cartão 6 na página Metodologia do protótipo, com os resultados de D53 a D57.

## D59 — Telas do protótipo com dados reais de 2023
- Início, Coletar, Conferir, Município (ficha), Gráficos e uma nova tela Testes da tese passam a usar dados reais de 2023. Só a tela Classificar (dicionário) segue como demonstração.
- Scripts: prototipo/build_prototipo_nacional.py (resultado e validação), build_tese_2023.py (testes da tese e gráficos, a partir dos .md de catalogo/) e build_real_2023.py (início, coleta, conferência e ficha). Rodar nessa ordem, da raiz do repositório.
- Conferir tem tolerância ajustável sobre os 5.568 municípios. A ficha mostra o cálculo agregado por município (receita livre, mínimos, Legislativo, dívida, precatórios, folha), não as linhas brutas da MSC, que ficam no Zenodo.
- Coletar mostra o diário do piloto guardado no repositório (1.272 entes); o diário da coleta nacional está no computador do pesquisador.

## D60 — Diagnóstico da baixa cobertura da Paraíba e do Acre (2023)
- Acre: 21 de 22 municípios com MSC sem natureza da receita; as contas fecham com a DCA (D20, D45).
- Paraíba (41 de 223 calculados): a MSC de dezembro vem curta (mediana de 68 linhas, contra cerca de 2.000 nos demais estados) e 124 municípios caem na soma das 12 matrizes mensais. Desses, 35 têm meses vazios (nenhum calculado), 32 fecham e 57 têm os 12 meses mas não fecham com a DCA.
- Entre os 57: a soma mensal fecha em 2; descartar linhas duplicadas (mesma entrada da MSC) fecha em 6 (+4); só dezembro ou o último mês não fecham nenhum. Em casos como Tavares, a conta de receita (621200000) não existe nas matrizes; em Camalaú, a receita e a despesa vêm em dobro. Conclusão: a maior parte não é recuperável pelo Siconfi.
- Não aplicado: a regra de duplicatas acrescentaria cerca de 4 municípios da PB; reavaliar numa próxima rodada nacional. Script: analises/diag_pb_2023.py. Hipótese não verificada: a falha vem do sistema contábil que os municípios usam para enviar a MSC; o SAGRES (TCE-PB) seria uma fonte alternativa, ainda não testada.

## D61 — Reformulação da tese a partir dos testes de 2023 (decidida em 13/11/2026)
- Enunciado: em que medida a norma nacional uniforme, pelos encargos que impõe e pela forma como os financia, reduz de modo desigual a margem de decisão de municípios com bases fiscais desiguais, e o que isso implica à luz da autonomia municipal e da correspondência entre encargo e fonte (CF, art. 167, § 7º). Separa duas fontes de desigualdade: encargos dentro da receita livre e vinculação do financiamento.
- Hipóteses (limiares a fixar com o orientador): H1 base menor, menor parcela livre da receita total (refutada se o IC 95%, erro agrupado por UF, excluir 5 pontos entre os quintis extremos); H2 encargos internos à receita livre pesam mais onde a base é menor (refutada se a diferença ficar dentro de ±2 pontos); H3 reajuste nacional uniforme consome mais margem onde a base é menor (painel, exposição × reajuste); H4 cobertura federal maior onde a base é menor e nenhum encargo sem fonte concentrado nas bases fracas; H5 baixa arrecadação associada à menor capacidade, sem sanção visível do art. 11.
- Cuidados: (a) medida principal de base fiscal independente (PIB por habitante), porque a base própria é parte da receita livre; (b) H5 usa essa medida para não ser circular; (c) margem sobre a receita total e vinculação são quase uma identidade (correlação 0,96) e não contam como duas provas; (d) 2023 é exploratório, 2024-2027 confirmatório.
- Análise comparativa: entre UFs, dentro da UF (quintis por UF, pares de porte e UF) e modelo em dois níveis, com cobertura por UF ao lado de cada resultado.
- Texto: explicações de dados e metodologia em linguagem simples, para o usuário e o orientador.

## D62 (13/11/2026) — Base independente (PIB por habitante IBGE) e análise comparativa UF/município
- PIB municipal 2023 (SIDRA 5938, var. 37) ÷ população do Censo 2022 = medida de capacidade independente da receita própria (resolve a circularidade de H1/H5). Arquivos: catalogo/pib_2023.csv, base_independente_2023.md, comparativo_2023.md; scripts em analises/.
- Resultado: Q1→Q5 de PIB por habitante: margem sobre receita total 24,4→38,3 (+13,9 pontos); sobre receita livre 52,1→56,7 (+4,6); vinculada 52,8→32,2. Com efeitos fixos de UF e erro agrupado: +4,2 pontos de margem (receita total) por unidade do log do PIB per capita (IC95% 3,6–4,8). Dentro da UF a relação é positiva em 20 de 20 UFs (Spearman mediano 0,21).
- Art. 11 LRF (critério relativo): municípios abaixo do critério em IPTU/ISS/ITBI: 25,3% no Q1 de PIB contra 3,6% no Q5.
- Modelo em dois níveis: 33% da variação da margem está entre UFs; efeito médio 4,2 (inclinação varia entre UFs, desvio 1,3; positiva em 19 de 20). Pares de mesma UF e porte: terço de maior PIB tem +3,4 pontos, positivo em 87% dos 87 grupos.
- Cuidados: UFs com <40 calculados ou cobertura <40% (RR, AP, AL, PB, RO, AC) fora das leituras por UF; sensibilidade com peso pela cobertura não muda o efeito (4,16). 2023 permanece exploratório. PIB pode refletir arrecadação via ISS de empresas — não é medida perfeita de capacidade.

## D63 (13/11/2026) — App: tela Comparativo e textos simples
- Nova tela Comparativo (aba Resultados): quintis de PIB por habitante, art. 11 e tabela por UF com cobertura; UFs com <40 calculados ou cobertura <40% marcadas "cobertura insuficiente". Quadro "Em palavras simples" na Metodologia. Script: prototipo/build_comparativo_2023.py (rodar após build_real_2023.py). Pendentes: Início/Ficha com quintil de PIB do estado, tela de hipóteses H1–H5, seletor de ano, textos simples do Protocolo/Roteiro.

## D64 (13/11/2026) — Conferência da proposta do chat Tese
- Os números de 2023 (p_m, p_mt) são da margem AMPLA (sem descontar a folha livre); o prompt enviado ao chat Tese dizia o contrário e foi corrigido. Estrita: mediana 37,7% da receita livre e 22,2% da receita total.
- UFs com cobertura <60%: AC, AL, AP, BA, GO, MT, PB (7, sem DF); <50%: AC, AL, AP, MT, PB. O app usa n<40 ou cobertura <40% (exclui também RO e RR por n<40). Corte único a decidir.
- Os 3.891 são municípios calculados com receita tributária e PIB (mesmo conjunto).
- Pendentes da proposta: PIB defasado (usar média 2021–2023 fixa), margem em R$ por habitante por quintil de PIB, robustez com renda do Censo e sem economias concentradas, margem com e sem Fundeb, versão estrita por PIB.

## D65 · Readequação do aplicativo ao projeto de 66 páginas (2026-11-13)
- Nova tela **Hipóteses** (H1–H5): enunciado, tipo, o que 2023 sugere (valores recalculados), confirma/derruba (Quadro 7), o que falta; 2023 exploratório, 2024–2026 confirmatórios, regra 2 de 3 anos com cobertura ≥65%; limiares são propostas a fixar com o orientador.
- Tela **Comparativo** reescrita como Apêndice D (Tabelas 3–7 por quintil de PIB por habitante, tabela por UF com cobertura). Fonte: analises/tabelas_projeto_2023.py → catalogo/tabelas_projeto_2023.json.
- Tela antiga de base própria renomeada "Base própria: o efeito automático"; Ficha do município mostra PIB por habitante e faixa Q1–Q5; Início com a nova pergunta; Metodologia com card de regras e normas pendentes.
- Diferenças ≤0,4 ponto frente às Tabelas 5 e 7 do projeto decorrem do recálculo no repositório.
- Script: prototipo/build_readequacao_2023.py (rodar após build_comparativo_2023.py).

## D66 · Gráficos: comparar estados e municípios (2026-11-13)
- Aba Gráficos ganhou "Comparar estados" (ranking por indicador: margem ampla mediana, margem % receita total, vinculada, PIB por habitante, cobertura; UFs com cobertura insuficiente em cinza com asterisco) e "Comparar municípios" (régua com todos os municípios calculados da UF, mediana, e dois municípios A e B com posição na UF e PIB por habitante).
- Script: prototipo/build_graficos_comparar.py (rodar após build_readequacao_2023.py).

## D67 · Margem estrita publicada ao lado da ampla (2026-11-15)
- Pedido do usuário: o Atlas mostrava só a margem ampla nas telas de resultado. Passa a mostrar as duas (ampla e estrita, % da RCL): Início, Resultados 2023 (cartão, tabelas por UF e por porte, tabela de municípios), Ficha do município, Gráficos (indicador por UF e seletor "Medida nos municípios") e tabela por estado do Comparativo.
- Estrita em % da RCL = margem ampla % × (estrita R$ ÷ ampla R$), no mesmo denominador da ampla. Script: prototipo/build_estrita.py (rodar por último).
- Tabelas 3 a 7 do Comparativo seguem o Apêndice D do projeto (margem ampla como principal; estrita na Tabela 3).

## D68 · Patronal descontada na margem ampla; correções da auditoria; telas do site do programador (2026-11-18)
- Decisão do usuário (18/11/2026): a contribuição patronal paga com fonte livre (grupo 1, elemento 13) é descontada na margem ampla. Margem ampla = receita livre − mínimos − patronal − Legislativo − dívida − precatórios. Margem estrita = ampla − folha livre sem a patronal (numericamente igual à estrita anterior). Antes o texto dizia que a patronal era descontada, mas o código não descontava; agora código e texto conferem.
- Auditoria do programador (17/11/2026), três falhas confirmadas e corrigidas em app_coleta/: (1) paginação truncada: carrega() passa a detectar páginas faltantes ou hasMore e marca PAGINACAO_INCOMPLETA (município fica não calculado); coletar.py não grava a DCA de um município se alguma página falhou. (2) arquivos duplicados: carrega() usa só a versão mais recente de cada página. (3) patronal fora da ampla, acima.
- Validação no RN (167 municípios): mediana da margem ampla 35,5% → 33,9% da RCL; Caicó 35,2% → 33,4% (R$ 71,49 → 67,66 mi); estrita inalterada. Mediana da patronal ≈ 1,9% da receita livre.
- Reprodução a partir do repositório não é completa: faltam as 12 matrizes mensais MSCC (23 de 167 do RN diferem). Reprocessar com os brutos do computador do pesquisador: python analisar.py --pasta dados, depois a cadeia analises/ e prototipo/build_*.py.
- Os números do protótipo publicado ainda são anteriores a D68; o aplicativo exibe aviso fixo sobre isso.
- Telas novas (prototipo/build_site_novo.py, rodar por último): Mapa (malha municipal do IBGE, sete faixas, hachura para sem valor, zoom por UF, histograma, leitura por UF em dois níveis: fora da leitura e cobertura <60%), Correspondência (190 ações por classe e origem), busca de município por nome, linha da patronal na ficha. Mantidos: comparar dois municípios, ranking de estados, Tabelas 3 a 7.
- Universo: 5.570 entes do IBGE = 5.568 municípios + DF + Fernando de Noronha; o projeto exclui DF e FN do cálculo (a malha traz Noronha dentro de PE; o mapa a desenha sem valor).

## D69 · Alinhamento ao projeto recomposto (2026-11-19)
- Faixas de população passam a sete (até 5 mil; 5–10; 10–20; 20–50; 50–100; 100–500; mais de 500 mil), como na seção 3.2 da tese. Aplicadas ao aplicativo, aos relatórios e às análises que comparam "mesma UF e mesma faixa". Efeito medido nas Tabelas 3 a 7 (2023): só a Tabela 6 (art. 11 da LRF) muda, ≤0,3 ponto por quintil.
- Medida principal passa a ser a margem em % da receita total (rec_msc da MSC): mapa, histograma e ficha. Margem em % da RCL segue ao lado.
- PIB por habitante, média 2021–2023 (SIDRA 5938, variável 37, preços correntes, ÷ população do Censo 2022): arquivo catalogo/pib_media_2021_2023.csv. O valor de 2023 do SIDRA confere com pib_2023.csv nos 5.570 entes. 90,2% dos municípios ficam no mesmo quintil; 9,8% mudam um quintil; 0,05% mudam dois. Padrão continua pib_2023.csv (Apêndice D é 2023); para a série confirmatória use a variável de ambiente PIB_ARQ=pib_media_2021_2023.csv.
- Corrigido o rodar_tudo.bat: os scripts de analises/ precisam de argumentos (pasta do catálogo e arquivo de saída) e de transferencias_2023_por_acao.csv descompactado; a versão anterior os chamava sem argumentos e todos falhavam.
- Pendente (H4b e H4c): coletar classes 1 e 4 da MSC (IPTU lançado, dívida ativa, ISS, ITBI), valor adicionado dos serviços (SIDRA 5938), REGIC 2018 e renda domiciliar (Censo 2022).


## D70 · Coleta da H4b e da H4c (2026-11-19)
- `coletar.py --h4` (etapa `h4` do atlas.py) baixa da MSC patrimonial (MSCE, dezembro) a classe 4 do ano e as classes 1 do ano e do anterior.
- `analises/extrai_h4.py` gera `h4_2023.csv`: IPTU lançado (VPA 411210200), IPTU arrecadado (natureza 11125001), taxa de realização, dívida ativa tributária bruta (contas 121110*, PROVISÓRIO: confirmar no PCASP Estendido), dívida ativa recebida (11125003 + 11145113) e recuperação sobre o estoque do ano anterior.
- `analises/baixar_ibge_h4.py`: valor adicionado dos serviços (SIDRA 5938, var. 6575). Só 2021 está publicado; 2022 e 2023 ainda não. A lacuna de ano deve constar na tese.
- Pendentes manuais: REGIC 2018 (xlsx do IBGE) e renda domiciliar do Censo 2022. Sem eles, a H4c não roda.
- Teste em 3 municípios do RN: classes 1 e 4 coletadas; arrecadação e dívida ativa recebida dependem da MSCE já coletada (raw/.../msce) e ficaram zeradas só porque o teste não tinha essa pasta.

## D71 · Plano de trabalho revisado (2026-11-19)
- Frase central única; H2 (piso do magistério, diferenças em diferenças 2024–2026 com placebo saúde) como eixo causal.
- Regras travadas e seladas (modelo em `registro_regras_2024.md`) antes de abrir 2024; coleta bruta pode ser selada por hash sem análise.
- Viés de cobertura tratado como achado, com sensibilidade; validação com cinco municípios clientes e comparação SIOPE; sem contato com a CNM (retirado pelo autor no mesmo dia).
- H4b e H4c passam a exploratórias. Detalhe em `plano_tese.md`.

## D72 · ITBI no H4b (2026-11-19)
- O ITBI incide sobre o valor das vendas de imóveis, que o município não publica; não há base direta como o valor adicionado (ISS) e o valor lançado (IPTU).
- Base indireta, exploratória: ITBI por habitante contra IPTU por habitante (2023, receita realizada na MSC): ITBI de R$ 2,4 (Q1) a R$ 96,1 (Q5) e IPTU de R$ 3,4 a R$ 147,7; Spearman 0,69 em 3.396 municípios, mediana 0,44 em 19 UFs com 40 ou mais.
- Limite: os dois dependem da mesma cobrança; só o IPTU lançado separa base de esforço. `extrai_h4.py` passa a gravar `itbi_arrec` (natureza 111253).


## D73 · Tolerância MSC×DCA de 3% como regra (2026-11-20)
- Diagnóstico da cobertura de 2023 (74,0% com 1%): 71% dos não calculados reprovam na conferência MSC×DCA (receita 704, despesa liquidada 386); 147 sem natureza de receita; 114 fonte livre atípica; 103 RREO anexo 3 vazio; 70 RCL suspeita. A taxa de falha é 18% onde vale a MSCE de dezembro e 60% onde só fecha a soma das 12 matrizes mensais; AC 95%, PB 82%, AL 66%, AP 56%, MT 51%, BA 46% contra PI 5%, RN 8%. Não depende do porte (26% a 31% em todas as faixas).
- Metade das reprovações por receita está a menos de 3% da DCA; com 3%, 4.336 calculados (77,8%). Cerca de 140 divergem 100% ou mais e parecem erro de envio ao Siconfi.
- A recoleta dirigida já foi feita (4.037 para 4.121); o que resta não se corrige por coleta.
- Regra: tolerância de 3% (arquivo `resultado_2023_tol3.csv`), 1% como sensibilidade. Limites de Manski da margem ampla por quintil (pior caso): diferença Q5−Q1 observada 12,6 p.p. (base de 4.336), limites −1,5 a +20,4; o pior caso não exclui o zero e a tese declara a limitação.
