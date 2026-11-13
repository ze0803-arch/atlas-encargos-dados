"""Testes jurídicos da tese, 2023: art. 167 §7º da CF (correspondência encargo-fonte) e art. 11 da LRF (efetiva arrecadação).
Uso: python testes_juridicos_2023.py CATALOGO JURIDICO_CSV SAIDA.md"""
import sys, pandas as pd, numpy as np
from scipy import stats
cat, jur, out = sys.argv[1], sys.argv[2], sys.argv[3]
b = pd.read_csv(f'{cat}/testes_tese_2023_base.csv'); j = pd.read_csv(jur)
tr = pd.read_csv(f'{cat}/transferencias_2023.csv'); cv = pd.read_csv(f'{cat}/convenios_2023.csv')
d = b.merge(j, on='cod_ibge', how='inner').merge(tr[['cod_ibge','sus_acs_ace','outras_voluntarias_especificas']], on='cod_ibge', how='left').merge(cv, on='cod_ibge', how='left').fillna({'convenios_liberado':0})
d = d[d.calc == True].copy()
for c in d.columns:
    if c.startswith(('d_','rf_','n_')): d[c] = d[c].fillna(0)
d['q'] = pd.qcut(d.trib_pc, 5, labels=['Q1 (menor)','Q2','Q3','Q4','Q5 (maior)'])
L = []
P = lambda s='': L.append(s)
def tab(df, **k): P(df.round(k.get('r',1)).to_markdown()); P()
def sp(x, y):
    m = x.notna() & y.notna() & np.isfinite(x) & np.isfinite(y); r, p = stats.spearmanr(x[m], y[m]); return round(r,3), p
def kw(col):
    g = [x[col].dropna().values for _, x in d.groupby('q', observed=True)]; return stats.kruskal(*g)[1]
P('# Testes jurídicos, 2023'); P(); P(f'Municípios calculados com MSCE e dados de impostos: {len(d)}. Medianas; quintis da receita tributária própria por habitante (Q1 = base menor).'); P()
# ---------- art. 167 §7º ----------
P('## A. Art. 167, § 7º, da CF: o encargo vem com a fonte correspondente?'); P()
P('Por área, a despesa liquidada na função é separada pela fonte de recursos que a paga: transferência federal vinculada (SUS 1600/1601 e ACS 1604; FNAS 1660; FNDE 1550-1553 e 1569 e FUNDEB 1540-1543), fonte livre (1500/1501) e outras. "Descoberto" é a parte paga com fonte livre, isto é, o encargo que o município financia com a própria base.'); P()
areas = [('Saúde (função 10)','d_f10',['d_f10_sus','d_f10_acs'],'d_f10_livre'),('Assistência social (função 08)','d_f08',['d_f08_fnas'],'d_f08_livre'),('Educação (função 12)','d_f12',['d_f12_fnde','d_f12_fundeb'],'d_f12_livre')]
res = []
for nome, tot, fed, liv in areas:
    for c in fed + [liv, tot]:
        if c not in d: d[c] = 0
    d['_t'] = d[tot]; ok = d._t > 0
    d[f'cob_{tot}'] = np.where(ok, d[fed].sum(axis=1) / d._t * 100, np.nan)
    d[f'des_{tot}'] = np.where(ok, d[liv] / d._t * 100, np.nan)
    d[f'pc_{tot}'] = np.where(ok, d._t / d['pop'], np.nan)
    res.append((nome, tot))
rows = []
for nome, tot in res:
    for q, x in d.groupby('q', observed=True):
        rows.append(dict(area=nome, q=q, n=x[f'cob_{tot}'].notna().sum(), despesa_pc=x[f'pc_{tot}'].median(), federal_vinculada_pct=x[f'cob_{tot}'].median(), fonte_livre_pct=x[f'des_{tot}'].median()))
t = pd.DataFrame(rows); P('### A1. Cobertura por fonte, mediana por quintil (% da despesa da função)'); P(); P(t.round(1).to_markdown(index=False)); P()
P('### A2. Testes (Spearman com a receita tributária por habitante; Kruskal-Wallis entre quintis)'); P()
r2 = []
for nome, tot in res:
    for lab, col in (('federal vinculada', f'cob_{tot}'), ('fonte livre', f'des_{tot}'), ('despesa por habitante', f'pc_{tot}')):
        rho, p = sp(d.trib_pc, d[col]); r2.append(dict(area=nome, medida=lab, rho=rho, p_spearman=f'{p:.2g}', p_kw=f'{kw(col):.2g}'))
P(pd.DataFrame(r2).to_markdown(index=False)); P()
# excesso sobre o mínimo constitucional
r0 = pd.read_csv(f'{cat}/resultado_2023.csv')[['cod_ibge','minimos_exigidos']]
d = d.merge(r0, on='cod_ibge', how='left', suffixes=('_b',''))
tt = d.d_f10 + d.d_f12; lv = d.d_f10_livre + d.d_f12_livre
d['min_pct'] = np.where(tt > 0, d.minimos_exigidos / tt * 100, np.nan)
d['exc_pct'] = np.where(tt > 0, (lv - d.minimos_exigidos).clip(lower=0) / tt * 100, np.nan)
d['exc_any'] = np.where(tt > 0, (lv > d.minimos_exigidos * 1.05) * 100, np.nan)
P('### A1b. Quanto da parte paga com fonte livre (saúde e educação juntas) é o mínimo constitucional (25% e 15%) e quanto é excedente'); P()
P('O mínimo vem da CF (arts. 198 e 212), não de lei; o § 7º trata de encargo imposto por lei. Excedente = fonte livre gasta nas funções 10 e 12 acima do mínimo exigido calculado pelo sistema.'); P()
t6 = d.groupby('q', observed=True).agg(minimo_pct_despesa=('min_pct','median'), excedente_pct_despesa=('exc_pct','median'), municipios_com_excedente_acima_5pct=('exc_any','mean'))
P(t6.round(1).to_markdown()); P()
rho, p = sp(d.trib_pc, d.exc_pct); P(f'Excedente sobre o mínimo: rho com a base própria = {rho}, p = {p:.2g}; KW p = {kw("exc_pct"):.2g}'); P()
# pisos
P('### A3. Pisos: o lado federal (o custo é tratado no teto de exposição, D54)'); P()
P('Assistência federal ao piso da enfermagem (Lei 14.581/2023, Portaria GM/MS 1.135/2023) e vencimentos de ACS/ACE (fonte 1604), por habitante e como % da despesa de pessoal da função 10 (MSC):'); P()
pa = pd.read_csv(f'{cat}/transferencias_2023_por_acao.csv.gz')
enf = pa[pa['NOME AÇÃO'].str.contains('PISO SALARIAL DOS PROFISSIONAIS DA ENFERMAGEM', na=False)].groupby('cod_ibge').v.sum().rename('enf_fed')
d = d.merge(enf, on='cod_ibge', how='left'); d['enf_fed'] = d.enf_fed.fillna(0)
d['enf_pc'] = d.enf_fed / d['pop']; d['acs_pc'] = d.rf_acs / d['pop']
d['enf_pess10'] = np.where(d.d_f10_pessoal > 0, d.enf_fed / d.d_f10_pessoal * 100, np.nan)
d['acs_pess10'] = np.where(d.d_f10_pessoal > 0, d.rf_acs / d.d_f10_pessoal * 100, np.nan)
g = d.groupby('q', observed=True)
t3 = g.agg(n=('cod_ibge','size'), enf_recebeu=('enf_fed', lambda s: (s > 0).mean() * 100), enf_pc=('enf_pc','median'), enf_pct_pessoal_saude=('enf_pess10','median'), acs_pc=('acs_pc','median'), acs_pct_pessoal_saude=('acs_pess10','median'))
P(t3.round(1).to_markdown()); P()
for lab, col in (('enfermagem (R$/hab)','enf_pc'), ('ACS/ACE (R$/hab)','acs_pc'), ('enfermagem % pessoal saúde','enf_pess10'), ('ACS % pessoal saúde','acs_pess10')):
    rho, p = sp(d.trib_pc, d[col]); P(f'- {lab}: rho = {rho}, p = {p:.2g}; Kruskal-Wallis p = {kw(col):.2g}')
P()
# Fundeb 70%
d['fund70'] = np.where(d.d_fundeb_tot > 0, d.d_fundeb_pessoal / d.d_fundeb_tot * 100, np.nan)
P('### A4. FUNDEB: pessoal (elementos 11, 13 e 16) sobre a despesa nas fontes 1540-1543 (aproximação do mínimo de 70%)'); P()
P(f'Mediana {d.fund70.median():.1f}%; {(d.fund70>=70).mean()*100:.1f}% dos {d.fund70.notna().sum()} com despesa nessas fontes estão em 70% ou mais. Por quintil (mediana): ' + '; '.join(f'{k} {v:.1f}%' for k, v in d.groupby('q', observed=True).fund70.median().items())); P()
# Investimento
d['inv_pct'] = np.where(d.d_tot > 0, d.d_g4 / d.d_tot * 100, np.nan)
d['inv_livre_pct'] = np.where(d.d_g4 > 0, d.d_g4_livre / d.d_g4 * 100, np.nan)
d['inv_pc'] = d.d_g4 / d['pop']
P('### A5. Poder de investir (grupo de despesa 4)'); P()
t5 = d.groupby('q', observed=True).agg(inv_pc=('inv_pc','median'), inv_pct_despesa=('inv_pct','median'), inv_pago_com_fonte_livre_pct=('inv_livre_pct','median'))
P(t5.round(1).to_markdown()); P()
for lab, col in (('investimento por habitante','inv_pc'), ('investimento % da despesa','inv_pct'), ('% do investimento pago com fonte livre','inv_livre_pct')):
    rho, p = sp(d.trib_pc, d[col]); P(f'- {lab}: rho = {rho}, p = {p:.2g}; KW p = {kw(col):.2g}')
P()
# ---------- art. 11 LRF ----------
P('## B. Art. 11 da LRF: efetiva arrecadação dos impostos municipais'); P()
P('Requisito: instituição, previsão e efetiva arrecadação de todos os tributos da competência do ente; o parágrafo único veda transferências voluntárias ao ente que não o cumpra quanto aos impostos. Teste operacional: receita realizada nas naturezas IPTU (1112.50), ITBI (1112.53) e ISS (1114.51) na MSC de dezembro de 2023. "Zero" = nenhuma arrecadação lançada; "baixa" = menos de R$ 10 por habitante.'); P()
for k, lab in (('iptu','IPTU'),('itbi','ITBI'),('iss','ISS')):
    d[f'{k}_pc'] = d[f'n_{k}'] / d['pop']; d[f'{k}_zero'] = d[f'n_{k}'] <= 0; d[f'{k}_baixa'] = d[f'{k}_pc'] < 10
d['qualquer_zero'] = d.iptu_zero | d.itbi_zero | d.iss_zero; d['qualquer_baixa'] = d.iptu_baixa | d.itbi_baixa | d.iss_baixa
d['fx'] = pd.cut(d['pop'], [0, 5000, 10000, 20000, 50000, 1e9], labels=['até 5 mil','5 a 10 mil','10 a 20 mil','20 a 50 mil','50 mil ou mais'])
P('### B1. Municípios sem arrecadação (% do grupo)'); P()
for by, nm in (('q','quintil de base própria'), ('fx','porte')):
    t = d.groupby(by, observed=True).agg(n=('cod_ibge','size'), IPTU_zero=('iptu_zero','mean'), ITBI_zero=('itbi_zero','mean'), ISS_zero=('iss_zero','mean'), algum_zero=('qualquer_zero','mean'), algum_baixa=('qualquer_baixa','mean'))
    for c in t.columns[1:]: t[c] = t[c] * 100
    P(f'Por {nm}:'); P(); P(t.round(1).to_markdown()); P()
tot = d[['iptu_zero','itbi_zero','iss_zero','qualquer_zero','qualquer_baixa']].mean() * 100
P(f'Total ({len(d)}): IPTU zero {tot.iptu_zero:.1f}%; ITBI zero {tot.itbi_zero:.1f}%; ISS zero {tot.iss_zero:.1f}%; algum dos três zero {tot.qualquer_zero:.1f}%; algum abaixo de R$ 10/hab {tot.qualquer_baixa:.1f}%.'); P()
P('### B2. Associação com a base fiscal (logit simples com o log da receita tributária por habitante e da população, efeitos fixos de UF omitidos; o sinal indica a direção)'); P()
import statsmodels.api as sm
d['lt'] = np.log(d.trib_pc.clip(lower=1)); d['lp'] = np.log(d['pop'])
rows = []
for c in ('iptu_zero','itbi_zero','iss_zero','qualquer_zero'):
    m = sm.Logit(d[c].astype(int), sm.add_constant(d[['lt','lp']])).fit(disp=0)
    rows.append(dict(desfecho=c, coef_log_trib_pc=m.params['lt'], p=f"{m.pvalues['lt']:.2g}", coef_log_pop=m.params['lp'], p_pop=f"{m.pvalues['lp']:.2g}"))
P(pd.DataFrame(rows).round(3).to_markdown(index=False)); P()
P('### B3. Exposição à sanção do parágrafo único: transferências voluntárias da União recebidas em 2023'); P()
d['vol'] = d.convenios_liberado + d.outras_voluntarias_especificas.fillna(0)
for lab, col in (('algum imposto com arrecadação zero','qualquer_zero'),('algum imposto abaixo de R$ 10/hab','qualquer_baixa')):
    s = d[d[col]]
    P(f'- {lab}: {len(s)} municípios ({len(s)/len(d)*100:.1f}%); receberam R$ {s.vol.sum()/1e9:,.2f} bilhões em convênios e ações voluntárias específicas ({s.vol.sum()/d.vol.sum()*100:.1f}% do total do grupo analisado); mediana por habitante R$ {(s.vol/s["pop"]).median():.0f} contra R$ {(d[~d[col]].vol/d[~d[col]]["pop"]).median():.0f} nos demais.')
P(); P('Observação: "outras voluntárias específicas" inclui a assistência ao piso da enfermagem, que é obrigação legal; a soma é limite superior da exposição.')
open(out, 'w').write('\n'.join(L)); print('ok', len(d))
