#!/usr/bin/env python3
"""Testes de consistência interna (nível 2 de confiança, decisão D31) sobre resultado_<ano>.csv.
Uso: python confianca.py --pasta dados   -> grava <pasta>/confianca_<ano>.json {cod_ibge: [testes que falharam]} para os calculados."""
import argparse, csv, json, os
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); A = ap.parse_args()
f = lambda r, k: float(r[k]) if r.get(k) not in ('', None) else None
TESTES = [
 ('T1', lambda r: 0.8 <= f(r,'rec_livre')/f(r,'base_impostos') <= 1.3 if f(r,'base_impostos') else None),                 # receita livre / base de impostos
 ('T2', lambda r: f(r,'leg')/f(r,'base_impostos') <= 0.07 if f(r,'base_impostos') else None),                              # Legislativo em fonte livre <= 7% da base
 ('T3', lambda r: f(r,'folha_livre') <= f(r,'pessoal_rgf')*1.02 if f(r,'pessoal_rgf') else None),                          # folha livre <= DTP do Executivo (RGF)
 ('T4', lambda r: (f(r,'divida')+f(r,'prec')) <= 0.15*f(r,'rec_livre') if f(r,'rec_livre') else None),                    # dívida + precatórios <= 15% da receita livre
 ('T5', lambda r: 0 <= f(r,'margem_ampla') <= f(r,'rec_livre')),
 ('T7', lambda r: 0 <= f(r,'margem_ampla_pct_rcl') <= 0.8 if r['margem_ampla_pct_rcl'] else None),
 ('T8', lambda r: r['rcl_suspeita'] != 'True'),
]
rows = [r for r in csv.DictReader(open(os.path.join(A.pasta, f'resultado_{A.ano}.csv'), encoding='utf-8')) if r['status'] == 'calculado']
out = {r['cod_ibge']: [n for n, t in TESTES if t(r) is False] for r in rows}
json.dump(out, open(os.path.join(A.pasta, f'confianca_{A.ano}.json'), 'w'))
print(len(out), 'calculados;', sum(1 for v in out.values() if not v), 'sem nenhuma falha')
