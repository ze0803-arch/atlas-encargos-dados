import pandas as pd, numpy as np, json
U='/mnt/user-data/uploads/atlas-encargos-dados-main/atlas-encargos-dados-main/app_coleta/dados/resultado_2023.csv'
C='/home/claude/atlas-encargos-dados/catalogo/'
r=pd.read_csv(U); j=pd.read_csv(C+'juridico_base_2023.csv')[['cod_ibge','n_iss','n_iptu','n_itbi']]
p=pd.read_csv(C+'pib_2023.csv'); v=pd.read_csv('/tmp/th4/va.csv')
d=r.merge(j,on='cod_ibge',how='left').merge(p,on='cod_ibge',how='left').merge(v,on='cod_ibge',how='left')
bins=[0,5000,10000,20000,50000,100000,500000,1e12]; lab=['Até 5 mil','5–10 mil','10–20 mil','20–50 mil','50–100 mil','100–500 mil','Mais de 500 mil']
d['faixa']=pd.cut(d['pop'],bins,labels=lab); d['pibpc']=d.pib_mil*1000/d['pop']
tot=len(d); cal=d[d.status=='calculado'].copy()
print(tot,len(cal))
cal['m_rt']=cal.margem_ampla/cal.rec_msc*100
cal['e_rt']=cal.margem_estrita/cal.rec_msc*100
cal['m_rl']=cal.margem_ampla/cal.rec_livre*100
cal['vinc']=(1-cal.rec_livre/cal.rec_msc)*100
cal['m_pc']=cal.margem_ampla/cal['pop']
cal['rec_pc']=cal.rec_msc/cal['pop']
cal=cal[cal.m_rt.between(-100,100)&cal.pibpc.notna()]
cal['q']=pd.qcut(cal.pibpc.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
out={}
out['cob']={'total':int(tot),'calc':int(len(cal)),'por_uf':[[u,int((d.uf==u).sum()),int((cal.uf==u).sum())] for u in sorted(d.uf.unique())]}
g=cal.groupby('q')
out['h1']={k:[round(float(x),1) for x in g[c].median()] for k,c in dict(m_rt='m_rt',e_rt='e_rt',m_rl='m_rl',vinc='vinc',m_pc='m_pc',pib='pibpc',rec_pc='rec_pc').items()}
out['h1']['n']=[int(x) for x in g.size()]
gf=cal.groupby('faixa',observed=True)
out['faixas']=[[f,int(len(x)),round(float(x.m_rt.median()),1),round(float(x.e_rt.median()),1),round(float(x.vinc.median()),1),int((d.faixa==f).sum())] for f,x in gf]
# H3 por UF
rows=[]
for u,x in cal.groupby('uf'):
    if len(x)>=40:
        rho=x[['pibpc','m_rt']].corr(method='spearman').iloc[0,1]
        # terço rico x pobre dentro UF×faixa
        rows.append([u,len(x),int((d.uf==u).sum()),round(float(rho),2)])
    else: rows.append([u,len(x),int((d.uf==u).sum()),None])
out['h3']=rows
# pares: terço de maior PIB com margem maior, por UF×faixa
par=0;ok=0
for (u,f),x in cal.groupby(['uf','faixa'],observed=True):
    if len(x)>=9:
        x=x.sort_values('pibpc'); k=len(x)//3
        par+=1; ok+= x.m_rt.iloc[-k:].median()>x.m_rt.iloc[:k].median()
out['pares']=[par,ok]
# H4a
d2=d[d['pop']>0].copy()
for c,nm in (('n_iptu','iptu'),('n_iss','iss'),('n_itbi','itbi')):
    d2[nm+'_pc']=d2[c].fillna(0)/d2['pop']
cal2=cal.merge(d2[['cod_ibge','iptu_pc','iss_pc','itbi_pc','va_servicos_mil']],on='cod_ibge')
res={'IPTU':[], 'ISS':[], 'ITBI':[], 'Algum':[]}
flags=pd.DataFrame(index=cal2.index)
for nm in ('iptu','iss','itbi'):
    med=cal2.groupby(['uf','faixa'],observed=True)[nm+'_pc'].transform('median')
    flags[nm]=(cal2[nm+'_pc']<0.1*med)&(med>0)
flags['algum']=flags.any(axis=1)
for nm,key in (('iptu','IPTU'),('iss','ISS'),('itbi','ITBI'),('algum','Algum')):
    res[key]=[round(float(100*flags.loc[cal2.q==q,nm].mean()),1) for q in range(1,6)]
out['h4a']=res; out['h4a_tot']=round(float(100*flags.algum.mean()),1)
# H4b ISS decomposição
ok=cal.copy(); ok['iss_pc']=ok.n_iss.fillna(0)/ok['pop']; ok=ok[(ok.n_iss>0)&(ok.va_servicos_mil>0)].copy()
ok['vapc']=ok.va_servicos_mil*1000/ok['pop']; ok['aliq']=ok.n_iss/(ok.va_servicos_mil*1000)*100
gq=ok.groupby('q')
out['h4b']={'iss_pc':[round(float(x),0) for x in gq.iss_pc.median()],'va_pc':[round(float(x),0) for x in gq.vapc.median()],'aliq':[round(float(x),2) for x in gq.aliq.median()],'n':int(len(ok))}
l=lambda c: np.log(gq[c].median())
dl=l('iss_pc')[1]-l('iss_pc')[5]; dv=l('vapc')[1]-l('vapc')[5]
out['h4b']['parte_base']=round(float(100*dv/dl),0)
# municipios para dispersão
m=cal[['cod_ibge','ente','uf','pop','pibpc','m_rt','e_rt','vinc','q']].copy()
m['fx']=m['pop'].apply(lambda x: next(i for i,b in enumerate(bins[1:]) if x<=b))
arr=[[int(a.cod_ibge),a.ente,a.uf,int(a['pop']),int(a.pibpc),round(float(a.m_rt),1),round(float(a.e_rt),1),round(float(a.vinc),1),int(a.q),int(a.fx)] for _,a in m.iterrows()]
json.dump(arr,open('municipios.json','w'),ensure_ascii=False,separators=(',',':'))
t=json.load(open(C+'tabelas_projeto_2023.json'))
out['h2']={'pess_educ':t['t7']['pess_educ'],'custo':t['t7']['custo'],'pess_saude':t['t7']['pess_saude'],'rho':t['t7']['rho']}
out['t5']=t['t5']
json.dump(out,open('dados.json','w'),ensure_ascii=False,separators=(',',':'),default=lambda o: o.item() if hasattr(o,'item') else str(o))
print(json.dumps({k:out[k] for k in ('h1','faixas','h3','pares','h4a','h4a_tot','h4b','h2')},ensure_ascii=False)[:3500]); print(len(arr))
