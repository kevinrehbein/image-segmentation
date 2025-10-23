# Image Segmentation CLI

Uma ferramenta de linha de comando (Python/OpenCV) que segmenta imagens usando dois métodos principais: filtragem de cor no espaço HSV ou thresholding (limiarização) baseado em uma escala de cinza.

Este script permite isolar partes de uma imagem com base em suas características de cor (HSV) ou brilho (Threshold), gerando uma máscara em preto e branco e uma imagem de "overlay" com o fundo removido.

## Requisitos

Para rodar este script, você precisará das seguintes bibliotecas Python:

- opencv-python
- numpy

Você pode instalá-las usando o pip:

```bash
pip install opencv-python numpy
```

## Como Rodar

O script é executado através da linha de comando. Os dois argumentos principais e obrigatórios são --input (a imagem de origem) e --method (o método de segmentação).

### Sintaxe Básica

```bash
python3 main.py --input <caminho_para_imagem> --method <hsv | threshold> [opções...]
```

### Argumentos da Linha de Comando

| Argumento              | Obrigatório | Descrição                                                            |
| :--------------------- | :---------- | :------------------------------------------------------------------- |
| --input                | Sim         | O caminho para a imagem de entrada (ex: example.jpg).                |
| --method               | Sim         | O método de segmentação: hsv ou threshold.                           |
|                        |             |                                                                      |
| **Opções (HSV)**       |             |                                                                      |
| --target               | Não         | Cor alvo predefinida. Padrão: green. Opções: green, blue.            |
| --hmin, --hmax         | Não         | Sobrescreve os valores mínimos/máximos de Matiz (Hue).               |
| --smin, --smax         | Não         | Sobrescreve os valores mínimos/máximos de Saturação (Saturation).    |
| --vmin, --vmax         | Não         | Sobrescreve os valores mínimos/máximos de Valor (Value/Brightness).  |
|                        |             |                                                                      |
| **Opções (Threshold)** |             |                                                                      |
| --thresh-val           | Não         | O valor do limiar (0-255). Padrão: 127.                              |
| --thresh-inv           | Não         | Inverte o threshold. Se usado, segmenta pixels abaixo do thresh-val. |

---

## O Raciocínio por Trás (Metodologia)

Este script implementa duas abordagens clássicas de segmentação de imagem.

### 1\. Método hsv

**Raciocínio:**

1.  A imagem de entrada (BGR) é convertida para o espaço de cor HSV (cv2.cvtColor(image, cv2.COLOR_BGR2HSV)).
2.  O script define um intervalo (limite inferior e superior) para os valores de H, S e V. Existem padrões para 'green' e 'blue', mas eles podem ser totalmente personalizados via argumentos (--hmin, --smin, etc.).
3.  A função cv2.inRange é usada para criar uma máscara. Qualquer pixel da imagem HSV que se enquadre dentro do intervalo especificado se torna branco (255) na máscara, e qualquer pixel fora do intervalo se torna preto (0).

### 2\. Método threshold

**Raciocínio:**
Esta é a forma mais simples de segmentação. Ela não se importa com a cor, apenas com o brilho. É útil para separar objetos claros de fundos escuros, ou vice-versa.

1.  A imagem de entrada é primeiro convertida para escala de cinza (cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)).
2.  A função cv2.threshold é aplicada. Ela compara cada pixel da imagem em escala de cinza com um valor de limiar (--thresh-val). O valor padrão para é 127.
3.  Por padrão (cv2.THRESH_BINARY), qualquer pixel acima do limiar se torna branco (255) e o restante se torna preto (0).
4.  Se a flag --thresh-inv for usada, o comportamento é invertido (cv2.THRESH_BINARY_INV): pixels abaixo do limiar se tornam brancos, e o restante, preto.

---

## Exemplos de Uso

**Exemplo 1: Segmentar o verde (folhagem) usando HSV**

```bash
python3 main.py --input ./example.jpg --method hsv --target green
```

- O script usará os limites padrão para 'green' (H: 20-60, S: 0-255, V: 0-255).

**Exemplo 2: Segmentar o céu (azul) usando HSV**

```bash
python3 main.py --input example.jpg --method hsv --target blue
```

- O script usará os limites padrão para 'blue' (H: 90-130, S: 0-255, V: 0-255).

**Exemplo 3: Segmentar áreas escuras usando Threshold (Invertido)**

```bash
python3 main.py --input example.jpg --method threshold --thresh-val 127 --thresh-inv
```

- Isso converterá a imagem para escala de cinza e tornará brancos todos os pixels com valor de brilho inferior a 127.

**Exemplo 4: Segmentar usando HSV com valores personalizados**
(Para um verde mais específico, talvez mais escuro e mais saturado)

```bash
python3 main.py --input example.jpg --method hsv --hmin 30 --hmax 70 --smin 50 --vmin 50
```
