"""Composição da receita realizada de 2023 por município, pela natureza de receita da MSCE (conta 621200000).
Grupos (classificação por natureza de receita do MCASP; prefixos de 4 e 5 dígitos):
  propria_tributaria      11* (impostos, taxas, contribuição de melhoria)
  propria_contribuicoes   12* (previdenciárias e COSIP)
  propria_patrimonial_serv 13* e 16* (patrimonial, financeiras e serviços)
  propria_outras          19* (multas, dívida ativa não tributária, restituições etc.)
  transf_constitucionais  1711*, 1712*, 1721*, 1722* (FPM, ITR, compensações e royalties da União; ICMS, IPVA, compensações dos Estados)
  transf_fundeb           175* e 1715*/1716* (Fundeb: contribuição retornada e complementação da União)
  transf_fundo_a_fundo    1713*, 1723* (SUS, FNDE, FNAS e demais fundo a fundo)
  transf_voluntarias      1714*, 1724*, 1734*, 24* (convênios e transferências de capital)
  transf_outras           demais 17* e 2[2-9] de outras origens
  capital_outras          21*, 22*, 29* (crédito, alienação e outras de capital)
  intraorcamentaria       7* e deduções 9* (separadas)
Municípios cuja fonte é a soma das 12 matrizes mensais (MSCC_12m, D19) usam as pastas mscc_mNN ao lado de msce.
Uso (na raiz): python analises/composicao_receita.py PASTA_MSCE  -> catalogo/composicao_receita_2023.csv e .md"""
import sys, glob, gzip, json, collections, pandas as pd
B = sys.argv[1].rstrip('/') + '/'
r = pd.read_csv('catalogo/resultado_2023_tol3.csv'); cal = r[r.status == 'calculado']
def grupo(n):
    if n.startswith('7') or n.startswith('9'): return 'intraorcamentaria'
    if n.startswith('11'): return 'propria_tributaria'
    if n.startswith('12'): return 'propria_contribuicoes'
    if n.startswith(('13', '16')): return 'propria_patrimonial_serv'
    if n.startswith('19'): return 'propria_outras'
    if n.startswith(('1711', '1712', '1721', '1722')): return 'transf_constitucionais'
    if n.startswith(('175', '1715', '1716')): return 'transf_fundeb'
    if n.startswith(('1713', '1723')): return 'transf_fundo_a_fundo'
    if n.startswith(('1714', '1724', '1734', '24')): return 'transf_voluntarias'
    if n.startswith('17') or n.startswith('23'): return 'transf_outras'
    if n.startswith(('21', '22', '29')): return 'capital_outras'
    return 'nao_classificada'
rows = []
for _, x in cal.iterrows():
    k = x.cod_ibge
    fs = glob.glob(f'{B}*_{k}_msce_p*.json.gz') if x.fonte_msc != 'MSCC_12m' else sum((glob.glob(f'{B[:-5]}mscc_m{m:02d}/*_{k}_mscc_m{m:02d}_p*.json.gz') for m in range(1, 13)), [])
    if not fs: continue
    D, C = collections.Counter(), collections.Counter()
    for f in fs:
        for i in json.load(gzip.open(f)).get('items', []):
            if i['conta_contabil'] == '621200000': (D if i['natureza_conta'] == 'D' else C)[i['natureza_receita'] or ''] += i['valor']
    # a convenção de sinal varia por município (D19): escolhe entre D-C, C-D e só débitos a que mais se aproxima da receita da MSC (sem intraorçamentárias)
    modos = {'D-C': lambda n: D[n] - C[n], 'C-D': lambda n: C[n] - D[n], 'D': lambda n: D[n]}
    nrs = set(D) | set(C); ext = lambda m: sum(modos[m](n) for n in nrs if not n.startswith(('7', '9')))
    m = min(modos, key=lambda m: abs(ext(m) / x.rec_msc - 1)); g = collections.Counter()
    for n in nrs: g[grupo(n)] += modos[m](n)
    rows.append(dict(cod_ibge=k, uf=x.uf, pop=x['pop'], rec_msc=x.rec_msc, modo_sinal=m, **g))
d = pd.DataFrame(rows).fillna(0); G = [c for c in d.columns if c not in ('cod_ibge', 'uf', 'pop', 'rec_msc', 'modo_sinal')]
d['soma_grupos'] = d[G].sum(axis=1) - d.intraorcamentaria; d['fecha_pct'] = (d.soma_grupos / d.rec_msc - 1) * 100   # a receita da MSC não inclui as intraorçamentárias
d.round(2).to_csv('catalogo/composicao_receita_2023.csv', index=False)
b = 1e9; t = d[G].sum() / b
txt = f"# Composição da receita realizada de 2023 (MSCE)\n\nBase: {len(d)} municípios calculados com MSCE. Total da MSC: R$ {d.rec_msc.sum()/b:.1f} bi; soma dos grupos sem intraorçamentárias: R$ {d.soma_grupos.sum()/b:.1f} bi.\n\n| Grupo | R$ bi | % da soma |\n|---|---:|---:|\n"
for c in G: txt += f"| {c} | {t[c]:.1f} | {t[c]/(t.sum()-t['intraorcamentaria'])*100:.1f}% |\n"
txt += f"\nFechamento por município (soma dos grupos ÷ receita da MSC − 1): mediana {d.fecha_pct.median():.2f}%; dentro de 3% em {(d.fecha_pct.abs()<=3).mean()*100:.0f}% dos municípios.\n"
open('catalogo/composicao_receita_2023.md', 'w', encoding='utf-8').write(txt); print(txt)
