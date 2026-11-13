#!/usr/bin/env python3
"""Insere no protótipo a tela 'Testes da tese 2023' e os Gráficos reais, a partir dos .md de catalogo/.
Uso (da raiz do repositório): python prototipo/build_tese_2023.py"""
import re, json
C = 'catalogo/'; H = 'prototipo/atlas_prototipo.html'

def tabelas(arq):
    """Devolve lista de (titulo, linhas) para cada tabela markdown do arquivo."""
    out, tit, cur = [], '', None
    for l in open(C + arq + '.md', encoding='utf8').read().split('\n'):
        if l.startswith('#'): tit = l.lstrip('# ').strip()
        if l.startswith('|'):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if cur is None: cur = {'t': tit, 'h': c, 'r': []}
            elif not set(''.join(c)) <= set(':- '): cur['r'].append(c)
        elif cur is not None: out.append(cur); cur = None
    if cur: out.append(cur)
    return out

def num(x):
    try: return round(float(x), 2)
    except ValueError: return x

def rows(t):
    h = [x or 'k' for x in t['h']]
    return [{h[i]: num(v) for i, v in enumerate(r)} for r in t['r']]

tt, tj, cp, rb, vc = tabelas('testes_tese_2023'), tabelas('testes_juridicos_2023'), tabelas('choque_pisos_2023'), tabelas('robustez_2023'), tabelas('vies_cobertura_2023')
a1 = rows(tj[0]); areas = []
for ar in dict.fromkeys(r['area'] for r in a1):
    s = [r for r in a1 if r['area'] == ar]
    areas.append(dict(area=ar, fed=[r['federal_vinculada_pct'] for r in s], livre=[r['fonte_livre_pct'] for r in s]))
TESE = dict(
    quint=rows(tt[0]), porte=rows(tt[1]), a1=areas, a1b=rows(tj[2]), a3=rows(tj[3]),
    b1=rows(tj[5]), pisos=rows(cp[0]), pisos_dep=rows(cp[1]),
    rob=rows(rb[0]), uf=rows(rb[1]), art11=rows(rb[2]),
    cobfx=rows(vc[1]), cobq=rows(vc[3]), ipw=rows(vc[5]), comp=rows(vc[2]))
J = json.dumps(TESE, ensure_ascii=False, separators=(',', ':'))

JS = r'''
/*TESE-START*/
const TESE=__J__;
const tb=(rows,cols)=>`<div class="tablewrap"><table class="data"><thead><tr>${cols.map(c=>`<th${c[2]?' class="num"':''}>${c[1]}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${cols.map(c=>`<td${c[2]?' class="num"':''}>${typeof r[c[0]]==='number'?nf1.format(r[c[0]]):esc(r[c[0]]??'')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
function renderTese(){
  const el=$('#v-tese'),Q=TESE.quint,q1=Q[0],q5=Q[4];
  el.innerHTML=`
  ${hd(4,'Testes da tese, 2023','Respostas da pesquisa com os dados reais de 2023 (municípios com margem calculada). Medianas por quintil de receita tributária própria por habitante: Q1 é a base menor. Os arquivos completos estão em catalogo/.',`<p>Cada teste está descrito na Seção metodológica e nas decisões D53 a D58. Os resultados valem para os municípios calculados; a análise de cobertura mostra que não há viés nas variáveis observadas.</p>`)}
  <div class="cards">
   <div class="card stat"><div class="n">${nf1.format(q1.margem_rec_total)}% → ${nf1.format(q5.margem_rec_total)}%</div><div class="l">margem sobre a receita total, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(q1.vinculada)}% → ${nf1.format(q5.vinculada)}%</div><div class="l">receita vinculada fora da livre, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(TESE.art11[0].algum_rel)}% → ${nf1.format(TESE.art11[4].algum_rel)}%</div><div class="l">com imposto abaixo do critério do art. 11 da LRF, Q1 → Q5</div></div>
   <div class="card stat"><div class="n">${nf1.format(TESE.pisos[0].margem_consumida_pct)}% → ${nf1.format(TESE.pisos[4].margem_consumida_pct)}%</div><div class="l">margem consumida por um reajuste de 14,95% do magistério (teto), Q1 → Q5</div></div>
  </div>
  <h3>Pergunta central: espaço de decisão por quintil de base própria</h3>
  ${tb(Q,[['q','Quintil'],['n','Municípios',1],['trib_pc','Base própria (R$/hab.)',1],['margem_pct','Margem, % receita livre',1],['margem_rec_total','Margem, % receita total',1],['vinculada','Vinculada, % receita total',1],['margem_pc','Margem (R$/hab.)',1]])}
  <h3>Mesma pergunta, dentro de cada UF</h3>
  ${tb(TESE.uf,[['qu','Quintil na UF',1],['n','Municípios',1],['margem_pct_rec_livre','Margem, % receita livre',1],['margem_pct_rec_total','Margem, % receita total',1],['vinculada','Vinculada, % receita total',1]])}
  <p class="muted">Dentro da mesma UF a diferença é pequena (rho = 0,069): parte relevante da assimetria está entre UFs e faixas de porte.</p>
  <h3>Robustez</h3>
  ${tb(TESE.rob,[['desfecho','Desfecho'],['amostra','Amostra'],['n','n',1],['rho','rho',1],['coef','Coeficiente',1],['p','p',1],['r2','R²',1]])}
  <h3>Art. 167, § 7º da CF: parte federal vinculada da despesa, por quintil (% da despesa da função)</h3>
  ${tb(TESE.a1.map(a=>({area:a.area,q1:a.fed[0],q2:a.fed[1],q3:a.fed[2],q4:a.fed[3],q5:a.fed[4]})),[['area','Função'],['q1','Q1',1],['q2','Q2',1],['q3','Q3',1],['q4','Q4',1],['q5','Q5',1]])}
  <p class="muted">Onde a base é menor, a transferência federal paga mais da despesa. A parte paga com fonte livre é quase só o mínimo constitucional (excedente mediano zero). O teste só vê o lado federal.</p>
  <h3>Art. 11 da LRF: arrecadação abaixo de 10% da mediana da mesma UF e faixa de porte (% do grupo)</h3>
  ${tb(TESE.art11,[['q','Quintil'],['iptu_rel','IPTU',1],['iss_rel','ISS',1],['itbi_rel','ITBI',1],['algum_rel','Algum',1]])}
  <h3>Pisos: choque uniforme de 14,95% sobre a despesa de pessoal da educação (teto de exposição)</h3>
  ${tb(TESE.pisos,[['q','Quintil'],['n','Municípios',1],['custo_max_pct_rec_livre','Custo máx., % rec. livre',1],['custo_max_pct_rec_total','Custo máx., % rec. total',1],['margem_consumida_pct','Margem consumida, %',1]])}
  <p class="muted">Sem a RAIS não se mede o custo efetivo: é o teto, porque só parte da folha está abaixo do piso.</p>
  <h3>Cobertura: quem ficou fora do cálculo</h3>
  ${tb(TESE.cobq,[['q','Quintil'],['n','Municípios',1],['cobertura_pct','Calculados, %',1]])}
  ${tb(TESE.ipw,[['desfecho','Desfecho'],['n','n',1],['coef_sem_peso','Coef. sem peso',1],['coef_ponderado','Coef. ponderado',1],['p_ponderado','p']])}
  <p class="note">A cobertura não depende do porte nem da base própria, e o resultado ponderado pela probabilidade de cobertura é igual ao original. Viés em variáveis não observadas não se descarta.</p>`;
}
function renderGraficos(){
  const el=$('#v-graficos'),Q=TESE.quint,P=PILOTO,calc=P.filter(r=>r.st==='calc');
  const cont={};P.filter(r=>r.st!=='calc').forEach(r=>r.fl.forEach(x=>cont[x]=(cont[x]||0)+1));
  const alert=Object.entries(cont).sort((a,b)=>b[1]-a[1]).slice(0,8).map(([k,v])=>({l:FLAGTXT[k]||k,v}));
  const ufs=[...new Set(P.map(r=>r.uf))].sort().map(u=>{const a=P.filter(r=>r.uf===u);return {l:u,v:Math.round(100*a.filter(r=>r.st==='calc').length/a.length)}});
  el.innerHTML=`
  <div class="vh"><h2>Gráficos: o quadro geral de 2023</h2></div>
  <p class="lead">Dados reais de 2023, municípios com margem calculada. Cada desenho responde a uma parte da pergunta da tese.</p>
  <div class="chartgrid">
   <div class="card chartcard"><h3>Quanto sobra para decidir, por base própria</h3>${svgBars(Q.map(r=>({l:r.q,v:r.margem_rec_total})))}<p>Mediana da margem sobre a receita total, por quintil de receita tributária própria por habitante.</p></div>
   <div class="card chartcard"><h3>Receita vinculada, por base própria</h3>${svgBars(Q.map(r=>({l:r.q,v:r.vinculada})))}<p>Parte da receita total que vem vinculada fora da receita livre. É dela que vem a diferença entre os quintis.</p></div>
   <div class="card chartcard"><h3>Quanto sobra para decidir, por porte</h3>${svgBars(TESE.porte.map(r=>({l:r.fx,v:r.margem_rec_total})))}<p>Mediana da margem sobre a receita total por faixa de população.</p></div>
   <div class="card chartcard"><h3>Art. 11 da LRF, por base própria</h3>${svgBars(TESE.art11.map(r=>({l:r.q,v:r.algum_rel})))}<p>% dos municípios com IPTU, ISS ou ITBI abaixo de 10% da mediana da mesma UF e faixa de porte.</p></div>
   <div class="card chartcard"><h3>Margem consumida pelo reajuste do piso</h3>${svgBars(TESE.pisos.map(r=>({l:r.q,v:r.margem_consumida_pct})))}<p>Teto: reajuste de 14,95% sobre a despesa de pessoal da educação, em % da margem.</p></div>
   <div class="card chartcard"><h3>Cobertura por UF (% calculados)</h3>${svgBars(ufs)}<p>Municípios com margem calculada em cada UF.</p></div>
   <div class="card chartcard"><h3>Por que não foram calculados</h3>${svgBars(alert)}<p>Municípios por tipo de alerta; um município pode ter mais de um.</p></div>
  </div>`;
}
/*TESE-END*/
'''.replace('__J__', J)

h = open(H, encoding='utf8').read()
h = re.sub(r'\n/\*TESE-START\*/.*?/\*TESE-END\*/\n', '\n', h, flags=re.S)
m = '/* ---------- Roteamento e eventos ---------- */'
assert m in h
h = h.replace(m, JS + '\n' + m, 1)
# remove a renderGraficos antiga (fictícia)
h = re.sub(r'function renderGraficos\(\)\{(?:(?!/\*TESE-START).)*?\n\}\n\n/\* ---------- Metodologia', '/* ---------- Metodologia', h, count=1, flags=re.S)
h = h.replace("resultados:['piloto','validacao','analitica']", "resultados:['piloto','tese','validacao','analitica']") if "'piloto','tese'" not in h else h
h = h.replace('<section class="view" id="v-validacao" hidden></section>', '<section class="view" id="v-tese" hidden></section>\n  <section class="view" id="v-validacao" hidden></section>', 1) if 'id="v-tese"' not in h else h
h = h.replace('const R={piloto:renderPiloto,', 'const R={piloto:renderPiloto,tese:renderTese,', 1) if 'tese:renderTese' not in h else h
open(H, 'w', encoding='utf8').write(h)
print('ok', len(h))
