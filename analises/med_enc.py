import csv,glob,gzip,json,collections,statistics as st
B='raw/siconfi/2023/'
rows=[x for x in csv.DictReader(open('resultado_2023.csv')) if x['status']=='calculado' and x['fonte_msc']=='MSCE' and x['convencao']=='liq+']
out=[]; elem=collections.Counter(); elem_n=collections.Counter()
for x in rows:
    k=x['cod_ibge']; it=[]
    for f in glob.glob(f'{B}msce/*_{k}_msce_p*.json.gz'): it+=json.load(gzip.open(f)).get('items',[])
    d=collections.defaultdict(float); tot=0.0
    for i in it:
        if i['conta_contabil'] in('622130300','622130400','622130700'):
            nd=i['natureza_despesa'] or ''; v=i['valor']*(1 if i['natureza_conta']=='D' else -1); fr=i['fonte_recursos'] or ''
            tot+=v; d['el'+nd[4:6]]+=v; d['gr'+nd[1:2]]+=v
            if i['funcao']=='08': d['f08']+=v; 
            if i['funcao']=='08' and fr in('1500','1501'): d['f08livre']+=v
            if i['funcao']=='08' and fr=='1660': d['f08fnas']+=v
            if nd[4:6]=='13' and fr in('1500','1501'): d['el13livre']+=v
            if nd[4:6]=='47' and fr in('1500','1501'): d['el47livre']+=v
            if nd[4:6]=='71': d['el71']+=v
            if nd[4:6]=='71' and fr in('1500','1501'): d['el71livre']+=v
    out.append((k,x['uf'],float(x['base_impostos']),float(x['rec_livre'] or 0),tot,dict(d)))
json.dump(out,open('../med_enc.json','w'))
q=lambda v:[round(sorted(v)[int(p*(len(v)-1))],4) for p in(0,.1,.5,.9,1)] if v else None
n=len(out); print(n)
for lab,key,den in [('el13 patronal /desp total','el13',4),('el13 livre / rec livre','el13livre',3),('el47 PASEP etc /desp total','el47',4),('el47 livre / rec livre','el47livre',3),('f08 /desp total','f08',4),('f08 livre/rec livre','f08livre',3),('f08 FNAS / f08','f08fnas','f08'),('el71 consórcio /desp total','el71',4),('el71 livre /rec livre','el71livre',3)]:
    v=[]
    for o in out:
        a=o[5].get(key,0.0); b=(o[den] if isinstance(den,int) else o[5].get(den,0.0))
        if b and b>0: v.append(a/b)
    print(lab,'n>0',sum(1 for o in out if o[5].get(key,0)>0),q(v))
