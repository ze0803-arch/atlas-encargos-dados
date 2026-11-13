#!/usr/bin/env python3
"""Receita tributária própria (RREO Anexo 01, 'Até o Bimestre (c)') por município. Uso: python extrai_tributaria.py <pasta dados> -> <pasta>/tributaria_2023.csv"""
import sys, glob, gzip, json, re, csv
D = sys.argv[1].rstrip('/') + '/'; out = {}
for f in glob.glob(D + 'raw/siconfi/2023/rreo_anexo01/*_rreo_anexo01_p*.json.gz'):
    k = re.search(r'_2023_(\d+)_rreo', f).group(1)
    for i in json.load(gzip.open(f)).get('items', []):
        if i['coluna'].startswith('Até o Bimestre (c)'):
            if i['cod_conta'] == 'ReceitaTributaria': out.setdefault(k, {})['trib'] = i['valor']
            if i['cod_conta'] == 'ReceitasCorrentes': out.setdefault(k, {})['rcorr'] = i['valor']
            if i['cod_conta'] == 'TotalReceitas': out.setdefault(k, {})['rtot'] = i['valor']
w = csv.writer(open(D + 'tributaria_2023.csv', 'w', newline='')); w.writerow(['cod_ibge', 'trib', 'rcorr', 'rtot'])
for k, v in sorted(out.items()): w.writerow([k, v.get('trib'), v.get('rcorr'), v.get('rtot')])
print(len(out))
