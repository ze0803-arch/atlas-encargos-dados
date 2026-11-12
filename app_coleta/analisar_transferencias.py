#!/usr/bin/env python3
"""Compara as transferências da União (Portal da Transparência) com a receita por fonte de recurso na MSC.
Uso: python analisar_transferencias.py --pasta dados --ano 2023
Entradas: <pasta>/transferencias_<ano>.csv e _por_acao.csv (transferencias.py, 12 meses), <pasta>/resultado_<ano>.csv (analisar.py), raw/siconfi.
Saídas: <pasta>/transferencias_msc_<ano>.csv (por município e grupo: Portal x MSC) e
        <pasta>/acoes_para_classificar_<ano>.csv (ações, para classificar em obrigação legal ou adesão)."""
import argparse, csv, glob, gzip, json, os, statistics as st
import pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); A = ap.parse_args()
P = lambda f: os.path.join(A.pasta, f)
B = os.path.join(A.pasta, 'raw', 'siconfi', A.ano) + os.sep
# grupo do Portal -> fontes da MSC (4 dígitos, com o 1 inicial)
FONTES = {'sus': ('1600', '1601'), 'sus_acs_ace': ('1604',), 'fnas': ('1660',), 'fnde': ('1550', '1551', '1552', '1553', '1569')}
GRUPO_PORTAL = {'sus': ['sus_atencao_primaria', 'sus_media_alta', 'sus_outros'], 'sus_acs_ace': ['sus_acs_ace'], 'fnas': ['fnas'],
                'fnde': ['salario_educacao', 'fnde_programas']}
def carrega(rel, cod):
    out = []
    for f in sorted(glob.glob(f'{B}{rel}/*_{cod}_{rel}_p*.json.gz')): out += json.load(gzip.open(f)).get('items', [])
    return out
res = pd.read_csv(P(f'resultado_{A.ano}.csv'), dtype={'cod_ibge': str})
res = res[res['status'] == 'calculado']
tr = pd.read_csv(P(f'transferencias_{A.ano}.csv'), dtype={'cod_ibge': str}).set_index('cod_ibge')
linhas = []
for _, r in res.iterrows():
    c = r['cod_ibge']
    if c not in tr.index: continue
    nome = r['fonte_msc']; rel = 'msce' if nome == 'MSCE' else None
    if nome == 'MSCE': itens = carrega('msce', c)
    else: itens = [i for mes in range(1, 13) for i in carrega('mscc_m%02d' % mes, c)]
    sg0 = 1 if r['convencao'].endswith('+') else -1; deb = r['convencao'].startswith('deb')
    por_fonte = {}
    for i in itens:
        if i['conta_contabil'] != '621200000': continue
        nr = i['natureza_receita'] or ''
        if nr[:1] not in ('1', '2', ''): continue
        sg = (1 if i['natureza_conta'] == 'D' else -1) * sg0
        v = (i['valor'] if sg == 1 else 0) if deb else i['valor'] * sg
        fr = (i['fonte_recursos'] or '')[1:]
        fr = '1' + fr if len(fr) == 3 else fr
        por_fonte[fr] = por_fonte.get(fr, 0) + v
    for g, fs in FONTES.items():
        portal = sum(tr.loc[c].get(x, 0) for x in GRUPO_PORTAL[g]); msc = sum(por_fonte.get(f, 0) for f in fs)
        linhas.append(dict(cod_ibge=c, ente=r['ente'], uf=r['uf'], grupo=g, portal=round(portal, 2), msc=round(msc, 2),
                           msc_sobre_portal=(msc / portal) if portal else None, rec_livre=r['rec_livre']))
out = pd.DataFrame(linhas); out.to_csv(P(f'transferencias_msc_{A.ano}.csv'), index=False)
print('Municípios calculados com transferências:', out['cod_ibge'].nunique())
for g, d in out.groupby('grupo'):
    d = d[d['portal'] > 0]
    if d.empty: continue
    q = d['msc_sobre_portal'].dropna()
    print(f'{g:12s} n={len(d):4d}  mediana MSC/Portal={q.median():.2f}  entre 0,9 e 1,1: {((q>=0.9)&(q<=1.1)).mean():.0%}  MSC zerada: {(d["msc"]==0).mean():.0%}')
# lista de ações para classificar
pa = pd.read_csv(P(f'transferencias_{A.ano}_por_acao.csv'), dtype={'cod_ibge': str})
ac = pa.groupby(['grupo', 'NOME ÓRGÃO', 'NOME AÇÃO']).agg(municipios=('cod_ibge', 'nunique'), total=('v', 'sum')).reset_index().sort_values('total', ascending=False)
ac['classificacao'] = ''   # a preencher: obrigacao_legal | adesao | automatica_constitucional | outra
ac['observacao'] = ''
ac.to_csv(P(f'acoes_para_classificar_{A.ano}.csv'), index=False)
print('Ações distintas:', len(ac), '→', P(f'acoes_para_classificar_{A.ano}.csv'))
