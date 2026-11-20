# Controles da H1 (e insumos da H2) (2023)

Base: 4336 municípios calculados com FPM, renda e PIB. Margem ampla em % da receita total (MSC).

## H1. Efeito do PIB por habitante sobre a margem (pontos por 1 log do PIB pc)

| Modelo | Coeficiente | IC 95% | R² |
|---|---|---|---|
| Sem controle | 6.58 | 6.22 a 6.93 | 0.24 |
| Efeito fixo de UF | 3.45 | 3.05 a 3.85 | 0.47 |
| + população | 4.23 | 3.84 a 4.63 | 0.52 |
| + FPM por habitante | 4.10 | 3.70 a 4.50 | 0.52 |
| + complementação Fundeb pc | 3.84 | 3.45 a 4.24 | 0.54 |
| + renda do responsável (Censo 2022) | 3.02 | 2.57 a 3.47 | 0.54 |

Leitura: se o coeficiente do PIB pc cai pouco ao entrar FPM, Fundeb e renda, a diferença entre quintis não é só dependência de transferência nem renda das famílias.

## H2

A exposição ao piso (folha da educação ÷ receita livre) vem da tabela t7 do projeto, que não se recalcula aqui. FPM por habitante, complementação do Fundeb por habitante e renda ficam prontos em `fpm_fundeb_2023.csv` e `renda_censo2022.csv` para entrar como controles no painel 2022 a 2026, quando 2024 for aberto (depois do registro de regras).