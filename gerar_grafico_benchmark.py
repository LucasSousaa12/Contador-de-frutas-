"""
gerar_grafico_benchmark.py
--------------------------
Benchmark completo: Serial vs 2, 4, 6, 8 e 12 workers.
Usa 15.388 imagens com tempo serial já medido.

Uso:
    python gerar_grafico_benchmark.py --dataset data/apples
"""

import argparse
import csv
import multiprocessing as mp
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from paralelo import process_parallel
from utils import load_image_paths


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", "-d", default="data/apples")
    parser.add_argument("--output",  "-o", default="output")
    return parser.parse_args()


def plot_benchmark(tempo_serial, bench_results, output_dir):
    workers  = [r["workers"]    for r in bench_results]
    tempos   = [r["tempo"]      for r in bench_results]
    speedups = [r["speedup"]    for r in bench_results]
    efics    = [r["eficiencia"] for r in bench_results]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Benchmark: Serial vs Paralelo — Contagem de Maçãs\n"
        "(OpenCV + multiprocessing | 15.388 imagens)",
        fontsize=13, fontweight="bold"
    )

    cores = ["#2980b9", "#27ae60", "#e67e22", "#8e44ad", "#16a085"]

    # 1. Tempo de execução
    ax = axes[0][0]
    labels  = ["Serial"] + [f"{w}w" for w in workers]
    valores = [tempo_serial] + tempos
    bars = ax.bar(labels, valores, color=["#e74c3c"] + cores[:len(workers)])
    ax.set_title("Tempo de Execução (s)")
    ax.set_ylabel("Segundos")
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}s", ha="center", fontsize=8, fontweight="bold")

    # 2. Speedup real vs ideal
    ax = axes[0][1]
    ax.plot(workers, speedups, "o-", color="#2980b9", linewidth=2,
            markersize=8, label="Speedup real")
    ax.plot(workers, workers, "--", color="gray", alpha=0.6, label="Speedup ideal")
    ax.set_title("Speedup")
    ax.set_xlabel("Nº de Workers")
    ax.set_ylabel("Fator de aceleração")
    ax.legend()
    ax.grid(alpha=0.3)
    for w, s in zip(workers, speedups):
        ax.annotate(f"{s:.2f}x", (w, s), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9)

    # 3. Eficiência
    ax = axes[1][0]
    bars = ax.bar([f"{w}w" for w in workers],
                  [e * 100 for e in efics],
                  color=cores[:len(workers)])
    ax.axhline(100, color="gray", linestyle="--", alpha=0.5, label="100% ideal")
    ax.set_title("Eficiência dos Workers (%)")
    ax.set_ylabel("Eficiência (%)")
    ax.set_ylim(0, max(e * 100 for e in efics) + 20)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, efics):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val:.1%}", ha="center", fontsize=9, fontweight="bold")

    # 4. Lei de Amdahl
    ax = axes[1][1]
    melhor_s = max(speedups)
    melhor_w = workers[speedups.index(melhor_s)]
    p = min((melhor_s - 1) / (melhor_s * (1 - 1/melhor_w)), 0.99) if melhor_w > 1 else 0.9

    n_range = np.linspace(1, 16, 200)
    amdahl  = 1 / ((1 - p) + p / n_range)

    ax.plot(n_range, amdahl, "-", color="#c0392b", linewidth=2,
            label=f"Lei de Amdahl (p={p:.2f})")
    ax.plot(workers, speedups, "o", color="#2980b9", markersize=8, label="Speedup real")
    ax.set_title("Lei de Amdahl — Limite Teórico")
    ax.set_xlabel("Nº de Workers")
    ax.set_ylabel("Speedup")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = Path(output_dir) / "benchmark.png"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✔ Gráfico salvo em '{out}'")


def save_csv(tempo_serial, bench_results, output_dir):
    out = Path(output_dir) / "benchmark.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["modo", "workers", "tempo_s", "speedup", "eficiencia"])
        writer.writerow(["serial", 1, f"{tempo_serial:.3f}", "1.00", "100.00%"])
        for r in bench_results:
            writer.writerow([
                "paralelo", r["workers"],
                f"{r['tempo']:.3f}",
                f"{r['speedup']:.2f}",
                f"{r['eficiencia']:.1%}"
            ])
    print(f"✔ CSV salvo em '{out}'")


def main():
    args = parse_args()

    TEMPO_SERIAL  = 150.823
    WORKERS_LIST  = [2, 4, 6, 8, 12]

    print("\n" + "="*58)
    print("  BENCHMARK — Serial vs Paralelo (multiprocessing)")
    print("="*58)
    print(f"  Dataset      : {args.dataset}")
    print(f"  Tempo serial : {TEMPO_SERIAL}s")
    print(f"  Workers      : {WORKERS_LIST}")
    print(f"  CPUs         : {mp.cpu_count()}")
    print("="*58 + "\n")

    # Carregar imagens
    try:
        image_paths = load_image_paths(args.dataset)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

    # Testar cada configuração de workers
    bench_results = []
    for workers in WORKERS_LIST:
        print(f"Testando {workers} workers...", end=" ", flush=True)

        start   = time.perf_counter()
        _, _    = process_parallel(image_paths, num_workers=workers)
        elapsed = time.perf_counter() - start

        speedup    = TEMPO_SERIAL / elapsed
        eficiencia = speedup / workers

        print(f"concluído em {elapsed:.3f}s | Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.1%}")

        bench_results.append({
            "workers":    workers,
            "tempo":      elapsed,
            "speedup":    speedup,
            "eficiencia": eficiencia,
        })

    # Gerar outputs
    save_csv(TEMPO_SERIAL, bench_results, args.output)
    plot_benchmark(TEMPO_SERIAL, bench_results, args.output)

    # Resumo final
    print("\n" + "─"*58)
    print(f"  {'Modo':<18} {'Tempo':>8} {'Speedup':>10} {'Eficiência':>12}")
    print("─"*58)
    print(f"  {'Serial':<18} {TEMPO_SERIAL:>7.1f}s {'1.00x':>10} {'—':>12}")
    for r in bench_results:
        label = f"Paralelo {r['workers']}w"
        print(f"  {label:<18} {r['tempo']:>7.1f}s "
              f"{r['speedup']:>9.2f}x {r['eficiencia']:>11.1%}")
    print("─"*58 + "\n")


if __name__ == "__main__":
    mp.freeze_support()
    main()
