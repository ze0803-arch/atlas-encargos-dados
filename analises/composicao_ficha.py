"""Gera prototipo/pesquisa/composicao.json: participação (%) de cada um dos sete grupos de receita por município (ficha do aplicativo).
Lê catalogo/composicao_receita_2023.csv. Mesmos grupos de composicao_resumo.py. Só municípios com receita positiva."""
import json, pandas as pd
c = pd.read_csv('catalogo/composicao_receita_2023.csv')
g = pd.DataFrame({'g1': c.propria_tributaria, 'g2': c.propria_patrimonial_serv + c.propria_contribuicoes + c.propria_outras, 'g3': c.transf_constitucionais,
                  'g4': c.transf_fundeb, 'g5': c.transf_fundo_a_fundo, 'g6': c.transf_voluntarias, 'g7': c.transf_outras + c.capital_outras + c.nao_classificada})
t = g.sum(axis=1); ok = t > 0
out = {int(k): [round(float(v), 1) for v in r] for k, r in zip(c.cod_ibge[ok], (g[ok].div(t[ok], axis=0) * 100).values)}
json.dump(out, open('prototipo/pesquisa/composicao.json', 'w'), separators=(',', ':')); print(len(out))
