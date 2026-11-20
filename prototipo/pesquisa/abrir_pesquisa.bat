@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Montando a versao de pesquisa...
python build_pesquisa.py || (echo ERRO ao montar. & pause & exit /b 1)
echo.
echo Abrindo http://localhost:8000/atlas_pesquisa.html (para encerrar, feche esta janela ou aperte Ctrl+C)
start "" "http://localhost:8000/atlas_pesquisa.html"
python -m http.server 8000
