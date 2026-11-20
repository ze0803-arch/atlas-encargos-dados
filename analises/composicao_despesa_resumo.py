"""Resume a composição da despesa liquidada por quintil de PIB por habitante, faixa de população e UF (aplicativo), e grava a composição de cada município (ficha).
Lê catalogo/composicao_despesa_2023.csv e prototipo/pesquisa/municipios.json. Grava catalogo/composicao_despesa_resumo_2023.json e prototipo/pesquisa/composicao_despesa.json.
Natureza (6 grupos): pessoal; outras correntes; juros; investimentos e inversões; amortização; outros. Função (8): educação; saúde; assistência e previdência; administração; urbanismo, saneamento e ambiente; transporte; Legislativa; demais.
A abertura por natureza só vale onde a MSCE informa a natureza da despesa; nos demais (sem_natureza) fica nula e o município entra só na abertura por função.
Participações ponderadas pelo valor (soma do grupo ÷ soma da despesa liquidada)."""
import json, pandas as pd
c = pd.read_csv('catalogo/composicao_despesa_2023.csv')
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8'))).iloc[:, [0, 2, 3, 6]]; M.columns = ['cod_ibge', 'uf', 'pop', 'q']
d = c.drop(columns=['uf', 'pop']).merge(M, on='cod_ibge')
d['has_nat'] = d.sem_natureza.abs() <= 0.5
d['n1'] = d.n_pessoal; d['n2'] = d.n_outras_correntes; d['n3'] = d.n_juros; d['n4'] = d.n_investimentos + d.n_inversoes; d['n5'] = d.n_amortizacao; d['n6'] = d.n_outros
d['f1'] = d.f_educacao; d['f2'] = d.f_saude; d['f3'] = d.f_assist_previdencia; d['f4'] = d.f_administracao; d['f5'] = d.f_urbanismo_saneamento_ambiente; d['f6'] = d.f_transporte; d['f7'] = d.f_legislativa; d['f8'] = d.f_demais_funcoes
N = [f'n{i}' for i in range(1, 7)]; F = [f'f{i}' for i in range(1, 9)]
d['tn'] = d[N].sum(axis=1); d['tf'] = d[F].sum(axis=1); d = d[d.tf > 0]
bins = [0, 5000, 10000, 20000, 50000, 100000, 500000, 1e12]; d['faixa'] = pd.cut(d['pop'], bins, labels=False)
def sh(x, G, t):
    x = x[x.has_nat] if G is N else x
    return [round(float(x[g].sum() / x[t].sum() * 100), 1) for g in G] if len(x) else [0] * len(G)
for g in N: d[g + 'p'] = d[g] / d.tn.where(d.tn > 0) * 100
for g in F: d[g + 'p'] = d[g] / d.tf * 100
dn = d[d.has_nat]
out = dict(n=int(len(d)), n_nat=int(len(dn)), total_bi_n=[round(float(dn[g].sum() / 1e9), 1) for g in N], total_bi_f=[round(float(d[g].sum() / 1e9), 1) for g in F],
           geral_n=sh(d, N, 'tn'), geral_f=sh(d, F, 'tf'),
           q_n=[sh(x, N, 'tn') for _, x in d.groupby('q')], q_f=[sh(x, F, 'tf') for _, x in d.groupby('q')],
           faixa_n=[sh(x, N, 'tn') for _, x in d.groupby('faixa')], faixa_f=[sh(x, F, 'tf') for _, x in d.groupby('faixa')],
           nfaixa=[int(len(x)) for _, x in d.groupby('faixa')], nq=[int(len(x)) for _, x in d.groupby('q')],
           mediana_pessoal_q=[round(float(x[x.has_nat].n1p.median()), 1) for _, x in d.groupby('q')],
           mediana_educ_q=[round(float(x.f1p.median()), 1) for _, x in d.groupby('q')], mediana_saude_q=[round(float(x.f2p.median()), 1) for _, x in d.groupby('q')],
           uf_f=sorted([[u, int(len(x))] + sh(x, F, 'tf') for u, x in d.groupby('uf') if len(x) >= 20], key=lambda r: -(r[2] + r[3])),
           uf_n=sorted([[u, int(len(x[x.has_nat]))] + sh(x, N, 'tn') for u, x in d.groupby('uf') if len(x[x.has_nat]) >= 20], key=lambda r: -r[2]))
json.dump(out, open('catalogo/composicao_despesa_resumo_2023.json', 'w'), ensure_ascii=False, separators=(',', ':'))
fi = {int(r.cod_ibge): [[round(float(r[g + 'p']), 1) for g in N] if r.has_nat and r.tn > 0 else None, [round(float(r[g + 'p']), 1) for g in F]] for _, r in d.iterrows()}
json.dump(fi, open('prototipo/pesquisa/composicao_despesa.json', 'w'), separators=(',', ':'))
print(out['n'], out['n_nat'], out['geral_n'], out['geral_f'], out['mediana_pessoal_q'], out['mediana_educ_q'], len(out['uf_f']), len(out['uf_n']), len(fi))
