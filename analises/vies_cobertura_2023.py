"""Viés de cobertura, 2023. Uso: python vies_cobertura_2023.py CATALOGO SAIDA.md"""
import sys, pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
cat, out = sys.argv[1], sys.argv[2]
r = pd.read_csv(f'{cat}/resultado_2023.csv'); t = pd.read_csv(f'{cat}/tributaria_2023.csv'); b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv')
d = r.merge(t[['cod_ibge','trib','rtot']], on='cod_ibge', how='left')
d = d[d['pop'] > 0].copy()
d['calc'] = (d.status == 'calculado').astype(int)
d['rec_pc'] = d.dca_rec / d['pop']; d['trib_pc'] = d.trib / d['pop']; d['lp'] = np.log(d['pop'])
d['faixa'] = pd.cut(d['pop'], [0,5000,10000,20000,50000,1e9], labels=['até 5 mil','5–10 mil','10–20 mil','20–50 mil','mais de 50 mil'])
L = ['# Viés de cobertura, 2023', '', f'Municípios com população: {len(d)}; calculados: {d.calc.sum()} ({d.calc.mean()*100:.1f}%).', '']
# motivos
fl = d[d.calc==0]['flags'].fillna('').str.split('|').explode().value_counts().head(8)
L += ['## Principais flags entre os não calculados (um município pode ter mais de uma)', '', fl.to_frame('n').to_markdown(), '']
# por faixa de porte
g = d.groupby('faixa', observed=True).agg(n=('calc','size'), cobertura_pct=('calc', lambda s: s.mean()*100)).round(1)
L += ['## Cobertura por faixa de porte', '', g.to_markdown(), '']
# comparação das variáveis disponíveis para todos
rows = []
for v, nome in (('pop','população'),('rec_pc','receita por habitante (DCA)'),('trib_pc','receita tributária própria por habitante')):
    a, c = d[d.calc==1][v].dropna(), d[d.calc==0][v].dropna()
    p = stats.mannwhitneyu(a, c).pvalue
    rows.append(dict(variavel=nome, mediana_calculados=round(a.median(),1), mediana_nao_calculados=round(c.median(),1), n_c=len(a), n_nc=len(c), p=f'{p:.2g}'))
L += ['## Calculados × não calculados (mediana; Mann-Whitney)', '', pd.DataFrame(rows).to_markdown(index=False), '']
# quintil de base entre todos que têm trib_pc
e = d.dropna(subset=['trib_pc']).copy(); e = e[e.trib_pc>0]
e['q'] = pd.qcut(e.trib_pc, 5, labels=['Q1 (menor)','Q2','Q3','Q4','Q5 (maior)'])
cq = e.groupby('q', observed=True).agg(n=('calc','size'), cobertura_pct=('calc', lambda s: s.mean()*100)).round(1)
L += ['## Cobertura por quintil de base tributária própria', '', cq.to_markdown(), '']
# logit da cobertura
e['lt'] = np.log(e.trib_pc.clip(lower=1)); e['lr'] = np.log(e.rec_pc.clip(lower=1))
m = smf.logit('calc ~ lp + lt + lr + C(uf)', e.dropna(subset=['lr'])).fit(disp=0)
L += ['## Logit: probabilidade de ser calculado (efeitos fixos de UF)', '', pd.DataFrame({'coef': m.params, 'p': m.pvalues}).loc[['lp','lt','lr']].round(3).to_markdown(), '']
# reponderação pelo inverso da probabilidade de cobertura
e2 = e.dropna(subset=['lr']).copy(); e2['pc'] = m.predict(e2).clip(0.05, 1); e2['w'] = 1/e2.pc
x = e2[e2.calc==1].merge(b[['cod_ibge','p_m','p_mt']], on='cod_ibge', how='inner').dropna(subset=['p_m','p_mt'])
res = []
for y, nome in (('p_m','margem % receita livre'),('p_mt','margem % receita total')):
    a = smf.ols(f'{y} ~ lt + lp + C(uf)', x).fit(cov_type='HC3')
    w = smf.wls(f'{y} ~ lt + lp + C(uf)', x, weights=x.w).fit(cov_type='HC3')
    res.append(dict(desfecho=nome, n=len(x), coef_sem_peso=round(a.params['lt'],2), coef_ponderado=round(w.params['lt'],2), p_ponderado=f'{w.pvalues["lt"]:.2g}'))
L += ['## Coeficiente da base própria, sem peso e ponderado pelo inverso da probabilidade de cobertura', '', pd.DataFrame(res).to_markdown(index=False), '']
# limites de Manski simples: se todos os não calculados tivessem margem da média do Q1 ou Q5 -> não aplicável; reporta apenas pesos extremos
L.append(f'Peso máximo usado: {e2.w.max():.1f}; mediana {e2.w.median():.2f}.')
open(out,'w').write('\n'.join(L)); print('\n'.join(L))
