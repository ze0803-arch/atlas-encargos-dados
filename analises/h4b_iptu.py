"""H4b, IPTU: base (lançado) contra esforço (taxa de realização) e dívida ativa, por quintil de PIB por habitante (2023).
Entra só quem tem coleta do H4 e nenhum sinal de problema em flag_h4 (SEM_LANCAMENTO_IPTU, ARREC_MAIOR_LANCADO, ARREC_NEGATIVO, DA_NEGATIVA)
e taxa de realização entre 0 e 1,5. Saídas: catalogo/h4b_iptu_2023.csv e .md; o aplicativo lê o .csv.
Uso (na raiz): python analises/h4b_iptu.py"""
import json, numpy as np, pandas as pd
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8'))).iloc[:, [0, 3, 6]]; M.columns = ['cod_ibge', 'pop', 'q']
h = pd.read_csv('catalogo/h4_2023.csv'); d = M.merge(h, on='cod_ibge', how='left'); n_calc = len(d)
d = d[d.tem_h4 == 1]; n_h4 = len(d)
d = d[d.flag_h4.isna() & d.taxa_realizacao.between(0, 1.5)].copy(); n_ok = len(d)
d['lanc_pc'] = d.iptu_lancado / d['pop']; d['arr_pc'] = d.iptu_arrec / d['pop']; d['da_pc'] = d.da_trib_bruta / d['pop']
d['rec_da'] = d.recuperacao_da.where(d.da_trib_bruta_ant > 0)
d['caixa'] = (d.taxa_realizacao - 1).abs() < 0.005   # lançado igual ao arrecadado: o lançamento é contabilizado na arrecadação (regime de caixa)
rows = []
for q, g in d.groupby('q'):
    rows.append(dict(quintil=q, n=len(g), lancado_pc=g.lanc_pc.median(), arrecadado_pc=g.arr_pc.median(), taxa_realizacao=g.taxa_realizacao.median(),
                     da_pc=g.da_pc.median(), recuperacao_da=g.rec_da.median(), n_da=int(g.rec_da.notna().sum()), pct_lancado_igual_arrecadado=g.caixa.mean() * 100, taxa_so_competencia=g[~g.caixa].taxa_realizacao.median(), n_competencia=int((~g.caixa).sum())))
o = pd.DataFrame(rows).round(3); o.to_csv('catalogo/h4b_iptu_2023.csv', index=False)
lb = np.log(o.lancado_pc.iloc[4] / o.lancado_pc.iloc[0]); la = np.log(o.arrecadado_pc.iloc[4] / o.arrecadado_pc.iloc[0]); parte = lb / la * 100
txt = f"""# H4b, IPTU por quintil de PIB por habitante (2023)

Calculados: {n_calc}. Com coleta do H4: {n_h4}. Sem sinais de problema e taxa de 0 a 1,5: {n_ok}.

{o.to_markdown(index=False)}

Razão Q5/Q1: lançado por habitante {np.exp(lb):.1f}x; arrecadado por habitante {np.exp(la):.1f}x. Parte da diferença do arrecadado explicada pela base (lançado), em escala log: {parte:.0f}%.
ATENÇÃO: onde o lançado é igual ao arrecadado (coluna pct_lancado_igual_arrecadado) o município contabiliza o IPTU no momento da arrecadação e não há taxa de realização real; a taxa só tem sentido na coluna taxa_so_competencia, e a proporção de municípios nessa situação cai com o PIB (a contabilidade, não só a cobrança, difere entre os quintis).
Dívida ativa tributária: saldo por habitante (CP + LP). Recuperação: dívida ativa recebida (IPTU e ISS) ÷ saldo do ano anterior; contas conforme D73b, a confirmar no PCASP Estendido.
"""
open('catalogo/h4b_iptu_2023.md', 'w', encoding='utf-8').write(txt); print(txt)
