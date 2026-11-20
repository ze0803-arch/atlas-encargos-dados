"""Resume a composição da receita por quintil de PIB por habitante, faixa de população e UF (para o aplicativo).
Lê catalogo/composicao_receita_2023.csv e prototipo/pesquisa/municipios.json. Grava catalogo/composicao_resumo_2023.json.
Sete grupos, em ordem: tributária própria; outras próprias; transferências constitucionais; Fundeb; fundo a fundo; voluntárias; outros.
Participações ponderadas pelo valor (soma do grupo ÷ soma da receita, sem intraorçamentárias)."""
import json, numpy as np, pandas as pd
c = pd.read_csv('catalogo/composicao_receita_2023.csv')
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8'))).iloc[:, [0, 2, 3, 6]]; M.columns = ['cod_ibge', 'uf', 'pop', 'q']
d = c.drop(columns=['uf', 'pop']).merge(M, on='cod_ibge')
d['g1'] = d.propria_tributaria; d['g2'] = d.propria_patrimonial_serv + d.propria_contribuicoes + d.propria_outras
d['g3'] = d.transf_constitucionais; d['g4'] = d.transf_fundeb; d['g5'] = d.transf_fundo_a_fundo; d['g6'] = d.transf_voluntarias
d['g7'] = d.transf_outras + d.capital_outras + d.nao_classificada
G = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7']; d['tot'] = d[G].sum(axis=1); d = d[d.tot > 0]
bins = [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e12]; d['faixa'] = pd.cut(d['pop'], bins, labels=False)
sh = lambda x: [round(float(x[g].sum() / x.tot.sum() * 100), 1) for g in G]
for g in G: d[g + 'p'] = d[g] / d.tot * 100
out = dict(n=int(len(d)), total_bi=[round(float(d[g].sum() / 1e9), 1) for g in G], geral=sh(d),
           q=[sh(x) for _, x in d.groupby('q')], faixa=[sh(x) for _, x in d.groupby('faixa')], nfaixa=[int(len(x)) for _, x in d.groupby('faixa')], nq=[int(len(x)) for _, x in d.groupby('q')],
           mediana_propria_q=[round(float((x.g1p + x.g2p).median()), 1) for _, x in d.groupby('q')], mediana_trib_q=[round(float(x.g1p.median()), 1) for _, x in d.groupby('q')],
           mediana_voluntarias_q=[round(float(x.g6p.median()), 1) for _, x in d.groupby('q')],
           uf=sorted([[u, int(len(x))] + sh(x) for u, x in d.groupby('uf') if len(x) >= 20], key=lambda r: -(r[2] + r[3])))
json.dump(out, open('catalogo/composicao_resumo_2023.json', 'w'), ensure_ascii=False, separators=(',', ':')); print(out['geral'], out['q'][0], out['q'][4], out['mediana_propria_q'], len(out['uf']))
