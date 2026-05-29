"""
main.py
-------
Ponto de entrada — versão serial.

Uso:
    python main.py --dataset <pasta_com_imagens> [opções]

Exemplos:
    python main.py --dataset data/apples
    python main.py --dataset data/apples --save-images
    python main.py --dataset data/apples --output meus_resultados
"""

import argparse
import sys
from pathlib import Path

from detector import detect_apples
from processor import process_serial
from utils import (
    load_image_paths,
    plot_summary,
    save_annotated_images,
    save_csv_report,
)


# ──────────────────────────────────────────────────────
# Argumentos de linha de comando
# ──────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Contagem serial de maçãs em imagens usando OpenCV"
    )
    parser.add_argument(
        "--dataset", "-d",
        type=str,
        default="data/apples",
        help="Pasta com as imagens do dataset (padrão: data/apples)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="Pasta de saída para os resultados (padrão: output)"
    )
    parser.add_argument(
        "--save-images",
        action="store_true",
        help="Salva imagens anotadas com os círculos de detecção"
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Limitar processamento às N primeiras imagens (útil para testes)"
    )
    return parser.parse_args()


# ──────────────────────────────────────────────────────
# Callback de progresso
# ──────────────────────────────────────────────────────

def progress_callback(done: int, total: int, result) -> None:
    """Exibe progresso em tempo real no terminal."""
    bar_len  = 30
    filled   = int(bar_len * done / total)
    bar      = "█" * filled + "░" * (bar_len - filled)
    pct      = done / total * 100
    filename = Path(result.image_path).name[:30]
    status   = f"ERR" if result.error else f"{result.apple_count:>3} maçãs"

    print(f"\r  [{bar}] {pct:5.1f}%  {filename:<30}  {status}", end="", flush=True)

    if done == total:
        print()  # quebra de linha ao finalizar


# ──────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    print("\n" + "=" * 58)
    print("   CONTAGEM DE MAÇÃS — Processamento Serial (OpenCV)")
    print("=" * 58)
    print(f"  Dataset  : {args.dataset}")
    print(f"  Saída    : {args.output}")
    if args.limit:
        print(f"  Limite   : {args.limit} imagens")
    print("=" * 58 + "\n")

    # ── 1. Carregar caminhos das imagens ─────────────
    try:
        image_paths = load_image_paths(args.dataset)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[ERRO] {e}")
        sys.exit(1)

    if args.limit:
        image_paths = image_paths[:args.limit]
        print(f"  (limitado às primeiras {args.limit} imagens)")

    # ── 2. Processamento serial ───────────────────────
    print(f"\nProcessando {len(image_paths)} imagens...\n")
    results, elapsed = process_serial(image_paths, progress_callback)

    # ── 3. Exportar resultados ────────────────────────
    print("\nGerando relatórios...")
    save_csv_report(results, elapsed, f"{args.output}/results.csv")
    plot_summary(results, elapsed, f"{args.output}/summary.png")

    if args.save_images:
        save_annotated_images(results, f"{args.output}/annotated")

    # ── 4. Resumo final no terminal ───────────────────
    total_apples = sum(r.apple_count for r in results)
    errors       = [r for r in results if r.error]

    print("\n" + "─" * 58)
    print(f"  Imagens processadas : {len(results)}")
    print(f"  Total de maçãs      : {total_apples}")
    print(f"  Média por imagem    : {total_apples / max(len(results), 1):.1f}")
    print(f"  Tempo total         : {elapsed:.3f}s")
    print(f"  Velocidade          : {len(results) / elapsed:.1f} imgs/s")
    if errors:
        print(f"  Erros               : {len(errors)}")
    print("─" * 58)
    print(f"\nArquivos gerados em '{args.output}/':")
    print("  📊  summary.png   — histograma + estatísticas")
    print("  📄  results.csv   — contagem por imagem")
    if args.save_images:
        print("  🖼   annotated/   — imagens com círculos verdes")
    print()


if __name__ == "__main__":
    main()
