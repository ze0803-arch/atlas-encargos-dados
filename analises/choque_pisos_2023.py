"""Exposição a um choque uniforme de piso, sem RAIS: custo máximo = índice x despesa de pessoal da função.
Magistério: índice de 14,95% (reajuste do piso em jan/2023). Teto do custo (supõe que toda a folha da função seja reajustada)."""
import sys, pandas as pd, numpy as np
from scipy import stats
cat = sys.argv[1]
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv'); j = pd.read_csv(f'{cat}/juridico_base_2023.csv').fillna(0)
d = b.merge(j, on='cod_ibge'); d = d[d.calc == True].copy()
d['q'] = pd.qcut(d.trib_pc, 5, labels=['Q1 (menor)','Q2','Q3','Q4','Q5 (maior)'])
rl = d.rec_livre.where(d.rec_livre > 0); rt = d.rtot.where(d.rtot > 0)
d['pess12_rl'] = d.d_f12_pessoal / rl * 100
d['pess12_rt'] = d.d_f12_pessoal / rt * 100
IDX = 0.1495
d['custo_pct_rl'] = IDX * d.pess12_rl
d['custo_pct_rt'] = IDX * d.pess12_rt
d['margem_pct'] = d.p_m; d['margem_rl'] = d.margem_pct
d['consome'] = d.custo_pct_rl / d.margem_pct.where(d.margem_pct > 0) * 100
d['pess10_rl'] = d.d_f10_pessoal / rl * 100
out = ['# Choque uniforme dos pisos, 2023 (sem RAIS)', '', f'Municípios: {len(d)}. Custo máximo do reajuste do piso do magistério = {IDX*100:.2f}% x despesa de pessoal da função 12 (todas as fontes). É teto: só parte da folha está abaixo do piso. Mede a exposição de cada município ao mesmo choque nacional.', '']
t = d.groupby('q', observed=True).agg(n=('cod_ibge','size'), pessoal_educ_pct_rec_livre=('pess12_rl','median'), custo_max_pct_rec_livre=('custo_pct_rl','median'), custo_max_pct_rec_total=('custo_pct_rt','median'), margem_pct_rec_livre=('margem_rl','median'), margem_consumida_pct=('consome','median'), pessoal_saude_pct_rec_livre=('pess10_rl','median'))
out += [t.round(1).to_markdown(), '']
for lab, c in (('pessoal da educação / receita livre','pess12_rl'),('custo máximo / receita livre','custo_pct_rl'),('custo máximo / receita total','custo_pct_rt'),('parcela da margem consumida','consome'),('pessoal da saúde / receita livre','pess10_rl')):
    m = d[c].notna() & np.isfinite(d[c]); r, p = stats.spearmanr(d.trib_pc[m], d[c][m]); g = [x[c].dropna().values for _, x in d.groupby('q', observed=True)]
    out.append(f'- {lab}: rho com a base própria = {r:.3f} (p = {p:.2g}); Kruskal-Wallis p = {stats.kruskal(*g)[1]:.2g}')
out += ['', 'Margem restante depois do choque máximo (mediana, % da receita livre):', '']
d['margem_pos'] = d.margem_pct - d.custo_pct_rl
t2 = d.groupby('q', observed=True).agg(antes=('margem_pct','median'), depois=('margem_pos','median'), municipios_margem_negativa_depois=('margem_pos', lambda s: (s < 0).mean() * 100))
out += [t2.round(1).to_markdown(), '']
open(f'{cat}/choque_pisos_2023.md', 'w').write('\n'.join(out)); print('\n'.join(out))
