"""Monta a lista de municípios que vale a pena recoletar (só os que a coleta pode melhorar).
Uso: python lista_recoleta.py PASTA_DADOS SAIDA.csv
Entram: (a) PAGINACAO_INCOMPLETA; (b) meses da MSC entregues e ainda faltando; (c) MSCE entregue e vazia na API; (d) MSCE com 30 linhas ou menos.
Não entram: divergência de receita, RREO vazio, fonte livre atípica etc. (problema da informação enviada pelo município; recoletar não muda)."""
import csv, sys
P, OUT = sys.argv[1].rstrip('/\\'), sys.argv[2]
r = {x['cod_ibge']: x for x in csv.DictReader(open(P + '/resultado_2023.csv', encoding='utf-8'))}
v = {x['cod_ibge']: x for x in csv.DictReader(open(P + '/verificacao_coleta.csv', encoding='utf-8'))}
w = csv.writer(open(OUT, 'w', newline='', encoding='utf-8')); w.writerow(['cod_ibge', 'ente', 'uf', 'motivo', 'status_atual'])
n = {}
for c, x in r.items():
    m = []
    if 'PAGINACAO_INCOMPLETA' in (x['flags'] or ''): m.append('paginacao_incompleta')
    if c in v and v[c]['meses_faltando_depois']: m.append('meses_entregues_faltando')
    if c in v and v[c]['msce_entregue_e_vazia_na_api'] == 'sim': m.append('msce_vazia_na_api')
    if int(x['n_msce'] or 0) <= 30 and not m: m.append('msce_curta')
    if m:
        w.writerow([c, x['ente'], x['uf'], '+'.join(m), x['status']])
        for k in m: n[k] = n.get(k, 0) + 1
print(n, 'total', sum(1 for c, x in r.items() if any([('PAGINACAO_INCOMPLETA' in (x['flags'] or '')), c in v and v[c]['meses_faltando_depois'], c in v and v[c]['msce_entregue_e_vazia_na_api'] == 'sim', int(x['n_msce'] or 0) <= 30])))
