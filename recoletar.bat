@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Recoleta dirigida: so os municipios que a coleta pode melhorar (cerca de 700). Retoma se interromper.
python analises\lista_recoleta.py app_coleta\dados app_coleta\dados\lista_recoleta.csv || goto :erro
cd app_coleta
python coletar.py --pasta dados --lista dados\lista_recoleta.csv || goto :erro
python analisar.py --pasta dados || goto :erro
python confianca.py --pasta dados || goto :erro
python comparar_siops.py --pasta dados
cd ..
copy /Y app_coleta\dados\resultado_2023.csv catalogo\ >nul
copy /Y app_coleta\dados\confianca_2023.json catalogo\ >nul
if exist app_coleta\dados\comparacao_siops_2023.csv copy /Y app_coleta\dados\comparacao_siops_2023.csv catalogo\ >nul
echo.
echo Pronto. Rode o rodar_tudo.bat (responda n) para refazer as analises e o aplicativo.
pause
exit /b 0
:erro
echo.
echo ERRO. Veja a mensagem acima.
pause
exit /b 1
