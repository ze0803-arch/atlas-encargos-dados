"""Refaz os testes com PIB por habitante (IBGE, 2023), medida de capacidade independente da receita própria.
Uso: python base_independente_2023.py CATALOGO SAIDA.md"""
import sys, pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
cat, out = sys.argv[1], sys.argv[2]
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv', dtype={'cod_ibge': str}); b = b[b.calc == True].copy()
p = pd.read_csv(f'{cat}/'+__import__('os').environ.get('PIB_ARQ','pib_2023.csv'), dtype={'cod_ibge': str}); j = pd.read_csv(f'{cat}/juridico_base_2023.csv', dtype={'cod_ibge': str}).fillna(0)
b = b.merge(p, on='cod_ibge', how='left'); b['pib_pc'] = b.pib_mil * 1000 / b['pop']; b = b[b.pib_pc > 0].copy()
b['lpib'] = np.log(b.pib_pc); b['lt'] = np.log(b.trib_pc.clip(lower=1)); b['lp'] = np.log(b['pop']); b['livre_rt'] = 100 - b.vinc
b['q'] = pd.qcut(b.pib_pc, 5, labels=['Q1 (menor)', 'Q2', 'Q3', 'Q4', 'Q5 (maior)'])
L = ['# Testes com PIB por habitante (medida independente), 2023', '', f'Municípios calculados com PIB: {len(b)}. Quintis do PIB por habitante.', '']
g = b.groupby('q', observed=True).agg(n=('uf', 'size'), pib_pc=('pib_pc', 'median'), trib_pc=('trib_pc', 'median'), margem_pct_rec_livre=('p_m', 'median'), margem_pct_rec_total=('p_mt', 'median'), vinculada=('vinc', 'median')).round(1)
L += ['## Por quintil de PIB por habitante (medianas)', '', g.to_markdown(), '']
rows = []
for y, nome in (('p_m', 'margem % receita livre'), ('p_mt', 'margem % receita total'), ('livre_rt', 'parcela livre da receita total')):
    for x, lab in (('lpib', 'log do PIB por habitante'), ('lt', 'log da base própria por habitante')):
        d = b[[y, x, 'lp', 'uf']].dropna()
        m = smf.ols(f'{y} ~ {x} + lp + C(uf)', d).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(d.uf)[0]})
        ci = m.conf_int().loc[x]; r = stats.spearmanr(d[x], d[y])[0]
        rows.append(dict(desfecho=nome, base=lab, n=len(d), rho=round(r, 3), coef=round(m.params[x], 2), ic95=f'[{ci[0]:.2f}; {ci[1]:.2f}]', p=f'{m.pvalues[x]:.2g}'))
L += ['## Efeito da base sobre a margem (efeitos fixos de UF, erro agrupado por UF, controle de população)', '', pd.DataFrame(rows).to_markdown(index=False), '']
# diferença Q1-Q5 na parcela livre
q1, q5 = g.iloc[0], g.iloc[-1]
L += [f'Diferença entre Q5 e Q1 de PIB: margem sobre a receita livre {q5.margem_pct_rec_livre - q1.margem_pct_rec_livre:+.1f} pontos; margem sobre a receita total {q5.margem_pct_rec_total - q1.margem_pct_rec_total:+.1f} pontos; vinculada {q5.vinculada - q1.vinculada:+.1f} pontos.', '']
# dentro da UF
b['qu'] = b.groupby('uf').pib_pc.transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) + 1 if len(s) >= 15 else np.nan)
gu = b.dropna(subset=['qu']).groupby('qu').agg(n=('uf', 'size'), margem_pct_rec_livre=('p_m', 'median'), margem_pct_rec_total=('p_mt', 'median'), vinculada=('vinc', 'median')).round(1)
L += ['## Quintis de PIB por habitante dentro de cada UF', '', gu.to_markdown(), '']
rhos = [stats.spearmanr(a.pib_pc, a.p_mt)[0] for _, a in b.groupby('uf') if len(a) >= 40]
L += [f'Correlação (Spearman) entre PIB por habitante e margem sobre a receita total dentro da UF: mediana {np.median(rhos):.2f}; positiva em {sum(r > 0 for r in rhos)} de {len(rhos)} UFs.', '']
# art 11 com capacidade independente
e = b.merge(j[['cod_ibge', 'n_iptu', 'n_iss', 'n_itbi']], on='cod_ibge')
e['fx'] = pd.cut(e['pop'], [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e9], labels=False)
for k in ('iptu', 'iss', 'itbi'):
    e[f'{k}_pc'] = e[f'n_{k}'] / e['pop']; med = e.groupby(['uf', 'fx'])[f'{k}_pc'].transform('median'); e[f'{k}_rel'] = (e[f'{k}_pc'] < 0.1 * med) & (med > 0)
e['algum'] = e.iptu_rel | e.iss_rel | e.itbi_rel
t = e.groupby('q', observed=True)[['iptu_rel', 'iss_rel', 'itbi_rel', 'algum']].mean().mul(100).round(1)
L += ['## Art. 11 da LRF, com quintis de PIB por habitante (% do grupo abaixo do critério relativo)', '', t.to_markdown(), '']
m = smf.logit('algum ~ lpib + lp + C(uf)', e.assign(algum=e.algum.astype(int))).fit(disp=0)
L += [f'Logit com efeitos fixos de UF: coeficiente do log do PIB por habitante = {m.params["lpib"]:.2f} (p = {m.pvalues["lpib"]:.2g}).', '']
open(out, 'w').write('\n'.join(L)); print('\n'.join(L))
