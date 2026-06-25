"""
paralelo.py
-----------
Processamento PARALELO das imagens usando multiprocessing.Pool.

Testa com 2, 4, 8 e 12 workers e compara com o tempo serial,
calculando speedup e eficiência para cada configuração.
"""

import time
import multiprocessing as mp
from multiprocessing import Pool

from detector import DetectionResult, detect_apples


# ─────────────────────────────────────────────────────
# Worker — deve estar no nível do módulo para funcionar
# com multiprocessing (necessário para serialização)
# ─────────────────────────────────────────────────────

def _worker(image_path: str) -> DetectionResult:
    return detect_apples(image_path)


# ─────────────────────────────────────────────────────
# Processamento paralelo
# ─────────────────────────────────────────────────────

def process_parallel(
    image_paths: list[str],
    num_workers: int
) -> tuple[list[DetectionResult], float]:
    """
    Processa imagens em paralelo com N workers.

    Usa imap_unordered: os workers processam imagens
    simultaneamente e retornam resultados conforme terminam.

    Parâmetros
    ----------
    image_paths : lista de caminhos das imagens
    num_workers : número de processos paralelos

    Retorno
    -------
    (resultados, tempo_em_segundos)
    """
    results = []
    start = time.perf_counter()

    with Pool(processes=num_workers) as pool:
        for result in pool.imap_unordered(_worker, image_paths):
            results.append(result)

    elapsed = time.perf_counter() - start
    return results, elapsed


# ─────────────────────────────────────────────────────
# Benchmark completo: serial + 2, 4, 8, 12 workers
# ─────────────────────────────────────────────────────

def run_benchmark(
    image_paths: list[str],
    tempo_serial: float,
    workers_list: list[int] = [2, 4, 8, 12]
) -> list[dict]:
    """
    Executa o processamento paralelo para cada configuração
    de workers e calcula métricas em relação ao tempo serial.

    Parâmetros
    ----------
    image_paths  : lista de caminhos das imagens
    tempo_serial : tempo da execução serial em segundos
    workers_list : lista de configurações de workers a testar

    Retorno
    -------
    Lista de dicionários com métricas por configuração
    """
    resultados = []

    print(f"\n{'='*58}")
    print(f"  BENCHMARK PARALELO — {len(image_paths)} imagens")
    print(f"  Tempo serial de referência: {tempo_serial:.3f}s")
    print(f"{'='*58}")

    for workers in workers_list:
        print(f"\n  Testando {workers} workers...", end=" ", flush=True)

        results, elapsed = process_parallel(image_paths, workers)

        speedup    = tempo_serial / elapsed
        eficiencia = speedup / workers

        print(f"concluído em {elapsed:.3f}s")
        print(f"    Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.1%}")

        resultados.append({
            "workers":    workers,
            "tempo":      elapsed,
            "speedup":    speedup,
            "eficiencia": eficiencia,
            "resultados": results,
        })

    print(f"\n{'='*58}\n")
    return resultados
