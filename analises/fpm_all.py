import gzip,json,glob,csv,collections,re,html,sys
from multiprocessing import Pool
exec(open('../comp.py').read().split("R={r['cod_ibge']")[0])
C={c['cod_ibge']:c for c in csv.DictReader(open('comparacao_siops_2023.csv'))}
def one(k):
    try:
        g=collections.defaultdict(float)
        for i in load(k):
            if i['conta_contabil']=='621200000' and (i['natureza_receita'] or '')[:4]=='1711':
                g[i['natureza_receita']]+=i['valor']*(1 if i['natureza_conta']=='D' else -1)
        f=g.get('17115111',0);de=g.get('17115121',0);s=1 if f>0 else -1
        S=siops(k)
        return k,f*s,de*s,S.get('FPM')
    except Exception as e: return k,None,None,None
if __name__=='__main__':
    with Pool(4) as p: res=p.map(one,list(C),chunksize=20)
    json.dump(res,open('/tmp/fpm_all.json','w'))
    print(len(res))
