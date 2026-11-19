#!/usr/bin/env python3
"""Atlas de Encargos: roda a coleta, o cálculo e a conferência em etapas, e gera um relatório de uma página.

Uso:
  python atlas.py --pasta dados                       # todas as etapas, 2023
  python atlas.py --pasta dados --uf RN               # só algumas UFs (coleta)
  python atlas.py --pasta dados --etapas analisar confianca comparar relatorio     # só estas etapas
  python atlas.py --pasta dados --ano 2024

Etapas, na ordem: siconfi, mscc, verificar, siops, siope, transferencias, convenios, analisar, comparar, confianca, relatorio, empacotar.
Cada etapa é retomável. Se uma falhar, o programa para e diz qual; basta rodar de novo.
"""
import argparse, collections, csv, glob, json, os, statistics as st, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
ETAPAS = ['siconfi', 'mscc', 'verificar', 'siops', 'siope', 'transferencias', 'convenios', 'analisar', 'comparar', 'confianca', 'relatorio', 'empacotar']
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--pasta', default='dados'); ap.add_argument('--ano', default='2023'); ap.add_argument('--uf', nargs='*', default=[])
ap.add_argument('--etapas', nargs='*', default=ETAPAS, choices=ETAPAS); ap.add_argument('--trabalhadores', default='4')
A = ap.parse_args()
py = sys.executable
def roda(nome, cmd):
    t0 = time.time(); print(f'\n=== Etapa {ETAPAS.index(nome) + 1}/{len(ETAPAS)}: {nome} ===', flush=True)
    r = subprocess.run([py] + cmd)
    if r.returncode: sys.exit(f'\nA etapa "{nome}" falhou (código {r.returncode}). Corrija ou rode de novo; as etapas anteriores ficam salvas.')
    print(f'--- {nome} concluída em {int(time.time() - t0)} s', flush=True)
uf = (['--uf'] + A.uf) if A.uf else []
base = ['--pasta', A.pasta, '--ano', A.ano]
def script(n): return os.path.join(AQUI, n)

def relatorio():
    p = lambda n: os.path.join(A.pasta, n)
    L = []; w = L.append
    rs = list(csv.DictReader(open(p(f'resultado_{A.ano}.csv'), encoding='utf-8')))
    conf = json.load(open(p(f'confianca_{A.ano}.json'))) if os.path.exists(p(f'confianca_{A.ano}.json')) else {}
    f = lambda x: float(x) if x not in ('', None) else None
    calc = [r for r in rs if r['status'] == 'calculado']; alta = [r for r in calc if not conf.get(r['cod_ibge'])]
    mp = [f(r['margem_ampla_pct_rcl']) for r in calc if f(r['margem_ampla_pct_rcl']) is not None]
    w(f'# Atlas de Encargos {A.ano}: relatório da execução\n')
    w(f'- Municípios: **{len(rs)}** · calculados: **{len(calc)}** ({100*len(calc)/len(rs):.0f}%) · alta confiança: **{len(alta)}** ({100*len(alta)/max(1,len(calc)):.0f}% dos calculados)')
    if mp: w(f'- Margem ampla mediana: **{100*st.median(mp):.1f}%** da RCL\n')
    w('## Cobertura por UF\n'); w('| UF | Municípios | Calculados | % | Alta confiança | Margem mediana (% RCL) |'); w('|---|---|---|---|---|---|')
    for u in sorted({r['uf'] for r in rs}):
        a = [r for r in rs if r['uf'] == u]; c = [r for r in a if r['status'] == 'calculado']; m = [f(r['margem_ampla_pct_rcl']) for r in c if f(r['margem_ampla_pct_rcl']) is not None]
        w(f"| {u} | {len(a)} | {len(c)} | {100*len(c)/len(a):.0f}% | {sum(1 for r in c if not conf.get(r['cod_ibge']))} | {('%.1f%%' % (100*st.median(m))) if m else '—'} |")
    w('\n## Por porte\n'); w('| Faixa | Municípios | Calculados | % | Margem mediana (% RCL) |'); w('|---|---|---|---|---|')
    fx = [('até 5 mil', 0, 5000), ('5 a 10 mil', 5000, 10000), ('10 a 20 mil', 10000, 20000), ('20 a 50 mil', 20000, 50000), ('50 a 100 mil', 50000, 100000), ('100 a 500 mil', 100000, 500000), ('mais de 500 mil', 500000, 1e12)]
    for nome, lo, hi in fx:
        a = [r for r in rs if lo <= int(r['pop']) < hi]; c = [r for r in a if r['status'] == 'calculado']; m = [f(r['margem_ampla_pct_rcl']) for r in c if f(r['margem_ampla_pct_rcl']) is not None]
        if a: w(f"| {nome} | {len(a)} | {len(c)} | {100*len(c)/len(a):.0f}% | {('%.1f%%' % (100*st.median(m))) if m else '—'} |")
    cont = collections.Counter(x for r in rs if r['status'] != 'calculado' for x in r['flags'].split('|') if x != 'OK')
    w('\n## Motivos dos não calculados\n'); w(' · '.join(f'{k} ({v})' for k, v in cont.most_common()) or '—')
    if os.path.exists(p(f'comparacao_siops_{A.ano}.csv')):
        cs = list(csv.DictReader(open(p(f'comparacao_siops_{A.ano}.csv'), encoding='utf-8')))
        def s(x):
            d = sorted(abs(float(l['diferenca_pct'])) for l in x)
            return (len(d), st.median(d), d[int(0.9 * len(d))], 100 * sum(v <= 1 for v in d) / len(d), 100 * sum(v <= 10 for v in d) / len(d)) if d else None
        w('\n## Mínimo de saúde × SIOPS (|diferença| %)\n'); w('| Grupo | n | Mediana | p90 | ≤1% | ≤10% |'); w('|---|---|---|---|---|---|')
        for nome, x in (('Calculados', [l for l in cs if l['status'] == 'calculado']), ('Todos', cs)):
            v = s(x)
            if v: w(f'| {nome} | {v[0]} | {v[1]:.2f} | {v[2]:.1f} | {v[3]:.0f}% | {v[4]:.0f}% |')
        ext = sorted(cs, key=lambda l: -abs(float(l['diferenca_pct'])))[:10]
        w('\nMaiores diferenças (a investigar): ' + '; '.join(f"{l['ente']}/{l['uf']} {float(l['diferenca_pct']):+.0f}%" for l in ext))
    # Bloco P (D37-D40): medido à parte, não desconta a margem
    rl = [r for r in calc if f(r['rec_livre']) and f(r['rec_livre']) > 0]
    cons = [f(r['consorcios']) / f(r['rec_livre']) for r in rl if r.get('consorcios') not in ('', None)]
    if cons:
        w('\n## Bloco P (pactuação), medido à parte da margem\n'); w('| Item | Calculados com dado | Mediana (% da receita livre) | p90 |'); w('|---|---|---|---|')
        q = lambda v: sorted(v)[int(0.9 * (len(v) - 1))]
        w(f'| Consórcios (modalidade 71) | {sum(1 for x in cons if x > 0)} | {100*st.median(cons):.2f}% | {100*q(cons):.2f}% |')
        if os.path.exists(p(f'convenios_{A.ano}.csv')):
            cv = {l['cod_ibge']: l for l in csv.DictReader(open(p(f'convenios_{A.ano}.csv'), encoding='utf-8'))}
            v = [float(cv[r['cod_ibge']]['contrapartida_ano']) / f(r['rec_livre']) if r['cod_ibge'] in cv else 0.0 for r in rl]
            w(f'| Contrapartida de convênios da União | {sum(1 for x in v if x > 0)} | {100*st.median(v):.2f}% | {100*q(v):.2f}% |')
        if os.path.exists(p(f'transferencias_{A.ano}.csv')):
            tr = {l['cod_ibge']: l for l in csv.DictReader(open(p(f'transferencias_{A.ano}.csv'), encoding='utf-8'))}
            for g, nome in (('sus_atencao_primaria', 'SUS atenção primária (recebido)'), ('sus_media_alta', 'SUS média e alta complexidade (recebido)'), ('sus_acs_ace', 'SUS agentes de saúde (recebido)'), ('fnas', 'FNAS (recebido)')):
                v = [float(tr[r['cod_ibge']].get(g) or 0) / f(r['rec_livre']) if r['cod_ibge'] in tr else 0.0 for r in rl]
                if any(v): w(f'| {nome} | {sum(1 for x in v if x > 0)} | {100*st.median(v):.2f}% | {100*q(v):.2f}% |')
    w('\n## Próximos passos\n\n1. Subir os pacotes de `dados/pacotes` ao Zenodo (navegador).\n2. Enviar ao GitHub o catálogo: `diario_extracao.csv`, `diario_siops.csv`, `resultado_%s.csv`, `confianca_%s.json`, `siops_%s.csv`, `comparacao_siops_%s.csv`, `convenios_%s.csv`, `transferencias_%s.csv`.\n3. Levar este relatório ao Claude para investigar as exceções.' % ((A.ano,) * 6))
    txt = '\n'.join(L); open(p(f'relatorio_{A.ano}.md'), 'w', encoding='utf-8').write(txt); print('\n' + txt); print(f'\nRelatório gravado em {p("relatorio_%s.md" % A.ano)}')

for e in ETAPAS:
    if e not in A.etapas: continue
    if e == 'siconfi': roda(e, [script('coletar.py'), '--pasta', A.pasta, '--ano', A.ano, '--trabalhadores', A.trabalhadores] + uf)
    elif e == 'mscc': roda(e, [script('coletar.py'), '--pasta', A.pasta, '--ano', A.ano, '--completar-mscc'] + uf)
    elif e == 'verificar': roda(e, [script('coletar.py'), '--pasta', A.pasta, '--ano', A.ano, '--verificar'] + uf)
    elif e == 'siops': roda(e, [script('coletar_siops.py'), '--pasta', A.pasta, '--ano', A.ano] + uf)
    elif e == 'siope': roda(e, [script('coletar_siope.py'), '--pasta', A.pasta, '--ano', A.ano] + uf)
    elif e == 'transferencias': roda(e, [script('transferencias.py')] + base)
    elif e == 'convenios':
        pc = os.path.join(A.pasta, 'convenios')
        if not glob.glob(os.path.join(pc, '*_Convenios.csv')): roda('convenios', [script('baixar_convenios.py'), '--pasta', A.pasta])
        if glob.glob(os.path.join(pc, '*_Convenios.csv')) and glob.glob(os.path.join(pc, '*_Convenios_OrdensBancarias.csv')): roda(e, [script('convenios.py'), '--pasta', A.pasta, '--csvs', pc, '--ano', A.ano])
        else: print(f'\n=== Etapa {ETAPAS.index(e) + 1}/{len(ETAPAS)}: convenios ===\nPulada: baixe o arquivo de convênios em portaldatransparencia.gov.br/download-de-dados/convenios (o mais recente), descompacte os dois CSV em {pc} e rode de novo.')
    elif e == 'analisar': roda(e, [script('analisar.py')] + base)
    elif e == 'confianca': roda(e, [script('confianca.py')] + base)
    elif e == 'comparar': roda(e, [script('comparar_siops.py')] + base)
    elif e == 'relatorio':
        print(f'\n=== Etapa {ETAPAS.index(e) + 1}/{len(ETAPAS)}: relatorio ==='); relatorio()
    elif e == 'empacotar': roda(e, [script('coletar.py'), '--pasta', A.pasta, '--ano', A.ano, '--empacotar'])
print('\nConcluído.')
