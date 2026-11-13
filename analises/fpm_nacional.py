#!/usr/bin/env python3
"""Teste do FPM nacional: Cota-Parte FPM do SIOPS (raw/siops/2023/<cod>.html.gz) contra a natureza 17115111 da MSCE.
Uso: python fpm_nacional.py <pasta dados> <pasta com <cod>.html.gz do SIOPS>   (saída: fpm_nacional_2023.json)"""
import sys, gzip, json, glob, csv, re, html, collections
from multiprocessing import Pool
D = sys.argv[1].rstrip('/') + '/'; SI = sys.argv[2].rstrip('/') + '/'; B = D + 'raw/siconfi/2023/'
num = lambda s: float(s.replace('.', '').replace(',', '.')) if re.fullmatch(r'-?[\d.]+,\d+', s) else None
def siops_fpm(k):
    h = gzip.open(f'{SI}{k}.html.gz', 'rt', encoding='utf-8', errors='ignore').read()
    h = re.sub(r'<(script|style)[\s\S]*?</\1>', '', h); h = re.sub(r'</(tr|p|div)>', '\n', h); h = re.sub(r'</t[dh]>', ' | ', h); h = html.unescape(re.sub(r'<[^>]+>', '', h))
    for l in h.split('\n'):
        p = [x.strip() for x in re.sub(r'\s+', ' ', l).split('|')]
        if p and p[0].startswith('Cota-Parte FPM'):
            v = [x for x in (num(y) for y in p[1:]) if x is not None]
            if len(v) >= 3: return v[2]
def one(k):
    try:
        g = collections.defaultdict(float)
        for f in glob.glob(f'{B}msce/*_{k}_msce_p*.json.gz'):
            for i in json.load(gzip.open(f)).get('items', []):
                if i['conta_contabil'] == '621200000' and (i['natureza_receita'] or '')[:8] in ('17115111', '17115121'):
                    g[i['natureza_receita'][:8]] += i['valor'] * (1 if i['natureza_conta'] == 'D' else -1)
        f = g.get('17115111', 0); s = 1 if f > 0 else -1
        return k, f * s, siops_fpm(k)
    except Exception: return k, None, None
if __name__ == '__main__':
    C = [c for c in csv.DictReader(open(D + 'comparacao_siops_2023.csv'))]
    with Pool(4) as p: res = p.map(one, [c['cod_ibge'] for c in C], chunksize=20)
    json.dump(res, open(D + 'fpm_nacional_2023.json', 'w')); print(len(res))
