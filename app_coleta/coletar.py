#!/usr/bin/env python3
"""Coletor do Siconfi para o Atlas de Encargos.

Baixa, para cada município, as respostas originais da API do Siconfi (extrato de entregas,
MSC de dezembro, RREO, RGF e DCA), grava cada resposta comprimida com hash SHA-256 e
registra tudo no diário de extração. É retomável: município que já tem a última peça
(DCA I-E) é pulado. Ao concluir uma UF, empacota em .tar.

Uso:
  python coletar.py                      # todas as UFs, exercício 2023, pasta ./dados
  python coletar.py --uf RN PB           # só estas UFs
  python coletar.py --uf RN --limite 3   # teste rápido com 3 municípios
  python coletar.py --enviar             # após cada UF, envia o catálogo ao GitHub (pasta dentro de um repositório)
"""
import argparse, csv, datetime, gzip, hashlib, json, os, subprocess, sys, tarfile, threading, time
from concurrent.futures import ThreadPoolExecutor
try:
    import requests
except ImportError:
    sys.exit('Falta o pacote requests. Instale com: pip install requests')

API = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/'
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--pasta', default='dados')
ap.add_argument('--ano', type=int, default=2023)
ap.add_argument('--uf', nargs='*', default=[], help='siglas das UFs (padrão: todas)')
ap.add_argument('--trabalhadores', type=int, default=4, help='requisições simultâneas (máx. 4 recomendado)')
ap.add_argument('--limite', type=int, default=0, help='processa só N municípios (teste)')
ap.add_argument('--empacotar', action='store_true', help='reempacota as UFs concluídas (inclui as matrizes mensais) e, com --enviar, envia ao GitHub')
ap.add_argument('--enviar', action='store_true', help='git add/commit/push do catálogo ao concluir cada UF (os pacotes de brutos não vão ao GitHub)')
ap.add_argument('--verificar', action='store_true', help='confere cada município concluído contra o extrato de entregas e refaz o que o município entregou mas veio vazio (matrizes mensais e MSCE); grava verificacao_coleta.csv')
ap.add_argument('--completar-mscc', action='store_true', help='nos municípios já concluídos, busca as 12 matrizes mensais onde a MSCE não fecha com a DCA')
ap.add_argument('--h4', action='store_true', help='H4b/H4c: busca da MSC de encerramento as classes 1 (saldo final, ano e ano anterior) e 4 (variação do ano), para IPTU lançado e dívida ativa')
A = ap.parse_args()
ANO = A.ano
RAW = os.path.join(A.pasta, 'raw', 'siconfi', str(ANO))
os.makedirs(A.pasta, exist_ok=True)
S = requests.Session()
lock = threading.Lock()
DIARIO = os.path.join(A.pasta, 'diario_extracao.csv')
novo = not os.path.exists(DIARIO)
df = open(DIARIO, 'a', newline='', encoding='utf-8'); dw = csv.writer(df)
if novo:
    dw.writerow(['data_hora_utc','fonte','relatorio','ente','url','http','linhas','resultado','tentativas','segundos','bytes_gz','sha256','arquivo'])
def agora(): return datetime.datetime.now(datetime.timezone.utc)
def dizer(m): print(agora().strftime('%H:%M:%S'), m, flush=True)

def req(rel, ente, ep, params, pagina=1):
    t0 = time.time(); http = None; body = None; err = ''; final = API + ep; tent = 0
    for tent in range(1, 4):
        try:
            r = S.get(API + ep, params=params, timeout=180); http = r.status_code; final = r.url
            if http == 200: body = r.content; break
        except Exception as e: err = str(e)[:80]
        time.sleep(2 * tent)
    js = None; n = 0; arq = ''; sha = ''; nb = 0
    if body is not None:
        try:
            js = json.loads(body); n = len(js.get('items', [])) if isinstance(js, dict) else 0
        except Exception: js = None
        d = os.path.join(RAW, rel); os.makedirs(d, exist_ok=True)
        arq = os.path.join(d, f'siconfi_{ANO}_{ente}_{rel}_p{pagina:03d}_{agora().strftime("%Y%m%dT%H%M%S")}.json.gz')
        gz = gzip.compress(body, mtime=0)
        with open(arq, 'wb') as f: f.write(gz)
        sha = hashlib.sha256(gz).hexdigest(); nb = len(gz)
    res = 'sucesso' if (http == 200 and n > 0) else ('vazio' if http == 200 else 'erro')
    with lock:
        dw.writerow([agora().strftime('%Y-%m-%dT%H:%M:%SZ'),'siconfi',rel,ente,final,http or err,n,res,tent,round(time.time()-t0,1),nb,sha,os.path.relpath(arq, A.pasta) if arq else '']); df.flush()
    time.sleep(0.25)
    return js, n

FALHOU = set()   # municípios com alguma página que falhou nesta rodada (D68)

def paginado(rel, ente, ep, params):
    out = []; off = 0; pg = 1
    while True:
        p = dict(params); p['offset'] = off
        js, n = req(rel, ente, ep, p, pg)
        if js is None:
            # D68: antes, a falha de uma página encerrava a coleta em silêncio e o município ficava como concluído com a matriz truncada.
            FALHOU.add(ente); print(f'AVISO: página {pg} de {rel} ({ente}) falhou; município fica pendente e será refeito na próxima rodada.', file=sys.stderr, flush=True)
            return out
        out += js['items']
        if not js.get('hasMore'): return out
        off += js.get('limit', 5000); pg += 1


def itens_raw(rel, cod):
    d = os.path.join(RAW, rel); out = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.split('_')[2] == str(cod):
                out += json.load(gzip.open(os.path.join(d, f))).get('items', [])
    return out

def precisa_mscc(e):
    """A MSCE de dezembro não fecha com a DCA (receita, 1%) ou veio vazia/curta: testa as 12 matrizes mensais."""
    msce = itens_raw('msce', e)
    if len(msce) <= 30: return True
    dca = next((i['valor'] for i in itens_raw('dca_IC', e) if i['cod_conta'] == 'ReceitasExcetoIntraOrcamentarias' and i['coluna'] == 'Receitas Brutas Realizadas'), None)
    if not dca: return False
    deb = cre = sdeb = 0.0
    for i in msce:
        if i['conta_contabil'] == '621200000' and (i['natureza_receita'] or '')[:1] in ('1', '2', ''):
            if i['natureza_conta'] == 'D': deb += i['valor']; sdeb += i['valor']
            else: cre += i['valor']
    return min(abs((deb - cre) / dca - 1), abs((cre - deb) / dca - 1), abs(sdeb / dca - 1)) > 0.01

def entregas_msc(e):
    """Do extrato de entregas: meses da MSC Agregada entregues pela Prefeitura e se há MSC de Encerramento."""
    ex = [x for x in itens_raw('extrato_entregas', e) if str(x.get('instituicao', '')).startswith('Prefeitura')]
    meses = {x['periodo'] for x in ex if x['entregavel'] == 'MSC Agregada'}
    return meses, any('erramento' in x['entregavel'] for x in ex)

def busca_mscc(e, so_faltantes=False):
    """Busca as 12 matrizes mensais. Se o município entregou o mês (extrato) e a API devolve vazio, tenta de novo (3x)."""
    entregues, _ = entregas_msc(e)
    for mes in range(1, 13):
        rel = 'mscc_m%02d' % mes
        if so_faltantes and itens_raw(rel, e): continue
        for t in range(3):
            r = paginado(rel, e, 'msc_orcamentaria', dict(id_ente=e, an_referencia=ANO, me_referencia=mes, co_tipo_matriz='MSCC', classe_conta=6, id_tv='period_change'))
            if r or mes not in entregues: break
            time.sleep(5 * (t + 1))

def municipio(m):
    e = str(m['cod_ibge'])
    ex = paginado('extrato_entregas', e, 'extrato_entregas', dict(id_ente=e, an_referencia=ANO))
    ent = set(x['entregavel'] for x in ex)
    rreo_simp = any('Resumido de Execução Orçamentária Simplificado' in x for x in ent)
    rgf_simp = any('Gestão Fiscal Simplificado' in x for x in ent)
    paginado('msce', e, 'msc_orcamentaria', dict(id_ente=e, an_referencia=ANO, me_referencia=12, co_tipo_matriz='MSCE', classe_conta=6, id_tv='period_change'))
    tipos = ['RREO Simplificado','RREO'] if rreo_simp else ['RREO','RREO Simplificado']
    for an in ('03','01'):
        for t in tipos:
            if paginado('rreo_anexo'+an, e, 'rreo', dict(an_exercicio=ANO, nr_periodo=6, co_tipo_demonstrativo=t, no_anexo='RREO-Anexo '+an, id_ente=e)): break
    combos = [('RGF Simplificado','S',2),('RGF','Q',3),('RGF','S',2)] if rgf_simp else [('RGF','Q',3),('RGF Simplificado','S',2),('RGF','S',2)]
    for an, pod in (('01','E'),('01','L'),('02','E')):
        for t, per, nr in combos:
            if paginado(f'rgf_anexo{an}_{pod}', e, 'rgf', dict(an_exercicio=ANO, in_periodicidade=per, nr_periodo=nr, co_tipo_demonstrativo=t, no_anexo='RGF-Anexo '+an, co_esfera='M', co_poder=pod, id_ente=e)): break
    for an in ('I-C','I-D'):
        paginado('dca_'+an.replace('-',''), e, 'dca', dict(an_exercicio=ANO, no_anexo='DCA-Anexo '+an, id_ente=e))
    if precisa_mscc(e): busca_mscc(e)
    if e in FALHOU:
        dizer('INCOMPLETO ' + m['ente'] + ' ' + m['uf'] + ' (página falhou; não marcado como concluído)'); return
    paginado('dca_IE', e, 'dca', dict(an_exercicio=ANO, no_anexo='DCA-Anexo I-E', id_ente=e))  # por último: marca município concluído
    if e in FALHOU: dizer('INCOMPLETO ' + m['ente'] + ' ' + m['uf']); return
    dizer('fim ' + m['ente'] + ' ' + m['uf'])

def concluidos():
    d = os.path.join(RAW, 'dca_IE')
    return set(f.split('_')[2] for f in os.listdir(d)) if os.path.isdir(d) else set()

def empacotar(uf, cods, enviar=None):
    """Empacota os brutos da UF em partes de até 80 MB (limite do GitHub: 100 MB por arquivo)."""
    saida = os.path.join(A.pasta, 'pacotes'); os.makedirs(saida, exist_ok=True)
    cods = set(cods); arqs = []
    for rel in sorted(os.listdir(RAW)):
        for f in sorted(os.listdir(os.path.join(RAW, rel))):
            if f.split('_')[2] in cods: arqs.append((rel, f))
    partes = [[]]; tam = 0
    for rel, f in arqs:
        t = os.path.getsize(os.path.join(RAW, rel, f)) + 1024
        if tam + t > 80_000_000 and partes[-1]: partes.append([]); tam = 0
        partes[-1].append((rel, f)); tam += t
    for antigo in os.listdir(saida):
        if antigo.startswith(f'{uf}_completo'): os.remove(os.path.join(saida, antigo))
    for k, parte in enumerate(partes, 1):
        alvo = os.path.join(saida, f'{uf}_completo_p{k:02d}.tar')
        with tarfile.open(alvo, 'w') as tf:
            for rel, f in parte: tf.add(os.path.join(RAW, rel, f), arcname=f'raw/siconfi/{ANO}/{rel}/{f}')
        dizer(f'{uf}: pacote {os.path.basename(alvo)} {os.path.getsize(alvo)//1024} KB')
    if A.enviar: enviar_git(f'Siconfi {ANO}: UF {uf} completa')

def enviar_git(msg):
    """Envia só o catálogo (diário, resultado, lista de entes). Os pacotes de brutos são grandes demais para o GitHub
    (cerca de 2 GB no país) e vão para o Zenodo; nunca se enviam os arquivos soltos de raw/."""
    itens = [p for p in ('diario_extracao.csv', f'resultado_{ANO}.csv', 'entes.json') if os.path.exists(os.path.join(A.pasta, p))]
    subprocess.run(['git', 'add'] + itens, cwd=A.pasta)
    subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=A.pasta)
    subprocess.run(['git', 'push'], cwd=A.pasta)

def completar_mscc(ufs, entes):
    por = {str(e['cod_ibge']): e for e in entes if e['uf'] in ufs}
    d = os.path.join(RAW, 'mscc_m12')
    ja = set(f.split('_')[2] for f in os.listdir(d)) if os.path.isdir(d) else set()
    alvo = [c for c in sorted(concluidos() & set(por)) if c not in ja and precisa_mscc(c)]  # (use --verificar para lacunas em municípios que já têm algum mês)
    if A.limite: alvo = alvo[:A.limite]
    dizer(f'MSCC mensal: {len(alvo)} municípios a completar')
    with ThreadPoolExecutor(A.trabalhadores) as ex: list(ex.map(busca_mscc, alvo))

def busca_h4(e):
    """H4b/H4c (projeto recomposto, seção 3.8): IPTU lançado (VPA, classe 4) e dívida ativa (classe 1), MSC de encerramento (msc_patrimonial)."""
    base = dict(id_ente=e, me_referencia=12, co_tipo_matriz='MSCE')
    for rel, ano, cl, tv in (('h4_c4', ANO, 4, 'period_change'), ('h4_c1', ANO, 1, 'ending_balance'), ('h4_c1_ant', ANO - 1, 1, 'ending_balance')):
        d = os.path.join(RAW, rel)
        if os.path.isdir(d) and any(f.split('_')[2] == str(e) for f in os.listdir(d)): continue
        paginado(rel, e, 'msc_patrimonial', dict(base, an_referencia=ano, classe_conta=cl, id_tv=tv))

def coletar_h4(ufs, entes):
    alvo = sorted(str(e['cod_ibge']) for e in entes if e['uf'] in ufs)
    if A.limite: alvo = alvo[:A.limite]
    dizer(f'H4: {len(alvo)} municípios (classes 1 e 4 da MSC)')
    with ThreadPoolExecutor(A.trabalhadores) as ex: list(ex.map(busca_h4, alvo))

def verificar(ufs, entes):
    """Confere cada município concluído: mês entregue (extrato) sem dados no bruto -> busca de novo; MSCE entregue e vazia -> tenta de novo.
    Registra o resultado em verificacao_coleta.csv (município, lacunas antes/depois, MSCE na API)."""
    por = {str(e['cod_ibge']): e for e in entes if e['uf'] in ufs}
    alvo = sorted(concluidos() & set(por))
    if A.limite: alvo = alvo[:A.limite]
    saida = os.path.join(A.pasta, 'verificacao_coleta.csv'); linhas = []
    def um(c):
        entregues, enc = entregas_msc(c)
        faltam = lambda: [m for m in sorted(entregues) if not itens_raw('mscc_m%02d' % m, c)]
        antes = faltam() if precisa_mscc(c) else []
        if antes: busca_mscc(c, so_faltantes=True)
        depois = faltam() if antes else []
        msce_vazia = len(itens_raw('msce', c)) <= 30
        if msce_vazia and enc:
            for t in range(2):
                if paginado('msce', c, 'msc_orcamentaria', dict(id_ente=c, an_referencia=ANO, me_referencia=12, co_tipo_matriz='MSCE', classe_conta=6, id_tv='period_change')): break
                time.sleep(5)
            msce_vazia = len(itens_raw('msce', c)) <= 30
        with lock: linhas.append([c, por[c]['ente'], por[c]['uf'], ' '.join(map(str, antes)), ' '.join(map(str, depois)), 'sim' if (enc and msce_vazia) else 'nao'])
    dizer(f'verificação: {len(alvo)} municípios concluídos')
    with ThreadPoolExecutor(A.trabalhadores) as ex: list(ex.map(um, alvo))
    with open(saida, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['cod_ibge', 'ente', 'uf', 'meses_faltando_antes', 'meses_faltando_depois', 'msce_entregue_e_vazia_na_api']); w.writerows(sorted(linhas))
    rec = sum(1 for l in linhas if l[3] and not l[4]); aberto = sum(1 for l in linhas if l[4])
    dizer(f'lacunas recuperadas: {rec}; ainda em aberto (entregues mas vazios na API): {aberto}; MSCE vazia na API: {sum(1 for l in linhas if l[5]=="sim")}. Detalhe em {saida}')

def main():
    arq_entes = os.path.join(A.pasta, 'entes.json')
    if not os.path.exists(arq_entes):
        js = S.get(API + 'entes', timeout=180).json()
        with open(arq_entes, 'w', encoding='utf-8') as f: json.dump(js['items'], f, ensure_ascii=False)
    entes = [e for e in json.load(open(arq_entes, encoding='utf-8')) if e['esfera'] == 'M']
    ufs = [u.upper() for u in A.uf] or sorted(set(e['uf'] for e in entes))
    if A.empacotar:
        feitos = concluidos()
        for uf in ufs:
            cods = [str(e['cod_ibge']) for e in entes if e['uf'] == uf]
            if cods and all(c in feitos for c in cods): empacotar(uf, cods)
        if A.enviar: enviar_git(f'Siconfi {ANO}: pacotes e catálogo')
        dizer('CONCLUÍDO'); return
    if A.verificar:
        verificar(ufs, entes); dizer('CONCLUÍDO'); return
    if A.completar_mscc:
        completar_mscc(ufs, entes); dizer('CONCLUÍDO'); return
    if A.h4:
        coletar_h4(ufs, entes); dizer('CONCLUÍDO'); return
    for uf in ufs:
        lista = sorted([e for e in entes if e['uf'] == uf], key=lambda e: e['cod_ibge'])
        feitos = concluidos()
        pend = [e for e in lista if str(e['cod_ibge']) not in feitos]
        if A.limite: pend = pend[:A.limite]
        dizer(f'{uf}: {len(lista)} municípios, {len(pend)} a coletar')
        with ThreadPoolExecutor(A.trabalhadores) as ex: list(ex.map(municipio, pend))
        if not A.limite and all(str(e['cod_ibge']) in concluidos() for e in lista):
            empacotar(uf, [str(e['cod_ibge']) for e in lista])
    dizer('CONCLUÍDO')
main()
