"""H4c: base fora do território (REGIC 2018). Compara VA de serviços (2021) e ISS realizado (2023) por habitante entre municípios dependentes de um centro
(Centro de Zona e Centro Local, grupos 4 e 5) e os centros maiores (Metrópole, Capital Regional e Centro Sub-Regional, grupos 1 a 3), dentro de
células faixa de população x quintil de PIB por habitante. Critério provisório: diferença de pelo menos 15% (dependentes abaixo).
Uso (na raiz): python analises/h4c_regic.py -> catalogo/h4c_regic_2023.md e .csv"""
import json, numpy as np, pandas as pd
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8'))).iloc[:, [0, 2, 3, 4, 6]]
M.columns = ['cod_ibge', 'uf', 'pop', 'pibpc', 'q']
g = pd.read_csv('catalogo/regic_2018.csv'); j = pd.read_csv('catalogo/juridico_base_2023.csv')[['cod_ibge', 'n_iss']]
v = pd.read_csv('catalogo/va_servicos.csv')[['cod_ibge', 'va_servicos_mil']]
d = M.merge(g, on='cod_ibge', how='left').merge(j, on='cod_ibge', how='left').merge(v, on='cod_ibge', how='left')
bins = [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e12]; d['faixa'] = pd.cut(d['pop'], bins)
d['iss_pc'] = d.n_iss / d['pop']; d['va_pc'] = d.va_servicos_mil * 1000 / d['pop']
def teste(dep_grupos, cen_grupos, var):
    x = d[d.grupo.isin(dep_grupos + cen_grupos) & d[var].notna() & (d[var] > 0)].copy(); x['dep'] = x.grupo.isin(dep_grupos)
    rows = []
    for (f, q), c in x.groupby(['faixa', 'q'], observed=True):
        a, b = c[c.dep][var], c[~c.dep][var]
        if len(a) >= 5 and len(b) >= 5: rows.append((f, q, len(a), len(b), a.median() / b.median()))
    r = pd.DataFrame(rows, columns=['faixa', 'q', 'n_dep', 'n_cen', 'razao'])
    if r.empty: return None
    w = (r.n_dep + r.n_cen); lm = np.average(np.log(r.razao), weights=w)
    return dict(celulas=len(r), n_dep=int(r.n_dep.sum()), n_cen=int(r.n_cen.sum()), razao=round(float(np.exp(lm)), 3),
                celulas_abaixo_85=int((r.razao <= 0.85).sum()), celulas_abaixo_100=int((r.razao < 1).sum()))
out = []
for nome, dep, cen in (('Principal: dependentes (4 e 5) x centros (1 a 3)', [4, 5], [1, 2, 3]), ('Sensibilidade: só Centro Local (5) x centros (1 a 4)', [5], [1, 2, 3, 4])):
    for var, rot in (('va_pc', 'VA dos serviços por habitante (2021)'), ('iss_pc', 'ISS realizado por habitante (2023)')):
        r = teste(dep, cen, var)
        if r: out.append(dict(teste=nome, variavel=rot, **r))
o = pd.DataFrame(out); o.to_csv('catalogo/h4c_regic_2023.csv', index=False)
n = d.grupo.value_counts().sort_index().to_dict()
txt = f"""# H4c, base fora do território (REGIC 2018)

Base: {len(d)} municípios calculados; hierarquia (grupos 1 a 5): {n}. Razão = mediana dos dependentes ÷ mediana dos centros, dentro de células faixa de população × quintil de PIB por habitante (células com 5 ou mais em cada grupo), média ponderada em escala log.

{o.to_markdown(index=False)}

Critério provisório: dependentes pelo menos 15% abaixo dos centros (razão ≤ 0,85). Limites: classificação de 2018 contra receita de 2023; VA dos serviços de 2021; o quintil de PIB por habitante usa o valor adicionado, então a comparação é em parte circular.
"""
open('catalogo/h4c_regic_2023.md', 'w', encoding='utf-8').write(txt); print(txt)
