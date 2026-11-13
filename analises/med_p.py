import csv,glob,gzip,json,collections,statistics as st
B='raw/siconfi/2023/'
G={'saude_sus':('1600','1601','1602','1603','1604'),'assist_fnas':('1660',),'fnde':('1550','1551','1552','1553','1569'),'convenios':('1570','1700')}
rows=[x for x in csv.DictReader(open('resultado_2023.csv')) if x['status']=='calculado' and x['fonte_msc']=='MSCE' and x['convencao']=='liq+']
out=[]
for x in rows:
    k=x['cod_ibge']; it=[]
    for f in glob.glob(f'{B}msce/*_{k}_msce_p*.json.gz'): it+=json.load(gzip.open(f)).get('items',[])
    r=collections.defaultdict(float)
    for i in it:
        if i['conta_contabil']=='621200000':
            nr=i['natureza_receita'] or ''
            if nr[:1] in('1','2',''):
                fr=i['fonte_recursos'] or ''; v=i['valor']*(1 if i['natureza_conta']=='D' else -1); r['tot']+=v
                for g,fs in G.items():
                    if fr in fs: r[g]+=v
    out.append((k,x['uf'],float(x['rec_livre'] or 0),dict(r)))
json.dump(out,open('../med_p.json','w'))
q=lambda v:[round(sorted(v)[int(p*(len(v)-1))],4) for p in(0,.1,.5,.9,1)]
print(len(out))
for g in G:
    v=[o[3].get(g,0)/o[3]['tot'] for o in out if o[3].get('tot',0)>0]
    print(g,'n>0',sum(1 for o in out if o[3].get(g,0)>0),'% da receita total',q(v))
v=[sum(o[3].get(g,0) for g in G)/o[3]['tot'] for o in out if o[3].get('tot',0)>0]; print('P total / receita',q(v))
