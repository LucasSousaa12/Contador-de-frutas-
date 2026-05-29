"""
processor.py
------------
Processamento SERIAL das imagens — processa uma por vez.

Exporta apenas a função process_serial(), que:
  - Percorre a lista de caminhos de imagens em ordem
  - Chama detect_apples() para cada uma
  - Registra o tempo total de execução
  - Retorna os resultados e métricas de desempenho
"""

import time
from typing import Callable

from detector import DetectionResult, detect_apples


def process_serial(
    image_paths: list[str],
    progress_callback: Callable[[int, int, DetectionResult], None] | None = None
) -> tuple[list[DetectionResult], float]:
    """
    Processa todas as imagens de forma serial (sequencial).

    Parâmetros
    ----------
    image_paths : list[str]
        Lista com os caminhos das imagens a processar.

    progress_callback : callable, opcional
        Função chamada após cada imagem processada.
        Recebe: (imagens_concluídas, total, resultado_atual)
        Útil para exibir progresso no terminal.

    Retorno
    -------
    tuple[list[DetectionResult], float]
        - Lista com os resultados de cada imagem
        - Tempo total de execução em segundos
    """
    results: list[DetectionResult] = []
    total = len(image_paths)

    start_time = time.perf_counter()

    for i, path in enumerate(image_paths):
        result = detect_apples(path)
        results.append(result)

        if progress_callback:
            progress_callback(i + 1, total, result)

    elapsed = time.perf_counter() - start_time
    return results, elapsed
