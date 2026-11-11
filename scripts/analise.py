import gzip,json,glob,csv,collections,re,os
B='raw/siconfi/2023/'
def load(rel,cod):
    out=[]
    for f in sorted(glob.glob(f'{B}{rel}/*_{cod}_{rel}_p*.json.gz')):
        out+=json.load(gzip.open(f)).get('items',[])
    return out
LIVRE={'500','501'}  # fonte[1:] recursos não vinculados (hipótese a validar)
rows=[]
import json as _j
_ent={str(e['cod_ibge']):e for e in _j.load(open('../entes.json'))}
_cods=sorted(set(os.path.basename(f).split('_')[2] for f in glob.glob(B+'extrato_entregas/*.json.gz')))
am=[dict(cod_ibge=c,ente=_ent[c]['ente'],uf=_ent[c]['uf'],populacao=_ent[c]['populacao'],faixa='',motivo='') for c in _cods if c in _ent]
for m in am:
    c=m['cod_ibge']; r=dict(cod_ibge=c,ente=m['ente'],uf=m['uf'],pop=int(m['populacao']),faixa=m['faixa'],motivo=m['motivo'])
    ms=load('msce',c); r['n_msce']=len(ms)
    dc=load('dca_IC',c); dd=load('dca_ID',c)
    r['dca_rec']=next((i['valor'] for i in dc if i['cod_conta']=='ReceitasExcetoIntraOrcamentarias' and i['coluna']=='Receitas Brutas Realizadas'),None)
    r['dca_liq']=next((i['valor'] for i in dd if i['cod_conta']=='TotalDespesas' and i['coluna']=='Despesas Liquidadas'),None)
    rc=load('rreo_anexo03',c); r['n_rreo3']=len(rc)
    r['rcl_rreo']=next((i['valor'] for i in rc if i['cod_conta']=='RREO3ReceitaCorrenteLiquida' and i['coluna'].startswith('TOTAL')),None)
    rg=load('rgf_anexo01_E',c)
    r['rcl_rgf']=next((i['valor'] for i in rg if i['cod_conta']=='ReceitaCorrenteLiquidaAjustada' ),None)
    r['pessoal_rgf']=next((i['valor'] for i in rg if i['cod_conta']=='DespesaComPessoalTotal'),None)
    rec=liq=recA=recB=base=0.0; rl=0.0; leg=div=prec=pes13=pesoutro=min_=0.0
    for i in ms:
        cc=i['conta_contabil']; sg=1 if i['natureza_conta']=='D' else -1; v=i['valor']*sg; nat=(i['natureza_receita'] or '')[:1]
        fr=(i['fonte_recursos'] or '')[1:]
        if cc=='621200000':
            if nat in('1','2'):
                recA+=i['valor'] if sg==1 else 0; recB+=v
                nr=i['natureza_receita']
                if nr[:3]=='111' or nr[:4] in('1711','1721'): base+=v
                if fr in LIVRE: rl+=v
        elif cc in('622130300','622130400','622130700'):
            liq+=v
            if fr in LIVRE:
                nd=i['natureza_despesa'] or ''
                g=nd[1:2]; e=nd[4:6]
                po=(i['poder_orgao'] or '')[:1]
                if po=='2': leg+=v
                elif g in('2','6'): div+=v
                elif e=='91': prec+=v
                elif i['funcao'] in('10','12'): min_+=v
                elif g=='1': pesoutro+=v
    rec=recA if abs(recA/(r['dca_rec'] or 1)-1)<=abs(recB/(r['dca_rec'] or 1)-1) else recB; r['rec_variante']='A_so_debito' if rec==recA else 'B_liquido_D-C'
    r['base_impostos']=base; r['minimos_exigidos']=0.40*base
    r.update(rec_msce=rec,liq_msce=liq,rec_livre=rl,leg=leg,divida=div,prec=prec,minimos_funcao=min_,folha_livre=pesoutro)
    r['rec_dif']=(rec/r['dca_rec']-1) if r['dca_rec'] and rec else None
    r['liq_dif']=(liq/r['dca_liq']-1) if r['dca_liq'] and liq else None
    fl=[]
    if r['n_msce']==0: fl.append('SEM_MSCE')
    elif r['n_msce']<=30: fl.append('MSCE_INCOMPLETA')
    else:
        if r['rec_dif'] is None or abs(r['rec_dif'])>0.01: fl.append('REC_DIVERGE')
        if r['liq_dif'] is None or abs(r['liq_dif'])>0.01: fl.append('LIQ_DIVERGE')
    if not r['n_rreo3']: fl.append('RREO3_VAZIO')
    pass  # RCL RREO x RGF: RGF só traz RCL ajustada (outra definição); conferência removida
    r['flags']='|'.join(fl) or 'OK'
    if fl and any(f in fl for f in('SEM_MSCE','MSCE_INCOMPLETA','REC_DIVERGE','LIQ_DIVERGE')):
        r['margem_ampla']=r['margem_estrita']=None; r['status']='marcado_nao_calculado'
    else:
        a=rl-r['minimos_exigidos']-leg-div-prec; r['margem_ampla']=a; r['margem_estrita']=a-pesoutro; r['status']='calculado'
    r['margem_ampla_pct_rcl']=(r['margem_ampla']/r['rcl_rreo']) if r['margem_ampla'] is not None and r['rcl_rreo'] else None
    rows.append(r)
cols=list(rows[0]); w=csv.DictWriter(open('resultado_2023.csv','w',newline=''),cols); w.writeheader(); w.writerows(rows)
print(collections.Counter(r['status'] for r in rows))
print(collections.Counter(f for r in rows for f in r['flags'].split('|')))
for r in rows:
    print(f"{r['ente'][:22]:22} {r['uf']} {r['n_msce']:5} rec{(r['rec_dif'] or 0)*100:7.1f}% liq{(r['liq_dif'] or 0)*100:7.1f}% {r['flags']:40} {r['status'][:4]} amp%RCL={'' if r['margem_ampla_pct_rcl'] is None else round(r['margem_ampla_pct_rcl']*100,1)}")
