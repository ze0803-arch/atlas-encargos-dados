import pandas as pd, numpy as np, json, csv
D='conv/'
c=pd.read_csv(D+'20261023_Convenios.csv',sep=';',encoding='latin1',dtype=str); c.columns=[x.strip() for x in c.columns]
for col in ['VALOR CONVÊNIO','VALOR LIBERADO','VALOR CONTRAPARTIDA']: c[col]=c[col].str.replace('.','',regex=False).str.replace(',','.',regex=False).astype(float)
c['cnpj']=c['CÓDIGO CONVENENTE'].str.replace(r'\D','',regex=True).str.zfill(14)
ent={str(e['cod_ibge']):str(e['cnpj']).zfill(14) for e in json.load(open('atlas/entes.json')) if e['esfera']=='M'}
inv={v:k for k,v in ent.items()}
m=c[c['cnpj'].isin(inv)].copy(); m['cod_ibge']=m['cnpj'].map(inv)
print('convênios com convenente = prefeitura:',len(m),'de',len(c[c['TIPO CONVENENTE']=='Administração Pública Municipal']))
o=pd.read_csv(D+'20261023_Convenios_OrdensBancarias.csv',sep=';',encoding='latin1',dtype=str); o.columns=[x.strip() for x in o.columns]
o['v']=o['VALOR LIBERADO'].str.replace('.','',regex=False).str.replace(',','.',regex=False).astype(float); o['ano']=pd.to_datetime(o['DATA EMISSÃO OB'],format='%d/%m/%Y',errors='coerce').dt.year
o23=o[o.ano==2023].groupby('NÚMERO CONVÊNIO')['v'].sum().rename('lib23')
m=m.merge(o23,left_on='NÚMERO CONVÊNIO',right_index=True,how='inner'); m=m[m['VALOR CONVÊNIO']>0]
m['cp23']=np.minimum(m['lib23']/m['VALOR CONVÊNIO'],1.0)*m['VALOR CONTRAPARTIDA']
g=m.groupby('cod_ibge').agg(convenios_lib_2023=('lib23','sum'),contrapartida_2023=('cp23','sum'),n_convenios=('lib23','size')).reset_index()
g.to_csv(D+'convenios_2023.csv',index=False)
r=pd.read_csv('atlas/resultado_2023.csv',dtype={'cod_ibge':str}); r=r[r.status=='calculado'].merge(g,on='cod_ibge',how='left').fillna({'convenios_lib_2023':0,'contrapartida_2023':0,'n_convenios':0})
rl=r[r.rec_livre>0]
f=lambda s:[round(x,4) for x in s.quantile([0,.1,.5,.9,1]).tolist()]
print('calculados',len(r),'com convênio liberado em 2023:',(r.n_convenios>0).sum())
print('liberado 2023 / rec livre',f(rl.convenios_lib_2023/rl.rec_livre)); print('contrapartida 2023 / rec livre',f(rl.contrapartida_2023/rl.rec_livre))
w=rl[rl.contrapartida_2023>0]; print('só com contrapartida>0 (n=%d)'%len(w),f(w.contrapartida_2023/w.rec_livre))
print('contrapartida/liberado total',round(rl.contrapartida_2023.sum()/rl.convenios_lib_2023.sum(),4))
print(w.groupby('uf').apply(lambda d:(d.contrapartida_2023/d.rec_livre).median()).round(4).to_dict())
