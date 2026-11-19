"""Tabelas do Apêndice D do projeto de tese (quintis de PIB por habitante, 2023) recalculadas do repositório, em JSON para o app.
Uso: python tabelas_projeto_2023.py CATALOGO SAIDA.json"""
import sys, json, pandas as pd, numpy as np
from scipy import stats
cat, out = sys.argv[1], sys.argv[2]
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv', dtype={'cod_ibge': str}); b = b[b.calc == True].copy()
p = pd.read_csv(f'{cat}/'+__import__('os').environ.get('PIB_ARQ','pib_2023.csv'), dtype={'cod_ibge': str}); j = pd.read_csv(f'{cat}/juridico_base_2023.csv', dtype={'cod_ibge': str}).fillna(0)
b = b.merge(p, on='cod_ibge'); b['pib_pc'] = b.pib_mil*1000/b['pop']; b = b[b.pib_pc > 0].copy()
Q = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']; b['q'] = pd.qcut(b.pib_pc, 5, labels=Q)
rl = b.rec_livre.where(b.rec_livre > 0)
b['minimos_rl'] = b.p_min_; b['leg_rl'] = b.p_leg
R = {}
g = b.groupby('q', observed=True)
R['t3'] = dict(n=g.size().tolist(), pib=g.pib_pc.median().round(0).tolist(), rec_pc=g.rec_pc.median().round(0).tolist(), m_rt=g.p_mt.median().round(1).tolist(),
               m_rl=g.p_m.median().round(1).tolist(), m_pc=g.marg_pc.median().round(0).tolist(), m_estrita_rt=g.p_met.median().round(1).tolist(), vinc=g.vinc.median().round(1).tolist(),
               minimos=g.minimos_rl.median().round(1).tolist(), leg=g.leg_rl.median().round(1).tolist())
# dentro da UF
tot = pd.read_csv(f'{cat}/resultado_2023.csv', dtype={'cod_ibge': str}); tot = tot[~tot.cod_ibge.str.startswith('53')].groupby('uf').size(); cal = b.groupby('uf').size()
okuf = [u for u in cal.index if cal[u] >= 40 and cal[u]/tot[u] >= .4]; R['uf_fora'] = sorted(set(tot.index) - set(okuf))
bu = b[b.uf.isin(okuf)].copy()
bu['qu'] = bu.groupby('uf').pib_pc.transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False)+1 if len(s) >= 15 else np.nan)
gu = bu.dropna(subset=['qu']).groupby('qu'); R['t4'] = dict(n=gu.size().tolist(), m_rt=gu.p_mt.median().round(1).tolist(), m_rl=gu.p_m.median().round(1).tolist(), vinc=gu.vinc.median().round(1).tolist())
# função: cobertura federal
d = b.merge(j, on='cod_ibge'); 
for c in d.columns:
    if c.startswith('d_'): d[c] = d[c].fillna(0)
d3 = d[d.cod_ibge.isin(j.cod_ibge)].copy()
areas = {'Saúde': ('d_f10', ['d_f10_sus', 'd_f10_acs']), 'Assistência social': ('d_f08', ['d_f08_fnas']), 'Educação': ('d_f12', ['d_f12_fnde', 'd_f12_fundeb'])}
t5 = {}
for nome, (tot, fed) in areas.items():
    for c in fed:
        if c not in d3: d3[c] = 0
    ok = d3[tot] > 0; d3['c'] = np.where(ok, d3[fed].sum(axis=1)/d3[tot]*100, np.nan)
    t5[nome] = d3.groupby('q', observed=True).c.median().round(1).tolist()
R['t5'] = t5
# art. 11
e = d.copy(); e['fx'] = pd.cut(e['pop'], [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e9], labels=False)
for k in ('iptu', 'iss', 'itbi'):
    e[k] = e[f'n_{k}']/e['pop']; med = e.groupby(['uf', 'fx'])[k].transform('median'); e[k+'_r'] = (e[k] < .1*med) & (med > 0)
e['alg'] = e.iptu_r | e.iss_r | e.itbi_r
R['t6'] = {k: e.groupby('q', observed=True)[c].mean().mul(100).round(1).tolist() for k, c in (('IPTU', 'iptu_r'), ('ISS', 'iss_r'), ('ITBI', 'itbi_r'), ('Algum', 'alg'))}
R['n_jur'] = int(len(d3))
# piso
IDX = 0.1495; d3['pess12'] = d3.d_f12_pessoal/d3.rec_livre.where(d3.rec_livre > 0)*100; d3['custo'] = IDX*d3.pess12
d3['consome'] = d3.custo/d3.p_m.where(d3.p_m > 0)*100; d3['pess10'] = d3.d_f10_pessoal/d3.rec_livre.where(d3.rec_livre > 0)*100
d3['antes'] = d3.p_m; d3['depois'] = d3.p_m - d3.custo
g7 = d3.groupby('q', observed=True)
R['t7'] = {k: g7[c].median().round(1).tolist() for k, c in (('pess_educ', 'pess12'), ('custo', 'custo'), ('consome', 'consome'), ('antes', 'antes'), ('depois', 'depois'), ('pess_saude', 'pess10'))}
m = d3.consome.notna() & np.isfinite(d3.consome); R['t7']['rho'] = round(float(stats.spearmanr(d3.pib_pc[m], d3.consome[m])[0]), 2)
# H1 e outros
import statsmodels.formula.api as smf
b['lpib'] = np.log(b.pib_pc); b['lp'] = np.log(b['pop'])
def fe(y):
    m = smf.ols(f'{y} ~ lpib + lp + C(uf)', b).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(b.uf)[0]}); ci = m.conf_int().loc['lpib']; return [round(m.params['lpib'], 2), round(ci[0], 2), round(ci[1], 2)]
R['h1'] = dict(rt=fe('p_mt'), rl=fe('p_m'), corr_vinc=round(float(b.p_mt.corr(100-b.vinc)), 2))
R['n'] = int(len(b))
json.dump(R, open(out, 'w'), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False)[:3000])
