"""Limites de Manski para a margem ampla por quintil de PIB por habitante (H1).
Os municipios nao calculados entram no pior caso: margem = piso ou teto do suporte (p1 e p99 dos calculados).
Uso (na raiz do repositorio): python analises/limites_manski.py
Saidas: catalogo/limites_manski_2023.csv e .md"""
import json, numpy as np, pandas as pd
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8')))
M = M.iloc[:, [0, 2, 3, 4, 6, 14]]; M.columns = ['cod', 'uf', 'pop', 'pibpc', 'q', 'amp']
pib = pd.read_csv('catalogo/pib_2023.csv'); r = pd.read_csv('catalogo/resultado_2023.csv')
t = r[['cod_ibge', 'ente', 'uf', 'pop']].merge(pib, on='cod_ibge')
t = t[t.cod_ibge.astype(str).str.len() == 7]; t['pibpc'] = t.pib_mil * 1000 / t['pop']
t = t.dropna(subset=['pibpc']); t = t[t['pop'] > 0]
corte = np.quantile(M.pibpc, [.2, .4, .6, .8])          # quintis definidos entre os calculados
t['q'] = np.searchsorted(corte, t.pibpc, side='right') + 1
t = t.merge(M[['cod', 'amp']], left_on='cod_ibge', right_on='cod', how='left'); t['calc'] = t.amp.notna()
lo, hi = np.percentile(M.amp, [1, 99])
rows = []
for q, g in t.groupby('q'):
    n, k = len(g), g.calc.sum(); obs = g.amp.mean(); f = 1 - k / n
    rows.append(dict(quintil=q, entes=n, calculados=int(k), falta_pct=round(f * 100, 1), media_observada=round(obs, 2),
                     limite_inf=round(obs * (1 - f) + lo * f, 2), limite_sup=round(obs * (1 - f) + hi * f, 2)))
o = pd.DataFrame(rows); o.to_csv('catalogo/limites_manski_2023.csv', index=False)
d_obs = o.media_observada.iloc[4] - o.media_observada.iloc[0]
d_inf = o.limite_inf.iloc[4] - o.limite_sup.iloc[0]; d_sup = o.limite_sup.iloc[4] - o.limite_inf.iloc[0]
txt = f"""# Limites de Manski, margem ampla por quintil de PIB por habitante (2023)

Suporte da margem: de {lo:.1f}% a {hi:.1f}% da receita total (percentis 1 e 99 dos calculados). Quintis definidos entre os calculados; os demais entram pelo PIB por habitante.

{o.to_markdown(index=False)}

Diferença entre o quintil de maior e o de menor PIB (pontos percentuais): observada {d_obs:.1f}; limites {d_inf:.1f} a {d_sup:.1f}.
Leitura: o limite é o pior caso, sem nenhuma hipótese sobre quem falta. Se o limite inferior da diferença for positivo, o sinal da H1 resiste mesmo ao pior caso.
"""
open('catalogo/limites_manski_2023.md', 'w', encoding='utf-8').write(txt); print(txt)
