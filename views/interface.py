''' Proyecto #1: Bombero Inteligente - Inteligencia artificial
Hecho por:
    - Janiert Sebastián Salas - 201941265
    - Diego Fernando Victoria - 202125877
    - Jhon Alexander Valencia - 202042426
'''

import tkinter as tk
import numpy as np

class mainInterface(tk.Tk):

    global matriz

    with open("resources/map.txt", "r") as archivo:
        lineas = archivo.readlines()
        matriz = np.array([list(map(int, linea.strip().split())) for linea in lineas])

    def __init__(self):
        
        super().__init__()

        # Obtener las dimensiones de la pantalla
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        
        # Calcular las dimensiones y posición de la ventana
        windowWidth, windowHeight = round(screen_width / 2), round(screen_height / 2)
        x, y = round((screen_width - windowWidth) / 2), round((screen_height - windowHeight) / 2) 
        self.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
        #self.geometry(f"+{x}+{y}")
        self.config(bg="white")
        self.title("Proyecto #1: Bombero inteligente - Inteligencia artificial")
        self.resizable(0,0)

        # Crear el contenedor izquierdo
        self.left_frame = tk.Frame(self, padx=10, pady=10, bg="white")
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.place(relx=0, rely=0, relwidth=0.65, relheight=1)

        # Crear el contenedor derecho
        self.right_frame = tk.Frame(self, padx=10, pady=10, bg="white")
        self.right_frame.pack(side="right", fill="y")
        self.right_frame.place(relx=0.64, rely=0, relwidth=0.35, relheight=1)
        
        # Canvas para representar la matríz en el contenedor izquierdo
        self.canvas_matriz = tk.Canvas(self.left_frame, bg="white", bd=2, relief="solid")
        self.canvas_matriz.pack(expand=True, fill="both")

        # Canvas para representar un Canvas en el contenedor derecho
        self.right_canvas = tk.Canvas(self.right_frame, bg="white", bd=2, relief="solid")
        self.right_canvas.pack(expand=True, fill="both")

        # Elementos en el contenedor derecho
        self.label_derecho = tk.Label(self.right_canvas, text="Contenedor derecho")
        self.label_derecho.pack()

        # Función para crear 100 rectángulos en el Canvas
        self.dibujar_matriz()

    def dibujar_matriz(self):
        # Número de filas y columnas en la matriz
        filas = 10
        columnas = 10

        # Tamaño de cada celda en el Canvas
        ancho_celda = self.canvas_matriz.winfo_reqwidth() // columnas
        alto_celda = self.canvas_matriz.winfo_reqheight() // filas

        for fila in range(filas):
            for columna in range(columnas):

                # Calcular coordenadas de la celda
                x1 = columna * ancho_celda
                y1 = fila * alto_celda
                x2 = x1 + ancho_celda
                y2 = y1 + alto_celda

                # Color y texto para el rectángulo
                texto = ""
                if matriz[fila][columna] == 0:
                    color = "white"
                elif matriz[fila][columna] == 1:
                    color = "gray"
                elif matriz[fila][columna] == 2:
                    color = "orange"
                elif matriz[fila][columna] == 3:
                    color = "red"
                    texto = "1L"
                elif matriz[fila][columna] == 4:
                    color = "red"
                    texto = "2L"
                elif matriz[fila][columna] == 5:
                    color = "green"
                elif matriz[fila][columna] == 6:
                    color = "lightblue"

                # Dibujar rectángulo en el Canvas
                self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                x_centro = (x1 + x2) // 2
                y_centro = (y1 + y2) // 2
                self.canvas_matriz.create_text(x_centro, y_centro, text=texto, fill="black")

if __name__ == "__main__":
    app = mainInterface()
    app.mainloop()