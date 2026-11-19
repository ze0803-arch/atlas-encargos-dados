#!/usr/bin/env python3
"""Telas novas (D68): Mapa, Correspondência, busca de município, histograma, leitura por UF em dois níveis,
aviso de que os números são anteriores à regra D68 e linha da patronal na ficha.
Rodar por último (após build_estrita.py), a partir da raiz do repositório. Idempotente.
Precisa da malha municipal do IBGE (qualidade mínima) em --malha (padrão /tmp/br.json):
https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio
"""
import json, math, csv, gzip, collections, sys, os
MALHA = sys.argv[1] if len(sys.argv) > 1 else '/tmp/br.json'
H = 'prototipo/atlas_prototipo.html'
h = open(H, encoding='utf8').read()
if '/*SITE-START*/' in h:
    i = h.index('/*SITE-START*/'); j = h.index('/*SITE-END*/') + len('/*SITE-END*/')
    h = h[:i] + h[j:]
    for old in ['<section class="view" id="v-mapa" hidden></section><section class="view" id="v-corresp" hidden></section>']:
        h = h.replace(old, '')
    h = h.replace('<div class="note" id="d68"', '<div class="note" id="d68x"')  # marcador para limpeza
    import re
    h = re.sub(r'<div class="note" id="d68x".*?</div>', '', h, flags=re.S)
    h = re.sub(r'<datalist id="dlMun">.*?</datalist>', '', h, flags=re.S)

# ---------- 1. malha -> caminhos SVG ----------
g = json.load(open(MALHA))
K = 40.0
LON0, LAT0 = -74.1, 5.4
COS = math.cos(math.radians(-14))
def P(lon, lat):
    return (round((lon - LON0) * COS * K), round((LAT0 - lat) * K))
paths = {}; box = {}
for f in g['features']:
    c = f['properties']['codarea']; geom = f['geometry']
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    d = []
    for poly in polys:
        for ring in poly:
            pts = []
            for lon, lat in ring:
                p = P(lon, lat)
                if not pts or p != pts[-1]: pts.append(p)
            if len(pts) > 1 and pts[0] == pts[-1]: pts.pop()
            if len(pts) < 3: continue
            s = 'M%d,%d' % pts[0]; px, py = pts[0]
            segs = []
            for x, y in pts[1:]:
                segs.append('%d,%d' % (x - px, y - py)); px, py = x, y
            d.append(s + 'l' + ' '.join(segs) + 'z')
            u = c[:2]
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            b = box.setdefault(u, [10**9, 10**9, -10**9, -10**9])
            b[0] = min(b[0], min(xs)); b[1] = min(b[1], min(ys)); b[2] = max(b[2], max(xs)); b[3] = max(b[3], max(ys))
    if d: paths[c] = ''.join(d)
allb = [min(b[0] for b in box.values()), min(b[1] for b in box.values()), max(b[2] for b in box.values()), max(b[3] for b in box.values())]
MAPA = {'p': paths, 'box': box, 'all': allb}
print('municípios na malha:', len(paths), 'tamanho KB:', round(len(json.dumps(MAPA, separators=(',', ':'))) / 1024))

# ---------- 2. Correspondência ----------
cl = list(csv.DictReader(open('catalogo/classificacao_acoes_2023.csv', encoding='utf8')))
tot = collections.defaultdict(float); nm = collections.defaultdict(set)
for r in csv.DictReader(gzip.open('catalogo/transferencias_2023_por_acao.csv.gz', 'rt', encoding='utf8')):
    k = r['NOME AÇÃO']; v = float(r['v'] or 0)
    tot[k] += v
    if v: nm[k].add(r['cod_ibge'])
CORR = []
sem = 0
for r in cl:
    k = r['NOME AÇÃO']
    if k not in tot: sem += 1
    CORR.append([r['grupo'], k, r['classe'], r['origem'], round(tot.get(k, 0)), len(nm.get(k, ()))])
print('ações:', len(CORR), 'sem valor na base:', sem, 'total R$ bi:', round(sum(x[4] for x in CORR) / 1e9, 1))

# ---------- 3. injeção no HTML ----------
CSS = """
/*SITE-CSS*/
:root{--s1:#E4F1F4;--s2:#BEDDE5;--s3:#93C6D3;--s4:#62A8BD;--s5:#3A859F;--s6:#1F647D;--s7:#0B3F52;--nc:#C9CFD6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--s1:#17333C;--s2:#1E4A58;--s3:#2A6578;--s4:#3D869B;--s5:#62A9BD;--s6:#92CBDA;--s7:#C8EBF4;--nc:#3A4755}}
:root[data-theme="dark"]{--s1:#17333C;--s2:#1E4A58;--s3:#2A6578;--s4:#3D869B;--s5:#62A9BD;--s6:#92CBDA;--s7:#C8EBF4;--nc:#3A4755}
.mapwrap{border:1px solid var(--line);border-radius:6px;background:var(--surface);padding:8px;max-width:100%}
.mapsvg{display:block;width:100%;height:auto;max-height:78vh}
.mapsvg path{stroke:var(--surface);stroke-width:.6;cursor:pointer}
.mapsvg path:hover{stroke:var(--ink);stroke-width:2}
.mapsvg .s1{fill:var(--s1)}.mapsvg .s2{fill:var(--s2)}.mapsvg .s3{fill:var(--s3)}.mapsvg .s4{fill:var(--s4)}.mapsvg .s5{fill:var(--s5)}.mapsvg .s6{fill:var(--s6)}.mapsvg .s7{fill:var(--s7)}
.mapsvg .nc{fill:url(#hach)}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12px;color:var(--muted);margin:8px 0}
.legend i{display:inline-block;width:18px;height:12px;border:1px solid var(--line);vertical-align:-2px;margin-right:4px}
#mapInfo{min-height:2.6em;margin:8px 0}
.note.d68{border-left-color:var(--warn);background:var(--warn-bg)}
"""
if '/*SITE-CSS*/' not in h:
    h = h.replace('</style>', CSS + '</style>', 1)

SEC = '<section class="view" id="v-mapa" hidden></section><section class="view" id="v-corresp" hidden></section>'
anchor = '<section class="view" id="v-metodologia" hidden></section>'
assert anchor in h
h = h.replace(anchor, anchor + SEC, 1)

BANNER = ('<div class="note d68" id="d68"><b>Atenção aos números desta versão.</b> Em 18/11/2026 a regra da margem ampla mudou (decisão D68): '
          'ela passa a descontar a contribuição patronal. O código de cálculo já está corrigido, mas os números mostrados aqui foram calculados '
          'antes da mudança e só serão atualizados quando os dados completos forem reprocessados no computador do pesquisador. '
          'A margem estrita não muda (a patronal já estava fora dela).</div><datalist id="dlMun"></datalist>')
nav = '<nav class="tabs" id="tabs" aria-label="Telas do aplicativo"></nav>'
assert nav in h
h = h.replace(nav, nav + BANNER, 1)

JS = r"""
/*SITE-START*/
const MAPA=@@MAPA@@;
const CORR=@@CORR@@;
const UFCOD={'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA','31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS','51':'MT','52':'GO','53':'DF'};
const CLASSE={automatica_constitucional:'Automática (constitucional)',obrigacao_legal:'Obrigação legal',adesao:'Adesão (voluntária)',outra:'Outra'};
const ORIGEM={formulario:'Formulário do projeto',proposta:'Proposta do pesquisador',padrao_a_revisar:'Padrão provisório, a revisar'};
const MRTf=r=>{if(r.st!=='calc'||r.m==null)return null;const b=FI(r.c,'rec_msc');return b>0?r.m/b*100:null};
const MREf=r=>{if(r.st!=='calc'||r.me==null)return null;const b=FI(r.c,'rec_msc');return b>0?r.me/b*100:null};
const MIND={mrt:['Margem ampla, % da receita total (medida principal)',MRTf],mre:['Margem estrita, % da receita total',MREf],mp:['Margem ampla, % da RCL',r=>r.st==='calc'&&r.mp!=null?r.mp*100:null],me:['Margem estrita, % da RCL',r=>r.st==='calc'&&MEp(r)!=null?MEp(r)*100:null],
 vinc:['Receita vinculada, % da receita',r=>{if(r.st!=='calc')return null;const a=FI(r.c,'rec_livre'),b=FI(r.c,'rec_msc');return a!=null&&b>0?(1-a/b)*100:null}],
 pib:['PIB por habitante, R$ (IBGE)',r=>(RD.PIBQ[r.c]||[null])[0]]};
function quant(a,k){a=a.filter(x=>x!=null).sort((x,y)=>x-y);const o=[];for(let i=1;i<k;i++)o.push(a[Math.min(a.length-1,Math.floor(i*a.length/k))]);return o}
let _mapCache=null;
function renderMapa(){
  const el=$('#v-mapa'),ind=S.mapInd||'mrt',uf=S.mapUF||'BR',f=MIND[ind][1];
  const ufs=Object.values(UFCOD).sort();
  const vals={};PILOTO.forEach(r=>{vals[r.c]=f(r)});
  const cut=quant(Object.values(vals),7);
  const cls=v=>{if(v==null)return 'nc';let k=0;while(k<6&&v>=cut[k])k++;return 's'+(k+1)};
  const byc={};PILOTO.forEach(r=>byc[r.c]=r);
  let b=MAPA.all,keys=Object.keys(MAPA.p);
  if(uf!=='BR'){const code=Object.keys(UFCOD).find(k=>UFCOD[k]===uf);b=MAPA.box[code];keys=keys.filter(k=>k.slice(0,2)===code)}
  const pad=10,vb=[b[0]-pad,b[1]-pad,b[2]-b[0]+2*pad,b[3]-b[1]+2*pad];
  const fm=v=>ind==='pib'?'R$ '+nf0.format(v):nf1.format(v)+'%%';
  const leg=cut.length?[`< ${fm(cut[0])}`,...cut.slice(1).map((c,i)=>`${fm(cut[i])} a ${fm(c)}`),`≥ ${fm(cut[5])}`]:[];
  const paths=keys.map(k=>{const r=byc[k];const v=r?vals[k]:null;return `<path data-rgo="${k}" data-v="${v==null?'':v}" class="${r?cls(v):'nc'}" d="${MAPA.p[k]}"/>`}).join('');
  const ncN=PILOTO.filter(r=>vals[r.c]==null&&(uf==='BR'||r.uf===uf)).length;
  const totN=PILOTO.filter(r=>uf==='BR'||r.uf===uf).length;
  const vv=Object.values(vals).filter(x=>x!=null);
  // histograma
  const hind=(ind==='mrt'||ind==='mre'||ind==='mp'||ind==='me')?ind:'mrt',hf=MIND[hind][1];
  const hv=PILOTO.filter(r=>uf==='BR'||r.uf===uf).map(hf).filter(x=>x!=null);
  const LO=-20,HI=80,W=5,nb=(HI-LO)/W,cnt=new Array(nb).fill(0);
  hv.forEach(v=>{let i=Math.floor((Math.min(Math.max(v,LO),HI-1e-9)-LO)/W);cnt[i]++});
  const mx=Math.max(1,...cnt),hw=640,hh=210,ml=34,bw=(hw-ml-8)/nb,med=medn(hv);
  let hs=`<svg viewBox="0 0 ${hw} ${hh}" role="img" aria-label="Histograma da ${MIND[hind][0]}" style="width:100%%;height:auto">`;
  cnt.forEach((n,i)=>{const hgt=n/mx*(hh-42),x=ml+i*bw;hs+=`<rect x="${(x+1).toFixed(1)}" y="${(hh-24-hgt).toFixed(1)}" width="${(bw-2).toFixed(1)}" height="${hgt.toFixed(1)}" style="fill:var(--b1)"/>`;
   if(n)hs+=`<text x="${(x+bw/2).toFixed(1)}" y="${(hh-27-hgt).toFixed(1)}" text-anchor="middle" font-size="10" style="fill:var(--muted)">${n}</text>`;
   if(i%%2===0)hs+=`<text x="${x.toFixed(1)}" y="${hh-8}" text-anchor="middle" font-size="10" style="fill:var(--muted)">${LO+i*W}</text>`});
  if(med!=null){const mxp=ml+(Math.min(Math.max(med,LO),HI)-LO)/(HI-LO)*(hw-ml-8);hs+=`<line x1="${mxp.toFixed(1)}" x2="${mxp.toFixed(1)}" y1="6" y2="${hh-24}" style="stroke:var(--accent)" stroke-width="2" stroke-dasharray="4 3"/><text x="${(mxp+4).toFixed(1)}" y="14" font-size="11" style="fill:var(--accent)">mediana ${nf1.format(med)}%%</text>`}
  hs+='</svg>';
  // leitura por UF, dois níveis
  const fora=RD.T.uf_fora;
  const lin=gUFdata().slice().sort((a,c)=>a.uf.localeCompare(c.uf)).map(x=>{const f1=fora.includes(x.uf),f2=x.cob!=null&&x.cob<60;
    return `<tr><td>${x.uf}</td><td class="num">${I0(x.tot)}</td><td class="num">${nf1.format(x.cob)}%%</td><td>${f1?'<span class="chip bad">fora da leitura</span>':'<span class="chip ok">na leitura</span>'}</td><td>${f2?'<span class="chip warn">cobertura abaixo de 60%%</span>':''}</td></tr>`}).join('');
  el.innerHTML=`
  ${hd('Δ','Mapa: onde a margem de decisão é maior ou menor','Cada município é pintado conforme o indicador escolhido, em sete faixas com o mesmo número de municípios (septis). Passe o mouse para ver os números; clique para abrir a ficha do município. Hachurado: município sem valor calculado.')}
  <div class="row"><label>Indicador<select data-m="ind">${Object.keys(MIND).map(k=>opt(k,MIND[k][0],ind)).join('')}</select></label>
  <label>Área<select data-m="uf"><option value="BR"${uf==='BR'?' selected':''}>Brasil</option>${ufs.map(u=>opt(u,u,uf)).join('')}</select></label>
  <label>Buscar município<input list="dlMun" data-busca placeholder="digite o nome" autocomplete="off"></label></div>
  <div class="mapwrap"><svg class="mapsvg" viewBox="${vb.join(' ')}" role="img" aria-label="Mapa dos municípios"><defs><pattern id="hach" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" style="fill:var(--surface)"/><line x1="0" y1="0" x2="0" y2="8" style="stroke:var(--muted)" stroke-width="2.5"/></pattern></defs>${paths}</svg></div>
  <div class="legend">${leg.map((t,i)=>`<span><i style="background:var(--s${i+1})"></i>${t}</span>`).join('')}<span><i style="background:repeating-linear-gradient(45deg,var(--surface),var(--surface) 3px,var(--muted) 3px,var(--muted) 4px)"></i>sem valor (${I0(ncN)} de ${I0(totN)})</span></div>
  <div id="mapInfo" class="muted">Passe o mouse sobre um município.</div>
  <p class="muted">As faixas usam o Brasil inteiro, mesmo quando a área escolhida é um estado, para que as cores sejam comparáveis entre estados. Estados fora da leitura (${fora.join(', ')}) aparecem pintados onde há valor, mas não entram nas conclusões.</p>
  <h3>Distribuição da ${MIND[hind][0].toLowerCase()}${uf==='BR'?'':' em '+uf}</h3>
  <div class="chartcard">${hs}<p>Barras de 5 pontos percentuais; valores abaixo de −20%% ou acima de 80%% ficam nas barras das pontas. ${I0(hv.length)} municípios com valor calculado.</p></div>
  <h3>Leitura por estado: dois níveis de cobertura</h3>
  <p class="muted">Nível 1 (regra do projeto): estados fora da leitura. Nível 2 (aviso adicional): estados em que menos de 60%% dos municípios têm margem calculada, onde a mediana do estado representa pouco do território.</p>
  <div class="tablewrap"><table class="data"><thead><tr><th>UF</th><th class="num">Entes</th><th class="num">Cobertura</th><th>Nível 1</th><th>Nível 2</th></tr></thead><tbody>${lin}</tbody></table></div>`;
}
function renderCorresp(){
  const el=$('#v-corresp'),fc=S.corC||'all',fo=S.corO||'all';
  const tot=CORR.reduce((a,x)=>a+x[4],0);
  const porC={};CORR.forEach(x=>{const o=porC[x[2]]=porC[x[2]]||{n:0,v:0};o.n++;o.v+=x[4]});
  const porO={};CORR.forEach(x=>{const o=porO[x[3]]=porO[x[3]]||{n:0,v:0};o.n++;o.v+=x[4]});
  let rows=CORR.filter(x=>(fc==='all'||x[2]===fc)&&(fo==='all'||x[3]===fo)).sort((a,b)=>b[4]-a[4]);
  const full=S.corAll;const sh=full?rows:rows.slice(0,20);
  el.innerHTML=`
  ${hd('Σ','Correspondência: de onde vem cada transferência e como foi classificada','Cada ação de transferência recebida pelos municípios em 2023 foi classificada como automática (vem da Constituição), obrigação legal ou adesão voluntária. A classe decide se o recurso conta como já comprometido por norma nacional.')}
  <div class="cards">${Object.keys(CLASSE).filter(k=>porC[k]).map(k=>`<div class="card stat"><div class="n">${nf1.format(porC[k].v/tot*100)}%%</div><div class="l">${CLASSE[k]}: ${porC[k].n} ações, R$ ${nf1.format(porC[k].v/1e9)} bi</div></div>`).join('')}</div>
  <p class="muted">Quem classificou: ${Object.keys(ORIGEM).filter(k=>porO[k]).map(k=>`${ORIGEM[k]} (${porO[k].n} ações, ${nf1.format(porO[k].v/tot*100)}%% do valor)`).join('; ')}. As ações de padrão provisório ainda precisam de revisão antes de qualquer conclusão sobre adesão.</p>
  <div class="row"><label>Classe<select data-co="c"><option value="all">todas</option>${Object.keys(CLASSE).map(k=>opt(k,CLASSE[k],fc)).join('')}</select></label>
  <label>Origem da classificação<select data-co="o"><option value="all">todas</option>${Object.keys(ORIGEM).map(k=>opt(k,ORIGEM[k],fo)).join('')}</select></label>
  <button data-co="all" type="button">${full?'Mostrar só as 20 maiores':'Mostrar todas ('+rows.length+')'}</button></div>
  <div class="tablewrap"><table class="data"><thead><tr><th>Ação</th><th>Classe</th><th>Origem</th><th class="num">Total 2023 (R$ mi)</th><th class="num">Municípios</th></tr></thead><tbody>${sh.map(x=>`<tr><td>${esc(x[1])}</td><td>${CLASSE[x[2]]||x[2]}</td><td>${ORIGEM[x[3]]||x[3]}</td><td class="num">${nf1.format(x[4]/1e6)}</td><td class="num">${I0(x[5])}</td></tr>`).join('')}</tbody></table></div>
  <p class="muted">${full?'Todas as ações do filtro.':'As 20 maiores do filtro.'} Total das ${CORR.length} ações: R$ ${nf1.format(tot/1e9)} bi.</p>`;
}
document.addEventListener('change',e=>{const t=e.target;
 if(t.dataset.m==='ind'){S.mapInd=t.value;renderMapa()}else if(t.dataset.m==='uf'){S.mapUF=t.value;renderMapa()}
 else if(t.dataset.co==='c'){S.corC=t.value;renderCorresp()}else if(t.dataset.co==='o'){S.corO=t.value;renderCorresp()}
 else if(t.dataset.busca!==undefined){const m=PILOTO.find(r=>r.ente+' — '+r.uf===t.value);if(m){S.rUF=m.uf;S.rMun=m.c;location.hash='#municipio'}}});
document.addEventListener('click',e=>{const t=e.target;if(t.dataset&&t.dataset.co==='all'){S.corAll=!S.corAll;renderCorresp()}});
document.addEventListener('mouseover',e=>{const p=e.target.closest&&e.target.closest('.mapsvg path');if(!p)return;const m=PILOTO.find(r=>r.c===p.dataset.rgo),inf=$('#mapInfo');if(!inf)return;
 if(!m){inf.textContent='Fora do universo do estudo (DF e Fernando de Noronha).';return}
 const v=p.dataset.v===''?null:+p.dataset.v,ind=S.mapInd||'mrt';
 inf.innerHTML=`<b>${esc(m.ente)}</b> · ${m.uf} · ${nf0.format(m.pop)} hab.<br>${MIND[ind][0]}: ${v==null?'sem valor calculado'+(m.fl&&m.fl.length?' ('+m.fl.map(x=>FLAGTXT[x]||x).join('; ')+')':''):(ind==='pib'?'R$ '+nf0.format(v):nf1.format(v)+'%%')} · ampla ${MRTf(m)==null?'—':nf1.format(MRTf(m))+'%%'} · estrita ${MREf(m)==null?'—':nf1.format(MREf(m))+'%%'} da receita total <span class="muted">(clique para abrir a ficha)</span>`});
// busca na ficha + datalist
$('#dlMun').innerHTML=PILOTO.map(r=>`<option value="${esc(r.ente+' — '+r.uf)}"></option>`).join('');
const _rf=renderFichaR;renderFichaR=function(){_rf();const e=$('#v-fichaR'),hr=e.querySelector('.row');const sm=e.querySelector('[data-r=mun]'),mm=sm&&PILOTO.find(r=>r.c===sm.value),cd=e.querySelector('.cards');if(cd&&mm)cd.insertAdjacentHTML('afterbegin',`<div class="card stat"><div class="n">${MRTf(mm)==null?'—':nf1.format(MRTf(mm))+'%%'}</div><div class="l">margem ampla, % da receita total (medida principal da tese) · estrita ${MREf(mm)==null?'—':nf1.format(MREf(mm))+'%%'}</div></div>`);if(hr)hr.insertAdjacentHTML('beforeend','<label>Buscar pelo nome<input list="dlMun" data-busca placeholder="digite o nome do município" autocomplete="off"></label>')};
R.fichaR=renderFichaR;
R.mapa=renderMapa;R.corresp=renderCorresp;
TABS.splice(TABS.findIndex(t=>t[0]==='graficos')+1,0,['mapa','Mapa'],['corresp','Correspondência']);
VIEWS.mapa=['mapa'];VIEWS.corresp=['corresp'];
$('#tabs').innerHTML=TABS.map(t=>`<a href="#${t[0]}" data-tab="${t[0]}">${t[1]}</a>`).join('');
route();
/*SITE-END*/
"""
JS = JS.replace("%%", "%").replace("@@MAPA@@", json.dumps(MAPA, separators=(",", ":"))).replace("@@CORR@@", json.dumps(CORR, ensure_ascii=False, separators=(",", ":")))
# 'function renderFichaR' é declaração: reatribuir exige var; troca para permitir
if 'function renderFichaR(){' in h:
    pass
JS = JS.replace('const _rf=renderFichaR;renderFichaR=function(){', 'const _rf=renderFichaR;window.renderFichaR=renderFichaR=function(){')
h = h.replace('</script>\n\n</body></html>', JS + '</script>\n\n</body></html>')
assert '/*SITE-START*/' in h

# ---------- 4. ficha: linha da patronal e texto da margem ampla ----------
old = '<tr><td><b>= Margem ampla</b></td><td class="num"><b>${f(g(\'margem_ampla\'))}</b></td><td class="muted">receita livre − mínimos − Legislativo − dívida − precatórios</td></tr>'
new = ('<tr><td>(−) Contribuição patronal paga com fonte livre</td><td class="num">${f(g(\'patronal_livre\'))}</td><td class="muted">regra D68: desconta na margem ampla; "—" = ainda não reprocessado</td></tr>\n  '
       '<tr><td><b>= Margem ampla</b></td><td class="num"><b>${f(g(\'margem_ampla\'))}</b></td><td class="muted">receita livre − mínimos − patronal − Legislativo − dívida − precatórios (valor mostrado ainda sem o desconto da patronal)</td></tr>')
if new not in h:
    assert old in h
    h = h.replace(old, new, 1)
    h = h.replace('<tr><td>(−) Folha de pessoal paga com fonte livre</td>', '<tr><td>(−) Folha de pessoal paga com fonte livre (sem a patronal)</td>', 1)
open(H, 'w', encoding='utf8').write(h)
print('ok', round(len(h) / 1e6, 2), 'MB')
