#!/usr/bin/env python3
"""Coleta do SIOPE (FNDE) pela API OData pública de dados abertos. Etapa de conferência: nenhum cálculo da margem depende dela.
Uso: python coletar_siope.py --pasta dados --ano 2023 [--uf RN ...]
Descobre as tabelas do serviço em $metadata e, para cada UF, grava a resposta original (.json.gz) em <pasta>/raw/siope/.
Se o serviço do FNDE estiver fora do ar, avisa e termina sem erro (a etapa é opcional e pode ser repetida depois).
O FNDE não documenta os nomes das tabelas com clareza; o script lista o que encontrou em <pasta>/siope_tabelas.txt."""
import argparse, gzip, json, os, re, sys, time, hashlib
import requests
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); ap.add_argument('--uf', nargs='*', default=[]); ap.add_argument('--periodo', default='6'); A = ap.parse_args()
B = 'https://www.fnde.gov.br/olinda-ide/servico/DADOS_ABERTOS_SIOPE/versao/v1/odata'
D = os.path.join(A.pasta, 'raw', 'siope'); os.makedirs(D, exist_ok=True)
UFS = A.uf or ['AC','AL','AM','AP','BA','CE','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
def get(url, tent=3):
    for i in range(tent):
        try:
            r = requests.get(url, timeout=120, headers={'Accept': 'application/json'})
            if r.status_code == 200: return r
            print(f'  resposta {r.status_code} em {url[:110]}', flush=True)
        except Exception as e: print('  falha de rede:', e, flush=True)
        time.sleep(2 * (i + 1))
    return None
r = get(B + '/$metadata')
if r is None:
    print('AVISO: o serviço de dados abertos do SIOPE (FNDE) não respondeu. Etapa pulada; rode de novo mais tarde.'); sys.exit(0)
fn = re.findall(r'<FunctionImport[^>]*Name="([^"]+)"', r.text) or re.findall(r'<EntitySet[^>]*Name="([^"]+)"', r.text)
open(os.path.join(A.pasta, 'siope_tabelas.txt'), 'w').write('\n'.join(fn)); print('Tabelas encontradas:', ', '.join(fn) or '(nenhuma)')
alvo = [n for n in fn if re.search(r'receita|indicador|despesa|dados.?gerais', n, re.I)]
for n in alvo:
    for uf in UFS:
        f = os.path.join(D, f'{n}_{A.ano}_{A.periodo}_{uf}.json.gz')
        if os.path.exists(f): continue
        itens = []; url = f"{B}/{n}(ano={A.ano},periodo={A.periodo},uf='{uf}')?$format=json"
        while url:
            r = get(url)
            if r is None: print(f'  {n} {uf}: sem resposta; segue'); itens = None; break
            js = r.json(); itens += js.get('value', []); url = js.get('@odata.nextLink')
        if itens is None: continue
        raw = json.dumps({'tabela': n, 'ano': A.ano, 'periodo': A.periodo, 'uf': uf, 'value': itens}, ensure_ascii=False).encode()
        with gzip.open(f, 'wb') as g: g.write(raw)
        print(f'{n} {uf}: {len(itens)} linhas  sha256={hashlib.sha256(raw).hexdigest()[:12]}', flush=True)
print('SIOPE concluído.')
