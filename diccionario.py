import os
import time

# Ruta del directorio
directorio = "/DATA_RM/DATA/HYO@2025-01-27T16-14-33/position"

# Obtener la lista de archivos en el directorio
archivos = os.listdir(directorio)

# Filtrar solo archivos (excluyendo directorios)
archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(directorio, archivo))]

# Ordenar los archivos por fecha de modificación (los últimos modificados primero)
archivos.sort(key=lambda x: os.path.getmtime(os.path.join(directorio, x)), reverse=True)

# Listar los últimos 3 archivos
ultimos_3_archivos = archivos[:3]

# Obtener la fecha de creación del directorio
fecha_creacion_directorio = os.path.getctime(directorio)
fecha_creacion_directorio = time.ctime(fecha_creacion_directorio)

# Mostrar los resultados
print("Últimos 3 archivos:")
for archivo in ultimos_3_archivos:
    print(archivo)

print("\nFecha de creación del directorio:")
print(fecha_creacion_directorio)