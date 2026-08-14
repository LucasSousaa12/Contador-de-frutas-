# 🍎 contagem-macas-opencv

Análise serial e paralela da contagem de maçãs em imagens de pomares usando visão computacional clássica com OpenCV e Python, com medição de speedup e eficiência usando multiprocessamento.

---

## 📌 Descrição do Projeto

Este projeto tem como objetivo processar um dataset de imagens reais de pomares e **contar automaticamente quantas maçãs aparecem em cada foto**, utilizando técnicas de visão computacional clássica com OpenCV.

O problema consiste em identificar e contar maçãs em 15.388 imagens do dataset **MinneApple**, comparando o desempenho de uma solução **serial** e uma solução **paralela** com diferentes configurações de workers.

O algoritmo segue o pipeline:

```
Imagem → Suavização → Conversão HSV → Segmentação por cor → Morfologia → Contornos → Filtro → Contagem
```

Este trabalho foi desenvolvido como projeto prático da disciplina de **Programação Paralela**.

---

## 🗃️ Base de Dados

| Atributo              | Valor                                     |
|-----------------------|-------------------------------------------|
| Nome                  | MinneApple                                |
| Fonte                 | Universidade de Minnesota (UMN DRUM)      |
| Total de imagens      | 15.388                                    |
| Total de anotações    | 41.000+ instâncias de maçãs               |
| Maçãs por imagem      | 1 a 120                                   |
| Tamanho               | 2,68 GB                                   |
| Licença               | CC BY (uso livre)                         |
| Origem                | Häni, Roy & Isler — IEEE RA-L, 2020       |

🔗 Download: https://datasetninja.com/minne-apple  
🔗 Repositório oficial: https://github.com/nicolaihaeni/MinneApple

### Pastas utilizadas

| Pasta                       | Imagens    | Descrição                      |
|-----------------------------|------------|--------------------------------|
| `detection/train/images/`   | 670        | Fotos completas de pomar       |
| `detection/test/images/`    | 331        | Fotos completas de pomar       |
| `counting/test/images/`     | 991        | Recortes de partes das árvores |
| `counting/val/images/`      | 3.395      | Recortes de partes das árvores |
| `counting/train/images/`    | 7.000      | Recortes de partes das árvores |
| **Total**                   | **15.388** | —                              |

---

## ⚙️ O que o programa faz

O processamento segue os seguintes passos:

1. Carregar os caminhos de todas as imagens do dataset
2. Aplicar suavização com filtro Gaussiano (reduz ruído de textura)
3. Converter o espaço de cor de BGR para HSV
4. Criar máscaras de cor para maçãs vermelhas e verdes
5. Aplicar operações morfológicas para limpar ruídos
6. Detectar contornos externos dos objetos
7. Filtrar contornos por área e circularidade
8. Contar e anotar as maçãs detectadas em cada imagem
9. Gerar relatório CSV e gráficos de desempenho

### Serial

As 15.388 imagens são processadas **uma de cada vez**, de forma sequencial.

```
Imagem 1     → pipeline → resultado 1
Imagem 2     → pipeline → resultado 2
Imagem 3     → pipeline → resultado 3
...
Imagem 15388 → pipeline → resultado 15388
```

### Paralela

A solução paralela usa `multiprocessing.Pool` com `imap_unordered`:

```
                   ┌─── Worker 1  → detect(img_1, img_5, ...)
Pool.imap_unordered┼─── Worker 2  → detect(img_2, img_6, ...)  → resultados
                   ├─── Worker N  → detect(img_3, img_7, ...)
                   └─── Worker N  → detect(img_4, img_8, ...)
```

---

## 🔬 Como Funciona o Algoritmo

| Etapa            | Função OpenCV           | Objetivo                                    |
|------------------|-------------------------|---------------------------------------------|
| Suavização       | `GaussianBlur (7×7)`    | Reduz ruído de textura                      |
| Conversão de cor | `cvtColor BGR→HSV`      | Separa matiz (cor) de brilho                |
| Segmentação      | `inRange`               | Isola pixels vermelhos e verdes (maçãs)     |
| Limpeza          | `morphologyEx OPEN`     | Remove ruídos pequenos                      |
| Preenchimento    | `morphologyEx CLOSE`    | Preenche buracos internos das maçãs         |
| Detecção         | `findContours`          | Encontra bordas dos objetos segmentados     |
| Filtragem        | `contourArea` + fórmula | Filtra por área (1.500–200.000 px²) e forma |
| Anotação         | `circle` + `putText`    | Desenha círculos verdes e numera as maçãs   |

> **Por que HSV em vez de RGB?**  
> No espaço RGB, a mesma cor pode ter valores bem diferentes dependendo da iluminação. No HSV, o canal **Hue** (matiz) representa a cor de forma independente do brilho, tornando a segmentação muito mais estável em fotos de pomar com variações de luz.

---

## 📊 Resultados

### Execução Serial — 15.388 imagens

| Métrica             | Valor        |
|---------------------|--------------|
| Imagens processadas | 15.388       |
| Total de maçãs      | 2.928        |
| Média por imagem    | 0.2          |
| Tempo total         | 150.823s     |
| Velocidade          | 102.0 imgs/s |
| Taxa de sucesso     | 100%         |

---

### Benchmark Paralelo — Serial vs 2, 4, 6, 8 e 12 Workers

Os valores abaixo correspondem ao registro armazenado em `output/benchmark.csv`.

Fórmulas utilizadas:

| Métrica          | Fórmula                               |
| ---------------- | ------------------------------------- |
| Speedup          | S = T_serial / T_paralelo             |
| Eficiência       | E = S / N_workers                     |
| Redução de tempo | R = (1 - T_paralelo / T_serial) × 100 |

| Modo     | Workers | Tempo (s) |   Speedup | Eficiência | Redução de tempo |
| -------- | ------: | --------: | --------: | ---------: | ---------------: |
| Serial   |       1 |  150.823s |     1.00x |     100.0% |                — |
| Paralelo |       2 |   34.921s |     4.32x |     216.0% |            76.8% |
| Paralelo |       4 |   21.727s |     6.94x |     173.5% |            85.6% |
| Paralelo |       6 |   18.547s |     8.13x |     135.5% |            87.7% |
| Paralelo |       8 |   17.238s | **8.75x** |     109.4% |        **88.6%** |
| Paralelo |      12 |   17.577s |     8.58x |      71.5% |            88.3% |

> 🏆 **Melhor tempo registrado:** 8 workers, com 17.238s, speedup aparente de 8.75x e redução de 88.6% em relação ao tempo serial de referência.

### Interpretação e limitações do benchmark

* O tempo diminuiu até 8 workers; com 12 workers houve uma pequena regressão, compatível com o overhead de criação, comunicação e gerenciamento de processos.
* Cada imagem é processada independentemente, tornando o problema naturalmente adequado ao paralelismo.
* Os valores registram uma execução real, mas o tempo serial de 150.823s foi medido separadamente e inserido como constante no script de benchmark.
* A execução serial original exibia o progresso de cada imagem no terminal, enquanto as execuções paralelas foram medidas sem esse callback. Essa diferença pode influenciar a comparação.
* Por isso, eficiências acima de 100% devem ser tratadas como **speedup aparente**, e não como comprovação isolada de ganhos de cache ou speedup superlinear.
* Para um benchmark mais rigoroso, recomenda-se medir serial e paralelo na mesma execução, sem saída de progresso, repetir cada configuração e apresentar média e desvio padrão.

<img width="2084" height="1475" alt="Gráfico do benchmark serial e paralelo" src="https://github.com/user-attachments/assets/8d3c59ba-bbb8-44d0-b13b-6833c33c0dad" />


### Arquivos gerados

| Arquivo                     | Conteúdo                                       |
|-----------------------------|------------------------------------------------|
| `output/results.csv`        | Contagem de maçãs por imagem                   |
| `output/summary.png`        | Histograma de distribuição + estatísticas      |
| `output/grafico_serial.png` | Evolução da detecção por imagem                |
| `output/benchmark.png`      | Gráfico de speedup, eficiência e Lei de Amdahl |
| `output/benchmark.csv`      | Métricas numéricas do benchmark                |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia       | Versão mínima | Uso                               |
|------------------|---------------|-----------------------------------|
| Python           | 3.10          | Linguagem principal               |
| opencv-python    | 4.8.0         | Processamento de imagem           |
| numpy            | 1.24.0        | Operações matriciais              |
| matplotlib       | 3.7.0         | Geração de gráficos               |
| multiprocessing  | stdlib        | Paralelismo com Pool de processos |

---

## 📁 Estrutura do Repositório

```
contagem-macas-opencv/
│
├── data/
│   └── apples/                      # Imagens do MinneApple (baixar separadamente)
│
├── output/
│   ├── results.csv                  # Contagem por imagem
│   ├── summary.png                  # Gráfico de distribuição
│   ├── grafico_serial.png           # Evolução serial por imagem
│   ├── benchmark.png                # Gráfico de benchmark
│   └── benchmark.csv                # Métricas do benchmark
│
├── detector.py                      # Algoritmo de detecção com OpenCV
├── processor.py                     # Processamento serial
├── paralelo.py                      # Processamento paralelo com multiprocessing
├── gerar_grafico_benchmark.py       # Benchmark serial vs paralelo
├── grafico_serial.py                # Gráfico da execução serial
├── utils.py                         # Dataset, relatórios e gráficos
├── main.py                          # Ponto de entrada (CLI)
├── requirements.txt                 # Dependências Python
└── README.md
```
---

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/LucasSousaa12/Contador-de-frutas-.git
cd Contador-de-frutas-
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Baixar o dataset

Acesse https://datasetninja.com/minne-apple, baixe e extraia.  
Copie as imagens das pastas abaixo para `data/apples/`:
- `detection/train/images/`
- `detection/test/images/`
- `counting/test/images/`
- `counting/val/images/`
- `counting/train/images/` (7.000 imagens)

### 4. Executar

```bash
# Processamento serial completo
python main.py --dataset data/apples

# Benchmark serial vs paralelo (2, 4, 6, 8 e 12 workers)
python gerar_grafico_benchmark.py --dataset data/apples

# Gráfico da execução serial
python grafico_serial.py

# Testar com poucas imagens
python main.py --dataset data/apples --limit 10
```

---

## 📖 Referência do Dataset

> Häni, N., Roy, P., & Isler, V. (2020). **MinneApple: A Benchmark Dataset for Apple Detection and Segmentation**.  
> *IEEE Robotics and Automation Letters*, 5(2), 852–858.  
> https://doi.org/10.1109/LRA.2020.2965061
