"""Valor adicionado dos serviços por município (IBGE, PIB dos Municípios, Sidra tabela 5938, variável 6575:
serviços exclusive administração, defesa, educação e saúde públicas e seguridade social). Uso: python baixar_ibge_h4.py SAIDA.csv
Baixa o ano mais recente publicado (hoje 2021; 2022 e 2023 ainda não saíram) e grava cod_ibge, ano, va_servicos_mil. Precisa de internet."""
import csv, sys, requests
for ano in (2023, 2022, 2021, 2020):
    r = requests.get(f'https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/6575/p/{ano}', timeout=300); r.raise_for_status()
    d = r.json()[1:]; ok = [x for x in d if x['V'] not in ('-', '...', 'X', '')]
    print(ano, len(ok), 'de', len(d), 'com valor')
    if len(ok) > 5000: break
else: sys.exit('Nenhum ano com valor adicionado dos serviços publicado.')
w = csv.writer(open(sys.argv[1], 'w', newline='')); w.writerow(['cod_ibge', 'ano', 'va_servicos_mil'])
for x in ok: w.writerow([x['D1C'], ano, x['V']])
print('Gravado', sys.argv[1], 'ano', ano)
