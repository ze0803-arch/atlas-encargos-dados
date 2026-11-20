@echo off
chcp 65001 >nul
rem ============================================================
rem Atlas de Encargos: recalcula tudo e remonta o aplicativo.
rem Coloque este arquivo na raiz do repositorio (pasta que contem
rem app_coleta, analises, catalogo e prototipo) e de dois cliques.
rem Para parar: Ctrl+C. Cada etapa mostra o que esta fazendo.
rem ============================================================
setlocal
cd /d "%~dp0"
set DADOS=app_coleta\dados
set MALHA=%TEMP%\br.json

if not exist "%DADOS%\entes.json" (echo ERRO: nao achei %DADOS%\entes.json & pause & exit /b 1)

echo Conferindo pacotes do Python (scipy, statsmodels, tabulate, pandas, requests)...
python -c "import scipy, statsmodels, tabulate, pandas, requests" 2>nul || (echo Instalando pacotes que faltam... & python -m pip install scipy statsmodels tabulate pandas requests || (echo ERRO: nao consegui instalar os pacotes & pause & exit /b 1))

echo.
echo === ETAPA 0 (opcional): atualizar a coleta (Siconfi, SIOPS, SIOPE, Portal da Transparencia) ===
echo O Siconfi e o SIOPS sao baixados da internet. Demora de 4 a 6 horas e retoma de onde parou.
set /p COLETA=Atualizar a coleta agora? (s/n): 
if /i "%COLETA%"=="s" (
  cd app_coleta
  python atlas.py --pasta dados --etapas siconfi mscc verificar siops siope h4 transferencias convenios || (cd .. & goto :erro)
  cd ..
)

echo.
echo === ETAPA 1 de 4: recalcular os resultados (demora; mostra o progresso) ===
cd app_coleta
python analisar.py --pasta dados || goto :erro
python analisar.py --pasta dados --tol 0.03 || goto :erro
python confianca.py --pasta dados || goto :erro
python comparar_siops.py --pasta dados
cd ..
copy /Y "%DADOS%\resultado_2023.csv" catalogo\ >nul
copy /Y "%DADOS%\confianca_2023.json" catalogo\ >nul
if exist "%DADOS%\resultado_2023_tol3.csv" copy /Y "%DADOS%\resultado_2023_tol3.csv" catalogo\ >nul
if exist "%DADOS%\comparacao_siops_2023.csv" copy /Y "%DADOS%\comparacao_siops_2023.csv" catalogo\ >nul

echo.
echo === ETAPA 2 de 4: analises da tese (se uma falhar, segue para a proxima) ===
rem testes_tese precisa de transferencias_2023_por_acao.csv sem compactar dentro de catalogo
if exist "%DADOS%\transferencias_2023_por_acao.csv" (copy /Y "%DADOS%\transferencias_2023_por_acao.csv" catalogo\ >nul) else if not exist catalogo\transferencias_2023_por_acao.csv python -c "import gzip,shutil;shutil.copyfileobj(gzip.open('catalogo/transferencias_2023_por_acao.csv.gz'),open('catalogo/transferencias_2023_por_acao.csv','wb'))"
set C=catalogo
echo - extrai_tributaria (RREO anexo 01)
python analises\extrai_tributaria.py "%DADOS%" || echo   AVISO: extrai_tributaria falhou
if exist "%DADOS%\tributaria_2023.csv" copy /Y "%DADOS%\tributaria_2023.csv" %C%\ >nul
echo - extrai_juridico (MSCE por natureza, fonte e funcao; demora)
python analises\extrai_juridico.py "%DADOS%" %C%\juridico_base_2023.csv || echo   AVISO: extrai_juridico falhou
echo - testes_tese_2023
python analises\testes_tese_2023.py %C% >nul || echo   AVISO: testes_tese_2023 falhou
echo - tabelas_projeto_2023
python analises\tabelas_projeto_2023.py %C% %C%\tabelas_projeto_2023.json || echo   AVISO: tabelas_projeto_2023 falhou
echo - comparativo_2023
python analises\comparativo_2023.py %C% %C%\comparativo_2023.md >nul || echo   AVISO: comparativo_2023 falhou
echo - testes_juridicos_2023
python analises\testes_juridicos_2023.py %C% %C%\juridico_base_2023.csv %C%\testes_juridicos_2023.md >nul || echo   AVISO: testes_juridicos_2023 falhou
echo - robustez_2023
python analises\robustez_2023.py %C% %C%\robustez_2023.md >nul || echo   AVISO: robustez_2023 falhou
echo - vies_cobertura_2023
python analises\vies_cobertura_2023.py %C% %C%\vies_cobertura_2023.md >nul || echo   AVISO: vies_cobertura_2023 falhou
echo - base_independente_2023
python analises\base_independente_2023.py %C% %C%\base_independente_2023.md >nul || echo   AVISO: base_independente_2023 falhou
echo - choque_pisos_2023
python analises\choque_pisos_2023.py %C% >nul || echo   AVISO: choque_pisos_2023 falhou
echo - h4 (IPTU lancado, taxa de realizacao, divida ativa; valor adicionado dos servicos)
python analises\extrai_h4.py "%DADOS%" %C%\h4_2023.csv || echo   AVISO: extrai_h4 falhou
python analises\baixar_ibge_h4.py %C%\va_servicos.csv || echo   AVISO: baixar_ibge_h4 falhou

echo.
echo === ETAPA 3 de 4: malha municipal do IBGE (para o mapa) ===
if not exist "%MALHA%" curl -L -o "%MALHA%" "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio" || goto :erro

echo.
echo === ETAPA 4 de 4: remontar o aplicativo ===
python prototipo\build_prototipo_nacional.py catalogo || goto :erro
python prototipo\build_tese_2023.py || goto :erro
python prototipo\build_real_2023.py || goto :erro
python prototipo\build_comparativo_2023.py || goto :erro
python prototipo\build_readequacao_2023.py || goto :erro
python prototipo\build_graficos_comparar.py || goto :erro
python prototipo\build_estrita.py || goto :erro
python prototipo\build_site_novo.py "%MALHA%" || goto :erro

echo.
echo PRONTO. Aplicativo atualizado em prototipo\atlas_prototipo.html
pause
exit /b 0

:erro
echo.
echo PAROU COM ERRO na etapa acima. Copie a mensagem e envie para quem estiver ajudando.
pause
exit /b 1
