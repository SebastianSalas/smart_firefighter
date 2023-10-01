''' Proyecto #1: Bombero Inteligente - Inteligencia artificial
Hecho por:
    - Janiert Sebastián Salas - 201941265
    - Diego Fernando Victoria - 202125877
    - Jhon Alexander Valencia - 202042426
'''

import ctypes
from tkinter import Tk, Label, Button

def screenSize():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    ancho, alto = round(user32.GetSystemMetrics(0) / 2), round(user32.GetSystemMetrics(1) / 2)
    size = str(ancho) + "x" + str(alto) + "+" + str(round(ancho / 2)) + "+" + str(round(alto / 2))
    return size

ventana = Tk()
ventana.geometry(screenSize())
ventana.title("Proyecto #1: Bombero inteligente - Inteligencia artificial")
ventana.resizable(0,0)

ventana.mainloop()