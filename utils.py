"""
utils.py
--------
Utilitários de suporte:
  - Carregar caminhos de imagens do dataset
  - Salvar imagens anotadas
  - Exportar relatório CSV
  - Gerar gráficos de resumo
"""

import csv
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from detector import DetectionResult


# ──────────────────────────────────────────────────────
# Carregamento do dataset
# ──────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def load_image_paths(dataset_dir: str, recursive: bool = True) -> list[str]:
    """
    Varre o diretório e retorna uma lista ordenada de caminhos de imagens.

    Parâmetros
    ----------
    dataset_dir : str
        Pasta raiz do dataset.
    recursive : bool
        Se True, busca também em subpastas.

    Levanta
    -------
    FileNotFoundError : se o diretório não existir
    ValueError        : se nenhuma imagem for encontrada
    """
    root = Path(dataset_dir)
    if not root.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {dataset_dir}")

    pattern = "**/*" if recursive else "*"
    paths = sorted(
        str(p) for p in root.glob(pattern)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not paths:
        raise ValueError(
            f"Nenhuma imagem encontrada em '{dataset_dir}'.\n"
            f"Formatos suportados: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    print(f"✔ Dataset carregado: {len(paths)} imagens em '{dataset_dir}'")
    return paths


# ──────────────────────────────────────────────────────
# Exportação de resultados
# ──────────────────────────────────────────────────────

def save_annotated_images(
    results: list[DetectionResult],
    output_dir: str = "output/annotated"
) -> None:
    """
    Salva no disco as imagens com os círculos de detecção desenhados.
    Cria o diretório de saída se ele não existir.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    saved = 0
    for r in results:
        if r.error:
            continue
        dest = out / f"{Path(r.image_path).stem}_annotated.jpg"
        cv2.imwrite(str(dest), r.annotated_image)
        saved += 1

    print(f"✔ {saved} imagens anotadas salvas em '{output_dir}'")


def save_csv_report(
    results: list[DetectionResult],
    elapsed: float,
    output_path: str = "output/results.csv"
) -> None:
    """
    Exporta relatório CSV com: nome do arquivo, contagem de maçãs e erros.
    Inclui uma linha de rodapé com totais e tempo de execução.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Cabeçalho
        writer.writerow(["arquivo", "macas_detectadas", "erro"])

        # Dados por imagem
        for r in results:
            writer.writerow([
                Path(r.image_path).name,
                r.apple_count,
                r.error or ""
            ])

        # Rodapé com totais
        writer.writerow([])
        writer.writerow(["TOTAL DE IMAGENS", len(results), ""])
        writer.writerow(["TOTAL DE MAÇÃS",  sum(r.apple_count for r in results), ""])
        writer.writerow(["TEMPO SERIAL (s)", f"{elapsed:.3f}", ""])

    print(f"✔ Relatório CSV salvo em '{output_path}'")


# ──────────────────────────────────────────────────────
# Geração de gráficos
# ──────────────────────────────────────────────────────

def plot_summary(
    results: list[DetectionResult],
    elapsed: float,
    output_path: str = "output/summary.png"
) -> None:
    """
    Gera um painel com:
      - Histograma da distribuição de maçãs por imagem
      - Tabela de estatísticas gerais
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    counts = [r.apple_count for r in results if not r.error]
    if not counts:
        print("Sem dados para plotar.")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Resumo — Detecção Serial de Maçãs (OpenCV)", fontsize=14, fontweight="bold")

    # ── Histograma ──────────────────────────────────────
    bins = range(0, max(counts) + 2)
    ax1.hist(counts, bins=bins, color="#e67e22", edgecolor="white", rwidth=0.82)
    ax1.set_title("Distribuição de Maçãs por Imagem")
    ax1.set_xlabel("Nº de Maçãs Detectadas")
    ax1.set_ylabel("Nº de Imagens")
    ax1.axvline(np.mean(counts), color="#c0392b", linestyle="--",
                linewidth=1.5, label=f"Média: {np.mean(counts):.1f}")
    ax1.legend()

    # ── Tabela de estatísticas ──────────────────────────
    erros = sum(1 for r in results if r.error)
    stats = [
        ["Total de imagens",     len(results)],
        ["Imagens com erro",     erros],
        ["Total de maçãs",       sum(counts)],
        ["Média por imagem",     f"{np.mean(counts):.2f}"],
        ["Mediana",              f"{np.median(counts):.1f}"],
        ["Máximo",               max(counts)],
        ["Mínimo",               min(counts)],
        ["Desvio padrão",        f"{np.std(counts):.2f}"],
        ["Tempo serial (s)",     f"{elapsed:.3f}"],
        ["Imgs/segundo",         f"{len(results)/elapsed:.2f}"],
    ]

    ax2.axis("off")
    table = ax2.table(
        cellText=stats,
        colLabels=["Métrica", "Valor"],
        loc="center",
        cellLoc="left"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1.3, 1.7)
    ax2.set_title("Estatísticas Gerais")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✔ Gráfico de resumo salvo em '{output_path}'")
