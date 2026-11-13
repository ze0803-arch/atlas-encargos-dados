import csv,glob,gzip,json,statistics as st,sys
B='raw/siconfi/2023/'
rows=[x for x in csv.DictReader(open('resultado_2023.csv')) if x['status']=='calculado' and x['fonte_msc']=='MSCE' and x['convencao']=='liq+']
out=[]
for x in rows:
    k=x['cod_ibge']; it=[]
    for f in glob.glob(f'{B}msce/*_{k}_msce_p*.json.gz'): it+=json.load(gzip.open(f)).get('items',[])
    fu=pes=fu12=0.0; prec=0.0; prec_livre=0.0; cos_r=cos_d=0.0; fu_rec=0.0
    for i in it:
        cc=i['conta_contabil']; fr=(i['fonte_recursos'] or ''); s=1 if i['natureza_conta']=='D' else -1; v=i['valor']*s
        if cc in('622130300','622130400','622130700'):
            nd=i['natureza_despesa'] or ''
            if fr in('1540','1541','1542','1543'):
                fu+=v
                if nd[1:2]=='1': pes+=v
            if nd[4:6]=='91': 
                prec+=v
                if fr in('1500','1501'): prec_livre+=v
            if fr=='1751': cos_d+=v
        elif cc=='621200000':
            nr=i['natureza_receita'] or ''
            if nr[:1] in('1','2',''):
                if fr in('1540','1541','1542','1543'): fu_rec+=v
                if fr=='1751': cos_r+=v
    out.append((k,x['uf'],float(x['base_impostos']),fu,pes,fu_rec,prec,prec_livre,cos_r,cos_d,float(x['rec_livre'] or 0)))
json.dump(out,open('../med_fundeb.json','w'))
q=lambda v:[round(sorted(v)[int(p*(len(v)-1))],3) for p in(0,.1,.5,.9,1)] if v else None
print(len(out))
print('FUNDEB despesa liq / receita FUNDEB',q([o[3]/o[5] for o in out if o[5]>0]))
print('pessoal/ despesa fundeb',q([o[4]/o[3] for o in out if o[3]>0]))
print('n com pessoal/desp fundeb>=0.7',sum(1 for o in out if o[3]>0 and o[4]/o[3]>=0.7),'de',sum(1 for o in out if o[3]>0))
print('prec/base',q([o[6]/o[2] for o in out if o[2]>0]),'n>0',sum(o[6]>0 for o in out))
print('prec livre / rec livre',q([o[7]/o[10] for o in out if o[10]>0]),'n>0',sum(o[7]>0 for o in out))
print('COSIP receita n>0',sum(o[8]>0 for o in out),'desp n>0',sum(o[9]>0 for o in out),'desp/rec',q([o[9]/o[8] for o in out if o[8]>0]))
