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

echo.
echo === ETAPA 0 (opcional): atualizar a coleta (Siconfi, SIOPS, SIOPE, Portal da Transparencia) ===
echo O Siconfi e o SIOPS sao baixados da internet. Demora de 4 a 6 horas e retoma de onde parou.
set /p COLETA=Atualizar a coleta agora? (s/n): 
if /i "%COLETA%"=="s" (
  cd app_coleta
  python atlas.py --pasta dados --etapas siconfi mscc verificar siops siope transferencias convenios || (cd .. & goto :erro)
  cd ..
)

echo.
echo === ETAPA 1 de 4: recalcular os resultados (demora; mostra o progresso) ===
cd app_coleta
python analisar.py --pasta dados || goto :erro
python confianca.py --pasta dados || goto :erro
python comparar_siops.py --pasta dados
cd ..
copy /Y "%DADOS%\resultado_2023.csv" catalogo\ >nul
copy /Y "%DADOS%\confianca_2023.json" catalogo\ >nul
if exist "%DADOS%\comparacao_siops_2023.csv" copy /Y "%DADOS%\comparacao_siops_2023.csv" catalogo\ >nul

echo.
echo === ETAPA 2 de 4: analises da tese (se uma falhar, segue para a proxima) ===
for %%S in (comparativo_2023 tabelas_projeto_2023 testes_tese_2023 testes_juridicos_2023 robustez_2023 vies_cobertura_2023) do (
  echo - %%S
  python analises\%%S.py || echo   AVISO: %%S falhou; confira o caminho dos arquivos dentro do script.
)

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
