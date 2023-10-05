import os
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

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
        
        # Propiedades de la ventana
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
        self.canvas_matriz.bind("<Configure>", self.dibujar_matriz)

        # Canvas en el contenedor derecho
        self.right_canvas = tk.Canvas(self.right_frame, bg="white", bd=2, relief="solid")
        self.right_canvas.pack(expand=True, fill="both")
        self.right_canvas.bind("<Configure>", self.right_canvas_resize)

        # Primera imagen en el contenedor derecho
        first_image = Image.open("resources/images/firefighter.png")
        self.photo = ImageTk.PhotoImage(first_image)
        self.first_label = tk.Label(self.right_canvas, image = self.photo)
        self.first_label.config(bg="white")
        self.first_label.pack(padx= 10, pady=10, fill="x")
        
        # Etiqueta con el título del programa
        self.title_label = tk.Label(self.right_canvas, text="Bombero inteligente", fg="red", font=("Helvetica", 18))
        self.title_label.config(bg="white")
        self.title_label.pack(pady="5", padx="10", fill="x")
        
        # Etiqueta de selección de tipo de búsqueda
        self.selec_search_label = tk.Label(self.right_canvas, text="Seleccione el tipo de búsqueda:", fg="black", font=("Helvetica", 11), anchor="w", justify="left")
        self.selec_search_label.config(bg="white")
        self.selec_search_label.pack(pady="5", padx="10", fill="x")
        
        # Selector de tipo de búsqueda
        search_options = ["Seleccionar...", "Búsqueda no informada", "Búsqueda informada"]
        selected_search = tk.StringVar(self)
        selected_search.set(search_options[0])
        select_search = tk.OptionMenu(self.right_canvas, selected_search, *search_options)
        select_search.pack(padx="10", fill="x")
        select_search.config(font=('Helvetica', 10), bg="indianred", fg="black")
        
        # Etiqueta de selección de algoritmo
        self.select_algorithm_label = tk.Label(self.right_canvas, text="Seleccione el algoritmo:", fg="black", font=("Helvetica", 11), anchor="w", justify="left")
        self.select_algorithm_label.config(bg="white")
        self.select_algorithm_label.pack(pady="5", padx="10", fill="x")
        
        # Selector del algoritmo de búsqueda a utilizar
        search_algorithms = {
            "Búsqueda no informada": ["Seleccionar...", "Amplitud", "Costo uniforme", "Profundidad"],
            "Búsqueda informada": ["Seleccionar...", "Avara", "A*"]
        }

        # Selector del algortimo a utilizar
        self.selected_algorithm = tk.StringVar(self.right_canvas)
        self.select_algorithm_search = tk.OptionMenu(self.right_canvas, self.selected_algorithm, "")
        self.search_algorithm_options = {}

        # Crear el menú desplegable para el tipo de búsqueda seleccionado
        for algorithm_type, algorithm_list in search_algorithms.items():
            algorithm_menu = tk.OptionMenu(self.right_canvas, self.selected_algorithm, *algorithm_list)
            algorithm_menu.config(font=('Helvetica', 10), bg="indianred", fg="black")
            algorithm_menu.pack(padx="10", fill="x")
            algorithm_menu.pack_forget()
            self.search_algorithm_options[algorithm_type] = algorithm_menu

        def search(*args):
            algorithm_type = selected_search.get()
            self.selected_algorithm.set(algorithm_list[0])
            
            # Ocultar los menús
            for menu in self.search_algorithm_options.values():
                menu.pack_forget()

            # Mostrar el menú correspondiente al tipo de búsqueda seleccionado
            if algorithm_type in self.search_algorithm_options:
                self.select_algorithm_search = self.search_algorithm_options[algorithm_type]
                self.select_algorithm_search.pack(padx="10", fill="x")
                
                # Establecer el primer elemento como seleccionado
                algorithms_for_type = search_algorithms.get(algorithm_type, [])
                if algorithms_for_type:
                    self.selected_algorithm.set(algorithms_for_type[0])

        selected_search.trace_add("write", search)

        # Crear un frame para contener los botones
        self.button_frame = tk.Frame(self.right_canvas, bg="white")
        self.button_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

        # Botón de inicio del algoritmo
        start_button = tk.Button(self.button_frame, text="Iniciar", bg="indianred", fg="black")
        start_button.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        start_button.config(font=('Helvatica', 11))

        # Botón de reiniciar
        restart_button = tk.Button(self.button_frame, text="Reiniciar", bg="indianred", fg="black")
        restart_button.pack(side=tk.RIGHT, fill="x", expand=True, padx=5)
        restart_button.config(font=('Helvatica', 11))

    def resize_first_image(self, image, size):
        return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))

    def right_canvas_resize(self, event):
        # Manejar el evento de redimensionar el Canvas y la imagen
        self.photo = self.resize_first_image(Image.open("resources/images/firefighter.png"), (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4)))
        self.first_label.config(image=self.photo)

    def agent_movements_event(self):
        self.bind("<Up>", lambda event: self.agent_movements(event, "<Up>"))
        self.bind("<Down>", lambda event: self.agent_movements(event, "<Down>"))
        self.bind("<Left>", lambda event: self.agent_movements(event, "<Left>"))
        self.bind("<Right>", lambda event: self.agent_movements(event, "<Right>"))

    def dibujar_matriz(self, event):

        # Eliminar dibujos anteriores
        self.canvas_matriz.delete("all")
        # Número de filas y columnas en la matriz
        rows = 10
        columns = 10
        # Tamaño de cada rectángulo en el Canvas
        rectangle_width = self.canvas_matriz.winfo_width() // columns
        rectangle_height = self.canvas_matriz.winfo_height() // rows

        # Crear imagen del bombero en el contenedor izquierdo
        self.agent_image = ImageTk.PhotoImage(Image.open("resources/images/firefighter_icon.png").resize((round(rectangle_width * 0.8), round(rectangle_height * 0.8)), Image.LANCZOS))
        self.label_agent_icon = tk.Label(self.canvas_matriz, image = self.agent_image, width= rectangle_width ** 0.9, height= rectangle_height ** 0.9)
        self.label_agent_icon.config(highlightbackground="white", highlightthickness="0")

        for row in range(rows):
            for column in range(columns):

                # Calcular coordenadas de la celda
                x1 = column * rectangle_width # Esquina superior izquierda 
                y1 = row * rectangle_height # Esquina superior izquierda
                x2 = x1 + rectangle_width # Esquina inferior derecha
                y2 = y1 + rectangle_height # Esquina inferior derecha
                x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

                # Color y texto para el rectángulo
                texto = ""
                if matriz[row][column] == 0: # Casilla libre
                    color = "white"
                elif matriz[row][column] == 1: # Obstáculo
                    color = "#767171"
                elif matriz[row][column] == 2: # Punto de fuego
                    color = "#ED7D31"
                    texto = "F"
                elif matriz[row][column] == 3: # Cubo de un litro
                    color = "#FF0000"
                    texto = "C1L"
                elif matriz[row][column] == 4: # Cubo de dos litros
                    color = "#FF0000"
                    texto = "C2L"
                elif matriz[row][column] == 5: # Punto de inicio
                    color = "#00B050"
                    texto = "PI"

                    if (x1 == 0 and y1 != 0): # Posición cuando X=0 y Y!=0
                        self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(y1 ** 0.35))
                    elif (x1 != 0 and y1 == 0): # Posición cuando X!=0 y Y=0
                        self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(rectangle_height ** 0.55))
                    elif (x1 == 0 and y1 == 0): # Posición cuando X=0 y Y=0
                        self.label_agent_icon.place(x=x1 + (rectangle_width * 0.15), y=y1 + round(rectangle_height ** 0.55))
                    else: # Posición en cualquier otro caso
                        self.label_agent_icon.place(x=x1 + round(x1 ** 0.35), y=y1 + round(y1 ** 0.35))

                    self.agent_movements_event()
                elif matriz[row][column] == 6: # Hidrante
                    color = "#00B0F0"
                    texto = "H"

                # Dibujar rectángulos en el Canvas
                self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                self.canvas_matriz.create_text(x_center, y_center, text=texto, fill="black", font=("Helvetica", 14))

    def agent_movements(self, event, movement):

        # 
        x, y = int(self.label_agent_icon.place_info()['x']), int(self.label_agent_icon.place_info()['y'])
        rectangle_width, rectangle_height = self.canvas_matriz.winfo_width() // len(matriz[0]), self.canvas_matriz.winfo_height() // len(matriz)

        if movement == "<Up>":  # Movimiento hacia arriba del agente
            y -= rectangle_height
        elif movement == "<Down>": # Movimiento hacia abajo del agente
            y += rectangle_height
        elif movement == "<Left>":
            x -= rectangle_width
        elif movement == "<Right>":
            x += rectangle_width

        # Asignar los nuevos valores
        self.label_agent_icon.place(x=x, y=y)


if __name__ == "__main__":
    app = mainInterface()
    app.mainloop()
    #os.system('cls') # Limpia la terminal
