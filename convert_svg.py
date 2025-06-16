from PIL import Image
from io import BytesIO
import cairosvg
import os

# Caminho para o diretório de imagens
img_dir = os.path.join('static', 'img')

# Converter SVG para PNG
svg_path = os.path.join(img_dir, 'whatsapp.svg')
png_path = os.path.join(img_dir, 'whatsapp.png')

# Verificar se o arquivo SVG existe
if os.path.exists(svg_path):
    # Converter SVG para PNG
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=64, output_height=64)
    print(f"Arquivo convertido e salvo em {png_path}")
else:
    print(f"Arquivo SVG não encontrado: {svg_path}")
