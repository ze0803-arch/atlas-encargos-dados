#!/usr/bin/env python3
"""Compara o mínimo de saúde do sistema (15% x (base de impostos - FPM d/e)) com a Despesa Mínima em ASPS declarada no SIOPS (D33).
Uso: python comparar_siops.py --pasta dados   -> <pasta>/comparacao_siops_<ano>.csv e resumo na tela."""
import argparse, collections, csv, os, statistics as st
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); A = ap.parse_args()
f = lambda x: float(x) if x not in ('', None) else None
res = {r['cod_ibge']: r for r in csv.DictReader(open(os.path.join(A.pasta, f'resultado_{A.ano}.csv'), encoding='utf-8'))}
sio = list(csv.DictReader(open(os.path.join(A.pasta, f'siops_{A.ano}.csv'), encoding='utf-8')))
linhas = []
for p in sio:
    r = res.get(p['cod_ibge']); mn = f(p['minimo_asps_XVII']); lom = bool(f(p.get('minimo_lom')))
    if lom and f(p.get('base_realizada_III')): mn = 0.15 * f(p['base_realizada_III'])  # município com % da Lei Orgânica: compara a base, não o mínimo declarado (D41)
    if not r or not mn or not f(r['base_impostos']): continue
    sis = 0.15 * (f(r['base_impostos']) - (f(r['fpm_parcela_de']) or 0))
    linhas.append(dict(cod_ibge=p['cod_ibge'], ente=r['ente'], uf=r['uf'], status=r['status'], minimo_sistema=round(sis, 2), minimo_siops=mn,
                       diferenca_pct=round(100 * (sis / mn - 1), 3), parcela_de_identificada=bool(f(r['fpm_parcela_de'])), lei_organica=lom))
if linhas:
    with open(os.path.join(A.pasta, f'comparacao_siops_{A.ano}.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(linhas[0])); w.writeheader(); w.writerows(linhas)
def stats(x):
    ad = sorted(abs(l['diferenca_pct']) for l in x)
    if not ad: return None
    return dict(n=len(ad), mediana=st.median(ad), p90=ad[int(0.9 * len(ad))], max=ad[-1], ate1=100 * sum(v <= 1 for v in ad) / len(ad), ate10=100 * sum(v <= 10 for v in ad) / len(ad))
tudo = stats(linhas); calc = stats([l for l in linhas if l['status'] == 'calculado'])
print('Comparação do mínimo de saúde com o SIOPS (|diferença| em %):')
for nome, s in (('todos', tudo), ('calculados', calc)):
    if s: print(f"  {nome}: n={s['n']} mediana {s['mediana']:.2f} · p90 {s['p90']:.1f} · máx {s['max']:.0f} · ≤1%: {s['ate1']:.0f}% · ≤10%: {s['ate10']:.0f}%")
