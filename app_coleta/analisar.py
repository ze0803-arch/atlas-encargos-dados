#!/usr/bin/env python3
"""Calcula, por município, a conferência MSC x DCA e a margem de decisão do Atlas de Encargos.

Uso: python analisar.py --pasta dados      (a mesma pasta usada por coletar.py)
Saída: <pasta>/resultado_2023.csv. Regras documentadas em catalogo/decisoes.md.

Fonte da MSC por município (decisão D19): usa a MSCE de dezembro; se ela não fechar com a DCA
(receita e despesa liquidada, tolerância de 1%) e houver as 12 matrizes mensais (MSCC), testa a soma
dos 12 meses. Também testa as duas convenções de sinal (D-C e C-D) e "só débitos" na receita.
"""
import argparse, collections, csv, glob, gzip, json, os, re
ap = argparse.ArgumentParser(); ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); ap.add_argument('--tol', type=float, default=0.01, help='tolerância MSC x DCA (padrão 1%%; D45); com outro valor grava resultado_<ano>_tol<N>.csv, só para sensibilidade')
A = ap.parse_args()
B = os.path.join(A.pasta, 'raw', 'siconfi', A.ano) + os.sep
LIVRE = {'500', '501'}   # fonte[1:]: recursos não vinculados (1500 e 1501)
TOL = A.tol

PAG_INCOMPLETA = set()   # (relatório, município) cuja paginação ficou truncada: página faltando ou última página com hasMore (D68)

def carrega(rel, cod):
    """Lê as respostas de um município e relatório. D68: (1) se a mesma página foi baixada mais de uma vez, usa só a mais recente
    (antes, as repetições eram somadas duas vezes); (2) se faltar página ou a última ainda tiver hasMore, registra em PAG_INCOMPLETA."""
    pags = {}
    for f in sorted(glob.glob(f'{B}{rel}/*_{cod}_{rel}_p*.json.gz')):
        mt = re.search(r'_p(\d+)(?:_(\d{8}T\d{6}))?\.json\.gz$', os.path.basename(f))
        n = int(mt.group(1)) if mt else 1; ts = (mt.group(2) or '') if mt else ''
        if n not in pags or ts >= pags[n][0]: pags[n] = (ts, f)
    out = []; ultimo = None
    for n in sorted(pags):
        js = json.load(gzip.open(pags[n][1])); out += js.get('items', []); ultimo = js
    if pags:
        if sorted(pags) != list(range(1, len(pags) + 1)) or (ultimo or {}).get('hasMore'): PAG_INCOMPLETA.add((rel, cod))
    return out

def calcula(itens, modo):
    """modo: ('liq', +1) débito positivo; ('liq', -1) crédito positivo; ('deb', +1) só débitos na receita."""
    tipo, s0 = modo
    m = dict(rec=0.0, liq=0.0, base=0.0, semnat=0.0, rl=0.0, leg=0.0, div=0.0, prec=0.0, min_=0.0, folha=0.0, patr=0.0, fpm_de=0.0, cons=0.0)
    for i in itens:
        cc = i['conta_contabil']; sg = (1 if i['natureza_conta'] == 'D' else -1) * s0; v = i['valor'] * sg
        fr = (i['fonte_recursos'] or '')[1:]
        if cc == '621200000':
            nr = i['natureza_receita'] or ''
            if nr[:1] in ('1', '2', ''):
                vv = (i['valor'] if sg == 1 else 0) if tipo == 'deb' else v
                m['rec'] += vv
                if nr == '': m['semnat'] += vv
                if nr[:3] == '111' or nr[:4] in ('1711', '1721'): m['base'] += vv
                if nr[:6] == '171151' and nr[6:8] != '11': m['fpm_de'] += vv   # FPM art. 159, I, d e e: entra na base do ensino, não na da saúde (D29)
                if fr in LIVRE: m['rl'] += vv
        elif cc in ('622130300', '622130400', '622130700'):
            m['liq'] += v
            if fr in LIVRE:
                nd = i['natureza_despesa'] or ''; g = nd[1:2]; e = nd[4:6]; po = (i['poder_orgao'] or '')[:1]
                if nd[2:4] == '71' and po != '2': m['cons'] += v   # D37 (corrigida em D43): consórcios = modalidade de aplicação 71 (contrato de rateio), bloco P; coluna à parte. O elemento 71 é principal da dívida, não consórcio
                if po == '2': m['leg'] += v
                elif g in ('2', '6'): m['div'] += v
                elif e == '91': m['prec'] += v
                elif i['funcao'] in ('10', '12'): m['min_'] += v
                elif g == '1':
                    m['folha'] += v
                    if e == '13': m['patr'] += v   # D68: contribuição patronal (elemento 13) paga com recurso livre fora de saúde, educação e Legislativo
    return m

ent = {str(e['cod_ibge']): e for e in json.load(open(os.path.join(A.pasta, 'entes.json'), encoding='utf-8'))}
cods = sorted(set(os.path.basename(f).split('_')[2] for f in glob.glob(B + 'dca_IE/*.json.gz')))
rows = []
for _i, c in enumerate(cods):
    if _i % 200 == 0: print('analisando %d de %d ...' % (_i, len(cods)), flush=True)
    if c not in ent: continue
    e = ent[c]; r = dict(cod_ibge=c, ente=e['ente'], uf=e['uf'], pop=int(e['populacao']))
    msce = carrega('msce', c); r['n_msce'] = len(msce)
    mscc = []
    for mes in range(1, 13): mscc += carrega('mscc_m%02d' % mes, c)
    dc = carrega('dca_IC', c); dd = carrega('dca_ID', c)
    r['dca_rec'] = next((i['valor'] for i in dc if i['cod_conta'] == 'ReceitasExcetoIntraOrcamentarias' and i['coluna'] == 'Receitas Brutas Realizadas'), None)
    r['dca_liq'] = next((i['valor'] for i in dd if i['cod_conta'] == 'TotalDespesas' and i['coluna'] == 'Despesas Liquidadas'), None)
    rc = carrega('rreo_anexo03', c); r['n_rreo3'] = len(rc)
    r['rcl_rreo'] = next((i['valor'] for i in rc if i['cod_conta'] == 'RREO3ReceitaCorrenteLiquida' and i['coluna'].startswith('TOTAL')), None)
    rgfe = carrega('rgf_anexo01_E', c); rgfl = carrega('rgf_anexo01_L', c)
    pick = lambda its, cod, col: next((i['valor'] for i in its if i['cod_conta'] == cod and i['coluna'] == col), None)
    r['pessoal_rgf'] = pick(rgfe, 'DespesaComPessoalTotal', 'Valor')          # DTP do Poder Executivo (RGF Anexo 01)
    r['dtp_leg'] = pick(rgfl, 'DespesaComPessoalTotal', 'Valor')              # DTP do Poder Legislativo
    r['rcl_ajustada'] = pick(rgfe, 'ReceitaCorrenteLiquidaAjustada', 'Valor')  # base dos limites da LRF (art. 20)
    r['dtp_exec_pct_rcla'] = pick(rgfe, 'DespesaComPessoalTotal', '% sobre a RCL Ajustada')  # % como publicado no RGF
    r['dtp_total_pct_rcla'] = (100 * (r['pessoal_rgf'] + r['dtp_leg']) / r['rcl_ajustada']) if r['pessoal_rgf'] is not None and r['dtp_leg'] is not None and r['rcl_ajustada'] else None
    r['deducao_fundeb'] = next((i['valor'] for i in dc if i['cod_conta'] == 'ReceitasExcetoIntraOrcamentarias' and i['coluna'] == 'Deduções - FUNDEB'), None)
    r['rec_liquida_fundeb'] = (r['dca_rec'] - (r['deducao_fundeb'] or 0)) if r['dca_rec'] is not None else None  # = receita realizada do RREO Anexo 01
    # escolhe a melhor combinação (fonte, convenção) contra a DCA
    cand = []
    for nome, itens in (('MSCE', msce), ('MSCC_12m', mscc)):
        if len(itens) <= 30: continue
        for modo in (('liq', 1), ('liq', -1), ('deb', 1)):
            m = calcula(itens, modo)
            er = (abs(m['rec'] / r['dca_rec'] - 1) if r['dca_rec'] else 9) + (abs(m['liq'] / r['dca_liq'] - 1) if r['dca_liq'] else 9)
            cand.append((er, nome, modo, m))
    if cand:
        er, nome, modo, m = min(cand, key=lambda x: x[0])
    else:
        nome, modo, m = 'nenhuma', ('liq', 1), calcula([], ('liq', 1))
    r['fonte_msc'] = nome; r['convencao'] = modo[0] + ('+' if modo[1] > 0 else '-')
    r['rec_msc'] = m['rec']; r['liq_msc'] = m['liq']; r['base_impostos'] = m['base']; r['fpm_parcela_de'] = m['fpm_de']; r['minimos_exigidos'] = 0.25 * m['base'] + 0.15 * (m['base'] - m['fpm_de'])  # D29: 25% ensino + 15% saúde
    r.update(rec_livre=m['rl'], leg=m['leg'], divida=m['div'], prec=m['prec'], minimos_funcao=m['min_'], folha_livre=m['folha'], patronal_livre=m['patr'], consorcios=m['cons'])
    r['rec_dif'] = (m['rec'] / r['dca_rec'] - 1) if r['dca_rec'] and m['rec'] else None
    r['liq_dif'] = (m['liq'] / r['dca_liq'] - 1) if r['dca_liq'] and m['liq'] else None
    fl = []
    if not msce and not mscc: fl.append('SEM_MSCE')
    elif nome == 'nenhuma': fl.append('MSCE_INCOMPLETA')
    else:
        if r['rec_dif'] is None or abs(r['rec_dif']) > TOL: fl.append('REC_DIVERGE')
        if r['liq_dif'] is None or abs(r['liq_dif']) > TOL: fl.append('LIQ_DIVERGE')
        if m['rec'] and abs(m['semnat']) / abs(m['rec']) > 0.2: fl.append('SEM_NATUREZA_RECEITA')
    if any((rel, c) in PAG_INCOMPLETA for rel in (['msce'] if nome == 'MSCE' else ['mscc_m%02d' % k for k in range(1, 13)])) and nome != 'nenhuma': fl.append('PAGINACAO_INCOMPLETA')   # D68
    if not r['n_rreo3']: fl.append('RREO3_VAZIO')
    # D26: codificação atípica da fonte livre (reclassificações entre fontes) -> marcar e não calcular
    if m['base'] and not ('SEM_MSCE' in fl or 'MSCE_INCOMPLETA' in fl):
        q = m['rl'] / m['base']
        if q < 0.6 or q > 1.5: fl.append('FONTE_LIVRE_ATIPICA')
    # D26: Legislativo muito acima do teto constitucional (7% da base) -> órgão codificado errado; marcar e não calcular
    if m['base'] and m['leg'] / m['base'] > 0.12: fl.append('LEGISLATIVO_ATIPICO')
    # D26: RCL do RREO inconsistente com a receita líquida da DCA -> não usar o percentual da RCL
    rl_ = r['rec_liquida_fundeb']
    r['rcl_suspeita'] = bool(not r['rcl_rreo'] or (rl_ and not 0.6 <= r['rcl_rreo'] / rl_ <= 1.10))
    if r['rcl_suspeita']: fl.append('RCL_SUSPEITA')
    # D50: receita da MSC incompatível com a população (> R$ 40.000 por habitante) -> erro de lançamento; marcar e não calcular
    if r['pop'] and r['rec_msc'] and r['rec_msc'] / r['pop'] > 40000: fl.append('RECEITA_INCOMPATIVEL')
    r['flags'] = '|'.join(fl) or 'OK'
    if any(f in fl for f in ('SEM_MSCE', 'MSCE_INCOMPLETA', 'PAGINACAO_INCOMPLETA', 'REC_DIVERGE', 'LIQ_DIVERGE', 'SEM_NATUREZA_RECEITA', 'FONTE_LIVRE_ATIPICA', 'LEGISLATIVO_ATIPICO', 'RECEITA_INCOMPATIVEL')):
        r['margem_ampla'] = r['margem_estrita'] = r['margem_ampla_p'] = None; r['status'] = 'marcado_nao_calculado'
    else:
        # D68: a margem ampla desconta também a contribuição patronal (bloco I); a estrita desconta o restante da folha (sem a patronal, para não contar duas vezes)
        a = m['rl'] - r['minimos_exigidos'] - m['patr'] - m['leg'] - m['div'] - m['prec']
        r['margem_ampla'] = a; r['margem_estrita'] = a - (m['folha'] - m['patr']); r['status'] = 'calculado'
        r['margem_ampla_p'] = a - m['cons']   # D37: margem ampla depois do bloco P (consórcios)
    r['margem_ampla_pct_rcl'] = (r['margem_ampla'] / r['rcl_rreo']) if r['margem_ampla'] is not None and r['rcl_rreo'] and not r['rcl_suspeita'] else None
    rows.append(r)
saida = os.path.join(A.pasta, 'resultado_' + A.ano + ('' if A.tol == 0.01 else '_tol%g' % (A.tol * 100)) + '.csv')
with open(saida, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)
print(collections.Counter(r['status'] for r in rows))
print(collections.Counter(x for r in rows for x in r['flags'].split('|')))
print('Resultado gravado em', saida)
