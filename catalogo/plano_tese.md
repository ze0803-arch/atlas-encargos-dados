# Plano de trabalho da tese (revisão de 19/11/2026)

## Frase central
Encargos fixados nacionalmente de modo uniforme consomem fatias muito diferentes da receita livre dos municípios, e a diferença acompanha a base fiscal de cada um. Todas as hipóteses servem a essa frase. Um resultado principal, um gráfico: margem ampla e estrita por quintil de PIB por habitante, dentro de UF e faixa de população.

## Frentes

### 1. Piso do magistério (H2) como eixo causal
- Desenho: diferenças em diferenças com 2024, 2025 e 2026. Tratamento contínuo = peso da folha da educação na receita livre (exposição). Controle/placebo = folha da saúde.
- Pendente: confirmar os percentuais do reajuste 2024–2026 na portaria do MEC; coletar Fundeb (complementação) e FPM; fixar a regra de exposição antes de abrir 2024.
- Já feito em 2023: razão de exposição entre extremos de quintil (ver tabelas_projeto_2023.json).

### 2. Regras travadas antes de 2024
- Arquivo `catalogo/registro_regras_2024.md` (modelo criado). Preencher, datar, gerar SHA-256 do arquivo e do código (`git rev-parse HEAD`), depositar no Zenodo/OSF antes de coletar ou abrir MSC 2024.
- Limiares do Quadro 7 ficam com o orientador (ainda a definir).
- Coleta bruta de 2022, 2024 e 2025 pode ser feita e selada por hash sem análise.

### 3. Quem falta (27% sem margem calculável)
Feito em `vies_cobertura_2023.md`: cobertura uniforme por porte (71–74%); calculados e não calculados têm população e receita por habitante parecidas; a receita tributária própria por habitante é um pouco maior entre os calculados (mediana 450 contra 414, p = 0,002) e a cobertura sobe de 69,6% (Q1) a 75,4% (Q5); a probabilidade de ser calculado não depende de população, base ou receita no logit com UF fixa; o coeficiente da base é igual com e sem ponderação (1,17 e 1,17; 3,21 e 3,19).
A fazer: repetir após a recoleta dirigida (710 municípios); limites de Manski (pior e melhor caso para os não calculados); reportar a má qualidade da informação como achado, ligada ao Ranking de Qualidade da Informação Contábil.

### 4. Validação fora do método
- Comparação com SIOPE/RREO (`comparar_siops.py`, já existe).
- Cinco municípios conferidos linha a linha com o contador responsável (clientes: Acari, Florânia, Ouro Branco, Timbaúba dos Batistas, São João do Sabugi). Ficha de cada um com a origem de cada número e a conferência.
- Guaratuba (DCA) e as 116 ações de transferência provisórias entram aqui.

### 5. CNM
- Pedir à CNM o que ela tem: estimativas de impacto do piso, relatos de associados, casos.
- Oferecer: simulador, comparação por porte e Estado, ficha por município.
- Manter independência: a CNM valida e comenta, não escolhe resultados.

## O que fica exploratório
H4c (REGIC) e H4b (decomposição do ISS) só avançam se sobrar tempo. Limites declarados: valor adicionado de 2021 contra ISS de 2023; quintil de PIB circular com o valor adicionado dos serviços.

## Linguagem
2023 mostra associação, não causa. "Causa" só depois de 2024–2026.

## Ordem sugerida
1. Rodar recoletar.bat e rodar_tudo.bat (usuário).
2. Preencher e selar registro_regras_2024.md (com o orientador).
3. Coletar e selar MSC 2022/2024/2025 sem analisar.
4. Fichas de validação dos cinco municípios.
5. Contato com a CNM com o protótipo.
6. Só então abrir 2024 conforme as regras seladas.
