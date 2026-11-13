import csv,glob,gzip,json,sys
B='raw/siconfi/2023/'
def L(rel,k):
    o=[]
    for f in sorted(glob.glob(f'{B}{rel}/*_{k}_{rel}_p*.json.gz')): o+=json.load(gzip.open(f)).get('items',[])
    return o
res=[]
for l in csv.DictReader(open('comparacao_siops_2023.csv')):
    k=l['cod_ibge']; t=0.0; found=False
    for rel in ['msce']:
        for i in L(rel,k):
            if i['conta_contabil']=='621200000':
                nr=i['natureza_receita'] or ''
                if nr[:3]=='111':
                    t+=i['valor']*(1 if i['natureza_conta']=='D' else -1)
    trib=None
    for i in L('rreo_anexo01',k):
        if i['cod_conta']=='ReceitaTributaria' and i['coluna'].startswith('Até o Bimestre'): trib=i['valor']
    res.append((k,l['ente'],l['uf'],float(l['diferenca_pct']),t,trib))
json.dump(res,open('teste_trib.json','w'))
