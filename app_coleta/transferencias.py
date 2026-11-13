#!/usr/bin/env python3
"""Transferências da União aos municípios por programa (bloco P e receitas vinculadas, D40).
Fonte: Portal da Transparência, "Recursos Transferidos": <ano><mês>_Transferencias.zip
(portaldatransparencia.gov.br/download-de-dados/transferencias/<ano><mês>).
Uso:  python transferencias.py --pasta dados --zips dados/transferencias --ano 2023
Baixa os 12 meses que faltarem em --zips (precisa de internet) e grava <pasta>/transferencias_<ano>.csv (por município e grupo)
e <pasta>/transferencias_<ano>_por_acao.csv (por município e ação, para conferência)."""
import argparse, glob, io, json, os, re, sys, unicodedata, zipfile
import pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--zips', default=None); ap.add_argument('--ano', default='2023'); ap.add_argument('--meses', nargs='*', default=[f'{m:02d}' for m in range(1, 13)]); A = ap.parse_args()
Z = A.zips or os.path.join(A.pasta, 'transferencias'); os.makedirs(Z, exist_ok=True)
def norm(s): return re.sub(r'[^A-Z0-9]', '', unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().upper())
ent = {x['uf'] + '|' + norm(x['ente']): str(x['cod_ibge']) for x in json.load(open(os.path.join(A.pasta, 'entes.json'))) if x['esfera'] == 'M'}
def baixa(mes):
    f = os.path.join(Z, f'{A.ano}{mes}_Transferencias.zip')
    if os.path.exists(f): return f
    import requests
    r = requests.get(f'https://portaldatransparencia.gov.br/download-de-dados/transferencias/{A.ano}{mes}', timeout=300, allow_redirects=True)
    if r.status_code != 200 or r.content[:2] != b'PK': sys.exit(f'Não consegui baixar {A.ano}{mes} (código {r.status_code}). Baixe no navegador e coloque o zip em {Z}.')
    open(f, 'wb').write(r.content); return f
def grupo(r):
    a, o, fu = r['NOME AÇÃO'].upper(), r['NOME ÓRGÃO'].upper(), r['NOME FUNÇÃO']
    if 'FUNDEB' in a: return 'fundeb'
    if r['TIPO TRANSFERÊNCIA'].startswith('Constitucionais'): return 'constitucional_royalties'
    if 'SALARIO-EDUCACAO' in a: return 'salario_educacao'
    if 'PISO DE ATENCAO PRIMARIA' in a: return 'sus_atencao_primaria'
    if 'MEDIA E ALTA COMPLEXIDADE' in a: return 'sus_media_alta'
    if 'AGENTES COMUNITARIOS' in a or 'AGENTES DE COMBATE' in a: return 'sus_acs_ace'
    if fu == 'Saúde' and ('SAUDE' in o): return 'sus_outros'
    if 'ASSISTENCIA SOCIAL' in o: return 'fnas'
    if any(k in a for k in ('ALIMENTACAO ESCOLAR', 'TRANSPORTE ESCOLAR', 'DINHEIRO DIRETO NA ESCOLA')): return 'fnde_programas'
    return 'outras_voluntarias_especificas'
frames = []
for mes in A.meses:
    z = zipfile.ZipFile(baixa(mes)); n = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
    t = pd.read_csv(z.open(n), sep=';', encoding='latin1', dtype=str); t.columns = [x.strip() for x in t.columns]
    t = t[t['CÓDIGO MUNICÍPIO SIAFI'].fillna('') != ''].copy(); t = t[t['TIPO FAVORECIDO'].isin(['Administração Pública Municipal', 'Administração Pública'])]
    t['v'] = t['VALOR TRANSFERIDO'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    t['grupo'] = t.apply(grupo, axis=1); t['mes'] = mes; frames.append(t)
t = pd.concat(frames); t['cod_ibge'] = (t['UF'] + '|' + t['NOME MUNICÍPIO'].map(norm)).map(ent)
# D46: grafias do Portal que diferem do IBGE (nome antigo, ortografia antiga ou sufixo); chave UF|nome normalizado do Portal -> código IBGE
ALIAS = {'PA|ELDORADODOSCARAJAS': '1502954', 'PA|SANTAISABELDOPARA': '1506500', 'TO|COUTODEMAGALHAES': '1706001', 'TO|FORTALEZADOTABOCAO': '1708254',
         'TO|SAOVALERIODANATIVIDADE': '1720499', 'CE|ITAPAGE': '2306306', 'RN|CAMPOGRANDEEXAUGUSTOSEVERO': '2401305', 'RN|JANUARIOCICCO': '2405306',
         'RN|SERRACAIADAEXPRESIDENTEJUSCELINO': '2410306', 'PB|SAODOMINGOSDEPOMBAL': '2513968', 'PB|SERIDO': '2515401', 'PE|BELEMDESAOFRANCISCO': '2601607',
         'PE|IGUARACI': '2606903', 'PE|LAGOADOITAENGA': '2608503', 'MG|BRASOPOLIS': '3108909', 'MG|DONAEUSEBIA': '3122900', 'MG|SAOTHOMEDASLETRAS': '3165206',
         'RJ|PARATI': '3303807', 'RJ|TRAJANODEMORAIS': '3305901', 'MT|POXOREO': '5107008'}
t['cod_ibge'] = t['cod_ibge'].fillna((t['UF'] + '|' + t['NOME MUNICÍPIO'].map(norm)).map(ALIAS))
nm = t[t['cod_ibge'].isna()]['NOME MUNICÍPIO'].nunique()
if nm: print(f'{nm} municípios sem código IBGE por nome (conferir): ', sorted(t[t['cod_ibge'].isna()]['UF'] + '|' + t[t['cod_ibge'].isna()]['NOME MUNICÍPIO'])[:10])
t = t[t['cod_ibge'].notna()]
g = t.pivot_table(index='cod_ibge', columns='grupo', values='v', aggfunc='sum', fill_value=0).reset_index(); g['total'] = g.drop(columns='cod_ibge').sum(axis=1)
g.to_csv(os.path.join(A.pasta, f'transferencias_{A.ano}.csv'), index=False)
t.groupby(['cod_ibge', 'grupo', 'NOME ÓRGÃO', 'NOME AÇÃO'])['v'].sum().reset_index().to_csv(os.path.join(A.pasta, f'transferencias_{A.ano}_por_acao.csv'), index=False)
print('Meses lidos:', ','.join(A.meses), '| municípios:', len(g)); print(g.drop(columns='cod_ibge').sum().round(0).to_string())
