"""Controles da H1 (e insumos da H2) com FPM, complementação do Fundeb e renda do Censo 2022 (2023).
Uso (na raiz): python analises/controles_h1_h2.py  -> catalogo/controles_h1_h2_2023.md"""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
M = pd.DataFrame(json.load(open('prototipo/pesquisa/municipios.json', encoding='utf-8')))
M.columns = ['cod','nome','uf','pop','pibpc','fx','q','recpc','vinc','min','patr','leg','div','prc','amp','fol','est','edu','sau']
F = pd.read_csv('catalogo/fpm_fundeb_2023.csv'); R = pd.read_csv('catalogo/renda_censo2022.csv')
d = M.merge(F, left_on='cod', right_on='cod', how='left').merge(R[['cod_ibge','V06004']], left_on='cod', right_on='cod_ibge', how='left')
d['fpm_pc'] = d.fpm_bruto_est / d['pop']; d['compl_pc'] = d.complem_uniao_fundeb.fillna(0) / d['pop']
d['renda'] = d.V06004; d = d[(d.fpm_pc > 0) & (d.renda > 0) & (d.pibpc > 0)].copy()
for c in ['pibpc','fpm_pc','renda','pop']: d['l_' + c] = np.log(d[c])
d['pibq'] = d.q
out = ['# Controles da H1 (e insumos da H2) (2023)', '', f'Base: {len(d)} municípios calculados com FPM, renda e PIB. Margem ampla em % da receita total (MSC).', '']
def ols(f, nome, termo):
    m = smf.ols(f, d).fit(cov_type='HC1'); b = m.params[termo]; ic = m.conf_int().loc[termo]
    out.append(f'| {nome} | {b:.2f} | {ic[0]:.2f} a {ic[1]:.2f} | {m.rsquared:.2f} |'); return m
out += ['## H1. Efeito do PIB por habitante sobre a margem (pontos por 1 log do PIB pc)', '', '| Modelo | Coeficiente | IC 95% | R² |', '|---|---|---|---|']
ols('amp ~ l_pibpc', 'Sem controle', 'l_pibpc')
ols('amp ~ l_pibpc + C(uf)', 'Efeito fixo de UF', 'l_pibpc')
ols('amp ~ l_pibpc + l_pop + C(uf)', '+ população', 'l_pibpc')
ols('amp ~ l_pibpc + l_fpm_pc + l_pop + C(uf)', '+ FPM por habitante', 'l_pibpc')
ols('amp ~ l_pibpc + l_fpm_pc + compl_pc + l_pop + C(uf)', '+ complementação Fundeb pc', 'l_pibpc')
m = ols('amp ~ l_pibpc + l_fpm_pc + compl_pc + l_renda + l_pop + C(uf)', '+ renda do responsável (Censo 2022)', 'l_pibpc')
out += ['', 'Leitura: se o coeficiente do PIB pc cai pouco ao entrar FPM, Fundeb e renda, a diferença entre quintis não é só dependência de transferência nem renda das famílias.', '']
out += ['## H2', '', 'A exposição ao piso (folha da educação ÷ receita livre) vem da tabela t7 do projeto, que não se recalcula aqui. FPM por habitante, complementação do Fundeb por habitante e renda ficam prontos em `fpm_fundeb_2023.csv` e `renda_censo2022.csv` para entrar como controles no painel 2022 a 2026, quando 2024 for aberto (depois do registro de regras).']
open('catalogo/controles_h1_h2_2023.md', 'w', encoding='utf-8').write('\n'.join(out)); print('\n'.join(out))
