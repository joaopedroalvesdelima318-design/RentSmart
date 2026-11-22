# RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico em Python com Programação Orientada a Objetos para automatizar os orçamentos da R.M Imóveis.

## Arquivos
- `rentsmart.py`: código-fonte executável.
- `projecao_exemplo.csv`: exemplo da projeção de 12 meses.
- `RentSmart_Parte_Teorica_Com_Evidencias.pdf`: documentação teórica com evidências, incluindo capturas de tela da execução do sistema e da geração da projeção financeira.

## Requisitos e execução
É necessário ter Python 3.8 ou superior. Não há bibliotecas externas para instalar.

1. Abra o terminal na pasta do projeto.
2. Execute `python rentsmart.py` (em alguns sistemas, `python3 rentsmart.py`).
3. Responda às perguntas apresentadas.
4. O sistema exibirá o orçamento e criará `projecao_rentsmart.csv` na mesma pasta.

## Regras implementadas
- Apartamento: aluguel-base de R$ 700,00; adicional de R$ 200,00 para dois quartos.
- Casa: aluguel-base de R$ 900,00; adicional de R$ 250,00 para dois quartos.
- Estúdio: aluguel-base de R$ 1.200,00.
- Casas e apartamentos: vaga opcional por R$ 300,00 mensais.
- Estúdio: zero vagas ou pacote inicial de duas vagas por R$ 250,00; cada vaga adicional custa R$ 60,00.
- Apartamento sem crianças: desconto de 5% após os adicionais.
- Taxa contratual de R$ 2.000,00, parcelável de uma a cinco vezes. A última parcela é ajustada quando necessário para que a soma seja exatamente R$ 2.000,00.

## Projeção CSV
O arquivo contém os 12 meses, separando aluguel mensal, parcela da taxa contratual e total previsto. Como o enunciado não informa reajustes, o aluguel permanece constante. A taxa aparece somente nos meses abrangidos pelo parcelamento.

## Classes
`Imovel` é a classe abstrata; `Apartamento`, `Casa` e `Estudio` especializam suas regras; `Orcamento` calcula e apresenta os valores e gera o CSV. A herança evita repetição e o polimorfismo permite que cada imóvel aplique seus próprios adicionais.
