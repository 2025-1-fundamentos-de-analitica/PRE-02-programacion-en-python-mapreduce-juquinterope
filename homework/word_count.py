"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
from itertools import groupby
import time


#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#
def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""

    if not os.path.exists("files/input"):
        os.makedirs("files/input")
    for file in glob.glob("files/raw/*"):
        for i in range(1, n + 1):
            with open(file, "r", encoding="utf-8") as f:
                with open(
                    f"files/input/{os.path.basename(file).split('.')[0]}_{i}.txt",
                    "w",
                    encoding="utf-8",
                ) as f2:
                    f2.write(f.read())


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
def load_input(input_directory):
    """Funcion load_input"""
    
    # Lista vacia para almacenar las tuplas
    lines = []

    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        # Verifica que el archivo exite
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                for line in file:
                    lines.append((filename, line))

    return lines


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    lines = []
    for filename, line in sequence:
        # Eliminar espacios en blanco al inicio y al final
        line = line.strip()
        # Eliminar caracteres especiales
        line = ''.join(e for e in line if e.isalnum() or e.isspace())
        # Convertir a minúsculas
        line = line.lower()
        lines.append((filename, line))

    return lines


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
    """Mapper"""
    # Lista vacia para almacenar las tuplas
    words = []

    for filename, line in sequence:
        # Separar la linea en palabras
        for word in line.split():
            words.append((word, 1))

    return words


#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    # Ordenar la lista de tuplas por la clave (palabra)
    sequence.sort(key=lambda x: x[0])
    return sequence


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    # Lista vacia para almacenar las tuplas
    result = []

    # Agrupar por clave (palabra) y sumar los valores
    for key, group in groupby(sequence, key=lambda x: x[0]):
        count = sum(value for _, value in group)
        result.append((key, count))

    return result


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""
    # Verifica si el directorio ya existe
    if os.path.exists(output_directory):
        # Si existe se borra
        for filename in glob.glob(os.path.join(output_directory, '*')):
            os.remove(filename)
    else:
        # Si no existe se crea
        os.makedirs(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""
    with open(os.path.join(output_directory, 'part-00000'), 'w') as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    with open(os.path.join(output_directory, '_SUCCESS'), 'w') as file:
        file.write('')


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    # Crea el directorio de salida
    create_ouptput_directory(output_directory)

    # Carga los archivos de texto
    lineas = load_input(input_directory)
    preprocesadas = line_preprocessing(lineas)

    # Mapea y agrupa las lineas
    map = mapper(preprocesadas)
    agrupadas = shuffle_and_sort(map)

    # Reduce las lineas
    reducidas = reducer(agrupadas)

    # Guarda el resultado en un archivo de texto
    save_output(output_directory, reducidas)
    create_marker(output_directory)


if __name__ == "__main__":
    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()

    # Imprime el tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
