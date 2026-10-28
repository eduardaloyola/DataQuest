"""
Limpeza dos dados WPP2024 (DataQuest 2026)
Gera:
  - paises_limpo.csv    : só países/áreas, 1950-2100, com Região/Sub-região e colunas do suplemento
  - agregados_limpo.csv : regiões, grupos de renda, mundo etc. (NUNCA somar com os países)
Uso: python limpeza_dados.py  (coloque os arquivos da ONU na pasta "dados/")
"""
import pandas as pd

PASTA = "dados/"   # pasta com os arquivos originais da ONU
SAIDA = "saida/"   # pasta onde os CSVs limpos serão salvos

import os
os.makedirs(SAIDA, exist_ok=True)

# 1) Carregar. keep_default_na=False + na_values explícito evita que a Namíbia
#    (ISO2 = "NA") seja lida como valor ausente.
df = pd.read_csv(PASTA + "WPP2024_Demographic_Indicators_Medium_csv.gz",
                 compression="gzip", encoding="utf-8-sig", low_memory=False,
                 keep_default_na=False, na_values=[""])
# colunas de texto ficam "" (não NaN) quando vazias -> padronizar
for c in ["Notes", "ISO3_code", "ISO2_code", "LocTypeName"]:
    df[c] = df[c].replace("", pd.NA)

# 2) Ano 2101 está 100% vazio nos indicadores (só tem TPopulation1Jan) -> remover
df = df[df["Time"] <= 2100].copy()

# 3) Os ~234 grupos "ad hoc" vêm sem tipo -> rotular
df["LocTypeName"] = df["LocTypeName"].fillna("Ad Hoc groups")

# 4) Nomes de Location NÃO são únicos (Australia/New Zealand e
#    Latin America and the Caribbean aparecem 2x, com LocIDs diferentes).
#    Sempre usar LocID como chave.

# 5) Marcar estimativa x projeção
df["Periodo"] = df["Time"].apply(lambda t: "Estimativa" if t <= 2023 else "Projecao")

# 6) Hierarquia: país -> sub-região -> região geográfica (via ParentID)
loc = df.drop_duplicates("LocID").set_index("LocID")
sub = loc[loc.LocTypeName == "Subregion"]["Location"]
reg = loc[loc.LocTypeName == "Geographic region"]["Location"]
sub_parent = loc[loc.LocTypeName == "Subregion"]["ParentID"]

# 7) Separar países de agregados
paises = df[df.LocTypeName == "Country/Area"].copy()
paises["Subregiao"] = paises["ParentID"].map(sub)
paises["Regiao"] = paises["ParentID"].map(sub_parent).map(reg)
# Alguns países (ex.: América do Norte) ligam direto à região, sem sub-região
# América do Norte: o ParentID (918) não existe como linha no arquivo -> preencher à mão
na = paises["ParentID"] == 918
paises.loc[na, ["Subregiao", "Regiao"]] = "Northern America"

# 8) Juntar suplemento (BirthsMale/Female, LE60*). Vaticano não tem linhas lá.
sup = pd.read_csv(PASTA + "WPP2024_Supplement_Births_and_LE60.csv", encoding="utf-8-sig",
                  keep_default_na=False, na_values=[""])
sup = sup.drop(columns=["ISO3_code", "Location"])
paises = paises.merge(sup, on=["LocID", "Time"], how="left")

# 9) Remover colunas administrativas sem valor analítico
drop = ["SortOrder", "SDMX_code", "LocTypeID", "ParentID", "VarID", "Variant", "Notes"]
paises = paises.drop(columns=drop)
agreg = df[df.LocTypeName != "Country/Area"].drop(columns=drop + ["ISO3_code", "ISO2_code"])

paises.to_csv(SAIDA + "paises_limpo.csv", index=False)
agreg.to_csv(SAIDA + "agregados_limpo.csv", index=False)
print("paises:", paises.shape, "| locais:", paises.LocID.nunique())
print("agregados:", agreg.shape, "| locais:", agreg.LocID.nunique())
