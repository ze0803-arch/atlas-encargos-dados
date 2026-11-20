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
  itbi_arrec         ITBI arrecadado (MSC classe 6, natureza 111253), base indireta do ITBI (H4b): comparado ao IPTU lançado por habitante
CORRIGIDO em 20/11/2026 contra o PCASP da Federação (Tesouro): 1.1.2.5 e 1.2.1.1.1.04 são dívida ativa tributária; 1.2.1.1.1.01 a 03 e 05 não são.
O detalhe abaixo do subtítulo (ex.: 1.2.1.1.1.04.03) deve ser conferido no PCASP Estendido de 2023. O sinal da receita (621200000) é fixado por município:
positivo quando a soma da receita tributária (naturezas 11*) é positiva. Coluna sinal_invertido marca onde foi preciso inverter."""
import csv, glob, gzip, json, sys, collections, os
P, OUT = sys.argv[1].rstrip('/'), sys.argv[2]
B = P + '/raw/siconfi/2023/'
DA_BRUTA, VPA_IPTU = ('11251', '1211104'), '411210200'   # D73b: dívida ativa tributária = curto prazo 1.1.2.5.1* + longo prazo 1.2.1.1.1.04* (antes: 121110*, que incluía créditos tributários a receber, clientes e empréstimos)
def carrega(rel, k):
    it = []
    fs = {}
    for f in sorted(glob.glob(f'{B}{rel}/*_{k}_{rel}_p*.json.gz')):
        n = f.split('_p')[-1][:3]; fs[n] = f          # última versão de cada página
    for f in fs.values(): it += json.load(gzip.open(f)).get('items', [])
    return it
rows = [x for x in csv.DictReader(open(P + '/resultado_2023.csv', encoding='utf-8'))]
w = csv.writer(open(OUT, 'w', newline='', encoding='utf-8'))
w.writerow(['cod_ibge', 'iptu_lancado', 'iptu_arrec', 'taxa_realizacao', 'da_trib_bruta', 'da_trib_bruta_ant', 'da_rec', 'recuperacao_da', 'itbi_arrec', 'tem_h4', 'sinal_invertido', 'flag_h4'])
n_ok = 0
for r in rows:
    k = r['cod_ibge']; c4, c1, c1a, ms = carrega('h4_c4', k), carrega('h4_c1', k), carrega('h4_c1_ant', k), carrega('msce', k)
    tem = bool(c4 or c1)
    lanc = abs(sum((1 if i['natureza_conta'] == 'D' else -1) * i['valor'] for i in c4 if i['conta_contabil'] == VPA_IPTU))
    def estoque(it): return sum((1 if i['natureza_conta'] == 'D' else -1) * i['valor'] for i in it if i['conta_contabil'].startswith(DA_BRUTA))
    arr = da = itbi = tot = 0.0
    for i in ms:
        if i['conta_contabil'] != '621200000': continue
        nr = i['natureza_receita'] or ''; v = (1 if i['natureza_conta'] == 'D' else -1) * i['valor']; tot += v if nr.startswith('11') else 0
        if nr.startswith('11125001'): arr += v
        elif nr.startswith(('11125003', '11145113')): da += v
        elif nr.startswith('111253'): itbi += v
    inv = int(tot < 0)
    if inv: arr, da, itbi = -arr, -da, -itbi
    eb, ea = estoque(c1), estoque(c1a)
    marca = ';'.join(x for x, c in (('SEM_LANCAMENTO_IPTU', lanc == 0 and arr > 0), ('ARREC_MAIOR_LANCADO', lanc > 0 and arr > 1.5 * lanc), ('ARREC_NEGATIVO', arr < 0), ('DA_NEGATIVA', eb < 0 or ea < 0)) if c)
    w.writerow([k, round(lanc, 2), round(arr, 2), round(arr / lanc, 4) if lanc > 0 else '', round(eb, 2), round(ea, 2), round(da, 2), round(da / ea, 4) if ea > 0 else '', round(itbi, 2), int(tem), inv, marca])
    n_ok += tem
print(len(rows), 'municípios;', n_ok, 'com dados de classes 1 e 4 coletados')
