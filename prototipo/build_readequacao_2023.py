#!/usr/bin/env python3
"""Readequa o protótipo ao projeto de tese reconfigurado (66 páginas): tela Comparativo por quintil de PIB (Apêndice D),
tela Hipóteses H1–H5, Início, ficha com faixa de PIB, regras e normas pendentes na Metodologia.
Uso (da raiz): python prototipo/build_readequacao_2023.py   — rodar DEPOIS de build_real_2023.py e build_comparativo_2023.py. Idempotente."""
import re, json, pandas as pd, numpy as np
C = 'catalogo/'; H = 'prototipo/atlas_prototipo.html'
T = json.load(open(C+'tabelas_projeto_2023.json'))
b = pd.read_csv(C+'testes_tese_2023_base.csv', dtype={'cod_ibge': str}); b = b[b.calc == True]
p = pd.read_csv(C+'pib_2023.csv', dtype={'cod_ibge': str}); r = pd.read_csv(C+'resultado_2023.csv', dtype={'cod_ibge': str})
b = b.merge(p, on='cod_ibge'); b['pib_pc'] = b.pib_mil*1000/b['pop']; b = b[b.pib_pc > 0]
cuts = list(b.pib_pc.quantile([.2, .4, .6, .8]))
r = r.merge(p, on='cod_ibge', how='left'); r['pib_pc'] = r.pib_mil*1000/r['pop']
PIBQ = {x.cod_ibge: [int(round(x.pib_pc)), int(1+sum(x.pib_pc > c for c in cuts))] for x in r.itertuples() if x.pib_pc == x.pib_pc and x.pib_pc > 0}
DATA = dict(T=T, PIBQ=PIBQ)
JS = r'''
/*READ-START*/
const RD=__J__;
const QL=['Q1','Q2','Q3','Q4','Q5'];
const qrow=(lab,a,fmt)=>{const o={ind:lab};a.forEach((v,i)=>o[QL[i]]=fmt?fmt(v):v);return o};
const qcols=[['ind','Indicador'],...QL.map(q=>[q,q,1])];
const I0=v=>nf0.format(v);
function renderComp(){
  const el=$('#v-comp'),t=RD.T,t3=t.t3,fora=t.uf_fora.join(', ');
  el.innerHTML=`
  ${hd(4,'Capacidade e margem: tabelas do Apêndice D do projeto','Os municípios são divididos em cinco grupos (quintis) pelo PIB por habitante do IBGE, que não depende do que a prefeitura arrecada. Q1 é o grupo de menor PIB por habitante e Q5 o de maior. Todos os números são de 2023, que é ano exploratório: servem para formular as hipóteses, não as confirmam nem as derrubam. Valores são medianas.',`<p>Cada tabela é recalculada no repositório (analises/tabelas_projeto_2023.py) e corresponde a uma tabela do Apêndice D do projeto de tese. Margem na versão ampla, sem descontar a folha, salvo indicação.</p>`)}
  <div class="cards">
   <div class="card stat"><div class="n">${nf1.format(t3.m_rt[0])}% → ${nf1.format(t3.m_rt[4])}%</div><div class="l">margem de decisão, % da receita total, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">R$ ${I0(t3.m_pc[0])} → ${I0(t3.m_pc[4])}</div><div class="l">margem por habitante, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(t3.vinc[0])}% → ${nf1.format(t3.vinc[4])}%</div><div class="l">receita com destino fixado em lei, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(t.t6.Algum[0])}% → ${nf1.format(t.t6.Algum[4])}%</div><div class="l">abaixo do critério de arrecadação (art. 11 da LRF), Q1 → Q5</div></div>
  </div>
  <p class="lead">Em palavras simples: os municípios de menor riqueza por habitante têm margem menor em todas as três medidas, inclusive em reais por habitante. Ou seja, não é só receber mais dinheiro carimbado: sobra também menos dinheiro livre para escolher. A maior parte da diferença vem da receita que já chega com destino fixado, não da receita livre.</p>
  <h3>Tabela 3 · Margem e composição da receita por quintil de PIB por habitante</h3>
  ${tb([qrow('Municípios',t3.n,I0),qrow('PIB por habitante (R$)',t3.pib,I0),qrow('Receita total por habitante (R$)',t3.rec_pc,I0),qrow('Margem, % da receita total',t3.m_rt),qrow('Margem, % da receita livre',t3.m_rl),qrow('Margem, R$ por habitante',t3.m_pc,I0),qrow('Margem estrita (com a folha), % da receita total',t3.m_estrita_rt),qrow('Receita vinculada, % da receita total',t3.vinc),qrow('Mínimos de educação e saúde, % da receita livre',t3.minimos),qrow('Câmara Municipal, % da receita livre',t3.leg)],qcols)}
  <p class="muted">Margem sobre a receita total e parcela vinculada são quase a mesma informação (correlação ${nf2.format(t.h1.corr_vinc)}): contam como uma só evidência. Com controle pelo estado, cada vez que o PIB por habitante é multiplicado por cerca de 2,7, a margem sobe ${nf1.format(t.h1.rt[0])} ponto(s) da receita total (intervalo de 95%: ${nf1.format(t.h1.rt[1])} a ${nf1.format(t.h1.rt[2])}) e ${nf1.format(t.h1.rl[0])} da receita livre.</p>
  <h3>Tabela 4 · O mesmo, com quintis formados dentro de cada estado</h3>
  ${tb([qrow('Municípios',t.t4.n,I0),qrow('Margem, % da receita total',t.t4.m_rt),qrow('Margem, % da receita livre',t.t4.m_rl),qrow('Receita vinculada, % da receita total',t.t4.vinc)],qcols)}
  <p class="muted">Dentro do mesmo estado a diferença é menor, mas existe em toda parte. Cerca de um terço da variação da margem está entre estados. Estados fora desta leitura por cobertura insuficiente (menos de 40 municípios calculados ou cobertura abaixo de 40%): ${fora}.</p>
  <h3>Tabela 5 · Quanto do gasto é coberto por recursos federais vinculados (art. 167, § 7º)</h3>
  ${tb(Object.keys(t.t5).map(k=>qrow(k,t.t5[k])),[['ind','Área'],...QL.map(q=>[q,q,1])])}
  <p class="muted">Cobre parte maior do gasto onde a capacidade é menor. Na educação inclui o Fundeb e a complementação da União. Municípios nesta tabela: ${I0(t.n_jur)}. Não aparece encargo sem fonte nessas três áreas; o que aparece é a fonte chegando com mais destino fixado nos municípios de menor capacidade.</p>
  <h3>Tabela 6 · Municípios abaixo do critério relativo de arrecadação (art. 11 da LRF), % do grupo</h3>
  ${tb(Object.keys(t.t6).map(k=>qrow(k==='Algum'?'Algum dos três':k,t.t6[k])),[['ind','Imposto'],...QL.map(q=>[q,q,1])])}
  <p class="muted">Critério: arrecadação abaixo de 10% da mediana dos municípios do mesmo estado e da mesma faixa de população. Ficar abaixo do critério não equivale a descumprir o art. 11: mostra onde está a dificuldade de arrecadar. O texto integral da norma ainda será conferido na fonte oficial.</p>
  <h3>Tabela 7 · Exposição ao reajuste de 14,95% do piso do magistério (2023)</h3>
  ${tb([qrow('Pessoal da educação, % da receita livre',t.t7.pess_educ),qrow('Custo máximo do reajuste, % da receita livre',t.t7.custo),qrow('Margem consumida pelo reajuste, %',t.t7.consome),qrow('Margem antes, % da receita livre',t.t7.antes),qrow('Margem depois, % da receita livre',t.t7.depois),qrow('Pessoal da saúde, % da receita livre',t.t7.pess_saude)],qcols)}
  <p class="muted">É um teto, porque supõe que toda a folha da educação acompanha o piso. Correlação entre a margem consumida e o PIB por habitante: ${nf2.format(t.t7.rho)}. Descreve a exposição; o efeito no tempo só poderá ser medido com os anos seguintes.</p>
  <h3>Por estado</h3>
  <p class="muted">Cobertura é o percentual de municípios do estado com margem calculada. Estados marcados não devem ser comparados.</p>
  ${tb(COMP.uf.map(x=>({uf:x.uf,n:I0(x.n),cob:I0(x.cob),pib:x.pib,m_rt:x.m_rt,vinc:x.vinc,leitura:x.ok?'ok':'cobertura insuficiente'})),[['uf','UF'],['n','Calculados',1],['cob','Cobertura, %',1],['pib','PIB por hab. (R$)',1],['m_rt','Margem, % da receita total',1],['vinc','Vinculada, %',1],['leitura','Leitura']])}
  <p class="muted">Limites: associação, não causa; o PIB pode refletir uma única empresa grande; cerca de 28% dos municípios não foram calculados, sem sinal de viés nas características observáveis.</p>`;
}
const HIP=[
 {h:'H1',nome:'Capacidade e margem',tipo:'confirmatória',en:'Municípios de maior capacidade econômica têm margem de decisão maior, em percentual da receita total. A diferença vem sobretudo da parcela da receita que chega com destino fixado, não da receita livre.',
  sug:t=>`Margem de ${nf1.format(t.t3.m_rt[0])}% (Q1) a ${nf1.format(t.t3.m_rt[4])}% (Q5) da receita total, e de R$ ${I0(t.t3.m_pc[0])} a R$ ${I0(t.t3.m_pc[4])} por habitante. A diferença é de ${nf1.format(t.t3.m_rt[4]-t.t3.m_rt[0])} pontos na receita total e ${nf1.format(t.t3.m_rl[4]-t.t3.m_rl[0])} na livre.`,
  c:'Margem sobe com o PIB por habitante, com controle pelo estado (intervalo de 95% acima de zero); diferença de pelo menos 5 pontos da receita total entre os quintis extremos; diferença na receita livre menor que a metade da diferença na receita total.',d:'Intervalo inclui zero ou diferença abaixo de 5 pontos; a segunda parte cai se a diferença na receita livre for igual ou maior que a da receita total.',f:'Anos de 2024 a 2026 com regras registradas; robustez com a renda do Censo 2022.'},
 {h:'H2',nome:'O mesmo reajuste pesa mais em quem tem menos',tipo:'confirmatória, com desenho de causa',en:'O reajuste nacional do piso do magistério reduz mais a margem dos municípios em que a folha do magistério pesa mais na receita livre, e esses municípios se concentram na faixa de menor capacidade.',
  sug:t=>`O reajuste de 14,95% consome ${nf1.format(t.t7.consome[0])}% da margem em Q1 e ${nf1.format(t.t7.consome[4])}% em Q5 (cerca de ${nf1.format(t.t7.consome[0]/t.t7.consome[4])} vezes). A exposição de Q1 é ${nf1.format(t.t7.pess_educ[0]/t.t7.pess_educ[4])} vezes a de Q5. Isso descreve exposição, não efeito.`,
  c:'Margem cai mais nos mais expostos nos anos de reajuste maior (efeito negativo, intervalo abaixo de zero); exposição do quintil de menor capacidade pelo menos 1,5 vez a do maior; placebo (folha da saúde) sem efeito.',d:'Efeito zero ou positivo, ou placebo com efeito do mesmo tamanho.',f:'Painel de 2023 a 2026 com os percentuais oficiais de reajuste e o teste de controle.'},
 {h:'H3',nome:'A diferença existe dentro do mesmo estado',tipo:'confirmatória',en:'A relação entre capacidade e margem não é só diferença entre estados: aparece entre municípios do mesmo estado e da mesma faixa de população.',
  sug:t=>`Relação positiva em 20 de 20 estados com dados suficientes (correlação mediana 0,21); positiva em 19 de 20 no modelo de dois níveis; o terço mais rico tem margem maior em 87% dos 87 grupos de mesmo estado e porte (diferença mediana de 3,4 pontos). Cerca de 33% da variação está entre estados. Dentro do estado, Q1→Q5: ${nf1.format(t.t4.m_rt[0])}% → ${nf1.format(t.t4.m_rt[4])}%.`,
  c:'Relação positiva dentro do estado em pelo menos 3/4 dos estados com cobertura suficiente; inclinação média positiva no modelo de dois níveis; terço mais rico com margem maior em pelo menos 2/3 dos pares.',d:'Correlação mediana dentro do estado igual ou menor que zero, ou relação positiva em menos da metade dos estados.',f:'Anos confirmatórios.'},
 {h:'H4',nome:'Arrecadação própria e art. 11 da LRF',tipo:'descritiva, confirmatória',en:'Uma parte relevante dos municípios fica abaixo de um critério objetivo de arrecadação dos impostos próprios, e eles se concentram na faixa de menor capacidade.',
  sug:t=>`${nf1.format(t.t6.Algum[0])}% dos municípios de Q1 ficam abaixo do critério contra ${nf1.format(t.t6.Algum[4])}% em Q5 (cerca de ${nf1.format(t.t6.Algum[0]/t.t6.Algum[4])} vezes). A dificuldade está no IPTU e no ITBI, quase nunca no ISS.`,
  c:'Pelo menos 10% dos municípios abaixo do critério relativo e proporção em Q1 pelo menos 3 vezes a de Q5.',d:'Proporção total abaixo de 10% ou razão entre os extremos abaixo de 1,5.',f:'Anos confirmatórios; conferência do texto integral do art. 11.'},
 {h:'H5',nome:'Consequência jurídica',tipo:'tese a demonstrar, por análise jurídica',en:'O art. 167, § 7º, lido com a ADI 7.222, a autonomia municipal, o dever de reduzir desigualdades e a divisão equilibrada do FPM: (a) vale para encargos criados por lei nacional depois de 2022; (b) exige fonte suficiente em cada grupo de municípios, não só na média; (c) torna relevante a forma do financiamento; (d) pode ser cobrado no Judiciário.',
  sug:t=>`Não aparece encargo sem fonte no agregado de saúde, educação e assistência: a cobertura federal é maior onde a capacidade é menor (saúde ${nf1.format(t.t5['Saúde'][0])}% em Q1 contra ${nf1.format(t.t5['Saúde'][4])}% em Q5). O que aparece é a fonte chegando com mais destino fixado, o que sustenta o item (c).`,
  c:'O texto, a história da EC 128/2022 e a ADI 7.222 sustentam os itens a a d, e os dados mostram municípios em que a fonte não cobre o encargo ou chega toda vinculada.',d:'O texto ou o STF limitam o § 7º ao agregado, ou os dados mostram fonte proporcional à necessidade e sem destino fixado.',f:'Análise jurídica; exame por encargo posterior a 2022; conferência das normas pendentes.'}];
function renderHip(){
  const el=$('#v-hip'),t=RD.T;
  el.innerHTML=`
  ${hd(4,'Hipóteses da tese','As cinco hipóteses do projeto, o que cada uma afirma, o que 2023 sugere e o que falta para a prova. 2023 é ano exploratório: os resultados abaixo não confirmam nem derrubam nenhuma hipótese.',`<p>Regras do projeto (seção 3.8): uma hipótese é confirmada se passar no critério em pelo menos dois dos três anos confirmatórios (2024 a 2026), com cobertura de pelo menos 65% dos municípios no ano. Os limiares são propostas a fixar com o orientador e a registrar, com data, antes de abrir 2024.</p>`)}
  <div class="cards">
   <div class="card stat"><div class="n">2023</div><div class="l">exploratório: formula as hipóteses</div></div>
   <div class="card stat"><div class="n">2024 a 2026</div><div class="l">confirmatórios, aguardando registro prévio das regras</div></div>
   <div class="card stat"><div class="n">2 em 3</div><div class="l">anos em que o critério deve ser cumprido, com cobertura ≥ 65%</div></div>
  </div>
  ${HIP.map(x=>`<div class="card" style="margin-block:12px"><h3>${x.h} · ${x.nome}</h3><p class="muted">${x.tipo} · situação: <b>exploratório 2023, aguardando 2024</b></p>
   <p>${x.en}</p><p><b>O que 2023 sugere:</b> ${x.sug(t)}</p>
   <p><b>Confirma se:</b> ${x.c}</p><p><b>Derruba se:</b> ${x.d}</p><p class="muted"><b>Falta:</b> ${x.f}</p></div>`).join('')}
  <p class="muted">Cuidados: o PIB por habitante é a medida de capacidade (não a arrecadação, que já compõe a receita livre); resultados são associação, não causa, exceto o desenho da H2; normas pendentes de conferência no texto oficial aparecem na Metodologia.</p>`;
}
/*READ-END*/
'''.replace('__J__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
h = open(H, encoding='utf8').read()
# renderComp antigo (bloco COMP) perde a função; mantém COMP (dados por UF)
h = re.sub(r'function renderComp\(\)\{.*?\n\}\n/\*COMP-END\*/', '/*COMP-END*/', h, flags=re.S)
h = re.sub(r'\n/\*READ-START\*/.*?/\*READ-END\*/\n', '\n', h, flags=re.S)
m = '/* ---------- Roteamento e eventos ---------- */'; assert m in h
h = h.replace(m, JS+'\n'+m, 1)
if 'id="v-hip"' not in h: h = h.replace('<section class="view" id="v-comp" hidden></section>', '<section class="view" id="v-comp" hidden></section>\n  <section class="view" id="v-hip" hidden></section>', 1)
h = re.sub(r"resultados:\[[^\]]*\]", "resultados:['piloto','hip','comp','tese','validacao']", h, count=1)
if 'hip:renderHip' not in h: h = h.replace('comp:renderComp,', 'comp:renderComp,hip:renderHip,', 1)
# Início
old = 'Quanto sobra do orçamento de cada município para ele decidir, depois das obrigações fixadas em norma nacional.'
new = 'Quando a obrigação é a mesma e a capacidade econômica é desigual, quanto espaço real de escolha resta a cada município? O Atlas mede a margem de decisão: o que sobra do orçamento para o município decidir, depois das obrigações fixadas em norma nacional.'
if old in h: h = h.replace(old, new, 1)
# Testes da tese (base própria) vira demonstração do efeito automático
h = h.replace("hd(4,'Testes da tese, 2023','Respostas da pesquisa com os dados reais de 2023 (municípios com margem calculada). Medianas por quintil de receita tributária própria por habitante: Q1 é a base menor.", "hd(4,'Base própria: o efeito automático (2023)','Atenção: neste quadro os grupos são formados pela arrecadação própria, que já faz parte da receita livre; por isso parte da relação com a margem é automática. A medida de capacidade da tese é o PIB por habitante (aba Comparativo). Medianas por quintil de receita tributária própria por habitante: Q1 é a base menor.", 1) if False else h
h = re.sub(r"hd\(4,'Testes da tese, 2023','Respostas da pesquisa", "hd(4,'Base própria: o efeito automático (2023)','Atenção: aqui os grupos são formados pela arrecadação própria, que já compõe a receita livre; parte da relação com a margem é automática. A medida de capacidade da tese é o PIB por habitante (Comparativo). Respostas da pesquisa", h, count=1)
# Ficha: faixa de PIB
anch = '<div class="l">margem ampla, % da RCL</div></div>\n  </div>\n  <h3>Cálculo (R$)</h3>'
if 'faixa de PIB por habitante' not in h and anch in h:
    h = h.replace(anch, '<div class="l">margem ampla, % da RCL</div></div>\n   <div class="card stat"><div class="n">${(RD.PIBQ[m.c]||[null])[0]==null?\'—\':\'R$ \'+nf0.format(RD.PIBQ[m.c][0])}</div><div class="l">PIB por habitante (IBGE, 2023)${RD.PIBQ[m.c]?\' · faixa Q\'+RD.PIBQ[m.c][1]+\' de 5 (Q1 = menor)\':\'\'}</div></div>\n  </div>\n  <h3>Cálculo (R$)</h3>', 1)
# Metodologia: card 7
card7 = '''<div class="card"><h3>7 · Regras das hipóteses e normas pendentes</h3>
    <ul><li>2023 é exploratório; 2024 a 2026 são confirmatórios, com regras registradas antes de abrir os dados.</li><li>Hipótese confirmada se passar no critério em 2 de 3 anos, com cobertura de pelo menos 65% dos municípios.</li><li>Limiares do Quadro 7 do projeto são propostas a fixar com o orientador.</li><li>Capacidade: PIB por habitante (média 2021–2023 na série confirmatória). Robustez: renda do Censo 2022, margem estrita, tolerância de 3%.</li></ul>
    <p><b>Normas ainda sem texto oficial conferido:</b> LRF art. 11 (texto integral), Lei 11.738/2008, Lei 14.113/2020, lei do crédito do piso da enfermagem (14.518 ou 14.581/2023), portaria do Ministério da Saúde (597 ou 1.135), Tema 1181 do STF, resoluções da ANEEL, portarias anuais do MEC com o reajuste do piso.</p></div>
   '''
if '7 · Regras das hipóteses' not in h:
    a = "conclusoes_2023.md.</p></div>\n  </div>`;"
    if a in h: h = h.replace(a, "conclusoes_2023.md.</p></div>\n   "+card7+"</div>`;", 1)
    else: print('AVISO: âncora da Metodologia não encontrada')
open(H, 'w', encoding='utf8').write(h); print('ok', len(h), 'Hipóteses' in h, '7 · Regras' in h, 'faixa de PIB' in h, 'efeito automático' in h)
