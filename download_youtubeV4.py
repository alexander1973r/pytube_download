# testing en python 3.9
from tkinter import *  # interface grafica
from tkinter import ttk  # usar Treeview
from PIL import Image, ImageTk  # manejo de imagen jpg
from pytube import YouTube  # descargar youtube
import threading  # crear hilo de ejecucion
from selenium import webdriver  # motor Selenium para browser
import datetime  # convertir en segundos
import os  # para ruta de archivos
import subprocess  # ejecutar subproces de comando shell
import configuracionV1 as Config  # configuracion del programa
import re  # para quitar caracteres especiales

# inicializacion de variables
ocultar = True
url = ''  # variable de ruta video youtube
pos = ''  # posicion de ventana padre
pos_hija = ''  # posicion ventana hija

# --------------------------------------------------
# cargar archivo de configuracion
Config.leer_archivo()
ruta_app = os.getcwd()  # ruta actual
ruta = os.path.join(ruta_app, Config.variables['RUTA'])  # ruta para almacenar
print(ruta)

# --------------------------------------------------
# ventana principal
root = Tk()  # se crea la instanacia de la root
root.title("Download Youtube V1")
root.geometry("230x200" + Config.variables['POSICION'])
print("230x200" + Config.variables['POSICION'])
root.resizable(height=FALSE, width=FALSE)  # no redimensiona
root.attributes("-topmost", True)  # colocar al frente la root

# boton para descargar video
img = Image.open("youtube_01.jpg")  # PIL carga la imagen
img = img.resize((150, 50), Image.ANTIALIAS)  # res 150 x 50
img = ImageTk.PhotoImage(img)  # convert to PhotoImage
#
b4 = Button(root)
b4.config(text="Download Youtube")
b4.config(image=img)
b4.config(compound=TOP)
b4.config(font=("arial", 12))
b4.pack(pady=10)

# boton para ver listado descargado
b2 = Button(text="[Ver] Listado",
            font=("arial", 12),
            width=16, bg='White')
b2.pack(pady=10)

# label de estatus
lbl_estatus = Label(root, text="Idle...",
                    font=('arial', 16),
                    bg="white", width=12)
lbl_estatus.pack(pady=10)
# ------------------------------------------------------

# cargar selenium con url youtube
# visitar el link
# https://sites.google.com/a/chromium.org/chromedriver/downloads
browser = webdriver.Chrome(executable_path=r"chromedriver88.exe")
str1 = browser.capabilities['browserVersion']
str2 = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
print(str1)
print(str2)
print(str1[0:2], '<-- Navegador')
print(str2[0:2], '<-- Driver')
if str1[0:2] != str2[0:2]:
    print("Favor descargar la version correcta del Driver Selenium")
    print("Link:")
    print('https://sites.google.com/a/chromium.org/chromedriver/downloads')
    browser.close()
    exit()
else:
    print("DRIVER CORRECTO de Chrome Selenium....")

# carga a la pagina
browser.get("https://www.youtube.com/")


# cerrar browser selenium y ventana ppal
def close_ppal_window():
    global pos
    global pos_hija
    # grabar nueva posicion de ventana
    pos = str(root.winfo_geometry())
    pos = pos[pos.find('+', 0):].strip()
    print(pos)  # obtenemos la ubicacion de geometria
    Config.variables['POSICION'] = pos
    pos_hija = str(ventanaHija.winfo_geometry())
    pos_hija = pos_hija[pos_hija.find('+', 0):].strip()
    Config.variables['HIJA'] = pos_hija
    Config.grabar_archivo()
    try:
        browser.close()
    except Exception as e:
        print("falla al cerrar Selenium...")
        print(e)
        print("puede ser que se ha cerrado antes...")

    root.quit()


root.protocol("WM_DELETE_WINDOW", close_ppal_window)  # evento cerrer ventana ppal

# MENU SUPERIOR
menubar = Menu(root)
root.config(menu=menubar)  # display the menu
menubar.add_command(label="Salir", command=close_ppal_window)


# -----------------------------------------------------
# Ventana Hija
# funcion para deshabilitar boton de cerrar ventana
def disable_close_window():
    pass


ventanaHija = Toplevel(root)  # le decimos cual es la ventana padr
ventanaHija.title("<Doble Click para ver Video Bajados>")
ventanaHija.geometry("400x200" + Config.variables['HIJA'])
# protocolo para direccinar el cerrar ventana en funcion
ventanaHija.protocol("WM_DELETE_WINDOW", disable_close_window)
ventanaHija.withdraw()  # ocultar ventana hija
# -------------------------------------------------------

# creando tabla con Treeview
tree = ttk.Treeview(ventanaHija, show='headings', height=5)
tree["columns"] = ("archivo", "tiempo", 'descarga')
tree["displaycolumns"] = ("archivo", "tiempo", 'descarga')  # columnas a mostrar
# creando columnas
tree.column("archivo", width=100)
tree.column("tiempo", width=50)
tree.column("descarga", width=50)
# encabezado de columnas Columna #0 es obligatoria
tree.heading("archivo", text="Archivo")
tree.heading("tiempo", text="tiempo")
tree.heading("descarga", text="Descarga")
# Scroll Y
treeYScroll = ttk.Scrollbar(ventanaHija, orient=VERTICAL)
treeYScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeYScroll.set)
treeYScroll.pack(side=RIGHT, fill=Y)
tree.pack(fill=BOTH, expand=1)
# boton para ver ruta archivos descargados
btn_02 = Button(ventanaHija, text="Ver Descargas")
btn_02.pack(padx=10, pady=10)


# ----------------------------------------------------
# funcion ocultar ventana hija
# funcion para ocultar / mostrar ventana
def mostrar_ventana(_event):
    global ocultar
    if ocultar:
        print('mostrar')
        b2.config(text="[ocultar] listado", bg='Yellow')
        ventanaHija.deiconify()  # mostrar ventana
        ocultar = False
    else:
        print('ocultar')
        b2.config(text="[Ver] listado", bg='White')
        ventanaHija.withdraw()  # ocultar ventana
        ocultar = True


# ----------------------------------------------
#     FUNCIONES
# ----------------------------------------------
# funcion para descargar video por hilo de tarea
def descargar_video():
    last_post = None

    # tiempo progreso descarga
    def draw_progress_bar(stream=None, _chunk=None, file_handle=None, _remaining=None):
        archivo_size = stream.filesize
        percent = (100 * (archivo_size - file_handle)) / archivo_size
        segundos = str(datetime.timedelta(seconds=video.length))
        salida_porcent = "{:00.0f}%".format(percent)
        print('nombre: ', video.title)
        print('length: ', video.length)
        print(segundos)  # conversion tiempo en unid seg
        lbl_salida = last_post + '-->' + salida_porcent
        print(lbl_salida)
        lbl_estatus.config(text=lbl_salida)  # porcentaje mostrado en ventana principal
        tree.item(last_post, values=(video.title, segundos, salida_porcent))  # modificar  item especifico del treeview

    try:
        last_post = tree.get_children()[-1]  # ultima posicion
        print('url video: ', url)
        video = YouTube(url, on_progress_callback=draw_progress_bar)
        print('last pos:', last_post)
        salida = None
        # seleccionamos un solo video en baja resolucion mp4
        if Config.variables['RESOLUCION'] == 'baja':
            salida = video.streams. \
                filter(progressive=True, file_extension='mp4', ). \
                order_by('resolution'). \
                asc(). \
                first()

        # seleccionamos un solo video en ALTA resolucion mp4
        if Config.variables['RESOLUCION'] == 'alta':
            salida = video.streams. \
                filter(progressive=True, file_extension='mp4', ). \
                order_by('resolution'). \
                desc(). \
                first()

        fichero_size = salida.filesize
        print('VIDEO SELECT: ', salida)
        print('filesize: ', fichero_size)
        # conversion de nombre
        nombre = video.title
        convert_ascii = str(nombre.encode("ascii", 'replace')) + '.mp4'  # convierte en ASCII
        line = re.sub('[!#$@\/:*?"<>|]', '', convert_ascii)  # set de caracteres a quitar
        salida.download(filename=line[1:], output_path=ruta)  # donde sera guardado el archivo
    except Exception as e:
        print('Falla en Descarga...')
        print(e)
        tree.item(last_post, values=(url, 'Falla en Descarga', '...'))


# Func de hilo de tarea para ejecutar funcion de descarga youtube
def boton_video(_event):
    global url
    print('descargar video [hilo de proceso]')
    url = browser.current_url  # obtener el URL
    tree.insert("", 'end', values=(url, "En espera...", "..."))  # insertar fila
    msg_send = threading.Thread(target=descargar_video)
    msg_send.daemon = True
    msg_send.start()


# Func saber posicion de ventana padre
def mover_ventana(_event):
    global pos
    pos = str(root.winfo_geometry())
    pos = pos[pos.find('+', 0):].strip()
    print(pos)  # obtenemos la ubicacion de geometria


# Func saber posicion ventana hija
def mover_ventana_hija(_event):
    global pos_hija
    pos_hija = str(ventanaHija.winfo_geometry())
    pos_hija = pos_hija[pos_hija.find('+', 0):].strip()
    print("ventana hija: ", pos_hija)  # obtenemos la ubicacion de geometria


# funcion para ir ruta por explorador
def ir_ruta(_event):
    atributo_path = '/n,' + ruta
    subprocess.run(["explorer.exe", atributo_path])


# eventos de ventana principal
root.bind('<Configure>', mover_ventana)  # evento ventana ppal mover
ventanaHija.bind('<Configure>', mover_ventana_hija)  # evento ventana ppal mover
b4.bind('<Button-1>', boton_video)  # boton descargar video
b2.bind('<Button-1>', mostrar_ventana)  # boton ocultar y mostrar lista
tree.bind('<Double-Button-1>', ir_ruta)  # boton ir a ruta navegador doble-click
btn_02.bind('<Button-1>', ir_ruta)  # boton ir a ruta navegador

root.mainloop()  # correr el ciclo para mostrar root
print("fin...")
