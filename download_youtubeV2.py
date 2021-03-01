# testing en python 3.9
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pytube import YouTube
import threading
from selenium import webdriver  # motor Selenium
import datetime

# --------------------------------------------------
# ventana principal
root = Tk()  # se crea la instanacia de la root
root.title("Download Youtube V1")
root.geometry("200x200")
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
                    font=('arial', 18),
                    bg="white", width=12)
lbl_estatus.pack(pady=10)
# MENU SUPERIOR
menubar = Menu(root)
root.config(menu=menubar)  # display the menu
menubar.add_command(label="Config")
menubar.add_command(label="Salir")
# ------------------------------------------------------


# cargar selenium con url youtube
# Carga de Selenium
browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
# carga a la pagina
browser.get("https://www.youtube.com/")


# -----------------------------------------------------
# Ventana Hija
# funcion para deshabilitar boton para cerrar ventana
def disable_close_window():
    pass


ventanaHija = Toplevel(root)  # le decimos cual es la ventana padr
ventanaHija.title("Hija")
ventanaHija.geometry("400x200")
# protocolo para direccinar el cerrar ventana en funcion
ventanaHija.protocol("WM_DELETE_WINDOW", disable_close_window)
# ventanaHija.withdraw()   # ocultar ventana hija
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

# ----------------------------------------------------
# funcion ocultar ventana hija
ocultar = True


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
url = ''
# funcion para descargar video por hilo de tarea
def descargar_video():
    # tiempo progreso descarga
    def draw_progress_bar(stream=None, chunk=None, file_handle=None, remaining=None):
        file_size = stream.filesize
        percent = (100 * (file_size - file_handle)) / file_size
        print('nombre: ', video.title)
        print('length: ', video.length)
        segundos = str(datetime.timedelta(seconds=video.length))
        print(segundos)  # conversion tiempo en unid seg
        salida_porcent = "{:00.0f}%".format(percent)
        print(salida_porcent)
        lbl_estatus.config(text=salida_porcent)  # porcentaje mostrado en ventana principal
        tree.item(last_post, values=(video.title, segundos, salida_porcent))  # modificar  item especifico del treeview

    last_post = tree.get_children()[-1]  # ultima posicion
    print('last pos:', last_post)
    print('url video: ', url)
    video = YouTube(url, on_progress_callback=draw_progress_bar)
    # seleccionamos video en baja resolucion mp4
    salida = video.streams. \
        filter(progressive=True, file_extension='mp4', ). \
        order_by('resolution'). \
        asc(). \
        first()

    file_size = salida.filesize
    print('VIDEO SELECT: ', salida)
    print('filesize: ', file_size)
    salida.download()


# hilo de tarea para ejecutar funcion de descarga youtube
def boton_video(_event):
    global url
    print('descargar video [hilo de proceso]')
    url = browser.current_url  # obtener el URL
    tree.insert("", 'end', values=("Cargando..", "En espera...", "..."))  # insertar fila
    msg_send = threading.Thread(target=descargar_video)
    msg_send.daemon = True
    msg_send.start()


def mover_ventana(_event):
    print(root.winfo_geometry())  # obtenemos la posicion de geometria
    # print(root.winfo_pointerxy())


def redimencionar(_event):
    root.geometry("500x200")


# eventos de ventana principal
root.bind('<Configure>', mover_ventana)
b4.bind('<Button-1>', boton_video)  # boton descargar video
b2.bind('<Button-1>', mostrar_ventana)  # boton ocultar y mostrar lista

root.mainloop()  # correr el ciclo para mostrar root
print("fin..")
