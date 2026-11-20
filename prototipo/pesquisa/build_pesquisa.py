"""Monta a versão de pesquisa do aplicativo.
Uso (na pasta prototipo/pesquisa): python build_pesquisa.py
Lê app.html (modelo) e dados.json e grava atlas_pesquisa.html. O HTML busca municipios.json e mapa.json pelo mesmo diretório,
então abra por um servidor local (python -m http.server) ou publique os três arquivos juntos."""
import json
s = open('app.html', encoding='utf-8').read()
d = json.load(open('dados.json', encoding='utf-8'))
assert '__DADOS__' in s
open('atlas_pesquisa.html', 'w', encoding='utf-8').write(s.replace('__DADOS__', json.dumps(d, ensure_ascii=False, separators=(',', ':'))))
print('ok')
