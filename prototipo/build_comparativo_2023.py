#!/usr/bin/env python3
"""Insere no protótipo a tela Comparativo (PIB por habitante, UFs, cobertura) e os textos em linguagem simples.
Uso (da raiz): python prototipo/build_comparativo_2023.py   — rodar DEPOIS de build_real_2023.py. Idempotente."""
import re, json, pandas as pd, numpy as np
from scipy import stats
C = 'catalogo/'; H = 'prototipo/atlas_prototipo.html'
r = pd.read_csv(C+'resultado_2023.csv', dtype={'cod_ibge': str})
b = pd.read_csv(C+'testes_tese_2023_base.csv', dtype={'cod_ibge': str}); b = b[b.calc == True].copy()
p = pd.read_csv(C+'pib_2023.csv', dtype={'cod_ibge': str}); b = b.merge(p, on='cod_ibge', how='left'); b['pib_pc'] = b.pib_mil*1000/b['pop']; b = b[b.pib_pc > 0]
j = pd.read_csv(C+'juridico_base_2023.csv', dtype={'cod_ibge': str}).fillna(0)
b['q'] = pd.qcut(b.pib_pc, 5, labels=['Q1 (menor)', 'Q2', 'Q3', 'Q4', 'Q5 (maior)'])
g = b.groupby('q', observed=True).agg(n=('uf', 'size'), pib=('pib_pc', 'median'), m_rt=('p_mt', 'median'), m_rl=('p_m', 'median'), vinc=('vinc', 'median')).round(1)
e = b.merge(j[['cod_ibge', 'n_iptu', 'n_iss', 'n_itbi']], on='cod_ibge'); e['fx'] = pd.cut(e['pop'], [0, 5000, 10000, 20000, 50000, 1e9], labels=False)
for k in ('iptu', 'iss', 'itbi'):
    e[k] = e[f'n_{k}']/e['pop']; med = e.groupby(['uf', 'fx'])[k].transform('median'); e[k+'_r'] = (e[k] < .1*med) & (med > 0)
e['alg'] = e.iptu_r | e.iss_r | e.itbi_r; a11 = e.groupby('q', observed=True).alg.mean().mul(100).round(1)
tot = r.groupby('uf').size(); cal = b.groupby('uf').size()
u = b.groupby('uf').agg(n=('uf', 'size'), pib=('pib_pc', 'median'), m_rt=('p_mt', 'median'), vinc=('vinc', 'median')).round(1)
u['tot'] = tot; u['cob'] = (u.n/u.tot*100).round(0); u = u.sort_values('m_rt')
DATA = dict(q=[dict(q=i, **row.to_dict(), a11=float(a11[i])) for i, row in g.iterrows()],
            uf=[dict(uf=i, ok=bool(x.n >= 40 and x.cob >= 40), **{k: (float(x[k]) if k != 'n' else int(x[k])) for k in ('n', 'pib', 'm_rt', 'vinc', 'tot', 'cob')}) for i, x in u.iterrows()])
JS = r'''
/*COMP-START*/
const COMP=__J__;
function renderComp(){
  const el=$('#v-comp'),Q=COMP.q,q1=Q[0],q5=Q[4],ok=COMP.uf.filter(x=>x.ok),fora=COMP.uf.filter(x=>!x.ok).map(x=>x.uf).join(', ');
  el.innerHTML=`
  ${hd(4,'Comparativo: municípios ricos e pobres, estados e cobertura','Aqui os municípios são divididos pelo PIB por habitante (IBGE, 2023), que não depende do que o município arrecada. Q1 é o grupo de menor PIB por habitante e Q5 o de maior. São números exploratórios de 2023: mostram associação, não causa.')}
  <div class="cards">
   <div class="card stat"><div class="n">${nf1.format(q1.m_rt)}% → ${nf1.format(q5.m_rt)}%</div><div class="l">margem de decisão sobre a receita total, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(q1.vinc)}% → ${nf1.format(q5.vinc)}%</div><div class="l">parte da receita com destino obrigatório, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(q1.a11)}% → ${nf1.format(q5.a11)}%</div><div class="l">com arrecadação própria muito baixa (art. 11 da LRF), Q1 → Q5</div></div>
  </div>
  <p class="lead">Em palavras simples: nos municípios de menor riqueza por habitante, mais dinheiro já chega com destino definido por lei, e sobra menos para o prefeito decidir. A diferença aparece também entre municípios do mesmo estado, em todos os 20 estados com dados suficientes.</p>
  <h3>Por faixa de PIB por habitante (medianas)</h3>
  ${tb(Q.map(x=>({q:x.q,n:x.n,pib:x.pib,m_rt:x.m_rt,m_rl:x.m_rl,vinc:x.vinc,a11:x.a11})),[['q','Faixa'],['n','Municípios',1],['pib','PIB por hab. (R$)',1],['m_rt','Margem, % da receita total',1],['m_rl','Margem, % da receita livre',1],['vinc','Receita vinculada, %',1],['a11','Abaixo do critério do art. 11, %',1]])}
  <h3>Por estado</h3>
  <p class="muted">A cobertura é o percentual de municípios do estado para os quais a margem pôde ser calculada. Estados com menos de 40 municípios calculados ou cobertura abaixo de 40% (${fora}) ficam marcados e não devem ser comparados.</p>
  ${tb(COMP.uf.map(x=>({uf:x.uf,n:x.n,cob:x.cob,pib:x.pib,m_rt:x.m_rt,vinc:x.vinc,leitura:x.ok?'ok':'cobertura insuficiente'})),[['uf','UF'],['n','Calculados',1],['cob','Cobertura, %',1],['pib','PIB por hab. (R$)',1],['m_rt','Margem, % da receita total',1],['vinc','Vinculada, %',1],['leitura','Leitura']])}
  <p class="muted">Cuidados: o PIB pode refletir uma única empresa grande; a cobertura é de cerca de 70% dos municípios; os números de 2023 não confirmam nem refutam hipótese alguma (a confirmação virá com 2024 a 2027). Detalhes em catalogo/base_independente_2023.md e comparativo_2023.md.</p>`;
}
/*COMP-END*/
'''.replace('__J__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
SIMPLES = '''<div class="card" style="grid-column:1/-1"><h3>Em palavras simples</h3>
    <p><b>Pergunta:</b> a lei federal cria as mesmas despesas obrigatórias para todos os municípios, mas cada um arrecada um valor diferente. Quanto sobra para o prefeito decidir?</p>
    <p><b>Margem de decisão:</b> é o que sobra do orçamento depois das obrigações (saúde, educação, salários, dívida, precatórios).</p>
    <p><b>Como lemos:</b> dividimos os municípios em cinco faixas de riqueza (PIB por habitante, do IBGE), comparamos faixas dentro do mesmo estado e sempre mostramos quantos municípios entraram no cálculo (cobertura).</p>
    <p><b>Limite:</b> os dados de 2023 mostram associação, não causa. Quintil = uma das cinco faixas iguais; receita vinculada = dinheiro com destino fixado em lei; cobertura = percentual de municípios calculados.</p></div>
   '''
h = open(H, encoding='utf8').read()
h = re.sub(r'\n/\*COMP-START\*/.*?/\*COMP-END\*/\n', '\n', h, flags=re.S)
m = '/* ---------- Roteamento e eventos ---------- */'; assert m in h
h = h.replace(m, JS+'\n'+m, 1)
if 'id="v-comp"' not in h: h = h.replace('<section class="view" id="v-tese" hidden></section>', '<section class="view" id="v-tese" hidden></section>\n  <section class="view" id="v-comp" hidden></section>', 1)
if "'tese','comp'" not in h: h = h.replace("resultados:['piloto','tese',", "resultados:['piloto','tese','comp',", 1)
if 'comp:renderComp' not in h: h = h.replace('tese:renderTese,', 'tese:renderTese,comp:renderComp,', 1)
if 'Em palavras simples' not in h: h = h.replace('<div class="mcols">\n   <div class="card"><h3>1 · Cálculos</h3>', '<div class="mcols">\n   '+SIMPLES+'<div class="card"><h3>1 · Cálculos</h3>', 1)
open(H, 'w', encoding='utf8').write(h); print('ok', len(h), 'palavras simples' , 'Em palavras simples' in h, "'tese','comp'" in h, 'comp:renderComp' in h)
