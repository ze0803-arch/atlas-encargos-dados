#!/usr/bin/env python3
"""Insere no protótipo as telas reais de 2023: Início, Coletar, Conferir e Ficha do município.
Uso (da raiz do repositório): python prototipo/build_real_2023.py   (rodar depois de build_prototipo_nacional.py e build_tese_2023.py)"""
import re, json, pandas as pd, numpy as np
C = 'catalogo/'; H = 'prototipo/atlas_prototipo.html'
r = pd.read_csv(C+'resultado_2023.csv', dtype={'cod_ibge': str}); r = r[~r.cod_ibge.str.startswith('53') & (r.cod_ibge != '2605459')]
s = pd.read_csv(C+'comparacao_siops_2023.csv', dtype={'cod_ibge': str}).set_index('cod_ibge')
F = ['rec_msc','dca_rec','rec_dif','liq_msc','dca_liq','liq_dif','base_impostos','fpm_parcela_de','minimos_exigidos','rec_livre','leg','divida','prec','folha_livre','consorcios','margem_ampla','margem_estrita','rcl_ajustada']
def v(x, d=0):
    return None if pd.isna(x) else (round(float(x), 4) if d else int(round(float(x))))
FICHA = {}
for _, x in r.iterrows():
    row = [v(x[k], 1 if k.endswith('_dif') else 0) for k in F]
    row.append(v(s.diferenca_pct.get(x.cod_ibge, np.nan), 1)); row.append(1 if (x.cod_ibge in s.index and bool(s.lei_organica.get(x.cod_ibge))) else 0)
    FICHA[x.cod_ibge] = row
d = pd.read_csv(C+'diario_extracao.csv'); ds = pd.read_csv(C+'diario_siops.csv')
dg = d.groupby(['fonte', 'relatorio', 'resultado']).agg(n=('url', 'size'), linhas=('linhas', 'sum'), mb=('bytes_gz', lambda b: b.sum()/1e6)).reset_index().round(1)
DIARIO = dict(rel=dg.to_dict('records'), entes=int(d.ente.nunique()), n=int(len(d)), de=d.data_hora_utc.min()[:10], ate=d.data_hora_utc.max()[:10],
              siops=dict(n=int(len(ds)), ok=int((ds.resultado == 'sucesso').sum())))
J1 = json.dumps(FICHA, separators=(',', ':')); J2 = json.dumps(DIARIO, ensure_ascii=False, separators=(',', ':')); J3 = json.dumps(F)

JS = r'''
/*REAL-START*/
const FCOLS=__J3__;const FICHA=__J1__;const DIARIO=__J2__;
const FI=(c,k)=>{const a=FICHA[c];if(!a)return null;const i=FCOLS.indexOf(k);return i<0?(k==='sd'?a[FCOLS.length]:k==='lo'?a[FCOLS.length+1]:null):a[i]};
const R$=v=>v==null?'—':nf0.format(v);
function renderInicioR(){
  const el=$('#v-inicioR'),P=PILOTO,calc=P.filter(r=>r.st==='calc'),alta=calc.filter(r=>r.cf==='A');
  el.innerHTML=`
  <h2 style="font-size:20px;margin-bottom:4px">Atlas de Encargos</h2>
  <p class="lead">Quanto sobra do orçamento de cada município para ele decidir, depois das obrigações fixadas em norma nacional. Dados reais de 2023, do Siconfi, do SIOPS e do Portal da Transparência. O DF e Fernando de Noronha ficam fora do universo municipal.</p>
  <div class="cards">
   <div class="card stat"><div class="n">${nf0.format(P.length)}</div><div class="l">municípios coletados</div></div>
   <div class="card stat"><div class="n">${nf0.format(calc.length)}</div><div class="l">com margem calculada (${nf0.format(100*calc.length/P.length)}%)</div></div>
   <div class="card stat"><div class="n">${nf0.format(alta.length)}</div><div class="l">com alta confiança (${nf0.format(100*alta.length/calc.length)}% dos calculados)</div></div>
   <div class="card stat"><div class="n">${nf1.format(100*medn(calc.map(r=>r.mp)))}%</div><div class="l">margem ampla mediana, % da RCL</div></div>
  </div>
  <h3>As etapas</h3>
  <ol class="lead"><li><b>Coletar:</b> o que foi buscado nas fontes públicas e como ficou registrado.</li><li><b>Conferir:</b> os dados fecham entre si? A tolerância é ajustável.</li><li><b>Classificar:</b> o dicionário que decide o bloco de cada receita e despesa (demonstração).</li><li><b>Resultados:</b> margem por município, testes da tese e validação.</li><li><b>Município:</b> a ficha com o cálculo linha a linha.</li></ol>
  <h3>Os quatro blocos em que o orçamento é dividido</h3>
  <ul><li><b>I</b> Obrigação de origem nacional: fontes vinculadas, mínimos de educação e saúde, contribuição patronal.</li><li><b>II</b> Estrutura e compromissos passados: Câmara, juros e amortização, precatórios.</li><li><b>III</b> Espaço de decisão: o que sobra do recurso livre.</li><li><b>IV</b> Recursos de outros entes: convênios, emendas, transferências especiais.</li></ul>`;
}
function renderColetaR(){
  const el=$('#v-coletaR'),D=DIARIO,P=PILOTO;
  const nome={siconfi:'Siconfi',siope:'SIOPE',ibge:'IBGE'};
  el.innerHTML=`
  ${hd(1,'Coletar: o que foi buscado nas fontes públicas','Cada pedido às fontes fica registrado no diário de extração, com data, endereço, resultado e marca de integridade (SHA-256). Abaixo, o diário do piloto guardado no repositório.',`<p>A coleta nacional de 2023 foi rodada pelo pesquisador no próprio computador (aplicativo coletar.py) e os dados brutos vão ao Zenodo; o repositório guarda scripts, catálogo e resultados. O diário abaixo cobre ${nf0.format(D.entes)} entes do piloto (${D.de} a ${D.ate}).</p>`)}
  <div class="cards">
   <div class="card stat"><div class="n">${nf0.format(D.n)}</div><div class="l">pedidos registrados no diário do piloto</div></div>
   <div class="card stat"><div class="n">${nf0.format(D.entes)}</div><div class="l">entes no diário</div></div>
   <div class="card stat"><div class="n">${nf0.format(D.siops.ok)} de ${nf0.format(D.siops.n)}</div><div class="l">consultas ao SIOPS com sucesso</div></div>
   <div class="card stat"><div class="n">${nf0.format(P.length)}</div><div class="l">municípios com dados de 2023 no resultado nacional</div></div>
  </div>
  ${tb(D.rel.map(x=>({fonte:nome[x.fonte]||x.fonte,relatorio:x.relatorio,resultado:x.resultado,n:x.n,linhas:x.linhas,mb:x.mb})),[['fonte','Fonte'],['relatorio','Relatório'],['resultado','Resultado'],['n','Pedidos',1],['linhas','Linhas',1],['mb','MB (gz)',1]])}
  <p class="muted">Resultado "vazio": a fonte respondeu sem dados (município que não entregou o relatório). Nenhum dado é corrigido na coleta.</p>`;
}
function renderConferirR(){
  const el=$('#v-conferirR'),tol=S.rTol??1,sd=S.rSd??10;
  const com=PILOTO.filter(r=>FI(r.c,'rec_msc')!=null&&FI(r.c,'dca_rec')!=null);
  const rd=c=>Math.abs(FI(c,'rec_dif')||0)*100,ld=c=>Math.abs(FI(c,'liq_dif')||0)*100;
  const fR=com.filter(r=>rd(r.c)>tol),fL=com.filter(r=>ld(r.c)>tol),ambos=com.filter(r=>rd(r.c)>tol||ld(r.c)>tol);
  const sdl=PILOTO.filter(r=>FI(r.c,'sd')!=null&&Math.abs(FI(r.c,'sd'))>sd&&r.st==='calc');
  const top=ambos.map(r=>({r,m:Math.max(rd(r.c),ld(r.c))})).sort((a,b)=>b.m-a.m).slice(0,40);
  el.innerHTML=`
  ${hd(2,'Conferir se os dados fecham','Compara a MSC com a DCA (receita e despesa liquidada) e o mínimo de saúde do sistema com o SIOPS. Cada teste só sinaliza o que não fecha; nenhum dado é corrigido. Ajuste a tolerância para ver quantos municípios passam a ter alerta.',`<p>A tolerância usada no cálculo de 2023 é de 1%. Com 3% voltam municípios ao cálculo (sensibilidade em D45 e D55). O teste do SIOPS é o T9: diferença acima de 10% tira o selo de alta confiança.</p>`)}
  <div class="row"><label>Tolerância MSC × DCA: <b class="mono">${nf1.format(tol)}%</b><input type="range" min="0.2" max="5" step="0.1" value="${tol}" data-rr="tol" aria-label="Tolerância MSC contra DCA"></label>
  <label>Limite do SIOPS: <b class="mono">${nf0.format(sd)}%</b><input type="range" min="1" max="30" step="1" value="${sd}" data-rr="sd" aria-label="Limite do SIOPS"></label></div>
  <div class="cards">
   <div class="card stat"><div class="n">${nf0.format(com.length)}</div><div class="l">municípios com MSC e DCA</div></div>
   <div class="card stat"><div class="n">${nf0.format(fR.length)}</div><div class="l">receita MSC × DCA acima de ${nf1.format(tol)}%</div></div>
   <div class="card stat"><div class="n">${nf0.format(fL.length)}</div><div class="l">despesa liquidada MSC × DCA acima de ${nf1.format(tol)}%</div></div>
   <div class="card stat"><div class="n">${nf0.format(ambos.length)}</div><div class="l">com alguma divergência (${nf0.format(100*ambos.length/com.length)}%)</div></div>
   <div class="card stat"><div class="n">${nf0.format(sdl.length)}</div><div class="l">calculados com mínimo de saúde acima de ${nf0.format(sd)}% do SIOPS</div></div>
  </div>
  <h3>As 40 maiores divergências MSC × DCA</h3>
  <div class="tablewrap"><table class="data"><thead><tr><th>Município</th><th>UF</th><th class="num">Receita MSC − DCA</th><th class="num">Liquidação MSC − DCA</th><th>Situação</th></tr></thead><tbody>
  ${top.map(({r})=>`<tr class="go" data-rgo="${r.c}"><td>${esc(r.ente)}</td><td>${r.uf}</td><td class="num">${nf1.format(100*(FI(r.c,'rec_dif')||0))}%</td><td class="num">${nf1.format(100*(FI(r.c,'liq_dif')||0))}%</td><td>${r.st==='calc'?'calculado':'marcado'}</td></tr>`).join('')}
  </tbody></table></div><p class="muted">Clique numa linha para abrir a ficha do município.</p>`;
}
function renderFichaR(){
  const el=$('#v-fichaR'),ufs=[...new Set(PILOTO.map(r=>r.uf))].sort(),uf=S.rUF||'RN';
  const lista=PILOTO.filter(r=>r.uf===uf).sort((a,b)=>a.ente.localeCompare(b.ente,'pt-BR'));
  const m=PILOTO.find(r=>r.c===S.rMun)&&PILOTO.find(r=>r.c===S.rMun).uf===uf?PILOTO.find(r=>r.c===S.rMun):lista[0];
  const c=m.c,g=k=>FI(c,k),f=v=>v==null?'—':R$(v);
  const lin=[['Receita realizada (MSC, conta 621200000)',g('rec_msc'),''],['Receita da DCA',g('dca_rec'),'para conferir'],['Receita livre (fontes 1500 e 1501)',g('rec_livre'),'base do cálculo'],['(−) Mínimos: 25% da base (educação) + 15% da base sem as parcelas d e e do FPM (saúde)',g('minimos_exigidos'),'base de impostos '+f(g('base_impostos'))],['(−) Legislativo (fonte livre)',g('leg'),''],['(−) Dívida: juros e amortização',g('divida'),''],['(−) Precatórios',g('prec'),'']];
  const ft=(m.ft||[]).map(t=>`<li>${t}: ${TESTETXT[t]||''}</li>`).join('');
  el.innerHTML=`
  ${hd(5,'Município: o cálculo linha a linha','Escolha a UF e o município. A ficha mostra de onde sai cada número da margem de decisão, em R$, e os alertas do município.')}
  <div class="row"><label>UF<select data-r="uf">${ufs.map(u=>opt(u,u,uf)).join('')}</select></label>
  <label>Município<select data-r="mun">${lista.map(x=>opt(x.c,x.ente,m.c)).join('')}</select></label></div>
  <div class="cards">
   <div class="card stat"><div class="n">${esc(m.ente)}</div><div class="l">${m.uf} · ${nf0.format(m.pop)} habitantes</div></div>
   <div class="card stat"><div class="n">${m.st==='calc'?'calculado':'não calculado'}</div><div class="l">${m.st==='calc'?(m.cf==='A'?'alta confiança':'confiança reduzida'):'ver alertas abaixo'}</div></div>
   <div class="card stat"><div class="n">${m.mp==null?'—':nf1.format(100*m.mp)+'%'}</div><div class="l">margem ampla, % da RCL</div></div>
  </div>
  <h3>Cálculo (R$)</h3>
  <div class="tablewrap"><table class="data"><tbody>${lin.map(l=>`<tr><td>${l[0]}</td><td class="num">${f(l[1])}</td><td class="muted">${l[2]}</td></tr>`).join('')}
  <tr><td><b>= Margem ampla</b></td><td class="num"><b>${f(g('margem_ampla'))}</b></td><td class="muted">receita livre − mínimos − Legislativo − dívida − precatórios</td></tr>
  <tr><td>(−) Folha de pessoal paga com fonte livre</td><td class="num">${f(g('folha_livre'))}</td><td class="muted"></td></tr>
  <tr><td><b>= Margem estrita</b></td><td class="num"><b>${f(g('margem_estrita'))}</b></td><td class="muted"></td></tr>
  <tr><td>Consórcios (bloco P, fora da margem)</td><td class="num">${f(g('consorcios'))}</td><td class="muted">sensibilidade</td></tr>
  <tr><td>RCL ajustada (RGF)</td><td class="num">${f(g('rcl_ajustada'))}</td><td class="muted">denominador da margem em %</td></tr></tbody></table></div>
  <h3>Conferências</h3>
  <ul><li>Receita MSC × DCA: ${g('rec_dif')==null?'—':nf2.format(100*g('rec_dif'))+'%'}; despesa liquidada MSC × DCA: ${g('liq_dif')==null?'—':nf2.format(100*g('liq_dif'))+'%'}.</li>
  <li>Mínimo de saúde contra o SIOPS: ${g('sd')==null?'sem SIOPS coletado':nf2.format(g('sd'))+'%'}${g('lo')?' (município com percentual maior na lei orgânica)':''}.</li>
  ${m.fl.length?`<li>Alertas: ${m.fl.map(x=>FLAGTXT[x]||x).join('; ')}.</li>`:'<li>Nenhum alerta.</li>'}
  ${ft?`</ul><p>Testes de consistência que falharam:</p><ul>${ft}`:''}</ul>`;
}
document.addEventListener('change',e=>{const t=e.target;if(t.dataset.r==='uf'){S.rUF=t.value;S.rMun=null;renderFichaR()}else if(t.dataset.r==='mun'){S.rMun=t.value;renderFichaR()}});
document.addEventListener('input',e=>{const t=e.target;if(t.dataset.rr==='tol'){S.rTol=+t.value;renderConferirR()}else if(t.dataset.rr==='sd'){S.rSd=+t.value;renderConferirR()}});
document.addEventListener('click',e=>{const a=e.target.closest('[data-rgo]');if(a){const c=a.dataset.rgo,m=PILOTO.find(r=>r.c===c);if(m){S.rUF=m.uf;S.rMun=c;location.hash='#municipio'}}});
/*REAL-END*/
'''.replace('__J1__', J1).replace('__J2__', J2).replace('__J3__', J3)

h = open(H, encoding='utf8').read()
h = re.sub(r'\n/\*REAL-START\*/.*?/\*REAL-END\*/\n', '\n', h, flags=re.S)
m = '/* ---------- Roteamento e eventos ---------- */'; assert m in h
h = h.replace(m, JS + '\n' + m, 1)
for sec in ('inicioR', 'coletaR', 'conferirR', 'fichaR'):
    if f'id="v-{sec}"' not in h: h = h.replace('<section class="view" id="v-tese" hidden></section>', f'<section class="view" id="v-tese" hidden></section>\n  <section class="view" id="v-{sec}" hidden></section>', 1)
h = re.sub(r'const VIEWS=\{.*?\};', "const VIEWS={inicio:['inicioR'],coletar:['coletaR'],conferir:['conferirR'],classificar:['dicionario'],resultados:['piloto','tese','validacao'],municipio:['fichaR'],graficos:['graficos'],metodologia:['metodologia']};", h, 1, flags=re.S)
if 'inicioR:renderInicioR' not in h:
    h = h.replace('const R={piloto:renderPiloto,', 'const R={inicioR:renderInicioR,coletaR:renderColetaR,conferirR:renderConferirR,fichaR:renderFichaR,piloto:renderPiloto,', 1)
h = h.replace('Protótipo · demais telas com dados fictícios · Piloto 2023 e Validação com dados reais', 'Protótipo · dados reais de 2023 · só a tela Classificar é demonstração')
open(H, 'w', encoding='utf8').write(h); print('ok', len(h))
