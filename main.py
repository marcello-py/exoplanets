# %% [markdown]
# # Análise de Exoplanetas na Zona Habitável
# Dataset: NASA Exoplanet Archive

# %% Importações
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# %% Carregar os dados
# comment='#' ignora as linhas de metadados no topo do CSV do Exoplanet Archive
df = pd.read_csv("data/PS_2026.09.06_12.32.13.csv", comment='#')

# %% Remover duplicatas de planetas
# Cada planeta pode ter várias linhas (uma por publicação/referência).
# default_flag == 1 marca a linha "oficial" escolhida pelo Archive.
df = df[df['default_flag'] == 1]
df = df.reset_index(drop=True)

print(f"Planetas únicos: {df.shape[0]}")

# %% Selecionar colunas essenciais
df = df[[
    'pl_name', 'hostname', 'discoverymethod', 'disc_year',
    'pl_insol', 'pl_eqt', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_orbeccen',
    'st_spectype', 'st_teff', 'st_rad', 'st_mass', 'st_lum',
    'sy_dist'
]]

# %% Coluna auxiliar: temperatura em Celsius (mais intuitiva pra leitura)
df['temperatura_celsius'] = df['pl_eqt'] - 273.15

# %% Checar nulos nas colunas-chave para o critério de habitabilidade
df[['pl_orbsmax', 'st_lum', 'pl_insol']].isna().sum()

# %% Critério de zona habitável
# Um planeta é considerado na zona habitável se recebe entre 0.35 e 1.75
# vezes a insolação que a Terra recebe (pl_insol == 1 para a Terra).
# Faixa conservadora usada na literatura.
df['habitavel'] = df['pl_insol'].between(0.35, 1.75)

# %% Filtrar só os planetas com dado de insolação disponível
# (pl_insol nulo vira False em .between(), então isolamos antes de contar)
df_habitavel = df[df['pl_insol'].notna()]

print(f"Planetas com dado de insolação: {df_habitavel.shape[0]}")
print(f"Planetas na zona habitável: {df_habitavel['habitavel'].sum()}")

# %% DataFrame final: só os planetas habitáveis
df_final = df_habitavel[df_habitavel['habitavel'] == True]
df_final.reset_index(drop=True, inplace=True)

df_final.head()

# %% [markdown]
# # Plot considerando a Temperatura de equilíbrio 

# %%
sns.set_theme(style="whitegrid")

cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
g = sns.relplot(
    data=df,
    x="pl_orbsmax", y="pl_eqt",
    hue="habitável", size="pl_bmasse",
   sizes=(10, 200),
)
g.set(xscale="log", yscale="log")
g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.despine(left=True, bottom=True)
plt.savefig('data/exoS.png')