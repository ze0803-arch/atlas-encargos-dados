#!/usr/bin/env python3
"""Mostra a margem estrita (além da ampla) nas telas reais: Resultados, Início, Ficha, Gráficos, Comparativo.
Rodar por último (após build_graficos_comparar.py). Idempotente."""
import re
H='prototipo/atlas_prototipo.html'; h=open(H,encoding='utf8').read()
def sub(old,new,cnt=1,must=True):
    global h
    if new in h: return
    assert old in h or not must, old[:80]
    h=h.replace(old,new,cnt)
# helper (hoisted) logo após PILOTO
if 'function MEp(' not in h:
    i=h.index('const PILOTO='); j=h.index('\n',i)
    h=h[:j+1]+"function MEp(r){return(r.me!=null&&r.m&&r.mp!=null)?r.mp*r.me/r.m:null}\n"+h[j+1:]
# Resultados reais: cards, UF, porte, tabela
sub("""<div class="card stat"><div class="n">${mm(medn(calc.map(r=>r.mp)))}</div><div class="l">Margem ampla mediana (% da RCL)</div></div>""",
 """<div class="card stat"><div class="n">${mm(medn(calc.map(r=>r.mp)))}</div><div class="l">Margem ampla mediana (% da RCL)</div></div>
   <div class="card stat"><div class="n">${mm(medn(calc.map(MEp).filter(v=>v!=null)))}</div><div class="l">Margem estrita mediana (% da RCL), depois da folha paga com recurso livre</div></div>""")
sub("m:medn(c.map(r=>r.mp))}});\n  const porFx","m:medn(c.map(r=>r.mp)),e:medn(c.map(MEp).filter(v=>v!=null))}});\n  const porFx")
sub("m:medn(c.map(r=>r.mp))}});\n  const pct","m:medn(c.map(r=>r.mp)),e:medn(c.map(MEp).filter(v=>v!=null))}});\n  const pct")
sub('<th class="num">Margem ampla mediana (% RCL)</th></tr></thead><tbody>\n  ${porFx','<th class="num">Margem ampla mediana (% RCL)</th><th class="num">Margem estrita mediana (% RCL)</th></tr></thead><tbody>\n  ${porFx')
sub('<th class="num">Margem ampla mediana (% RCL)</th></tr></thead><tbody>\n  ${porUF','<th class="num">Margem ampla mediana (% RCL)</th><th class="num">Margem estrita mediana (% RCL)</th></tr></thead><tbody>\n  ${porUF')
sub("<td class=\"num\">${mm(p.m)}</td></tr>`).join('')}\n  </tbody></table></div>\n  <h3>Por porte","<td class=\"num\">${mm(p.m)}</td><td class=\"num\">${mm(p.e)}</td></tr>`).join('')}\n  </tbody></table></div>\n  <h3>Por porte")
sub("<td class=\"num\">${mm(p.m)}</td></tr>`).join('')}\n  </tbody></table></div>\n  <p class=\"muted\">Motivos","<td class=\"num\">${mm(p.m)}</td><td class=\"num\">${mm(p.e)}</td></tr>`).join('')}\n  </tbody></table></div>\n  <p class=\"muted\">Motivos")
sub('<th class="num">Margem estrita (R$ mi)</th><th>Situação</th>','<th class="num">Margem estrita (R$ mi)</th><th class="num">Margem estrita (% RCL)</th><th>Situação</th>')
sub("${r.me==null?'—':nf1.format(r.me/1e6)}</td><td>${r.st==='calc'","${r.me==null?'—':nf1.format(r.me/1e6)}</td><td class=\"num\">${MEp(r)==null?'—':nf1.format(MEp(r)*100)+'%'}</td><td>${r.st==='calc'")
# Início real
sub("""<div class="l">margem ampla mediana, % da RCL</div></div>
  </div>
  <h3>As etapas</h3>""","""<div class="l">margem ampla mediana, % da RCL</div></div>
   <div class="card stat"><div class="n">${nf1.format(100*medn(calc.map(MEp).filter(v=>v!=null)))}%</div><div class="l">margem estrita mediana, % da RCL</div></div>
  </div>
  <h3>As etapas</h3>""")
# Ficha
sub("""<div class="l">margem ampla, % da RCL</div></div>
   <div class="card stat"><div class="n">${(RD.PIBQ""","""<div class="l">margem ampla, % da RCL</div></div>
   <div class="card stat"><div class="n">${MEp(m)==null?'—':nf1.format(100*MEp(m))+'%'}</div><div class="l">margem estrita, % da RCL (depois da folha paga com recurso livre)</div></div>
   <div class="card stat"><div class="n">${(RD.PIBQ""")
# Gráficos: indicador estrita por UF
sub("mp:['Margem ampla mediana, % da RCL','mp'],","mp:['Margem ampla mediana, % da RCL','mp'],me:['Margem estrita mediana, % da RCL','me'],")
sub("return COMP.uf.map(x=>{const a=(by[x.uf]||[]).slice().sort((p,q)=>p-q);return Object.assign({},x,{mp:a.length?medn(a):null,nmp:a.length})});",
    "const be={};PILOTO.filter(r=>r.st==='calc'&&MEp(r)!=null).forEach(r=>{(be[r.uf]=be[r.uf]||[]).push(MEp(r)*100)});\n  return COMP.uf.map(x=>{const a=(by[x.uf]||[]).slice().sort((p,q)=>p-q),e=be[x.uf]||[];return Object.assign({},x,{mp:a.length?medn(a):null,me:e.length?medn(e):null,nmp:a.length})});")
# Gráficos: comparar municípios com seletor de medida
sub("""<label>Indicador<select data-act="gMet">""","""<label>Medida nos municípios<select data-act="gMed"><option value="amp"${(S.gMed||'amp')==='amp'?' selected':''}>Margem ampla</option><option value="est"${S.gMed==='est'?' selected':''}>Margem estrita</option></select></label><label>Indicador<select data-act="gMet">""")
sub("const uA=S.gUA||'RN'","const md=S.gMed==='est'?(r=>{const v=MEp(r);return v==null?null:v}):(r=>r.mp),mdn=S.gMed==='est'?'estrita':'ampla',uA=S.gUA||'RN'")
sub("const calcDe=u=>PILOTO.filter(r=>r.uf===u&&r.st==='calc'&&r.mp!=null)","const calcDe=u=>PILOTO.filter(r=>r.uf===u&&r.st==='calc'&&r.mp!=null&&(S.gMed!=='est'||MEp(r)!=null))")
h=h.replace("const o=L.slice().sort((a,b)=>b.mp-a.mp)","const o=L.slice().sort((a,b)=>md(b)-md(a))")
h=h.replace("<b>${nf1.format(m.mp*100)}%</b> margem ampla da RCL<br>","<b>${nf1.format(md(m)*100)}%</b> margem ${mdn} da RCL (ampla ${nf1.format(m.mp*100)}% · estrita ${MEp(m)==null?'—':nf1.format(MEp(m)*100)+'%'})<br>")
h=h.replace("Mediana da UF: ${nf1.format(medn(L.map(r=>r.mp*100)))}%","Mediana da UF: ${nf1.format(medn(L.map(r=>md(r)*100)))}%")
h=h.replace("rows=[{l:uA,v:LA.map(r=>r.mp*100)}];if(uB!==uA)rows.push({l:uB,v:LB.map(r=>r.mp*100)});","rows=[{l:uA,v:LA.map(r=>md(r)*100)}];if(uB!==uA)rows.push({l:uB,v:LB.map(r=>md(r)*100)});")
h=h.replace("const diff=A&&B?(A.mp-B.mp)*100:null;","const diff=A&&B?(md(A)-md(B))*100:null;")
h=h.replace("{uf:uA,v:A&&A.mp*100,","{uf:uA,v:A&&md(A)*100,").replace("{uf:uB,v:B&&B.mp*100,","{uf:uB,v:B&&md(B)*100,")
h=h.replace("<p>Margem ampla, % da RCL. ${diff==null","<p>Margem ${mdn}, % da RCL. ${diff==null")
if "a==='gMed'" not in h: h=h.replace("if(a==='gMet'){S.gMet=t.value}","if(a==='gMed'){S.gMed=t.value;S.gMA=null;S.gMB=null}else if(a==='gMet'){S.gMet=t.value}",1)
# Comparativo: tabela por UF com ampla e estrita (medianas da UF a partir dos municípios)
sub("${tb(COMP.uf.map(x=>({uf:x.uf,n:I0(x.n),cob:I0(x.cob),pib:x.pib,m_rt:x.m_rt,vinc:x.vinc,leitura:","${tb(gUFdata().map(x=>({uf:x.uf,n:I0(x.n),cob:I0(x.cob),pib:x.pib,m_rt:x.m_rt,mpa:x.mp==null?'—':nf1.format(x.mp),mpe:x.me==null?'—':nf1.format(x.me),vinc:x.vinc,leitura:")
sub("['m_rt','Margem, % da receita total',1],['vinc','Vinculada, %',1]","['m_rt','Margem, % da receita total',1],['mpa','Margem ampla, % da RCL (mediana)',1],['mpe','Margem estrita, % da RCL (mediana)',1],['vinc','Vinculada, %',1]")
open(H,'w',encoding='utf8').write(h);print('ok')
