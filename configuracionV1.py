import os.path  # confirmar si existe un archivo

# DECLARACION DE VARIABLES
variables = {'RUTA':'downloads',
             'POSICION':'+0+0',
             'HIJA':'+0+0',
             'RESOLUCION':'alta'}

comentarios = """
# Comentarios de uso
# RUTA =  ubicacion donde sera guardado el video descargado youtube
# POSICION = posicion donde se ubicara la ventana
# HIJA = Posicion donde esta la ventana hija
# RESOLUCION = alta / baja  <--- son los dos modo de resolucion mp4 para modo automatico 
"""

leer = None

# cargar archivo
def leer_archivo():
    global leer
    # verificar si existe archivo
    if os.path.isfile('config.txt'):
        leer = True
    else:
        leer = False
        print("[ERROR] No existe archivo de configuracion")

    # si existe
    if leer:
        # Leyendo archivo por linea
        file1 = open('config.txt', 'r')
        contador = 0

        while True:
            contador += 1
            line = file1.readline()   # Get next line from file
            if not line:
                break
            # print("Linea{}: {}".format(contador, line.strip()))
            # detectar comentarios
            if line[:1] =='#':
                print("Comentario {}: {}".format(contador, line.strip()))
            else:
                # recorrer diccionario para optener valores
                for llave in variables:
                    if llave in line:
                        variables[llave] = line[line.find('=',0)+1:].strip()
                        print("Codigo {}: {}".format(contador, line.strip()))

        print('variables ->', variables) # salida valores recolectados

        file1.close()

# cargar archivo
def grabar_archivo():
    file1 = open('config.txt', 'w')

    # recorriendo variable
    for llave in variables.keys():
        dato = str(llave) + '=' + str(variables[llave]) + '\n'
        file1.write(dato)

    # colocar bloque de comentario
    for line in comentarios.splitlines():
        file1.write(line + '\n')


    file1.close()


# grabar_archivo()
# leer_archivo()
