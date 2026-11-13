#!/usr/bin/env python3
"""Reconstrói PILOTO e VALID do prototipo/atlas_prototipo.html com o resultado nacional 2023 (catalogo/).
Uso: python prototipo/build_prototipo_nacional.py <pasta com resultado_2023.csv, confianca_2023.json, comparacao_siops_2023.csv, convenios_2023.csv>
DF (53...) fica fora do denominador municipal."""
import sys, json, re, pandas as pd, numpy as np
D = sys.argv[1].rstrip('/') + '/'; H = 'prototipo/atlas_prototipo.html'
r = pd.read_csv(D+'resultado_2023.csv', dtype={'cod_ibge': str}); r = r[~r.cod_ibge.str.startswith('53')]
C = json.load(open(D+'confianca_2023.json'))
n = lambda x: None if pd.isna(x) else float(x)
rows = []
for _, x in r.iterrows():
    c = x.cod_ibge; calc = x.status == 'calculado'
    rows.append(dict(c=c, ente=x.ente.replace('Prefeitura Municipal de ', ''), uf=x.uf, pop=int(x['pop']), st='calc' if calc else 'marc',
        fl=[f for f in str(x.flags).split('|') if f not in ('OK', 'nan')], m=n(x.margem_ampla) if calc else None, me=n(x.margem_estrita) if calc else None,
        mp=n(x.margem_ampla_pct_rcl) if calc else None, rl=n(x.rec_livre) if calc else None,
        cf=(None if not calc else ('A' if not C.get(c) else 'R')), ft=C.get(c, []) if calc else []))
# VALID: SIOPS
s = pd.read_csv(D+'comparacao_siops_2023.csv', dtype={'cod_ibge': str}); s = s[~s.cod_ibge.str.startswith('53')].dropna(subset=['diferenca_pct'])
def est(g): a = g.diferenca_pct.abs(); return dict(n=int(len(g)), med=round(float(a.median()), 2), p1=int(round(100*(a <= 1).mean())), p10=int(round(100*(a <= 10).mean())), ex=int((a > 10).sum()))
sc = s[s.status == 'calculado']
V = dict(todos=est(s), calc=est(sc), uf={u: est(g) for u, g in sc.groupby('uf')})
ex = sc[sc.diferenca_pct.abs() > 10].sort_values('diferenca_pct', key=abs, ascending=False)
V['exc'] = [[e.ente, e.uf, round(abs(float(e.diferenca_pct)), 1)] for e in ex.itertuples()]
# bloco P
c = r[(r.status == 'calculado') & (r.rec_livre > 0)].copy()
cv = pd.read_csv(D+'convenios_2023.csv', dtype={'cod_ibge': str}).set_index('cod_ibge')
c['cons'] = c.consorcios.fillna(0); cc = c[c.cons > 0]
cp = (c.cod_ibge.map(cv.contrapartida_ano).fillna(0) / c.rec_livre * 100)
amp = (c.margem_ampla / c.rec_livre * 100).median(); ampp = (c.margem_ampla_p / c.rec_livre * 100).median()
V['p'] = dict(ncal=int(len(c)), ncons=int(len(cc)), cons_med=round(float((cc.cons/cc.rec_livre*100).median()), 2), cons_p90=round(float((cc.cons/cc.rec_livre*100).quantile(.9)), 2),
              amp=round(float(amp), 1), ampp=round(float(ampp), 1), cp_med=round(float(cp.median()), 2), cp_p90=round(float(cp.quantile(.9)), 2), nlib=0, lib_med=0)
h = open(H, encoding='utf8').read()
h = re.sub(r'const PILOTO=\[.*?\];\n', lambda m: 'const PILOTO='+json.dumps(rows, ensure_ascii=False, separators=(',', ':'))+';\n', h, 1, re.S)
h = re.sub(r'const VALID=\{.*?\};\n', lambda m: 'const VALID='+json.dumps(V, ensure_ascii=False, separators=(',', ':'))+';\n', h, 1, re.S)
h = h.replace('calculados com SIOPS (9 UFs)', 'calculados com SIOPS (${Object.keys(V.uf).length} UFs)')
h = h.replace("das UFs já coletadas.", "das 27 UFs (o DF fica fora do denominador municipal).")
for a, b in [('municípios em que o FPM do SIOPS é igual ao da MSC', 'municípios em que o FPM do SIOPS é igual ao da MSC (piloto de 9 UFs)'),
             ('das exceções acima de 10% têm esse padrão', 'das exceções acima de 10% têm esse padrão (piloto de 9 UFs)'),
             ('receita federal vinculada (SUS, FNDE, convênios, FNAS), % da receita total: teto do bloco P', 'receita federal vinculada (SUS, FNDE, convênios, FNAS), % da receita total, mediana de 3.522 municípios: teto do bloco P')]:
    h = h.replace(a, b)
h = h.replace('Validação do piloto 2023 e bloco P', 'Validação 2023 e bloco P')
open(H, 'w', encoding='utf8').write(h)
print(len(rows), sum(x['st'] == 'calc' for x in rows), V['todos'], V['calc'], len(V['exc']), V['p'])
