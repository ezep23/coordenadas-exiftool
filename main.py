import os
import subprocess

def buscar_archivo(nombre_archivo):
    # Buscar recursivamente el archivo en el sistema de archivos
    for root, _, files in os.walk(os.path.sep):
        if nombre_archivo in files:
            return os.path.join(root, nombre_archivo)
    return None

def obtener_coordenadas(ruta_absoluta_imagen):
    # Verificar si ExifTool está instalado y accesible
    try:
        subprocess.run(['exiftool', '-ver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("ExifTool no está instalado o no se puede acceder.")
        return None, None

    # Usar exiftool para obtener los metadatos de la imagen
    proceso = subprocess.Popen(['exiftool', '-n', '-GPSLatitude', '-GPSLongitude', ruta_absoluta_imagen], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    salida, _ = proceso.communicate()

    # Buscar las etiquetas de latitud y longitud en la salida
    latitud = None
    longitud = None
    for linea in salida.split('\n'):
        if 'GPSLatitude' in linea:
            latitud = linea.split(': ')[1]
        elif 'GPSLongitude' in linea:
            longitud = linea.split(': ')[1]

    return latitud, longitud

# Nombre de la imagen con su extensión
nombre_imagen = input("Ingrese el nombre de su archivo con su extensión: ").strip()

# Buscar el archivo en todo el sistema de archivos
ruta_absoluta_imagen = buscar_archivo(nombre_imagen)

# Verificar si se encontró el archivo
if ruta_absoluta_imagen is None:
    print("El archivo especificado no se encontró en el sistema.")
    exit()

# Obtener coordenadas de la imagen
latitud, longitud = obtener_coordenadas(ruta_absoluta_imagen)

if latitud is not None and longitud is not None:
    # Imprimir latitud y longitud en grados
    print(f"Latitud: {latitud} grados")
    print(f"Longitud: {longitud} grados")
else:
    print("No se pudo obtener la ubicación de la imagen.")
