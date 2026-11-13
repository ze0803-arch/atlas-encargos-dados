import gzip,json,glob,csv,collections,sys
sys.path.insert(0,'..')
exec(open('../comp.py').read().split("R={r['cod_ibge']")[0])  # load(), siops()
R={r['cod_ibge']:r for r in csv.DictReader(open('resultado_2023.csv'))}
C=[c for c in csv.DictReader(open('comparacao_siops_2023.csv')) if c['status']=='calculado' and c['diferenca_pct']!='']
fp=['Serrolândia','Sítio do Quinto','Guaçuí','Jaguaribara','Água Nova','Francisco Dantas','Mundo Novo','Mutuípe','Nova Itarana','Cardeal da Silva','Campinaçu','Itapirapuã','Pauini','Taipu','Érico Cardoso','Araguapaz','Itapiranga']
def comp(k):
    ms=load(k);g=collections.defaultdict(float);ded=collections.defaultdict(float)
    for i in ms:
        if i['conta_contabil']!='621200000':continue
        nr=i['natureza_receita'] or '';sg=1 if i['natureza_conta']=='D' else -1
        if nr[:4]=='1711':g[nr]+=i['valor']*sg
        if nr[:1]=='9':ded[nr]+=i['valor']*sg
    return g,ded
out=[]
for c in C:
    k=c['cod_ibge']
    if c['ente'] in fp: grp='exc'
    elif abs(float(c['diferenca_pct']))<=1 and c['uf'] in('BA','CE','RN'): grp='ctl'
    else: continue
    g,ded=comp(k);S=siops(k)
    fpm=g.get('17115111',0);de=g.get('17115121',0)
    sgn=1 if fpm>0 else -1
    fpm*=sgn;de*=sgn
    # dedução Fundeb sobre FPM: naturezas 9171151* 
    dfp=sum(v for n,v in ded.items() if n.startswith('9171151') or n.startswith('917115'))*sgn
    ded_tot=sum(ded.values())*sgn
    sf=S.get('FPM',0)
    out.append((grp,c['ente'],c['uf'],fpm,de,dfp,ded_tot,sf,dict(ded)))
json.dump(out,open('/tmp/fpm.json','w'),ensure_ascii=False)
for grp in('exc','ctl'):
    print('==',grp)
    for g_,e,u,fpm,de,dfp,dt,sf,dd in [o for o in out if o[0]==grp][:20]:
        gap=fpm-de-sf
        print(f"{e[:18]:18} {u} FPM={fpm/1e6:6.2f} de={de/1e6:5.2f} dedFPM={dfp/1e6:6.2f} dedTot={dt/1e6:6.2f} SIOPS={sf/1e6:6.2f} gap(FPM-de-SIOPS)={gap/1e6:6.2f} SIOPS/(FPM)={sf/fpm if fpm else 0:5.3f} SIOPS/(FPM-de)={sf/(fpm-de) if fpm-de else 0:5.3f}")
