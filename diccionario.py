import os
import time

# Ruta del directorio
directorio_principal = "/DATA_RM/DATA/HYO@2025-01-27T16-14-33/position"

# Obtener la lista de directorios dentro del directorio principal
directorios = [d for d in os.listdir(directorio_principal) if os.path.isdir(os.path.join(directorio_principal, d))]

# Ordenar los directorios por fecha de creación (el más reciente primero)
directorios.sort(key=lambda x: os.path.getctime(os.path.join(directorio_principal, x)), reverse=True)


# Seleccionar el último directorio creado
if directorios:
    ultimo_directorio = directorios[0]
    ruta_ultimo_directorio = os.path.join(directorio_principal, ultimo_directorio)

    # Obtener la lista de archivos en el último directorio
    archivos = [archivo for archivo in os.listdir(ruta_ultimo_directorio) if os.path.isfile(os.path.join(ruta_ultimo_directorio, archivo))]    


    # Ordenar los archivos por fecha de modificación (los últimos modificados primero)
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(ruta_ultimo_directorio, x)), reverse=True)
    print(archivos)
    # Listar los últimos 3 archivos
    ultimos_3_archivos = archivos[:3]

    # Obtener la fecha de creación del directorio
    fecha_creacion_directorio = os.path.getctime(ruta_ultimo_directorio)
    fecha_creacion_directorio = time.ctime(fecha_creacion_directorio)

    # Mostrar los resultados
    print("Últimos 3 archivos:")
    for archivo in ultimos_3_archivos:
        print(archivo)

print("\nFecha de creación del directorio:")
print(fecha_creacion_directorio)