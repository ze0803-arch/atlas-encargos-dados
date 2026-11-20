"""Composição da despesa liquidada de 2023 por município, pela MSCE (contas 622130300, 622130400 e 622130700, as mesmas de liq_msc).
Duas aberturas, cada uma fechando com a despesa liquidada total do município:
  por grupo de natureza da despesa (2º dígito da natureza): pessoal (1), juros (2), outras correntes (3), investimentos (4),
     inversões financeiras (5), amortização da dívida (6), outros (reserva e sem natureza);
  por função: Legislativa 01, Administração 04, Assistência e previdência 08-09, Saúde 10, Educação 12,
     Urbanismo, habitação, saneamento e ambiente 15-18, Transporte 26, demais funções.
Convenção de sinal por município (D19): 'liq+' = débito − crédito; 'liq-' = crédito − débito; 'deb+' = débito − crédito (como em analisar.py).
Municípios cuja fonte é a soma das 12 matrizes mensais (MSCC_12m) usam as pastas mscc_mNN ao lado de msce.
Intraorçamentárias (modalidade de aplicação 91) ficam dentro do total, porque liq_msc as inclui; a coluna 'intra' as mostra à parte.
Uso (na raiz): python analises/composicao_despesa.py PASTA_MSCE [LIMITE]  -> catalogo/composicao_despesa_2023.csv e .md"""
import sys, glob, gzip, json, collections, pandas as pd
B = sys.argv[1].rstrip('/') + '/'; LIM = int(sys.argv[2]) if len(sys.argv) > 2 else None
r = pd.read_csv('catalogo/resultado_2023_tol3.csv'); cal = r[r.status == 'calculado']
if LIM: cal = cal.head(LIM)
NAT = {'1': 'pessoal', '2': 'juros', '3': 'outras_correntes', '4': 'investimentos', '5': 'inversoes', '6': 'amortizacao'}
def fun(f):
    f = (f or '')[:2]
    if f == '01': return 'legislativa'
    if f == '04': return 'administracao'
    if f in ('08', '09'): return 'assist_previdencia'
    if f == '10': return 'saude'
    if f == '12': return 'educacao'
    if f in ('15', '16', '17', '18'): return 'urbanismo_saneamento_ambiente'
    if f == '26': return 'transporte'
    return 'demais_funcoes'
rows = []
for _, x in cal.iterrows():
    k = x.cod_ibge
    fs = glob.glob(f'{B}*_{k}_msce_p*.json.gz') if x.fonte_msc != 'MSCC_12m' else sum((glob.glob(f'{B[:-5]}mscc_m{m:02d}/*_{k}_mscc_m{m:02d}_p*.json.gz') for m in range(1, 13)), [])
    if not fs: continue
    ult = {}
    for f in sorted(fs): ult[(f.split('/')[-2], f.split('_p')[-1][:3])] = f   # última versão de cada página
    s0 = -1 if x.convencao == 'liq-' else 1
    gn, gf = collections.Counter(), collections.Counter(); intra = 0.0; sem = 0
    for f in ult.values():
        for i in json.load(gzip.open(f)).get('items', []):
            if i['conta_contabil'] not in ('622130300', '622130400', '622130700'): continue
            v = i['valor'] * (1 if i['natureza_conta'] == 'D' else -1) * s0; nd = i['natureza_despesa'] or ''
            if not nd: sem += v
            gn[NAT.get(nd[1:2], 'outros')] += v; gf['f_' + fun(i['funcao'])] += v
            if nd[2:4] == '91': intra += v
    rows.append(dict(cod_ibge=k, uf=x.uf, pop=x['pop'], liq_msc=x.liq_msc, convencao=x.convencao, sem_natureza=sem, intra=intra, **{'n_' + a: gn[a] for a in list(NAT.values()) + ['outros']}, **gf))
d = pd.DataFrame(rows).fillna(0)
N = [c for c in d.columns if c.startswith('n_')]; F = [c for c in d.columns if c.startswith('f_')]
d['soma_nat'] = d[N].sum(axis=1); d['soma_fun'] = d[F].sum(axis=1)
d['fecha_nat_pct'] = (d.soma_nat / d.liq_msc - 1) * 100; d['fecha_fun_pct'] = (d.soma_fun / d.liq_msc - 1) * 100
d.round(2).to_csv('catalogo/composicao_despesa_2023.csv', index=False)
b = 1e9; ok = (d.fecha_nat_pct.abs() <= 3)
txt = f"# Composição da despesa liquidada de 2023 (MSCE)\n\nBase: {len(d)} municípios calculados. Total liq_msc: R$ {d.liq_msc.sum()/b:.1f} bi.\n\n| Grupo de natureza | R$ bi | % |\n|---|---|---|\n"
for c in N: txt += f"| {c[2:]} | {d[c].sum()/b:.1f} | {d[c].sum()/d.soma_nat.sum()*100:.1f}% |\n"
txt += "\n| Função | R$ bi | % |\n|---|---|---|\n"
for c in F: txt += f"| {c[2:]} | {d[c].sum()/b:.1f} | {d[c].sum()/d.soma_fun.sum()*100:.1f}% |\n"
txt += f"\nFechamento por município (soma ÷ liq_msc − 1): natureza, mediana {d.fecha_nat_pct.median():.2f}%, dentro de 3% em {ok.mean()*100:.0f}%; função, mediana {d.fecha_fun_pct.median():.2f}%, dentro de 3% em {(d.fecha_fun_pct.abs()<=3).mean()*100:.0f}%. Sem natureza informada em {(d.sem_natureza.abs()>0.5).sum()} municípios.\n"
open('catalogo/composicao_despesa_2023.md', 'w', encoding='utf-8').write(txt); print(txt)
