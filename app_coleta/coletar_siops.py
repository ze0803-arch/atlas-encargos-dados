#!/usr/bin/env python3
"""Coletor do SIOPS (Demonstrativo da Saúde / RREO Anexo 12) para o Atlas de Encargos.

Faz o mesmo que o formulário do site siops.datasus.gov.br (Consulta de Lei de Responsabilidade Fiscal):
abre a página de consulta (cria a sessão) e envia o POST para rel_LRF.php com ano, UF, período e município.
Guarda o HTML original comprimido (SHA-256 no diário) e extrai: base de cálculo (III), despesa mínima em ASPS
(XVII, 15%), valor aplicado (XVI) e percentual aplicado, para o 6º bimestre.

Uso: python coletar_siops.py --pasta dados --uf RN          (usa <pasta>/entes.json, o mesmo do coletar.py)
     python coletar_siops.py --pasta dados                  (todas as UFs)
Saída: <pasta>/raw/siops/<ano>/<ibge>.html.gz, <pasta>/siops_<ano>.csv e <pasta>/diario_siops.csv. Retomável.
"""
import argparse, csv, gzip, hashlib, html, json, os, re, sys, threading, time, datetime
from concurrent.futures import ThreadPoolExecutor
try:
    import requests
except ImportError:
    sys.exit('Falta o pacote requests. Instale com: pip install requests')
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', type=int, default=2023)
ap.add_argument('--uf', nargs='*', default=[]); ap.add_argument('--periodo', default='2', help='2 = 6º bimestre (SIOPS)')
ap.add_argument('--trabalhadores', type=int, default=3); ap.add_argument('--limite', type=int, default=0)
A = ap.parse_args()
BASE = 'http://siops.datasus.gov.br/'
RAW = os.path.join(A.pasta, 'raw', 'siops', str(A.ano)); os.makedirs(RAW, exist_ok=True)
lock = threading.Lock(); dpath = os.path.join(A.pasta, 'diario_siops.csv'); novo = not os.path.exists(dpath)
df = open(dpath, 'a', newline='', encoding='utf-8'); dw = csv.writer(df)
if novo: dw.writerow(['data_hora_utc', 'ibge', 'http', 'bytes_html', 'sha256', 'resultado', 'tentativas'])

def num(s):
    s = s.strip()
    if not re.fullmatch(r'-?[\d.]+,\d+', s): return None
    return float(s.replace('.', '').replace(',', '.'))

def tokens(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S | re.I)
    t = html.unescape(re.sub(r'<[^>]+>', '\x00', h))
    return [re.sub(r'\s+', ' ', x.strip()) for x in re.split(r'[\x00\n\r\t]+', t) if x.strip()]

def apos(tk, rotulo, n=3, ini=0):
    for i in range(ini, len(tk)):
        if rotulo in tk[i]:
            v = [num(x) for x in tk[i + 1:i + 8]]; v = [x for x in v if x is not None]
            return v[:n], i
    return [], -1

def extrai(h):
    tk = tokens(h); r = {}
    r['homologado'] = next((re.search(r'Homologados em (\S+)', x).group(1) for x in tk if 'Homologados em' in x), '')
    v, i = apos(tk, 'TOTAL DAS RECEITAS RESULTANTES DE IMPOSTOS', 1); r['base_calculo_III'] = v[0] if v else None
    v, _ = apos(tk, 'Despesa Mínima a ser Aplicada em ASPS (XVII) = (III) x 15%', 1); r['minimo_asps_XVII'] = v[0] if v else None
    v, _ = apos(tk, 'VALOR APLICADO EM ASPS (XVI)', 3); r['aplicado_empenhado'], r['aplicado_liquidado'] = (v[0], v[1]) if len(v) >= 2 else (None, None)
    v, _ = apos(tk, 'APLICADO EM ASPS (XVI / III)', 3); r['pct_empenhado'], r['pct_liquidado'] = (v[0], v[1]) if len(v) >= 2 else (None, None)
    return r

def um(m):
    c = str(m['cod_ibge']); arq = os.path.join(RAW, c + '.html.gz')
    if os.path.exists(arq): return
    uf, mun = c[:2], c[:6]
    u = f'{BASE}consleirespfiscal.php?S=1&UF={uf};&Municipio={mun};&Ano={A.ano}&Periodo={A.periodo}'
    h = None; http = None; tent = 0
    for tent in range(1, 4):
        try:
            s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
            s.get(u, timeout=90)
            r = s.post(BASE + 'rel_LRF.php', data={'cmbAno': str(A.ano), 'cmbUF': uf, 'cmbPeriodo': A.periodo, 'cmbMunicipio[]': mun, 'BtConsultar': 'Consultar'}, headers={'Referer': u}, timeout=180)
            http = r.status_code; r.encoding = r.apparent_encoding or 'latin-1'
            if http == 200 and 'APLICADO EM ASPS' in r.text: h = r.text; break
        except Exception as e: http = str(e)[:60]
        time.sleep(3 * tent)
    sha = ''; res = 'vazio'
    if h:
        gz = gzip.compress(h.encode('utf-8'), mtime=0); open(arq, 'wb').write(gz); sha = hashlib.sha256(gz).hexdigest(); res = 'sucesso'
    with lock:
        dw.writerow([datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), c, http, len(h or ''), sha, res, tent]); df.flush()
    time.sleep(0.5)

def resumo(entes):
    saida = os.path.join(A.pasta, f'siops_{A.ano}.csv'); linhas = []
    for m in entes:
        c = str(m['cod_ibge']); arq = os.path.join(RAW, c + '.html.gz')
        if not os.path.exists(arq): continue
        r = extrai(gzip.open(arq, 'rt', encoding='utf-8').read()); r.update(cod_ibge=c, ente=m['ente'], uf=m['uf']); linhas.append(r)
    if linhas:
        cols = ['cod_ibge', 'ente', 'uf', 'homologado', 'base_calculo_III', 'minimo_asps_XVII', 'aplicado_empenhado', 'aplicado_liquidado', 'pct_empenhado', 'pct_liquidado']
        with open(saida, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(linhas)
    print(len(linhas), 'municípios em', saida)

entes = [e for e in json.load(open(os.path.join(A.pasta, 'entes.json'), encoding='utf-8')) if e['esfera'] == 'M' and (not A.uf or e['uf'] in [u.upper() for u in A.uf])]
if A.limite: entes = entes[:A.limite]
pend = [e for e in entes if not os.path.exists(os.path.join(RAW, str(e['cod_ibge']) + '.html.gz'))]
print(len(entes), 'municípios;', len(pend), 'a coletar', flush=True)
with ThreadPoolExecutor(A.trabalhadores) as ex: list(ex.map(um, pend))
resumo(entes)
