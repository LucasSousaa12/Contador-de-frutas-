"""
grafico_serial.py
-----------------
Gera gráfico da solução serial com dois painéis:
  - Superior: maçãs detectadas por imagem (linha) + média geral
  - Inferior: volume de imagens por faixa de maçãs (barras)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Configurações ──────────────────────────────────────
CSV_PATH    = "output/results.csv"
OUTPUT_PATH = "output/grafico_serial.png"
TEMPO       = 150.823   # troque pelo seu tempo real

# ── Carregar dados ─────────────────────────────────────
df = pd.read_csv(CSV_PATH)
df = df[pd.to_numeric(df["macas_detectadas"], errors="coerce").notna()]
df["macas_detectadas"] = df["macas_detectadas"].astype(int)
df = df[df["erro"].isna() | (df["erro"] == "")]
df = df.reset_index(drop=True)
df["indice"] = df.index + 1

total_imagens = len(df)
total_macas   = df["macas_detectadas"].sum()
media_geral   = df["macas_detectadas"].mean()

# ── Remover outliers extremos para visualização ────────
# Usa percentil 99 como teto do eixo Y (preserva os dados, só ajusta a escala)
teto_y = int(np.percentile(df["macas_detectadas"], 99)) + 2
teto_x = int(np.percentile(df["macas_detectadas"], 99)) + 2

# ── Figura ─────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(16, 9),
    gridspec_kw={"height_ratios": [1.4, 1]},
    facecolor="white"
)

fig.suptitle(
    f"Contagem de Maçãs por Imagem — MinneApple Dataset\n"
    f"Solução Serial ({total_imagens} imagens | {total_macas:,} maçãs detectadas | Tempo: {TEMPO}s)",
    fontsize=14, fontweight="bold", y=0.98
)

# ── Painel superior: linha ─────────────────────────────
ax1.plot(
    df["indice"], df["macas_detectadas"],
    color="#1f77b4", linewidth=0.8, alpha=0.85, label="Maçãs por imagem"
)
ax1.axhline(
    media_geral, color="#d62728", linewidth=1.5,
    linestyle="--", label=f"Média geral: {media_geral:.2f}"
)

ax1.set_title("Maçãs Detectadas por Imagem", fontsize=11, pad=8)
ax1.set_ylabel("Nº de Maçãs Detectadas", fontsize=10)
ax1.set_xlim(1, total_imagens)
ax1.set_ylim(0, teto_y)
ax1.legend(fontsize=9, loc="upper right")
ax1.grid(True, alpha=0.3, linestyle="--")
ax1.tick_params(axis="both", labelsize=9)
ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# ── Painel inferior: barras ────────────────────────────
df_filtrado = df[df["macas_detectadas"] <= teto_x]
contagem = df_filtrado["macas_detectadas"].value_counts().sort_index()

ax2.bar(
    contagem.index, contagem.values,
    color="#2ca02c", alpha=0.85, edgecolor="white", linewidth=0.5,
    label="Imagens/faixa"
)

ax2.set_title("Volume de Imagens por Quantidade de Maçãs Detectadas", fontsize=11, pad=8)
ax2.set_xlabel("Nº de Maçãs Detectadas", fontsize=10)
ax2.set_ylabel("Qtd. de Imagens", fontsize=10)
ax2.legend(fontsize=9, loc="upper right")
ax2.grid(True, alpha=0.3, linestyle="--", axis="y")
ax2.tick_params(axis="both", labelsize=9)
ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
plt.close()

print(f"✔ Gráfico salvo em '{OUTPUT_PATH}'")
print(f"  Total de imagens : {total_imagens}")
print(f"  Total de maçãs   : {total_macas:,}")
print(f"  Média geral      : {media_geral:.2f}")
print(f"  Escala Y/X       : 0 a {teto_y} (percentil 99)")