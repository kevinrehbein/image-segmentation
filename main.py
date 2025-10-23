import argparse
import cv2
import numpy as np
import os

def setup():
    parser = argparse.ArgumentParser(description='CLI para segmentação de imagem.')
    
    parser.add_argument('--input', type=str, required=True, help='Caminho para a imagem de entrada.')
    parser.add_argument('--method', type=str, required=True, choices=['hsv', 'threshold'], help='Método de segmentação a ser usado.')
    parser.add_argument('--target', type=str, choices=['green', 'blue'], default='green', help='(HSV) Cor alvo para segmentação.')

    parser.add_argument('--hmin', type=int, help='Valor minimo de Matiz (H).')
    parser.add_argument('--hmax', type=int, help='Valor maximo de Matiz (H).')
    parser.add_argument('--smin', type=int, help='Valor minimo de Saturação (S).')
    parser.add_argument('--smax', type=int, help='Valor maximo de Saturação (S).')
    parser.add_argument('--vmin', type=int, help='Valor minimo de Valor (V).')
    parser.add_argument('--vmax', type=int, help='Valor maximo de Valor (V).')
    
    parser.add_argument('--thresh-val', type=int, default=127, help='Valor de limiar (0-255).')
    parser.add_argument('--thresh-inv', action='store_true', help='Inverte o threshold (segmenta pixels < thresh-val).')
    
    return parser.parse_args()

def segment_by_hsv(image, args):

    default_ranges = {
        'green': {
            'lower': [20, 0, 0],    # H_min, S_min, V_min
            'upper': [60, 255, 255] # H_max, S_max, V_max
        },
        'blue': {
            'lower': [90, 0, 0],
            'upper': [130, 255, 255]
        }
    }
    
    target_color = args.target
    lower = np.array(default_ranges[target_color]['lower'])
    upper = np.array(default_ranges[target_color]['upper'])
    
    #Sobrescreve os limites se forem passados via CLI
    if args.hmin is not None: lower[0] = args.hmin
    if args.smin is not None: lower[1] = args.smin
    if args.vmin is not None: lower[2] = args.vmin
    if args.hmax is not None: upper[0] = args.hmax
    if args.smax is not None: upper[1] = args.smax
    if args.vmax is not None: upper[2] = args.vmax
        
    print(f"Segmentando HSV para '{target_color}' com limites:")
    print(f"  Lower: {lower}")
    print(f"  Upper: {upper}")

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  #Converte a imagem de BGR para HSV

    return cv2.inRange(hsv_image, lower, upper) #Cria e retorna a máscara

def segment_by_threshold(image, args):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    #Converte para escala de cinza
    
    if args.thresh_inv:
        thresh_type = cv2.THRESH_BINARY_INV
    else: thresh_type = cv2.THRESH_BINARY

    thresh_value = args.thresh_val
    
    ret, mask = cv2.threshold(
        gray_image,    # Imagem de entrada 
        thresh_value,  # Valor do limiar
        255,           # Valor maximo
        thresh_type    # Tipo de threshold
    )

    return mask

def save_results(original_image, mask, input_path):

    overlay = cv2.bitwise_and(original_image, original_image, mask=mask)
    
    base_name = os.path.splitext(input_path)[0] 
    mask_path = f"{base_name}_mask.png" 
    overlay_path = f"{base_name}_overlay.jpg"
    
    try:
        cv2.imwrite(mask_path, mask)
        cv2.imwrite(overlay_path, overlay)
        print(f"Resultados salvos com sucesso:")
        print(f"  Máscara: {mask_path}")
        print(f"  Overlay: {overlay_path}")
    except Exception as e:
        print(f"Erro ao salvar os arquivos: {e}")

def main():
    args = setup()
    
    image = cv2.imread(args.input)
    if image is None:
        print(f"Erro: Não foi possível carregar a imagem de {args.input}")
        return

    mask = None
    if args.method == 'hsv':
        mask = segment_by_hsv(image, args)
    elif args.method == 'threshold':
        mask = segment_by_threshold(image, args)
        
    if mask is None:
        print("Nenhum método de segmentação foi executado com sucesso.")
        return
    else:
        save_results(image, mask, args.input)

if __name__ == "__main__":
    main()