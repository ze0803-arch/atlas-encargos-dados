"""H4b e H4c (projeto recomposto, seção 3.8): IPTU lançado, taxa de realização do IPTU e recuperação da dívida ativa, por município.
Uso: python extrai_h4.py PASTA_DADOS SAIDA.csv   (PASTA_DADOS tem resultado_2023.csv e raw/siconfi/2023/{msce,h4_c1,h4_c1_ant,h4_c4}; os h4_* vêm de: python coletar.py --h4)
Saída por município:
  iptu_lancado       variação patrimonial aumentativa do IPTU (conta 4.1.1.2.1.02.00 = 411210200, variação do ano), em módulo
  iptu_arrec         IPTU arrecadado (MSC classe 6, natureza 11125001)
  taxa_realizacao    iptu_arrec / iptu_lancado
  da_trib_bruta      dívida ativa tributária, saldo final de dezembro do ano (contas 121110*; ver PROVISORIO)
  da_trib_bruta_ant  o mesmo no ano anterior
  da_rec             dívida ativa recebida (naturezas 11125003 IPTU e 11145113 ISS)
  recuperacao_da     da_rec / da_trib_bruta_ant
PROVISORIO: os códigos de conta da dívida ativa (121110 bruta, 121119 ajuste para perdas) foram lidos na MSC de um município grande;
a tese manda confirmá-los no PCASP Estendido de cada exercício (seção 3.8). Se o PCASP indicar outras contas, mude DA_BRUTA e DA_AJUSTE."""
import csv, glob, gzip, json, sys, collections, os
P, OUT = sys.argv[1].rstrip('/'), sys.argv[2]
B = P + '/raw/siconfi/2023/'
DA_BRUTA, DA_AJUSTE, VPA_IPTU = ('121110',), ('121119',), '411210200'
def carrega(rel, k):
    it = []
    fs = {}
    for f in sorted(glob.glob(f'{B}{rel}/*_{k}_{rel}_p*.json.gz')):
        n = f.split('_p')[-1][:3]; fs[n] = f          # última versão de cada página
    for f in fs.values(): it += json.load(gzip.open(f)).get('items', [])
    return it
rows = [x for x in csv.DictReader(open(P + '/resultado_2023.csv', encoding='utf-8'))]
w = csv.writer(open(OUT, 'w', newline='', encoding='utf-8'))
w.writerow(['cod_ibge', 'iptu_lancado', 'iptu_arrec', 'taxa_realizacao', 'da_trib_bruta', 'da_trib_bruta_ant', 'da_rec', 'recuperacao_da', 'tem_h4'])
n_ok = 0
for r in rows:
    k = r['cod_ibge']; c4, c1, c1a, ms = carrega('h4_c4', k), carrega('h4_c1', k), carrega('h4_c1_ant', k), carrega('msce', k)
    tem = bool(c4 or c1)
    lanc = abs(sum((1 if i['natureza_conta'] == 'D' else -1) * i['valor'] for i in c4 if i['conta_contabil'] == VPA_IPTU))
    def estoque(it): return sum((1 if i['natureza_conta'] == 'D' else -1) * i['valor'] for i in it if i['conta_contabil'].startswith(DA_BRUTA))
    arr = da = 0.0
    for i in ms:
        if i['conta_contabil'] != '621200000': continue
        nr = i['natureza_receita'] or ''; v = (1 if i['natureza_conta'] == 'D' else -1) * i['valor']
        if nr.startswith('11125001'): arr += v
        elif nr.startswith(('11125003', '11145113')): da += v
    eb, ea = estoque(c1), estoque(c1a)
    w.writerow([k, round(lanc, 2), round(arr, 2), round(arr / lanc, 4) if lanc > 0 else '', round(eb, 2), round(ea, 2), round(da, 2), round(da / ea, 4) if ea > 0 else '', int(tem)])
    n_ok += tem
print(len(rows), 'municípios;', n_ok, 'com dados de classes 1 e 4 coletados')
