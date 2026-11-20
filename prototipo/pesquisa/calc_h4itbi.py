"""ITBI e IPTU realizados por habitante, por quintil de PIB por habitante (H4b, base indireta do ITBI; D72).
Uso: python calc_h4itbi.py CATALOGO municipios.json h4itbi.json   (juridico_base_2023.csv no catálogo; municipios.json do aplicativo de pesquisa)
Resultado: medianas por quintil, Spearman ITBI x IPTU geral e mediana por UF (UFs com 40 ou mais municípios). Depois junte em dados.json na chave h4itbi."""
import sys, json, numpy as np, pandas as pd
from scipy import stats
cat, mun, out = sys.argv[1], sys.argv[2], sys.argv[3]
j = pd.read_csv(f'{cat}/juridico_base_2023.csv')[['cod_ibge', 'n_iptu', 'n_itbi']]
m = pd.DataFrame(json.load(open(mun)), columns=['cod','nome','uf','pop','pib','fx','q','recpc','vinc','min','patr','leg','div','prc','amp','fol','est','edu','sau'])
d = m.merge(j, left_on='cod', right_on='cod_ibge'); d['itbi'] = d.n_itbi / d['pop']; d['iptu'] = d.n_iptu / d['pop']
q = [[round(float(g.itbi.median()), 1), round(float(g.iptu.median()), 1), round(100 * float((g.n_itbi > 0).mean()), 1), int(len(g))] for _, g in d.groupby('q')]
e = d[(d.n_itbi > 0) & (d.n_iptu > 0)]
rho = stats.spearmanr(e.itbi, e.iptu)[0]
rs = [stats.spearmanr(g.itbi, g.iptu)[0] for _, g in e.groupby('uf') if len(g) >= 40]
json.dump({'q': q, 'rho': round(float(rho), 2), 'n': int(len(e)), 'rho_uf': round(float(np.median(rs)), 2), 'n_uf': len(rs)}, open(out, 'w'))
print(q, rho)
