# 🍎 contagem-macas-opencv

Análise serial da contagem de maçãs em imagens de pomares usando visão computacional clássica com OpenCV e Python.

---

## 📌 Descrição do Projeto

Este projeto tem como objetivo processar um dataset de imagens reais de pomares e **contar automaticamente quantas maçãs aparecem em cada foto**, utilizando técnicas de visão computacional clássica com OpenCV.

O problema consiste em identificar e contar maçãs em 1.001 imagens de alta resolução do dataset **MinneApple**, processando cada imagem de forma **serial** (uma por vez). O algoritmo segue o pipeline:

```
Imagem → Suavização → Conversão HSV → Segmentação por cor → Morfologia → Contornos → Filtro → Contagem
```

Este trabalho foi desenvolvido como projeto prático da disciplina de **Programação Paralela**.

---

## 🗃️ Base de Dados

| Atributo              | Valor                                        |
|-----------------------|----------------------------------------------|
| Nome                  | MinneApple                                   |
| Fonte                 | Universidade de Minnesota (UMN DRUM)         |
| Total de imagens      | 1.001                                        |
| Total de anotações    | 41.000+ instâncias de maçãs                  |
| Maçãs por imagem      | 1 a 120                                      |
| Tamanho               | 2,68 GB                                      |
| Período               | Imagens coletadas em pomares reais           |
| Licença               | CC BY (uso livre)                            |
| Origem                | Häni, Roy & Isler — IEEE RA-L, 2020          |

🔗 Download: https://datasetninja.com/minne-apple  
🔗 Repositório oficial: https://github.com/nicolaihaeni/MinneApple

### Pastas utilizadas

| Pasta                          | Imagens | Descrição                        |
|--------------------------------|---------|----------------------------------|
| `detection/train/images/`      | 670     | Fotos completas de pomar         |
| `detection/test/images/`       | 331     | Fotos completas de pomar         |
| **Total**                      | **1.001** | Imagens em alta resolução      |

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
9. Gerar relatório CSV e gráfico de distribuição

### Serial

As 1.001 imagens são processadas **uma de cada vez**, de forma sequencial. Cada imagem passa pelo pipeline completo antes de iniciar a próxima.

```
Imagem 1 → pipeline → resultado 1
Imagem 2 → pipeline → resultado 2
Imagem 3 → pipeline → resultado 3
...
Imagem 1001 → pipeline → resultado 1001
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

### Execução com 1.001 imagens (dataset completo)

| Métrica             | Valor       |
|---------------------|-------------|
| Imagens processadas | 1.001       |
| Total de maçãs      | 996         |
| Média por imagem    | 1.0         |
| Tempo total         | 44.097s     |
| Velocidade          | 22.7 imgs/s |
| Erros               | 0           |
| Taxa de sucesso     | 100%        |

### Distribuição de maçãs por imagem

| Maçãs por imagem | Qtd. de imagens | % do total |
|------------------|-----------------|------------|
| 0 maçãs          | ~5              | ~0.5%      |
| 1 maçã           | maioria         | ~70%       |
| 2 maçãs          | —               | ~20%       |
| 3+ maçãs         | —               | ~9.5%      |

### Arquivos gerados

| Arquivo             | Conteúdo                                   |
|---------------------|--------------------------------------------|
| `output/results.csv`  | Nome do arquivo e quantidade de maçãs detectadas por imagem |
| `output/summary.png`  | Histograma de distribuição + tabela de estatísticas |

---

## 📐 Próxima Etapa — Versão Paralela

A próxima etapa do projeto é implementar a versão **paralela** com `multiprocessing`, onde várias imagens são processadas simultaneamente para reduzir o tempo total.

| Métrica    | Descrição                                         |
|------------|---------------------------------------------------|
| Speedup    | Tempo serial ÷ Tempo paralelo                     |
| Eficiência | Speedup ÷ Número de workers                       |
| Lei de Amdahl | Limite teórico do ganho com base na fração paralelizável |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia       | Versão mínima | Uso                          |
|------------------|---------------|------------------------------|
| Python           | 3.10          | Linguagem principal          |
| opencv-python    | 4.8.0         | Processamento de imagem      |
| numpy            | 1.24.0        | Operações matriciais         |
| matplotlib       | 3.7.0         | Geração de gráficos          |
| multiprocessing  | stdlib        | Paralelismo (próxima etapa)  |

---

## 📁 Estrutura do Repositório

```
contagem-macas-opencv/
│
├── data/
│   └── apples/                   # Imagens do MinneApple (baixar separadamente)
│
├── output/
│   ├── results.csv               # Contagem por imagem
│   ├── summary.png               # Gráfico de distribuição
│   └── annotated/                # Imagens anotadas (--save-images)
│
├── detector.py                   # Algoritmo de detecção com OpenCV
├── processor.py                  # Processamento serial
├── utils.py                      # Dataset, relatórios e gráficos
├── main.py                       # Ponto de entrada (CLI)
├── requirements.txt              # Dependências Python
└── README.md
```

---

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/contagem-macas-opencv.git
cd contagem-macas-opencv
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Baixar o dataset

Acesse https://datasetninja.com/minne-apple, baixe e extraia.  
Copie as imagens das pastas `detection/train/images/` e `detection/test/images/` para `data/apples/`.

### 4. Executar

```bash
# Processamento completo
python main.py --dataset data/apples

# Testar com poucas imagens
python main.py --dataset data/apples --limit 10

# Salvar imagens anotadas
python main.py --dataset data/apples --save-images
```

---

## 📖 Referência do Dataset

> Häni, N., Roy, P., & Isler, V. (2020). **MinneApple: A Benchmark Dataset for Apple Detection and Segmentation**.  
> *IEEE Robotics and Automation Letters*, 5(2), 852–858.  
> https://doi.org/10.1109/LRA.2020.2965061


│── README.md
│── requirements.txt
