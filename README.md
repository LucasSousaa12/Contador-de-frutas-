# Contador-de-frutas-

# 🍎 Sistema Paralelo para Detecção e Contagem de Maçãs em Imagens

## 📌 Descrição do Projeto
Este projeto tem como objetivo desenvolver um sistema capaz de identificar e contar automaticamente maçãs em imagens digitais utilizando técnicas de processamento de imagens e programação paralela.

A aplicação divide a imagem em regiões e distribui o processamento entre múltiplos processos, permitindo uma execução mais rápida e eficiente em comparação com a abordagem sequencial.

O sistema utiliza imagens reais obtidas de datasets públicos do Kaggle e foi desenvolvido como projeto acadêmico da disciplina de Programação Paralela.

---

## 🎯 Objetivo Geral
Desenvolver uma aplicação que realize a detecção e a contagem automática de maçãs em imagens, aplicando programação paralela para reduzir o tempo de processamento.

---

## 🎯 Objetivos Específicos
- Carregar imagens contendo maçãs.
- Aplicar técnicas de pré-processamento e segmentação.
- Detectar e contar as maçãs presentes na imagem.
- Dividir a imagem em partes e processá-las em paralelo.
- Consolidar os resultados obtidos por cada processo.
- Comparar o desempenho entre execução sequencial e paralela.
- Calcular métricas de speedup e eficiência.

---

## 🛠️ Tecnologias Utilizadas
- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- Multiprocessing

---

## 📂 Dataset
As imagens utilizadas no projeto foram obtidas a partir de datasets públicos disponibilizados no Kaggle, contendo fotografias reais de maçãs.

---

## ⚙️ Funcionamento do Sistema
1. O usuário fornece uma imagem contendo maçãs.
2. A imagem é pré-processada para melhorar a detecção.
3. A imagem é dividida em regiões.
4. Cada região é processada por um processo independente.
5. O sistema identifica e contabiliza as maçãs detectadas.
6. Os resultados são consolidados.
7. É realizada a comparação entre execução sequencial e paralela.

---

## 📊 Métricas Avaliadas
- Tempo de execução sequencial:
 CONTAGEM DE MAÇÃS — Processamento Serial (OpenCV)
==========================================================
  Dataset  : data/apples
  Saída    : output
==========================================================

✔ Dataset carregado: 41 imagens em 'data/apples'

Processando 41 imagens...

  [█████░░░░░░░░░░░░░░░░░░░░░░░░░]  19.5%  dataset1_front_1351.png           2 maçãslibpng error: Read Error
  [██████████████████████████████] 100.0%  dataset4_front_900.png            3 maçãs

Gerando relatórios...
✔ Relatório CSV salvo em 'output/results.csv'
✔ Gráfico de resumo salvo em 'output/summary.png'

──────────────────────────────────────────────────────────
  Imagens processadas : 41
  
  Total de maçãs      : 51
  
  Média por imagem    : 1.2
  
  Tempo total         : 1.947s
  
  Velocidade          : 21.1 imgs/s
  
  Erros               : 1
  
- Tempo de execução paralelo
- Speedup
- Eficiência

---

## 📈 Fórmulas Utilizadas

Speedup:
S = T_serial / T_paralelo

Eficiência:
E = S / N

Onde:
- T_serial = tempo de execução sequencial
- T_paralelo = tempo de execução paralelo
- N = número de processos

---

## 📁 Estrutura do Projeto
```text
contador-macas/
│── dataset/
│── imagens/
│── src/
│   │── serial.py
│   │── paralelo.py
│   │── processamento.py
│── resultados/
│── README.md
│── requirements.txt
