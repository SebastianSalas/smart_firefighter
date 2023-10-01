import tkinter as tk
import numpy as np
import time
from views.writeMap import moverAgente_mapa


class Interfaz(tk.Tk):
    global matriz
    with open("resources/Prueba1.txt", "r") as archivo:
        lineas = archivo.readlines()
        matriz = np.array([list(map(int, linea.strip().split()))
                          for linea in lineas])
    
    def __init__(self):
        super().__init__()
        self.title("El Bombero Inteligente")
        self.geometry("900x600")
        self.config(bg="white")
        moverAgente_mapa(self, 0)