import os
import requests
from bs4 import BeautifulSoup
import base64
import html5lib


# ruta: C:\Users\soporte\Documents\OCR_TEST
# URL de la página web
url = "https://www.igp.gob.pe/observatorios/radio-observatorio-jicamarca/realtime/plot/400/reflectivity/"

# Carpeta donde se guardará la imagen
output_folder = "imagenes_descargadas"
os.makedirs(output_folder, exist_ok=True)

# Hacer una solicitud GET a la página
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    print("----------------------")
    # Buscar la etiqueta con id="image"
    img_tags = soup.find("img")
    print("img_tag",img_tags)
    for img_tag in img_tags:
        if img_tag.get("id")== "image":
            img_src = img_tag.get("src")
            print("img_src",img_src)

    
    if img_tag:
        # Obtener la URL de la imagen
        src = img_tag.get("src")

        print("SRC",src)
        
        if src.startswith("data:image/png;base64,"):
            # Extraer la parte codificada en Base64 (sin el prefijo)
            base64_string = src.split(",")[1]
            
            # Decodificar y guardar la imagen
            image_data = base64.b64decode(base64_string)
            with open("imagen_extraida.png", "wb") as f:
                f.write(image_data)
            
            print("Imagen extraída y guardada como 'imagen_extraida.png'")
        else:
            print("El atributo 'src' no contiene una imagen Base64.")
    else:
        print('No se encontró ninguna etiqueta con id="image".')
else:
    print(f"No se pudo acceder a la página: {url}, {response}")


