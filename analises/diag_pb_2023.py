import re,gzip,json,glob,sys,collections
import pandas as pd
src=open('/home/claude/atlas-encargos-dados/app_coleta/analisar.py').read()
fn=src[src.index('def calcula'):src.index('ent = {')]
LIVRE={'500','501'}
exec(fn)
B='/tmp/w/dados/raw/siconfi/2023/'
def carrega(rel,cod):
    out=[]
    for f in sorted(glob.glob(f'{B}{rel}/*_{cod}_{rel}_p*.json.gz')): out+=json.load(gzip.open(f)).get('items',[])
    return out
r=pd.read_csv('/home/claude/atlas-encargos-dados/catalogo/resultado_2023.csv',dtype={'cod_ibge':str})
pb=r[(r.uf=='PB')&(r.fonte_msc=='MSCC_12m')&(r.status!='calculado')]
res=[]
for _,x in pb.iterrows():
    c=x.cod_ibge; meses={m:carrega('mscc_m%02d'%m,c) for m in range(1,13)}
    ne=[m for m,v in meses.items() if v]
    if len(ne)<12 or not x.dca_rec or not x.dca_liq: continue
    def best(itens):
        b=None
        for modo in (('liq',1),('liq',-1),('deb',1)):
            m=calcula(itens,modo); e=abs(m['rec']/x.dca_rec-1)+abs(m['liq']/x.dca_liq-1)
            if b is None or e<b[0]: b=(e,m['rec']/x.dca_rec-1,m['liq']/x.dca_liq-1)
        return b
    soma=sum((meses[m] for m in meses),[]); dez=meses[12]
    seen=set(); dd=[]
    for m in meses:
        for i in meses[m]:
            k=(m,i['entrada_msc'],i['conta_contabil'],i['natureza_conta'],i['valor'],i['natureza_receita'],i['fonte_recursos'],i['natureza_despesa'],i['funcao'],i['poder_orgao'])
            if k in seen: continue
            seen.add(k); dd.append(i)
    res.append(dict(c=c,dup=len(soma)-len(dd),dedup=best(dd)[0],soma=best(soma)[0],dez=best(dez)[0],ult=min(best(meses[m])[0] for m in (11,12))))
d=pd.DataFrame(res); print(len(d))
print('com duplicatas:',(d.dup>0).sum());
for k in ('soma','dedup','dez','ult'): print(k,'fecha (<=2%):',(d[k]<=0.02).sum(),' mediana erro',round(d[k].median(),3))
d.to_csv('/tmp/pb_teste2.csv',index=False)
