# 🍎 Contagem de Maçãs — Processamento Serial com OpenCV

Projeto universitário de **Programação Paralela** em Python.
Detecta e conta maçãs em imagens usando **OpenCV** com segmentação de cor no espaço HSV e processamento **serial** (uma imagem por vez).

---

## 📁 Estrutura do Projeto

```
apple_serial/
├── main.py           # Ponto de entrada (CLI)
├── detector.py       # Algoritmo de detecção com OpenCV
├── processor.py      # Processamento serial
├── utils.py          # Carregamento de dataset, CSV e gráficos
├── requirements.txt  # Dependências Python
├── data/
│   └── apples/       # Imagens do dataset MinneApple
└── output/
    ├── results.csv   # Contagem por imagem
    └── summary.png   # Gráfico de distribuição
```

---

## 🍎 Dataset: MinneApple

| Propriedade       | Valor                              |
|-------------------|------------------------------------|
| Fonte             | Universidade de Minnesota (UMN)    |
| Tamanho           | 2,68 GB                            |
| Total de imagens  | 1.001                              |
| Anotações         | 41.000+ instâncias de maçãs        |
| Maçãs por imagem  | 1 a 120                            |
| Licença           | CC BY (uso livre)                  |
| Tipo              | Fotos reais de pomares             |

🔗 Download: https://datasetninja.com/minne-apple

---

## ⚙️ Instalação

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 2. Instalar dependências
pip install -r requirements.txt
```

### Dependências

| Biblioteca       | Versão mínima | Uso                          |
|------------------|---------------|------------------------------|
| opencv-python    | 4.8.0         | Processamento de imagem      |
| numpy            | 1.24.0        | Operações matriciais         |
| matplotlib       | 3.7.0         | Geração de gráficos          |

---

## 🚀 Como Executar

```bash
# Processamento completo
python main.py --dataset data/apples

# Testar com poucas imagens
python main.py --dataset data/apples --limit 10

# Salvar imagens anotadas
python main.py --dataset data/apples --save-images
```

---

## 📊 Resultados

### Execução com 41 imagens (amostra)

| Métrica               | Valor      |
|-----------------------|------------|
| Imagens processadas   | 41         |
| Total de maçãs        | 51         |
| Média por imagem      | 1.2        |
| Tempo total           | 1.947s     |
| Velocidade            | 21.1 imgs/s|
| Erros                 | 1          |
| Taxa de sucesso       | 97.6%      |

### Distribuição de maçãs por imagem

| Maçãs por imagem | Qtd. de imagens | % do total |
|------------------|-----------------|------------|
| 0 maçãs          | 7               | 17.1%      |
| 1 maçã           | 21              | 51.2%      |
| 2 maçãs          | 8               | 19.5%      |
| 3 maçãs          | 9.8%            | 9.8%       |
| 4+ maçãs         | 1               | 2.4%       |

> ⚠️ **1 erro:** arquivo PNG corrompido (`libpng error: Read Error`). Os demais 40 arquivos foram processados normalmente.

---

## 🔬 Como Funciona o Algoritmo

```
Imagem → GaussianBlur → BGR para HSV → Máscara de cor → Morfologia → Contornos → Filtro → Contagem
```

| Etapa              | Função OpenCV         | Objetivo                                      |
|--------------------|-----------------------|-----------------------------------------------|
| Suavização         | GaussianBlur (7×7)    | Reduz ruído de textura                        |
| Conversão de cor   | cvtColor BGR→HSV      | Separa matiz (cor) de brilho                  |
| Segmentação        | inRange               | Isola pixels vermelhos e verdes (maçãs)       |
| Limpeza            | morphologyEx OPEN     | Remove ruídos pequenos                        |
| Preenchimento      | morphologyEx CLOSE    | Preenche buracos internos                     |
| Detecção           | findContours          | Encontra bordas dos objetos                   |
| Filtragem          | contourArea + cálculo | Filtra por área (1.500–200.000 px²) e forma   |
| Anotação           | circle + putText      | Desenha círculos verdes e numera as maçãs     |

---

## 📖 Referência do Dataset

> Häni, N., Roy, P., & Isler, V. (2020). **MinneApple: A Benchmark Dataset for Apple Detection and Segmentation**.
> *IEEE Robotics and Automation Letters*, 5(2), 852–858.
> https://doi.org/10.1109/LRA.2020.2965061

│── README.md
│── requirements.txt
