import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import time

with open("resources/Prueba1.txt", "r") as archivo:
    lineas = archivo.readlines()
    matriz = np.array([list(map(int, linea.strip().split()))
                      for linea in lineas])
    
def moverAgente_mapa(self, ruta):
    # Definir los valores y las imágenes correspondientes
    self.libre = 0
    self.muro = 1
    self.fuego = 2
    self.un_litro = 3
    self.dos_litros = 4
    self.bombero = 5
    self.hidratante = 6
    
    self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
    #self.canvas.create_image()
    self.canvas.place(x=0, y=0)
    
    # Dibujar la matriz en el canvas
    for i in range(10):
        for j in range(10):
            x = j * 60
            y = i * 60

            if matriz[i][j] == self.libre:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="white")
            elif matriz[i][j] == self.muro:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="gray")
            elif matriz[i][j] == self.fuego:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="red")
            elif matriz[i][j] == self.un_litro:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="blue")
            elif matriz[i][j] == self.dos_litros:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="blue")
            elif matriz[i][j] == self.bombero:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="green")
            elif matriz[i][j] == self.hidratante:
                self.canvas.create_rectangle(x, y, x+60, y+60, fill="cyan")