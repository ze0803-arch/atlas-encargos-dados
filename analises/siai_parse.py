import re,subprocess,sys,json,csv,os
def num(s): return float(s.replace('.','').replace(',','.'))
NUM=r'-?\d{1,3}(?:\.\d{3})*,\d{2}'
def txt(p): return subprocess.run(['pdftotext','-layout',p,'-'],capture_output=True,text=True).stdout
def nums(l): return [num(x) for x in re.findall(NUM,l)]
def first(t,pat):
    for l in t.splitlines():
        if re.search(pat,l): 
            n=nums(l)
            if n: return n
    return None
def parse11(p):
    t=txt(p)
    b=first(t,r'^\s*3-\s*TOTAL DA RECEITA RESULTANTE DE IMPOSTOS')
    e=first(t,r'^\s*29-\s*APLICA')
    m=first(t,r'^\s*22-\s*TOTAL DAS DESPESAS DE MDE CUSTEADAS COM RECURSOS DE IMPOSTOS')
    return dict(base=b and b[-1], mde_exigido=e and e[0], mde_pct=e and e[-1], mde_impostos=m and m[-1])
def parse12(p):
    t=txt(p)
    mn=first(t,r'Despesa M[ií]nima a ser Aplicada em ASPS')
    ap=first(t,r'VALOR APLICADO EM ASPS \(XVI\)')
    return dict(asps_min=mn and mn[-1], asps_aplicado=ap and (ap[1] if len(ap)>1 else ap[0]))
if __name__=='__main__':
    d='siai/'; print(parse11(d+'serra_negra_rreo_2023_b6_anexo11.pdf'), parse12(d+'serra_negra_rreo_2023_b6_anexo12.pdf'))
