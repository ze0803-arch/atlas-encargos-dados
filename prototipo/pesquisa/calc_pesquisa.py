"""Gera dados.json e municipios.json da versão de pesquisa a partir dos resultados de 2023.
Uso (na pasta prototipo/pesquisa):  python calc_pesquisa.py ..\\..\\app_coleta\\dados\\resultado_2023.csv ..\\..\\catalogo
Entradas: resultado_2023.csv (cálculo por município) e, no catálogo, juridico_base_2023.csv (IPTU, ISS e ITBI realizados), pib_2023.csv,
va_servicos.csv (rodar_tudo.bat) e tabelas_projeto_2023.json (H2 e tabelas do projeto). Depois: python build_pesquisa.py.
Medida: margem em % da receita total da MSC (regra D68). Quintis de PIB por habitante entre os municípios calculados."""
import sys, json, numpy as np, pandas as pd
from scipy import stats
RES, CAT = sys.argv[1], sys.argv[2].rstrip('/\\')
r = pd.read_csv(RES)
j = pd.read_csv(f'{CAT}/juridico_base_2023.csv')[['cod_ibge', 'n_iss', 'n_iptu', 'n_itbi']]
p = pd.read_csv(f'{CAT}/pib_2023.csv'); v = pd.read_csv(f'{CAT}/va_servicos.csv')[['cod_ibge', 'va_servicos_mil']]
t = json.load(open(f'{CAT}/tabelas_projeto_2023.json'))
d = r.merge(j, on='cod_ibge', how='left').merge(p, on='cod_ibge', how='left').merge(v, on='cod_ibge', how='left')
bins = [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e12]
lab = ['Até 5 mil', '5–10 mil', '10–20 mil', '20–50 mil', '50–100 mil', '100–500 mil', 'Mais de 500 mil']
d['faixa'] = pd.cut(d['pop'], bins, labels=lab); d['pibpc'] = d.pib_mil * 1000 / d['pop']
tot = len(d); cal = d[d.status == 'calculado'].copy()
R = cal.rec_msc
cal['m_rt'] = cal.margem_ampla / R * 100; cal['e_rt'] = cal.margem_estrita / R * 100
cal['m_rl'] = cal.margem_ampla / cal.rec_livre * 100; cal['vinc'] = (1 - cal.rec_livre / R) * 100
cal['m_pc'] = cal.margem_ampla / cal['pop']; cal['rec_pc'] = R / cal['pop']
cal = cal[cal.m_rt.between(-100, 100) & cal.pibpc.notna()].copy()
cal['q'] = pd.qcut(cal.pibpc.rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
out = {}
out['cob'] = {'total': int(tot), 'calc': int(len(cal)), 'por_uf': [[u, int((d.uf == u).sum()), int((cal.uf == u).sum())] for u in sorted(d.uf.unique())]}
g = cal.groupby('q')
out['h1'] = {k: [round(float(x), 1) for x in g[c].median()] for k, c in dict(m_rt='m_rt', e_rt='e_rt', m_rl='m_rl', vinc='vinc', m_pc='m_pc', pib='pibpc', rec_pc='rec_pc').items()}
out['h1']['n'] = [int(x) for x in g.size()]
out['faixas'] = [[f, int(len(x)), round(float(x.m_rt.median()), 1), round(float(x.e_rt.median()), 1), round(float(x.vinc.median()), 1), int((d.faixa == f).sum())] for f, x in cal.groupby('faixa', observed=True)]
# H3: Spearman por UF (40 ou mais calculados), pares UF x faixa, terços por UF
rows = []
for u, x in cal.groupby('uf'):
    rows.append([u, len(x), int((d.uf == u).sum()), round(float(x[['pibpc', 'm_rt']].corr(method='spearman').iloc[0, 1]), 2) if len(x) >= 40 else None])
out['h3'] = rows
par = ok = 0; lo = {}; hi = {}
for (u, f), x in cal.groupby(['uf', 'faixa'], observed=True):
    if len(x) >= 9:
        x = x.sort_values('pibpc'); k = len(x) // 3; par += 1; ok += x.m_rt.iloc[-k:].median() > x.m_rt.iloc[:k].median()
        lo.setdefault(u, []).append(x.iloc[:k]); hi.setdefault(u, []).append(x.iloc[-k:])
out['pares'] = [par, int(ok)]
out['h3b'] = []
for u in sorted(lo):
    a, b = pd.concat(lo[u]), pd.concat(hi[u])
    out['h3b'].append([u, int((d.uf == u).sum()), int(len(a) + len(b)), round(float(a.m_rt.median()), 1), round(float(b.m_rt.median()), 1), round(float(a.e_rt.median()), 1), round(float(b.e_rt.median()), 1)])
# exemplo: UF e faixa de exemplo (RN, 10 a 20 mil), se tiver grupo com 20 ou mais
ex = None
for key in (('RN', '10–20 mil'),):
    x = cal[(cal.uf == key[0]) & (cal.faixa == key[1])].sort_values('pibpc')
    if len(x) >= 20:
        k = len(x) // 3; ex = {'uf': key[0], 'fx': lab.index(key[1]), 'n': int(len(x)), 't': int(k), 'pib_low': int(x.pibpc.iloc[:k].median()), 'pib_high': int(x.pibpc.iloc[-k:].median()), 'm_low': round(float(x.m_rt.iloc[:k].median()), 1), 'm_high': round(float(x.m_rt.iloc[-k:].median()), 1)}
out['h3ex'] = ex
# H4a (critério relativo, 10% da mediana de UF x faixa)
d2 = d[d['pop'] > 0].copy()
for c, nm in (('n_iptu', 'iptu'), ('n_iss', 'iss'), ('n_itbi', 'itbi')): d2[nm + '_pc'] = d2[c].fillna(0) / d2['pop']
cal2 = cal.merge(d2[['cod_ibge', 'iptu_pc', 'iss_pc', 'itbi_pc']], on='cod_ibge'); fl = pd.DataFrame(index=cal2.index)
for nm in ('iptu', 'iss', 'itbi'):
    med = cal2.groupby(['uf', 'faixa'], observed=True)[nm + '_pc'].transform('median'); fl[nm] = (cal2[nm + '_pc'] < 0.1 * med) & (med > 0)
fl['algum'] = fl.any(axis=1)
out['h4a'] = {k: [round(float(100 * fl.loc[cal2.q == q, nm].mean()), 1) for q in range(1, 6)] for nm, k in (('iptu', 'IPTU'), ('iss', 'ISS'), ('itbi', 'ITBI'), ('algum', 'Algum'))}
out['h4a_tot'] = round(float(100 * fl.algum.mean()), 1)
# H4b: ISS = base (valor adicionado dos serviços) x alíquota efetiva
o = cal.copy(); o['iss_pc'] = o.n_iss.fillna(0) / o['pop']; o = o[(o.n_iss > 0) & (o.va_servicos_mil > 0)].copy()
o['vapc'] = o.va_servicos_mil * 1000 / o['pop']; o['aliq'] = o.n_iss / (o.va_servicos_mil * 1000) * 100; gq = o.groupby('q')
out['h4b'] = {'iss_pc': [round(float(x), 0) for x in gq.iss_pc.median()], 'va_pc': [round(float(x), 0) for x in gq.vapc.median()], 'aliq': [round(float(x), 2) for x in gq.aliq.median()], 'n': int(len(o))}
l = lambda c: np.log(gq[c].median()); out['h4b']['parte_base'] = round(float(100 * (l('vapc')[1] - l('vapc')[5]) / (l('iss_pc')[1] - l('iss_pc')[5])), 0)
# H4b: ITBI por habitante contra IPTU por habitante (base indireta; D72)
e = cal2.merge(d[['cod_ibge', 'n_iptu', 'n_itbi']], on='cod_ibge', suffixes=('', '_x')); e = e[e.n_iptu.notna() & e.n_itbi.notna()].copy()
e['itbi'] = e.n_itbi / e['pop']; e['iptu'] = e.n_iptu / e['pop']
out['h4itbi'] = {'q': [[round(float(x.itbi.median()), 1), round(float(x.iptu.median()), 1), round(100 * float((x.n_itbi > 0).mean()), 1), int(len(x))] for _, x in e.groupby('q')]}
pos = e[(e.n_itbi > 0) & (e.n_iptu > 0)]
rs = [stats.spearmanr(x.itbi, x.iptu)[0] for _, x in pos.groupby('uf') if len(x) >= 40]
out['h4itbi'].update(rho=round(float(stats.spearmanr(pos.itbi, pos.iptu)[0]), 2), n=int(len(pos)), rho_uf=round(float(np.median(rs)), 2), n_uf=len(rs))
# H2 e tabelas do projeto (do catálogo)
out['h2'] = {k: t['t7'][k] for k in ('pess_educ', 'custo', 'pess_saude', 'rho')}; out['t5'] = t['t5']; out['t6'] = t['t6']
# municípios: componentes em % da receita total (educação 25% e saúde 15% sobre a base de impostos)
c = cal.copy(); c['fx'] = c['pop'].apply(lambda x: next(i for i, b in enumerate(bins[1:]) if x <= b)); P = lambda s: 100 * s / c.rec_msc
c['edu'] = P(0.25 * c.base_impostos); c['sau'] = P(0.15 * (c.base_impostos - c.fpm_parcela_de.fillna(0)))
c['min'] = P(c.minimos_exigidos); c['patr'] = P(c.patronal_livre.fillna(0)); c['leg'] = P(c.leg); c['div'] = P(c.divida); c['prc'] = P(c.prec)
c['fol'] = P(c.folha_livre - c.patronal_livre.fillna(0))
r1 = lambda s: round(float(s), 1)
arr = [[int(a.cod_ibge), a.ente, a.uf, int(a['pop']), int(a.pibpc), int(a.fx), int(a.q), int(round(a.rec_pc)), r1(a.vinc), r1(a['min']), r1(a.patr), r1(a.leg), r1(a['div']), r1(a.prc), r1(a.m_rt), r1(a.fol), r1(a.e_rt), r1(a.edu), r1(a.sau)] for _, a in c.iterrows()]
json.dump(arr, open('municipios.json', 'w'), ensure_ascii=False, separators=(',', ':'))
import os
if os.path.exists(f'{CAT}/h4c_regic_2023.csv'):
    out['h4c'] = [[x.teste, x.variavel, int(x.celulas), int(x.n_dep), int(x.n_cen), float(x.razao), int(x.celulas_abaixo_100)] for x in pd.read_csv(f'{CAT}/h4c_regic_2023.csv').itertuples()]
json.dump(out, open('dados.json', 'w'), ensure_ascii=False, separators=(',', ':'), default=lambda x: x.item() if hasattr(x, 'item') else str(x))
print('municípios:', tot, 'calculados na leitura:', len(cal), '| margem ampla por quintil:', out['h1']['m_rt'], '| pares:', out['pares'], '| h4a:', out['h4a']['Algum'])
