#!/bin/bash
# uso: siai_parse.sh DIR   (DIR com a2.pdf e a9.pdf)
cd "$1"
pdftotext -layout a2.pdf a2.txt; pdftotext -layout a9.pdf a9.txt
echo "== Anexo 2 (todas as fontes)"
grep -E "^\s*(3\.2\.00\.00\.00|3\.2\.90\.00\.00|4\.6\.00\.00\.00|4\.6\.90\.71\.00|3\.2\.90\.2[1-7]\.00|[34]\.[0-9]\.[0-9]{2}\.91\.00)" a2.txt | sed 's/  */ /g' | awk '{v=$NF; if (v!="0,00") print}'
echo "== Anexo 9, bloco Câmara"
awk '/ÓRGÃO: *0?1 /{f=1;next} f&&/ÓRGÃO:/{f=0} f' a9.txt | grep -oE "[0-9]{1,3}(\.[0-9]{3})*,[0-9]{2}|^ *[0-9]{1,3}\.?$" | grep -v "^0,00$" | tr "\n" " "; echo
