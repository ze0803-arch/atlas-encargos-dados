#!/usr/bin/env python3
"""Contrapartida de convênios da União por município (bloco P, D39). Entrada: 20261023_Convenios.zip descompactado
(Convenios.csv e Convenios_OrdensBancarias.csv, de portaldatransparencia.gov.br/download-de-dados/convenios/<ano>).
Uso: python convenios.py --pasta dados --csvs pasta_dos_csv --ano 2023  -> <pasta>/convenios_<ano>.csv
Método: contrapartida do ano = contrapartida total x (liberado no ano / valor do convênio), teto 1; liga a prefeitura pelo CNPJ de entes.json."""
import argparse
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--csvs', required=True); ap.add_argument('--ano', default='2023'); A = ap.parse_args()
import pandas as pd, numpy as np, json
D=A.csvs.rstrip('/')+'/'
ANO=int(A.ano)
import glob
F1=sorted(glob.glob(D+'*_Convenios.csv'))[-1]; F2=sorted(glob.glob(D+'*_Convenios_OrdensBancarias.csv'))[-1]
c=pd.read_csv(F1,sep=';',encoding='latin1',dtype=str); c.columns=[x.strip() for x in c.columns]
for col in ['VALOR CONVÊNIO','VALOR LIBERADO','VALOR CONTRAPARTIDA']: c[col]=c[col].str.replace('.','',regex=False).str.replace(',','.',regex=False).astype(float)
c['cnpj']=c['CÓDIGO CONVENENTE'].str.replace(r'\D','',regex=True).str.zfill(14)
ent={str(e['cod_ibge']):str(e['cnpj']).zfill(14) for e in json.load(open(A.pasta+'/entes.json')) if e['esfera']=='M'}
inv={v:k for k,v in ent.items()}
m=c[c['cnpj'].isin(inv)].copy(); m['cod_ibge']=m['cnpj'].map(inv)
print('convênios com convenente = prefeitura:',len(m),'de',len(c[c['TIPO CONVENENTE']=='Administração Pública Municipal']))
o=pd.read_csv(F2,sep=';',encoding='latin1',dtype=str); o.columns=[x.strip() for x in o.columns]
o['v']=o['VALOR LIBERADO'].str.replace('.','',regex=False).str.replace(',','.',regex=False).astype(float); o['ano']=pd.to_datetime(o['DATA EMISSÃO OB'],format='%d/%m/%Y',errors='coerce').dt.year
o23=o[o.ano==ANO].groupby('NÚMERO CONVÊNIO')['v'].sum().rename('lib_ano')
m=m.merge(o23,left_on='NÚMERO CONVÊNIO',right_index=True,how='inner'); m=m[m['VALOR CONVÊNIO']>0]
m['cp_ano']=np.minimum(m['lib_ano']/m['VALOR CONVÊNIO'],1.0)*m['VALOR CONTRAPARTIDA']
g=m.groupby('cod_ibge').agg(convenios_liberado=('lib_ano','sum'),contrapartida_ano=('cp_ano','sum'),n_convenios=('lib_ano','size')).reset_index()
g.to_csv(A.pasta+'/convenios_'+A.ano+'.csv',index=False)
print('Gravado', A.pasta+'/convenios_'+A.ano+'.csv', len(g), 'municípios')
