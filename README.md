# DataQuest 2026 — Limpeza dos dados WPP2024

> **Este repositório faz parte de uma competição, não é um projeto pessoal.**
> Trata-se da etapa de **limpeza de dados** feita pelo nosso grupo para o **DataQuest 2026**, um desafio internacional de análise de dados.

## Sobre o DataQuest
O DataQuest é um desafio em que equipes recebem dados reais, escolhem uma pergunta e contam o que descobriram com a análise. Nesta edição, os dados são o **World Population Prospects 2024 (WPP2024)**, da ONU: população, fecundidade, mortalidade e migração de países e regiões, de 1950 a 2100.


Este repositório mostra apenas **como preparamos os dados**. A análise e a apresentação final são feitas separadamente, dentro das regras da competição.

## O que o código faz
Trabalha sobre o arquivo **Medium** do WPP2024.
- Separa **países** (237) de **agregados** (continentes, grupos de renda, mundo), evitando contar população em dobro
- Remove o ano 2101 (só tem a população de 1º de janeiro; os demais indicadores estão vazios)
- Corrige a leitura da Namíbia (ISO2 = "NA" era lido como valor ausente)
- Usa `LocID` como chave, pois alguns nomes de local se repetem
- Cria as colunas `Periodo` (Estimativa até 2023 / Projecao de 2024 em diante), `Regiao` e `Subregiao`
- Junta as colunas do arquivo *Supplement* (nascimentos por sexo e expectativa de vida aos 60)

## Como rodar
1. Baixe os dados originais com a organização do DataQuest ou em https://population.un.org/wpp/ e coloque na pasta `dados/`:
   - `WPP2024_Demographic_Indicators_Medium_csv.gz`
   - `WPP2024_Supplement_Births_and_LE60.csv`
2. Instale o pandas: `pip install pandas`
3. Rode: `python limpeza_dados.py`
4. Os arquivos `paises_limpo.csv` e `agregados_limpo.csv` aparecem na pasta `saida/`.

Também há um notebook para o Google Colab: `DataQuest_Limpeza_WPP2024.ipynb`.

## Fonte dos dados
United Nations, Department of Economic and Social Affairs, Population Division. *World Population Prospects 2024*.
Os dados originais não estão neste repositório e seguem as condições de uso da ONU e do DataQuest.

---

## English summary
This repository contains the **data-cleaning step** our team did for **DataQuest 2026**, an international data analysis challenge. It is a competition entry, not a personal project. The data come from the UN **World Population Prospects 2024** (Medium variant). The script separates countries from regional aggregates, drops the empty 2101 row, fixes the Namibia `"NA"` ISO2 parsing issue, adds region columns and an estimate/projection flag, and merges the Supplement file. To run it: put the original files in `dados/`, then run `python limpeza_dados.py`.
