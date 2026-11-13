"""Extrai da MSCE de dezembro (2023) o que os testes jurídicos precisam, por município:
receita por natureza (impostos próprios) e por fonte, despesa liquidada por função e fonte.
Uso: python extrai_juridico.py PASTA_DADOS SAIDA.csv   (PASTA_DADOS tem resultado_2023.csv e raw/)"""
import csv, glob, gzip, json, sys, collections
from multiprocessing import Pool
P, OUT = sys.argv[1], sys.argv[2]
B = P + '/raw/siconfi/2023/msce/'
FED = {'1600':'sus','1601':'sus','1604':'acs','1660':'fnas','1550':'fnde','1551':'fnde','1552':'fnde','1553':'fnde','1569':'fnde',
       '1540':'fundeb','1541':'fundeb','1542':'fundeb','1543':'fundeb','1751':'cosip','1500':'livre','1501':'livre'}
FUN = ('08','10','12','15','17','04','06','09','13','15','16','20','26','27','28')
def trab(x):
    k = x['cod_ibge']; it = []
    for f in glob.glob(f'{B}*_{k}_msce_p*.json.gz'): it += json.load(gzip.open(f)).get('items', [])
    d = collections.defaultdict(float)
    for i in it:
        cc = i['conta_contabil']; fr = (i['fonte_recursos'] or '')
        sg = 1 if i['natureza_conta'] == 'D' else -1
        if cc == '621200000':
            nr = i['natureza_receita'] or ''
            if nr[:1] not in ('1', '2'): continue
            v = i['valor'] * sg
            d['r_tot'] += v
            for p, n in (('111250','iptu'),('111253','itbi'),('111451','iss'),('111303','irrf'),('112','taxas'),('124150','cosip'),('171','transf_corr')):
                if nr.startswith(p): d['n_' + n] += v
            g = FED.get(fr[:4]) 
            if g: d['rf_' + g] += v
        elif cc in ('622130300', '622130400', '622130700'):
            v = i['valor'] * sg
            f = i['funcao'] or ''; g = FED.get(fr[:4], 'outra')
            d['d_tot'] += v; d[f'd_tot_{g}'] += v
            if f in FUN:
                d[f'd_f{f}'] += v; d[f'd_f{f}_{g}'] += v
            nd = i['natureza_despesa'] or ''
            if nd[1:2] == '4': d['d_g4'] += v; d[f'd_g4_{g}'] += v
            if nd[1:2] == '1': d['d_g1'] += v; d[f'd_g1_{g}'] += v
            if f == '10' and nd[1:2] == '1': d['d_f10_pessoal'] += v
            if f == '10' and nd[1:2] == '1' and g == 'livre': d['d_f10_pessoal_livre'] += v
            if f == '12' and nd[1:2] == '1': d['d_f12_pessoal'] += v
            if f == '12' and nd[1:2] == '1' and g == 'livre': d['d_f12_pessoal_livre'] += v
            if f == '12' and nd[4:6] in ('11','13','16') and g == 'fundeb': d['d_fundeb_pessoal'] += v
            if g == 'fundeb': d['d_fundeb_tot'] += v
    d = dict(d); d['cod_ibge'] = k
    return d
if __name__ == '__main__':
    rows = [x for x in csv.DictReader(open(P + '/resultado_2023.csv')) if x['status'] == 'calculado' and x['fonte_msc'] == 'MSCE']
    with Pool(4) as p: res = p.map(trab, rows, chunksize=20)
    cols = sorted({c for r in res for c in r}); cols.remove('cod_ibge'); cols = ['cod_ibge'] + cols
    w = csv.DictWriter(open(OUT, 'w', newline=''), fieldnames=cols); w.writeheader()
    for r in res: w.writerow(r)
    print(len(res), len(cols))
