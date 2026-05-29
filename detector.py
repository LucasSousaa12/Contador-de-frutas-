"""
detector.py
-----------
Detecção de maçãs usando visão computacional clássica (OpenCV).

Pipeline:
  1. Carregar imagem
  2. Suavização com Filtro Gaussiano
  3. Conversão para HSV
  4. Segmentação por cor (maçãs vermelhas e verdes)
  5. Morfologia para limpar ruídos
  6. Detecção de contornos externos
  7. Filtro por área e circularidade
  8. Retorna contagem + imagem anotada
"""

import cv2
import numpy as np
from dataclasses import dataclass


# ──────────────────────────────────────────────────────
# Estrutura de resultado
# ──────────────────────────────────────────────────────

@dataclass
class DetectionResult:
    image_path: str       # caminho original da imagem
    apple_count: int      # número de maçãs detectadas
    annotated_image: np.ndarray  # imagem com círculos verdes
    error: str | None = None     # mensagem de erro (se houver)


# ──────────────────────────────────────────────────────
# Parâmetros de detecção
# (ajuste estes valores se necessário para seu dataset)
# ──────────────────────────────────────────────────────

# Maçãs VERMELHAS: no espaço HSV o vermelho cruza o 0°/360°,
# então precisamos de dois intervalos
RED_LOWER_1  = np.array([0,   80,  50])
RED_UPPER_1  = np.array([10, 255, 255])
RED_LOWER_2  = np.array([160, 80,  50])
RED_UPPER_2  = np.array([180, 255, 255])

# Maçãs VERDES
GREEN_LOWER  = np.array([35,  50,  50])
GREEN_UPPER  = np.array([85, 255, 255])

# Filtros de contorno
MIN_AREA        = 1_500    # px² mínima para ser uma maçã (elimina ruídos)
MAX_AREA        = 200_000  # px² máxima (elimina fundo inteiro colorido)
MIN_CIRCULARITY = 0.55     # 1.0 = círculo perfeito; maçãs ficam entre 0.60-0.85


# ──────────────────────────────────────────────────────
# Funções auxiliares (privadas)
# ──────────────────────────────────────────────────────

def _build_color_mask(hsv: np.ndarray) -> np.ndarray:
    """Cria máscara binária unindo pixels vermelhos e verdes."""
    mask_r1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask_r2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    mask_g  = cv2.inRange(hsv, GREEN_LOWER,  GREEN_UPPER)
    return cv2.bitwise_or(cv2.bitwise_or(mask_r1, mask_r2), mask_g)


def _clean_mask(mask: np.ndarray) -> np.ndarray:
    """
    Aplica operações morfológicas para limpar a máscara:
    - OPEN  (erosão + dilatação): remove ruídos pequenos
    - CLOSE (dilatação + erosão): preenche buracos dentro das maçãs
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    return mask


def _circularity(contour) -> float:
    """
    Mede o quão circular é um contorno.
    Fórmula: 4π·área / perímetro²
    Resultado: 1.0 = círculo perfeito, <1.0 = menos circular
    """
    area = cv2.contourArea(contour)
    peri = cv2.arcLength(contour, True)
    if peri == 0:
        return 0.0
    return (4 * np.pi * area) / (peri ** 2)


# ──────────────────────────────────────────────────────
# Função principal de detecção
# ──────────────────────────────────────────────────────

def detect_apples(image_path: str) -> DetectionResult:
    """
    Detecta e conta maçãs em uma única imagem.

    Parâmetros
    ----------
    image_path : str
        Caminho completo para o arquivo de imagem.

    Retorno
    -------
    DetectionResult
        Contém: caminho, contagem, imagem anotada e possível erro.
    """
    # ── Passo 1: Carregar imagem ──────────────────────
    img = cv2.imread(image_path)
    if img is None:
        blank = np.zeros((100, 100, 3), dtype=np.uint8)
        return DetectionResult(
            image_path=image_path,
            apple_count=0,
            annotated_image=blank,
            error=f"Não foi possível carregar: {image_path}"
        )

    # ── Passo 2: Suavização (reduz ruído de textura) ──
    blurred = cv2.GaussianBlur(img, (7, 7), 0)

    # ── Passo 3: Converter BGR → HSV ──────────────────
    # HSV separa matiz (cor) de brilho, tornando a segmentação
    # de cor mais robusta a variações de iluminação
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # ── Passo 4: Segmentação por cor + limpeza ────────
    mask = _build_color_mask(hsv)
    mask = _clean_mask(mask)

    # ── Passo 5: Encontrar contornos externos ─────────
    # RETR_EXTERNAL: apenas contornos mais externos (evita duplicatas)
    # CHAIN_APPROX_SIMPLE: comprime segmentos retos (economiza memória)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # ── Passo 6: Filtrar contornos ────────────────────
    apple_contours = [
        cnt for cnt in contours
        if MIN_AREA <= cv2.contourArea(cnt) <= MAX_AREA
        and _circularity(cnt) >= MIN_CIRCULARITY
    ]

    # ── Passo 7: Anotar imagem ────────────────────────
    annotated = img.copy()
    for i, cnt in enumerate(apple_contours):
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        center = (int(cx), int(cy))
        # Círculo verde ao redor da maçã
        cv2.circle(annotated, center, int(radius), (0, 255, 0), 2)
        # Número da maçã no centro
        cv2.putText(
            annotated, str(i + 1),
            (center[0] - 8, center[1] + 6),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

    # Contador total no canto superior esquerdo
    cv2.rectangle(annotated, (0, 0), (190, 42), (0, 0, 0), -1)
    cv2.putText(
        annotated, f"Macas: {len(apple_contours)}",
        (8, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2
    )

    return DetectionResult(
        image_path=image_path,
        apple_count=len(apple_contours),
        annotated_image=annotated
    )
