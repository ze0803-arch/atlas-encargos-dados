#!/usr/bin/env python3
"""Testes da pergunta central da tese com os dados de 2023: encargos fixados nacionalmente de forma uniforme reduzem na mesma medida
o espaço de decisão orçamentária de municípios com bases fiscais desiguais?
Uso: python testes_tese_2023.py <pasta dados>   (precisa de resultado_2023.csv e tributaria_2023.csv)  -> <pasta>/testes_tese_2023.md e .csv"""
import sys, json, numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
D = sys.argv[1].rstrip('/') + '/'
r = pd.read_csv(D + 'resultado_2023.csv', dtype={'cod_ibge': str}); t = pd.read_csv(D + 'tributaria_2023.csv', dtype={'cod_ibge': str})
cf = json.load(open(D + 'confianca_2023.json'))
r = r[~r.cod_ibge.str.startswith('53') & (r.cod_ibge != '2605459')].merge(t, on='cod_ibge', how='left')
r['alta'] = r.cod_ibge.map(lambda c: len(cf.get(c, [])) == 0)
r['calc'] = r.status == 'calculado'
r['trib_pc'] = r.trib / r['pop']; r['rec_pc'] = r.rec_msc / r['pop']
c = r[r.calc & (r.rec_livre > 0) & (r['pop'] > 0) & (r.trib > 0)].copy()
c['uf'] = c.uf
c['enc'] = c.minimos_exigidos + c.leg + c.divida + c.prec
for k, v in dict(m='margem_ampla', min_='minimos_exigidos', leg='leg', div='divida', prec='prec', fol='folha_livre', me='margem_estrita').items(): c['p_' + k] = c[v] / c.rec_livre * 100
c['p_enc'] = c.enc / c.rec_livre * 100; c['p_mt'] = c.margem_ampla / c.rec_msc * 100; c['p_met'] = c.margem_estrita / c.rec_msc * 100; c['vinc'] = (1 - c.rec_livre / c.rec_msc) * 100; c['marg_pc'] = c.margem_ampla / c['pop']
c['q'] = pd.qcut(c.trib_pc, 5, labels=['Q1 (menor)', 'Q2', 'Q3', 'Q4', 'Q5 (maior)'])
c['fx'] = pd.cut(c['pop'], [0, 5000, 10000, 20000, 50000, 1e9], labels=['até 5 mil', '5 a 10 mil', '10 a 20 mil', '20 a 50 mil', '50 mil ou mais'], right=False)
L = []; P = lambda s='': L.append(s)
def tab(g):
    x = c.groupby(g, observed=True).agg(n=('cod_ibge', 'size'), trib_pc=('trib_pc', 'median'), rec_pc=('rec_pc', 'median'), margem_pct=('p_m', 'median'), margem_rec_total=('p_mt', 'median'), minimos=('p_min_', 'median'), legislativo=('p_leg', 'median'),
        divida=('p_div', 'median'), precatorios=('p_prec', 'median'), encargos=('p_enc', 'median'), margem_estrita=('p_me', 'median'), vinculada=('vinc', 'median'), margem_pc=('marg_pc', 'median')).round(1)
    return x
P('# Testes da pergunta central, 2023'); P()
P(f'Municípios calculados com receita tributária e população: {len(c)} (alta confiança: {int(c.alta.sum())}). Medianas. "margem_pct" e os encargos são % da receita livre; "margem_rec_total" é % da receita total (o que resta do orçamento para a decisão local); "vinculada" é a % da receita total fora da receita livre.'); P()
P('## 1. Por quintil de receita tributária própria por habitante'); P(); qt = tab('q'); P(qt.to_markdown()); P()
P('## 2. Por porte'); P(); P(tab('fx').to_markdown()); P()
def testa(y):
    res = {}
    for nome, d in [('todos', c), ('alta confiança', c[c.alta]), ('sem 1% extremos', c[(c[y] > c[y].quantile(.01)) & (c[y] < c[y].quantile(.99))])]:
        rho, p = stats.spearmanr(d.trib_pc, d[y]); rho2, p2 = stats.spearmanr(d['pop'], d[y])
        kw = stats.kruskal(*[g[y].values for _, g in d.groupby('q', observed=True)])
        a, b = d[d.q == 'Q1 (menor)'][y], d[d.q == 'Q5 (maior)'][y]; mw = stats.mannwhitneyu(a, b)
        ols = smf.ols(y + ' ~ np.log(trib_pc) + np.log(Q("pop")) + C(uf)', d).fit(cov_type='HC3')
        res[nome] = dict(n=len(d), rho_trib=rho, p_trib=p, rho_pop=rho2, p_pop=p2, kw=kw.statistic, kw_p=kw.pvalue, med_Q1=a.median(), med_Q5=b.median(), dif_Q5_Q1=b.median() - a.median(), mw_p=mw.pvalue,
                         b_trib=ols.params['np.log(trib_pc)'], b_trib_p=ols.pvalues['np.log(trib_pc)'], b_pop=ols.params['np.log(Q("pop"))'], b_pop_p=ols.pvalues['np.log(Q("pop"))'], r2=ols.rsquared)
    return pd.DataFrame(res).T
P('## 3. Testes'); P()
P('### 3a. Margem ampla como % da receita livre'); P(); P(testa('p_m').round(4).to_markdown()); P()
P('### 3b. Margem ampla como % da receita total'); P(); P(testa('p_mt').round(4).to_markdown()); P()
P('Legenda: rho_trib = Spearman entre receita tributária por habitante e a margem; rho_pop = com a população; kw = Kruskal-Wallis entre os 5 quintis; med_Q1/med_Q5 e dif_Q5_Q1 = medianas dos quintis extremos e a diferença (p.p.); b_trib e b_pop = coeficientes de uma regressão linear da margem (p.p.) sobre o log da receita tributária por habitante e o log da população, com efeitos fixos de UF e erros robustos (HC3).'); P()
# decomposição da diferença Q5-Q1
dq = qt.loc['Q5 (maior)'] - qt.loc['Q1 (menor)']
P('## 4. De onde vem a diferença entre o quintil de maior e o de menor base (p.p. da receita livre)'); P()
P(pd.DataFrame({'Q1': qt.loc['Q1 (menor)', ['minimos', 'legislativo', 'divida', 'precatorios', 'encargos', 'margem_pct', 'margem_rec_total', 'vinculada']], 'Q5': qt.loc['Q5 (maior)', ['minimos', 'legislativo', 'divida', 'precatorios', 'encargos', 'margem_pct', 'margem_rec_total', 'vinculada']], 'Q5 - Q1': dq[['minimos', 'legislativo', 'divida', 'precatorios', 'encargos', 'margem_pct', 'margem_rec_total', 'vinculada']]}).round(1).to_markdown()); P()
# seleção: calculados x não
a = r.copy(); a['faixa'] = pd.cut(a['pop'], [0, 5000, 10000, 20000, 50000, 1e9], right=False, labels=['até 5 mil', '5 a 10 mil', '10 a 20 mil', '20 a 50 mil', '50 mil ou mais'])
s = a.groupby('faixa', observed=True).agg(municipios=('cod_ibge', 'size'), calculados=('calc', 'sum')); s['%'] = (s.calculados / s.municipios * 100).round(0)
s2 = a.groupby('calc').agg(trib_pc_mediana=('trib_pc', 'median'), rec_pc_mediana=('rec_pc', 'median'), pop_mediana=('pop', 'median')).round(0)
P('## 5. Seleção: quem ficou fora do cálculo'); P(); P(s.to_markdown()); P(); P(s2.to_markdown()); P()
open(D + 'testes_tese_2023.md', 'w').write('\n'.join(L)); c.drop(columns=['q', 'fx']).to_csv(D + 'testes_tese_2023_base.csv', index=False); print('\n'.join(L))
# 6. Blocos da União por classe (transferências do Portal classificadas no formulário), em % da receita total
import os
cl = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogo', 'classificacao_acoes_2023.csv'))
ta = pd.read_csv(D + 'transferencias_2023_por_acao.csv', dtype={'cod_ibge': str}).merge(cl[['grupo', 'NOME AÇÃO', 'classe']], on=['grupo', 'NOME AÇÃO'], how='left')
ta = ta[~ta.grupo.isin(['constitucional_royalties'])]  # FPM, royalties e CIDE entram na receita livre
pv = ta.pivot_table(index='cod_ibge', columns='classe', values='v', aggfunc='sum').fillna(0)
x = c.merge(pv, left_on='cod_ibge', right_index=True, how='left').fillna({k: 0 for k in pv.columns})
for k in pv.columns: x['u_' + k] = x[k] / x.rec_msc * 100
u = [k for k in x.columns if k.startswith('u_')]
x['q'] = pd.qcut(x.trib_pc, 5, labels=['Q1 (menor)', 'Q2', 'Q3', 'Q4', 'Q5 (maior)'])
P('## 6. Transferências federais vinculadas por classe, % da receita total (mediana por quintil; FPM, royalties e CIDE ficam fora, pois entram na receita livre)'); P()
P(x.groupby('q', observed=True)[u].median().round(1).to_markdown()); P()
P('Obrigação legal e automática constitucional (Fundeb, salário-educação) formam o bloco heterônomo vinculado; adesão é pactuação (bloco P).'); P()
open(D + 'testes_tese_2023.md', 'w').write('\n'.join(L)); print('\n'.join(L[-12:]))
