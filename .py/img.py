from PIL import Image

def make_white_pixels_transparent(input_image_path, output_image_path):
    # Abre a imagem
    img = Image.open(input_image_path).convert("RGBA")
    
    # Pega os dados da imagem
    data = img.getdata()
    
    # Cria uma nova lista de dados para a imagem
    new_data = []
    
    # Processa cada pixel na imagem
    for item in data:
        # Muda todos os pixels brancos (255, 255, 255) para transparentes (255, 255, 255, 0)
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    # Atualiza a imagem com os novos dados
    img.putdata(new_data)
    
    # Salva a nova imagem
    img.save(output_image_path, "PNG")

# Exemplo de uso
input_image_path = 'map.png'
output_image_path = 'newmap.png'
make_white_pixels_transparent(input_image_path, output_image_path)
