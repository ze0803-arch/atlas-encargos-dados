"""Robustez da pergunta central, 2023: (1) amostra com tolerância 3%; (2) outras medidas de base; (3) sem UFs de baixa cobertura; (4) quintis dentro da UF.
Uso: python robustez_2023.py CATALOGO SAIDA.md"""
import sys, pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
cat, out = sys.argv[1], sys.argv[2]
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv'); j = pd.read_csv(f'{cat}/juridico_base_2023.csv').fillna(0)
tb = pd.read_csv(f'{cat}/tributaria_2023.csv')
t3 = pd.read_csv(f'{cat}/resultado_2023_tol3.csv'); t3 = t3[t3.status == 'calculado'].copy()
L = ['# Robustez da pergunta central, 2023', '']
def fit(d, y, x, lab):
    d = d[[y, x, 'lp', 'uf']].replace([np.inf, -np.inf], np.nan).dropna()
    m = smf.ols(f'{y} ~ {x} + lp + C(uf)', d).fit(cov_type='HC3')
    r, p = stats.spearmanr(d[x], d[y])
    return dict(amostra=lab, n=len(d), rho=round(r, 3), coef=round(m.params[x], 2), p=f'{m.pvalues[x]:.2g}', r2=round(m.rsquared, 3))
rows = []
# base principal
d = b[b.calc == True].copy(); d['lp'] = np.log(d['pop']); d['lt'] = np.log(d.trib_pc.clip(lower=1)); d['margem_rt'] = d.p_mt
for y, nome in (('p_m', 'margem % receita livre'), ('margem_rt', 'margem % receita total')):
    r = fit(d, y, 'lt', 'principal (tol. 1%)'); r['desfecho'] = nome; rows.append(r)
# 1) tol 3%
s = t3.merge(tb[['cod_ibge', 'trib']], on='cod_ibge', how='inner') if 'trib' not in t3.columns else t3
s = s[(s['pop'] > 0) & (s.trib > 0)].copy()
s['rec_livre'] = pd.to_numeric(s.rec_livre, errors='coerce'); s['margem_ampla'] = pd.to_numeric(s.margem_ampla, errors='coerce')
s['p_m'] = s.margem_ampla / s.rec_livre * 100; s['margem_rt'] = s.margem_ampla / pd.to_numeric(s.rec_msc, errors='coerce') * 100
s['lt'] = np.log((s.trib / s['pop']).clip(lower=1)); s['lp'] = np.log(s['pop'])
s = s[(s.p_m.between(-100, 100))]
for y, nome in (('p_m', 'margem % receita livre'), ('margem_rt', 'margem % receita total')):
    r = fit(s, y, 'lt', 'tolerância 3%'); r['desfecho'] = nome; rows.append(r)
# 2) outras medidas de base (amostra com MSCE)
e = d.merge(j[['cod_ibge', 'n_iptu', 'n_iss', 'n_itbi']], on='cod_ibge', how='inner').fillna(0)
e['imp3_pc'] = (e.n_iptu + e.n_iss + e.n_itbi) / e['pop']; e['lt3'] = np.log(e.imp3_pc.clip(lower=1))
e['dep'] = e.trib / e.rtot.where(e.rtot > 0); e['dep'] = e.dep.clip(0, 1)
for x, lab in (('lt3', 'base = IPTU+ISS+ITBI por habitante'), ('dep', 'base = participação do tributo próprio na receita')):
    for y, nome in (('p_m', 'margem % receita livre'), ('margem_rt', 'margem % receita total')):
        r = fit(e, y, x, lab); r['desfecho'] = nome; rows.append(r)
# 3) sem UFs de baixa cobertura
cov = pd.read_csv(f'{cat}/resultado_2023.csv'); cov = cov.assign(c=(cov.status == 'calculado')).groupby('uf').c.mean()
ok = cov[cov >= 0.60].index; low = sorted(set(cov.index) - set(ok))
for y, nome in (('p_m', 'margem % receita livre'), ('margem_rt', 'margem % receita total')):
    r = fit(d[d.uf.isin(ok)], y, 'lt', f'só UFs com cobertura de 60% ou mais ({len(ok)} UFs)'); r['desfecho'] = nome; rows.append(r)
# 4) quintis dentro da UF
d['qu'] = d.groupby('uf').trib_pc.transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False, duplicates='drop') + 1 if len(s) >= 15 else np.nan)
g = d.dropna(subset=['qu']).groupby('qu').agg(n=('cod_ibge', 'size'), margem_pct_rec_livre=('p_m', 'median'), margem_pct_rec_total=('margem_rt', 'median'), vinculada=('vinc', 'median'))
L += ['## Coeficiente da base própria (log) sobre a margem, com efeitos fixos de UF e erro robusto (HC3), controlando pelo log da população', '']
T = pd.DataFrame(rows)[['desfecho', 'amostra', 'n', 'rho', 'coef', 'p', 'r2']]
L += [T.to_markdown(index=False), '', f'UFs com cobertura abaixo de 60% (excluídas na linha 3): {", ".join(low)}.', '', '## Quintis dentro de cada UF (UFs com 15 ou mais municípios calculados)', '', g.round(1).to_markdown(), '']
rho, p = stats.spearmanr(d.dropna(subset=['qu']).qu, d.dropna(subset=['qu']).margem_rt)
L.append(f'Spearman entre o quintil dentro da UF e a margem sobre a receita total: rho = {rho:.3f}, p = {p:.2g}.')
# art. 11, critério relativo
j2 = d.merge(j[['cod_ibge', 'n_iptu', 'n_iss', 'n_itbi']], on='cod_ibge').fillna(0)
j2['fx'] = pd.cut(j2['pop'], [0, 5000, 10000, 20000, 50000, 1e9], labels=False)
res = []
for k in ('iptu', 'iss', 'itbi'):
    j2[f'{k}_pc'] = j2[f'n_{k}'] / j2['pop']
    med = j2.groupby(['uf', 'fx'])[f'{k}_pc'].transform('median')
    j2[f'{k}_rel'] = (j2[f'{k}_pc'] < 0.1 * med) & (med > 0)
j2['algum_rel'] = j2.iptu_rel | j2.iss_rel | j2.itbi_rel
j2['q'] = pd.qcut(j2.trib_pc, 5, labels=['Q1 (menor)', 'Q2', 'Q3', 'Q4', 'Q5 (maior)'])
tt = j2.groupby('q', observed=True)[['iptu_rel', 'iss_rel', 'itbi_rel', 'algum_rel']].mean() * 100
L += ['', '## Art. 11 da LRF com critério relativo (arrecadação abaixo de 10% da mediana da mesma UF e faixa de porte, % do grupo)', '', tt.round(1).to_markdown(), '', f'Total com algum imposto abaixo do critério: {j2.algum_rel.mean()*100:.1f}% de {len(j2)}.']
open(out, 'w').write('\n'.join(L)); print('\n'.join(L))
