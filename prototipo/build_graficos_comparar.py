#!/usr/bin/env python3
"""Acrescenta à aba Gráficos duas ferramentas: comparar estados (ranking por indicador) e comparar municípios (régua de distribuição).
Rodar depois de build_readequacao_2023.py. Idempotente."""
import re
H='prototipo/atlas_prototipo.html'
JS=r'''
/*GCMP-START*/
const GMET={mp:['Margem ampla mediana, % da RCL','mp'],m_rt:['Margem, % da receita total (mediana)','m_rt'],vinc:['Receita vinculada, % da receita total','vinc'],pib:['PIB por habitante (R$)','pib'],cob:['Cobertura, % de municípios calculados','cob']};
function gUFdata(){
  const by={};PILOTO.filter(r=>r.st==='calc'&&r.mp!=null).forEach(r=>{(by[r.uf]=by[r.uf]||[]).push(r.mp*100)});
  return COMP.uf.map(x=>{const a=(by[x.uf]||[]).slice().sort((p,q)=>p-q);return Object.assign({},x,{mp:a.length?medn(a):null,nmp:a.length})});
}
function svgBarsH(items,hi,fmt){
  const w=640,lab=60,rh=22,H=items.length*rh+6,mx=Math.max(...items.map(i=>i.v)),bw=w-lab-70;
  let o=`<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Comparação entre estados">`;
  items.forEach((it,i)=>{const y=i*rh+3,wd=Math.max(1,it.v/mx*bw),on=it.l===hi;
   o+=`<text x="${lab-8}" y="${y+14}" text-anchor="end" font-size="12" style="fill:${on?'var(--ink)':'var(--muted)'};font-weight:${on?700:400}">${esc(it.l)}${it.ok===false?'*':''}</text><rect x="${lab}" y="${y}" width="${wd.toFixed(1)}" height="16" style="fill:${on?'var(--accent)':(it.ok===false?'var(--b5)':'var(--b1)')}" opacity="${it.ok===false?.55:1}"/><text x="${(lab+wd+6).toFixed(1)}" y="${y+13}" font-size="11" font-family="IBM Plex Mono,monospace" style="fill:var(--ink)">${fmt(it.v)}</text>`});
  return o+'</svg>';
}
function svgStrip(rows,marks){
  const W=640,rh=54,ml=70,mr=16,H=rows.length*rh+34;
  const all=rows.flatMap(r=>r.v),lo=Math.floor(Math.min(...all)/5)*5,hi=Math.ceil(Math.max(...all)/5)*5,X=v=>ml+(v-lo)/(hi-lo)*(W-ml-mr);
  let o=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Distribuição da margem ampla dos municípios">`;
  for(let t=lo;t<=hi;t+=5)o+=`<line x1="${X(t)}" x2="${X(t)}" y1="6" y2="${H-24}" style="stroke:var(--line)"/><text x="${X(t)}" y="${H-8}" text-anchor="middle" font-size="11" style="fill:var(--muted)">${t}%</text>`;
  rows.forEach((r,i)=>{const cy=i*rh+28;
   o+=`<text x="${ml-8}" y="${cy+4}" text-anchor="end" font-size="12" style="fill:var(--ink);font-weight:700">${esc(r.l)}</text>`;
   r.v.forEach((v,k)=>{o+=`<circle cx="${X(v).toFixed(1)}" cy="${(cy+((k*37)%17)-8).toFixed(1)}" r="2.3" style="fill:var(--b1)" opacity=".4"/>`});
   const m=medn(r.v);o+=`<line x1="${X(m)}" x2="${X(m)}" y1="${cy-18}" y2="${cy+18}" style="stroke:var(--ink)" stroke-width="2"/><text x="${X(m)}" y="${cy-21}" text-anchor="middle" font-size="10" style="fill:var(--ink)">mediana ${nf1.format(m)}%</text>`});
  marks.forEach(mk=>{const i=rows.findIndex(r=>r.l===mk.uf);if(i<0||mk.v==null)return;const cy=i*rh+28;
   o+=`<circle cx="${X(mk.v).toFixed(1)}" cy="${cy}" r="7" style="fill:${mk.cor};stroke:var(--surface)" stroke-width="2"/><text x="${X(mk.v).toFixed(1)}" y="${cy+4}" text-anchor="middle" font-size="9" font-weight="700" style="fill:var(--surface)">${mk.t}</text>`});
  return o+'</svg>';
}
function gCmpHTML(){
  const mt=S.gMet||'mp',U=gUFdata(),meta=GMET[mt],fmtv=mt==='pib'?(v=>nf0.format(v)):(v=>nf1.format(v)+'%');
  const lista=U.filter(x=>x[meta[1]]!=null).sort((a,b)=>b[meta[1]]-a[meta[1]]).map(x=>({l:x.uf,v:x[meta[1]],ok:x.ok}));
  const ufs=[...new Set(PILOTO.map(r=>r.uf))].sort();
  const calcDe=u=>PILOTO.filter(r=>r.uf===u&&r.st==='calc'&&r.mp!=null).sort((a,b)=>a.ente.localeCompare(b.ente,'pt-BR'));
  const uA=S.gUA||'RN',uB=S.gUB||'PE',LA=calcDe(uA),LB=calcDe(uB);
  const A=LA.find(r=>r.c===S.gMA)||LA[0],B=LB.find(r=>r.c===S.gMB)||LB[0];
  const pos=(m,L)=>{if(!m)return '—';const o=L.slice().sort((a,b)=>b.mp-a.mp);return (o.findIndex(r=>r.c===m.c)+1)+'º de '+L.length};
  const pibq=m=>{const p=RD.PIBQ[m&&m.c];return p?'R$ '+nf0.format(p[0])+' · Q'+p[1]:'—'};
  const card=(m,L,u,cor,t)=>m?`<div class="card" style="border-left:6px solid ${cor}"><h3>${t} · ${esc(m.ente)} (${u})</h3><p><b>${nf1.format(m.mp*100)}%</b> margem ampla da RCL<br>Posição na UF: ${pos(m,L)} (1º = maior margem)<br>Mediana da UF: ${nf1.format(medn(L.map(r=>r.mp*100)))}%<br>População: ${nf0.format(m.pop)}<br>PIB por habitante: ${pibq(m)}</p></div>`:'<div class="card empty">Sem municípios calculados nesta UF.</div>';
  const rows=[{l:uA,v:LA.map(r=>r.mp*100)}];if(uB!==uA)rows.push({l:uB,v:LB.map(r=>r.mp*100)});
  const diff=A&&B?(A.mp-B.mp)*100:null;
  return `<hr style="margin:28px 0;border:0;border-top:1px solid var(--line)">
  <div class="vh"><h2>Comparar estados</h2></div>
  <p class="lead">Escolha o indicador. Barras cinzas com asterisco são estados com cobertura insuficiente (menos de 40 municípios calculados ou cobertura abaixo de 40%): não devem ser comparados com os demais.</p>
  <div class="row"><label>Indicador<select data-act="gMet">${Object.keys(GMET).map(k=>opt(k,GMET[k][0],mt)).join('')}</select></label><label>Destacar UF<select data-act="gUA">${ufs.map(u=>opt(u,u,uA)).join('')}</select></label></div>
  <div class="card chartcard">${svgBarsH(lista,uA,fmtv)}<p>${esc(meta[0])}, 2023. Margem ampla mediana é calculada sobre a receita corrente líquida; as demais vêm do Comparativo.</p></div>
  <div class="vh" style="margin-top:24px"><h2>Comparar municípios</h2></div>
  <p class="lead">Cada ponto é um município com margem calculada em 2023; o traço é a mediana da UF. Os círculos A e B são os municípios escolhidos, o que mostra se a diferença entre eles é do tamanho da diferença que existe dentro do estado.</p>
  <div class="row"><label>UF de A<select data-act="gUA2">${ufs.map(u=>opt(u,u,uA)).join('')}</select></label><label>Município A<select data-act="gMA">${LA.map(r=>opt(r.c,r.ente,A&&A.c)).join('')}</select></label>
  <label>UF de B<select data-act="gUB">${ufs.map(u=>opt(u,u,uB)).join('')}</select></label><label>Município B<select data-act="gMB">${LB.map(r=>opt(r.c,r.ente,B&&B.c)).join('')}</select></label></div>
  <div class="chartgrid"><div class="card chartcard">${svgStrip(rows,[{uf:uA,v:A&&A.mp*100,cor:'var(--accent)',t:'A'},{uf:uB,v:B&&B.mp*100,cor:'var(--bad)',t:'B'}])}<p>Margem ampla, % da RCL. ${diff==null?'':'A menos B: '+nf1.format(diff)+' ponto(s) percentual(is).'}</p></div>
  <div>${card(A,LA,uA,'var(--accent)','A')}${card(B,LB,uB,'var(--bad)','B')}</div></div>
  <p class="muted">Leitura com cuidado: municípios de estados com cobertura insuficiente representam só parte do estado, e a margem aqui é a ampla, sem descontar a folha. É descrição de 2023, não explicação.</p>`;
}
const _rg=renderGraficos;renderGraficos=function(){_rg();$('#v-graficos').insertAdjacentHTML('beforeend',gCmpHTML())};R.graficos=renderGraficos;if(!$('#v-graficos').hidden)renderGraficos();
document.addEventListener('change',e=>{const t=e.target,a=t.dataset&&t.dataset.act;if(!a)return;
 if(a==='gMet'){S.gMet=t.value}else if(a==='gUA'||a==='gUA2'){S.gUA=t.value;S.gMA=null}else if(a==='gMA'){S.gMA=t.value}else if(a==='gUB'){S.gUB=t.value;S.gMB=null}else if(a==='gMB'){S.gMB=t.value}else return;
 renderGraficos()});
/*GCMP-END*/
'''
h=open(H,encoding='utf8').read()
h=re.sub(r'\n/\*GCMP-START\*/.*?/\*GCMP-END\*/\n','\n',h,flags=re.S)
m='/* ---------- Roteamento e eventos ---------- */';assert m in h
# precisa vir depois de R=... : colocar antes do fechamento do script
i=h.rindex('</script>');h=h[:i]+JS+h[i:]
open(H,'w',encoding='utf8').write(h);print('ok')
