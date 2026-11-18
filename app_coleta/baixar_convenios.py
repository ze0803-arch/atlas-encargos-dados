#!/usr/bin/env python3
"""Baixa o arquivo de convênios mais recente do Portal da Transparência (sem chave) e descompacta em <pasta>/convenios.
Os arquivos são publicados com a data no nome (AAAAMMDD_Convenios.zip); o script procura da data de hoje para trás.
Uso: python baixar_convenios.py --pasta dados"""
import argparse, datetime, io, os, sys, zipfile
import requests
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--dias', type=int, default=400); A = ap.parse_args()
D = os.path.join(A.pasta, 'convenios'); os.makedirs(D, exist_ok=True)
U = 'https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/convenios/%s_Convenios.zip'
hoje = datetime.date.today()
for i in range(A.dias):
    d = (hoje - datetime.timedelta(days=i)).strftime('%Y%m%d')
    if os.path.exists(os.path.join(D, f'{d}_Convenios.csv')): print('Já baixado:', d); sys.exit(0)
    r = requests.head(U % d, timeout=30)
    if r.status_code != 200: continue
    print(f'Baixando convênios de {d} ({int(r.headers.get("content-length", 0)) / 1e6:.0f} MB)...', flush=True)
    z = requests.get(U % d, timeout=900); z.raise_for_status()
    zipfile.ZipFile(io.BytesIO(z.content)).extractall(D); print('Descompactado em', D); sys.exit(0)
sys.exit(f'Não achei arquivo de convênios nos últimos {A.dias} dias. Baixe no navegador (portaldatransparencia.gov.br/download-de-dados/convenios).')
