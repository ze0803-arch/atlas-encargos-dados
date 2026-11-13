"""Análise comparativa UFs x municípios, 2023, com cuidados de cobertura.
Uso: python comparativo_2023.py CATALOGO SAIDA.md"""
import sys, pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
cat, out = sys.argv[1], sys.argv[2]
r = pd.read_csv(f'{cat}/resultado_2023.csv', dtype={'cod_ibge': str})
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv', dtype={'cod_ibge': str}); b = b[b.calc == True].copy()
p = pd.read_csv(f'{cat}/pib_2023.csv', dtype={'cod_ibge': str}); b = b.merge(p, on='cod_ibge', how='left'); b['pib_pc'] = b.pib_mil * 1000 / b['pop']
tot = r.groupby('uf').size().rename('total'); cal = b.groupby('uf').size().rename('calculados')
cob = pd.concat([tot, cal], axis=1).fillna(0); cob['cobertura_%'] = (cob.calculados / cob.total * 100).round(0)
L = ['# Análise comparativa entre UFs e municípios, 2023', '', 'Cuidado de cobertura: cada resultado traz o número de municípios calculados; UFs com menos de 40 municípios calculados ou cobertura abaixo de 40% ficam fora dos resultados por UF e marcadas.', '']
# tabela por UF
g = b.groupby('uf').agg(n=('uf', 'size'), trib_pc=('trib_pc', 'median'), pib_pc=('pib_pc', 'median'), margem_rt=('p_mt', 'median'), margem_livre=('p_m', 'median'), vinc=('vinc', 'median')).round(1)
g = g.join(cob['cobertura_%']); g['leitura'] = np.where((g.n < 40) | (g['cobertura_%'] < 40), 'cobertura insuficiente', 'ok')
L += ['## Tabela por UF (medianas dos municípios calculados)', '', g.sort_values('margem_rt').to_markdown(), '']
ok = g[g.leitura == 'ok'].index
d = b[b.uf.isin(ok)].copy(); d['lt'] = np.log(d.trib_pc.clip(lower=1)); d['lpib'] = np.log(d.pib_pc); d['lp'] = np.log(d['pop'])
d = d.dropna(subset=['lpib'])
# quintis dentro de cada UF e depois juntos
for v, nome in (('trib_pc', 'base própria por habitante'), ('pib_pc', 'PIB por habitante')):
    d['qu'] = d.groupby('uf')[v].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) + 1)
    t = d.groupby('qu').agg(n=('uf', 'size'), margem_rt=('p_mt', 'median'), margem_livre=('p_m', 'median'), vinc=('vinc', 'median')).round(1)
    kw = stats.kruskal(*[a.p_mt for _, a in d.groupby('qu')])
    L += [f'## Quintis de {nome} dentro de cada UF, depois juntados', '', t.to_markdown(), '', f'Teste de Kruskal-Wallis na margem sobre a receita total: p = {kw.pvalue:.2g}.', '']
# pares: mesmo porte e mesma UF, base alta x baixa
d['fx'] = pd.cut(d['pop'], [0, 5000, 10000, 20000, 50000, 1e9], labels=False)
dif = []
for (u, f), a in d.groupby(['uf', 'fx']):
    if len(a) >= 6:
        lo, hi = a[a.pib_pc <= a.pib_pc.quantile(.33)], a[a.pib_pc >= a.pib_pc.quantile(.67)]
        dif.append(dict(uf=u, fx=f, n=len(a), dif=hi.p_mt.median() - lo.p_mt.median()))
D = pd.DataFrame(dif)
L += ['## Pares de mesma UF e mesmo porte: terço de maior PIB por habitante menos terço de menor (margem sobre a receita total, pontos)', '', f'Grupos comparáveis: {len(D)}. Mediana da diferença: {D["dif"].median():.1f} pontos; positiva em {(D["dif"] > 0).mean() * 100:.0f}% dos grupos.', '']
# modelo em dois níveis
d['mrt'] = d.p_mt
m0 = smf.mixedlm('mrt ~ lpib + lp', d, groups=d.uf).fit(reml=True)
m1 = smf.mixedlm('mrt ~ lpib + lp', d, groups=d.uf, re_formula='~lpib').fit(reml=True)
icc = m0.cov_re.iloc[0, 0] / (m0.cov_re.iloc[0, 0] + m0.scale)
L += ['## Modelo em dois níveis (município dentro de UF)', '', f'- Parcela da variação da margem que está entre UFs (sem variáveis): {icc * 100:.0f}%.',
      f'- Efeito médio do log do PIB por habitante (intercepto aleatório): {m0.params["lpib"]:.2f} (erro {m0.bse["lpib"]:.2f}).',
      f'- Com inclinação aleatória: efeito médio {m1.params["lpib"]:.2f}; desvio-padrão da inclinação entre UFs {np.sqrt(m1.cov_re.iloc[1, 1]):.2f}.', '']
sl = {u: stats.linregress(a.lpib, a.p_mt).slope for u, a in d.groupby('uf') if len(a) >= 40}
L += [f'Inclinação por UF (UFs com 40+ municípios): mínima {min(sl.values()):.1f}, mediana {np.median(list(sl.values())):.1f}, máxima {max(sl.values()):.1f}; positiva em {sum(v > 0 for v in sl.values())} de {len(sl)}.', '']
# viés: ponderação por cobertura da UF
d = d.merge(cob['cobertura_%'], left_on='uf', right_index=True); w = 1 / (d['cobertura_%'] / 100)
mw = smf.wls('mrt ~ lpib + lp + C(uf)', d, weights=w).fit(cov_type='HC3')
L += [f'Sensibilidade (peso inverso da cobertura da UF, com efeitos fixos de UF): efeito do log do PIB por habitante {mw.params["lpib"]:.2f} (IC95% {mw.conf_int().loc["lpib",0]:.2f} a {mw.conf_int().loc["lpib",1]:.2f}).', '']
open(out, 'w').write('\n'.join(L)); print('\n'.join(L))
