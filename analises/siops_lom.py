import csv,gzip,re,html,glob,os,json
def txt(p):
    h=gzip.open(p,'rt',encoding='utf-8',errors='ignore').read()
    h=re.sub(r'<(script|style)[\s\S]*?</\1>','',h)
    h=re.sub(r'</(tr|p|div)>','\n',h);h=re.sub(r'</t[dh]>',' | ',h);h=re.sub(r'<[^>]+>','',h);h=html.unescape(h)
    return [re.sub(r'\s+',' ',l).strip() for l in h.split('\n') if l.strip()]
num=lambda s:float(s.replace('.','').replace(',','.')) if re.fullmatch(r'-?[\d.]+,\d+',s) else None
out={}
for p in sorted(glob.glob('raw/siops/2023/*.html.gz')):
    k=os.path.basename(p)[:7];L=txt(p);d={}
    for l in L:
        if 'TOTAL DAS RECEITAS RESULTANTES' in l.upper() and '(III)' in l:
            v=[num(x.strip()) for x in l.split('|')[1:]];v=[x for x in v if x is not None];d['III_prev']=v[1] if len(v)>1 else None;d['III_real']=v[2] if len(v)>2 else None
        if '(XVII)' in l and 'x 15%' in l:
            v=[num(x.strip()) for x in l.split('|')[1:]];v=[x for x in v if x is not None];d['xvii15']=v[0] if v else None
        if '(XVII)' in l and 'Lei Org' in l.replace('Ã¢','â'):
            v=[num(x.strip()) for x in l.split('|')[1:]];v=[x for x in v if x is not None];d['xviiLOM']=v[0] if v else None
    out[k]=d
json.dump(out,open('/tmp/siops_lom.json','w'))
print(len(out),sum(1 for d in out.values() if d.get('xviiLOM')),sum(1 for d in out.values() if d.get('xvii15')),sum(1 for d in out.values() if d.get('III_real')))
