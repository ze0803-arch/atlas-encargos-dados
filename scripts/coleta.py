import requests,json,gzip,hashlib,csv,time,os,threading,datetime,re,sys
from concurrent.futures import ThreadPoolExecutor
ROOT='atlas';ANO=2023
B="https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
S=requests.Session();lock=threading.Lock()
new=not os.path.exists(f'{ROOT}/diario_extracao.csv')
df=open(f'{ROOT}/diario_extracao.csv','a',newline='',encoding='utf-8');dw=csv.writer(df)
if new:dw.writerow(['data_hora_utc','fonte','relatorio','ente','url','http','linhas','resultado','tentativas','segundos','bytes_gz','sha256','arquivo'])
prog=open(f'{ROOT}/progresso.log','a',encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc)
def say(m):
    with lock:prog.write(now().strftime('%H:%M:%S ')+m+'\n');prog.flush()
def req(fonte,rel,ente,url,params=None,pagina=1,rows_key='items'):
    t0=time.time();http=None;body=None;tent=0;err=''
    for tent in range(1,4):
        try:
            r=S.get(url,params=params,timeout=180);http=r.status_code;final=r.url
            if http==200:body=r.content;break
        except Exception as e:err=str(e)[:80];final=url
        time.sleep(2*tent)
    try:final
    except NameError:final=url
    js=None;n=0;arq='';sha='';nb=0
    if body is not None:
        try:
            js=json.loads(body)
            n=len(js.get(rows_key,js.get('value',[]))) if isinstance(js,dict) else 0
        except Exception:js=None
        ts=now().strftime('%Y%m%dT%H%M%S')
        d=f'{ROOT}/raw/{fonte}/{ANO}/{rel}';os.makedirs(d,exist_ok=True)
        arq=f'{d}/{fonte}_{ANO}_{ente}_{rel}_p{pagina:03d}_{ts}.json.gz'
        gz=gzip.compress(body,mtime=0);open(arq,'wb').write(gz);sha=hashlib.sha256(gz).hexdigest();nb=len(gz)
    res='sucesso' if (http==200 and n>0) else ('vazio' if http==200 else 'erro')
    with lock:dw.writerow([now().strftime('%Y-%m-%dT%H:%M:%SZ'),fonte,rel,ente,final,http or err,n,res,tent,round(time.time()-t0,1),nb,sha,arq.replace(ROOT+'/','')]);df.flush()
    time.sleep(0.25)
    return js,n,res
def paged(fonte,rel,ente,ep,params):
    out=[];off=0;pg=1
    while True:
        p=dict(params);p['offset']=off
        js,n,res=req(fonte,rel,ente,B+ep,p,pg)
        if js is None:return out,res
        out+=js['items']
        if not js.get('hasMore'):return out,res
        off+=js.get('limit',5000);pg+=1
def muni(row):
    e=row['cod_ibge'];say('inicio '+row['ente']+' '+row['uf'])
    ex,_=paged('siconfi','extrato_entregas',e,'extrato_entregas',dict(id_ente=e,an_referencia=ANO))
    ent=set(x['entregavel'] for x in ex)
    rreo_simpl=any('Resumido de Execução Orçamentária Simplificado' in x for x in ent)
    rgf_simpl=any('Gestão Fiscal Simplificado' in x for x in ent)
    paged('siconfi','msce',e,'msc_orcamentaria',dict(id_ente=e,an_referencia=ANO,me_referencia=12,co_tipo_matriz='MSCE',classe_conta=6,id_tv='period_change'))
    tipos=['RREO Simplificado','RREO'] if rreo_simpl else ['RREO','RREO Simplificado']
    for an in ('03','01'):
        for t in tipos:
            r,res=paged('siconfi','rreo_anexo'+an,e,'rreo',dict(an_exercicio=ANO,nr_periodo=6,co_tipo_demonstrativo=t,no_anexo='RREO-Anexo '+an,id_ente=e))
            if r:break
    combos=[('RGF Simplificado','S',2),('RGF','Q',3),('RGF','S',2)] if rgf_simpl else [('RGF','Q',3),('RGF Simplificado','S',2),('RGF','S',2)]
    for an,pod in (('01','E'),('01','L'),('02','E')):
        for t,per,nr in combos:
            r,res=paged('siconfi','rgf_anexo%s_%s'%(an,pod),e,'rgf',dict(an_exercicio=ANO,in_periodicidade=per,nr_periodo=nr,co_tipo_demonstrativo=t,no_anexo='RGF-Anexo '+an,co_esfera='M',co_poder=pod,id_ente=e))
            if r:break
    for an in ('I-C','I-D','I-E'):
        paged('siconfi','dca_'+an.replace('-',''),e,'dca',dict(an_exercicio=ANO,no_anexo='DCA-Anexo '+an,id_ente=e))
    say('fim '+row['ente'])
rows=list(csv.DictReader(open(f'{ROOT}/amostra_piloto.csv',encoding='utf-8')))
# IBGE
def ibge():
    for rel,url in (('censo2022_pop_t4714','https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022'),('pib_t5938','https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/2021,2022,2023')):
        req('ibge',rel,'todos',url,None,1,'')
# SIOPE
def siope():
    base='https://www.fnde.gov.br/olinda-ide/servico/DADOS_ABERTOS_SIOPE/versao/v1/odata/'
    meta=S.get(base+'$metadata',timeout=60).text
    fns={m.group(1):re.findall(r'<Parameter Name="(\w+)"',m.group(2)) for m in re.finditer(r'<Function Name="(\w+)" IsComposable="true">(.*?)<ReturnType',meta,re.S)}
    ufs=sorted(set(r['uf'] for r in rows))
    for fn in ('Indicadores_Siope','Receita_Siope','Despesas_Siope','Remuneracao_Siope'):
        ps=fns.get(fn)
        for uf in ufs:
            vals={'Ano_Consulta':str(ANO),'Num_Peri':'6','Sig_UF':"'%s'"%uf}
            if not ps or any(p not in vals for p in ps):
                req('siope',fn,uf,base+fn,None);continue
            args=','.join('%s=%s'%(p,vals[p]) for p in ps)
            skip=0;pg=1
            while True:
                url=f"{base}{fn}({args})?$format=json&$top=50000&$skip={skip}"
                js,n,res=req('siope',fn,uf,url,None,pg,'value')
                if js is None or n<50000:break
                skip+=50000;pg+=1
    say('siope fim')
def main():
    say('ibge');ibge()
    say('siope');
    th=threading.Thread(target=siope);th.start()
    with ThreadPoolExecutor(4) as ex:list(ex.map(muni,rows))
    th.join();say('TUDO CONCLUIDO')
main()
