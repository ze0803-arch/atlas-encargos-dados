# Prompt para o chat "Tese" — reconfiguração do projeto

Cole o texto abaixo na conversa do chat Tese.

---

Preciso reconfigurar o projeto da minha tese de doutorado em Direito (UniCuritiba) a partir de resultados empíricos do "Atlas de Encargos", ferramenta que construí para medir a margem de decisão orçamentária dos 5.570 municípios brasileiros. Peço que você (1) leia todo o contexto, (2) aponte inconsistências com o que já está no projeto e (3) proponha a nova redação do problema, das hipóteses, dos objetivos, da metodologia e do capítulo empírico. Use linguagem simples: o texto será lido por mim e pelo orientador, que não é da área de dados. Explique qualquer termo técnico na primeira vez que aparecer.

## 1. Tema e pergunta reformulada
Encargos impostos por lei federal são uniformes em todo o país, mas as bases fiscais municipais são muito desiguais. Pergunta: quando a obrigação é a mesma e a capacidade própria de pagar é desigual, quanto espaço real de escolha (margem de decisão) resta ao município, e que consequências jurídicas isso tem? Eixos jurídicos: art. 167, §7º da CF (EC 128/2022: vedação de impor encargo sem indicar a fonte; ressalvas para obrigações espontaneamente assumidas e piso do salário mínimo), ADI 7222 (obrigação limitada aos recursos repassados pela União), art. 11 da LRF (arrecadação dos tributos próprios como requisito para transferências voluntárias, parágrafo único). Termos que uso: "espaço real de escolha" e "margem de decisão".

## 2. Método (resumo)
Margem = receita livre (fontes 1500/1501) menos mínimos constitucionais (25% educação, 15% saúde), Legislativo, dívida, precatórios e folha livre; dados Siconfi (MSC, DCA, RREO, RGF) e Siops; conferência MSC x DCA com tolerância de 1% (sensibilidade 3%); exclusão de receita incompatível (> R$ 40 mil/hab.). Série pretendida 2023–2027; 2023 é exploratório e 2024–2027 serão confirmatórios. Três cuidados que quero preservar: (a) usar medida de capacidade independente da arrecadação própria (PIB por habitante do IBGE), porque a base própria já compõe a receita livre e gera efeito mecânico; (b) comparar dentro da UF e em modelo de dois níveis, para não confundir efeito do município com efeito do estado; (c) mostrar sempre a cobertura junto de cada resultado.

## 3. Resultados de 2023 (exploratórios)
- Cobertura: margem calculada para 72,5% dos municípios (3.891 com PIB); teste de viés de cobertura não achou diferença nas características observáveis. Baixa cobertura: PB 17%, AC 5%, AL 33%, AP 44%; essas UFs ficam fora das leituras por UF.
- Quintis de PIB por habitante, do menor ao maior: margem sobre a receita total 24,4% → 38,3% (+13,9 pontos); sobre a receita livre 52,1% → 56,7% (+4,6); parcela vinculada 52,8% → 32,2%.
- Com efeitos fixos de UF e erro agrupado por UF: +4,2 pontos de margem (receita total) por unidade de log do PIB per capita (IC95% 3,6–4,8). Positivo em 20 de 20 UFs com dados suficientes (Spearman mediano dentro da UF 0,21); inclinação positiva em 19 de 20 no modelo de dois níveis.
- 33% da variação da margem está entre UFs; pares de mesma UF e porte: terço mais rico tem +3,4 pontos, em 87% dos 87 grupos.
- Base própria por habitante: Q1→Q5 = 26,3% → 37,6% da receita total; 52,7% → 56,8% da receita livre; margem sobre receita total é quase identidade com (100 − parcela vinculada), correlação 0,96, o que mostra que a desigualdade aparece sobretudo na parcela vinculada.
- Art. 11 (critério relativo, abaixo de 10% da mediana da UF e faixa de porte em IPTU/ISS/ITBI): 25,3% dos municípios do quintil mais pobre contra 3,6% do mais rico.
- Advertências: associação, não causa; PIB pode refletir uma empresa grande ou ISS; resultados de 2023 não confirmam hipótese alguma.

## 4. Hipóteses H1–H5 (versão atual, a rediscutir)
H1: maior capacidade própria (medida independente) associa-se a maior margem. H2: choques de piso uniforme (ex.: reajuste do piso do magistério, 14,95% em 2023) comprimem mais a margem dos municípios de menor capacidade. H3: a desigualdade de margem persiste dentro da UF. H4: parte relevante dos municípios fica abaixo de critério objetivo de arrecadação do art. 11, concentrados na faixa de menor capacidade. H5: a obrigação uniforme, sem indicação de fonte proporcional à capacidade, produz efeito jurídico relevante sob o art. 167, §7º. Cada uma precisa de critério de refutação com limiares a fixar com o orientador ANTES de olhar 2024. Delineamento causal proposto: exposição (peso da folha de magistério) × reajuste uniforme do piso, em painel 2023–2027.

## 5. Normas
Confirmadas em fontes oficiais: EC 128/2022; ADI 7222; LRF art. 11 parágrafo único (tema). Ainda sem texto oficial verificado: art. 11 integral, Lei 11.738/2008, Lei 14.113/2020, número da lei de crédito de 2023 (fontes divergem: 14.518 x 14.581), Portaria GM/MS (597 x 1.135), Tema 1181, ANEEL. Não afirme nada sobre esses itens sem indicar que estão pendentes.

## 6. O que quero de você
1. Diga o que muda no problema de pesquisa, nos objetivos geral e específicos, na justificativa e na originalidade.
2. Reescreva as hipóteses com critérios de refutação, marcando o que é exploratório e o que é confirmatório.
3. Proponha estrutura de capítulos (jurídico e empírico) e como cada resultado entra.
4. Liste riscos e objeções prováveis da banca (medida de capacidade, causalidade, cobertura, circularidade, escolha de limiares).
5. Aponte decisões que preciso tomar com o orientador.
6. Entregue tudo em português claro, sem jargão, com glossário no fim.

Repositório com dados e scripts: github.com/ze0803-arch/atlas-encargos-dados (catalogo/decisoes.md, D55–D62; catalogo/base_independente_2023.md; catalogo/comparativo_2023.md).
