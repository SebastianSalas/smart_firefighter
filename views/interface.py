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
        #self.resizable(0,0)

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
        # Evento para adaptar la matriz al tamaño del contenedor
        self.canvas_matriz.bind("<Configure>", self.dibujar_matriz)

        # Canvas en el contenedor derecho
        self.right_canvas = tk.Canvas(self.right_frame, bg="white", bd=2, relief="solid")
        self.right_canvas.pack(expand=True, fill="both")
        # Evento para adaptar el contenido al tamaño del contenedor
        self.right_canvas.bind("<Configure>", self.right_canvas_resize)

        # Crear elementos en el contenedor derecho
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
        options_1 = tk.StringVar(self)
        options_1.set(search_options[0])
        select_search = tk.OptionMenu(self.right_canvas, options_1, *search_options)
        select_search.pack(padx="10", fill="x")
        select_search.config(font=('Helvetica', 10), bg="indianred", fg="black")
        # Etiqueta de selección de algoritmo
        self.selec_algorithm = tk.Label(self.right_canvas, text="Seleccione el algoritmo:", fg="black", font=("Helvetica", 11), anchor="w", justify="left")
        self.selec_algorithm.config(bg="white")
        self.selec_algorithm.pack(pady="5", padx="10", fill="x")
        # Selector del algoritmo de búsqueda a utilizar
        search_algorithms = {
            "Búsqueda no informada": ["Amplitud", "Profundidad", "Costo uniforme"],
            "Búsqueda informada": ["Avara", "A*"]
        }

        self.selected_algorithm = tk.StringVar(self.right_canvas)
        self.search_algorithm_menu = tk.OptionMenu(self.right_canvas, self.selected_algorithm, "")
        self.search_algorithm_menus = {}

        for algorithm_type, algorithm_list in search_algorithms.items():
            algorithm_menu = tk.OptionMenu(self.right_canvas, self.selected_algorithm, *algorithm_list)
            algorithm_menu.config(font=('Helvetica', 10), bg="indianred", fg="black")
            algorithm_menu.pack(padx="10", fill="x")
            algorithm_menu.pack_forget()
            self.search_algorithm_menus[algorithm_type] = algorithm_menu

        def search(*args):
            algorithm_type = options_1.get()
            self.selected_algorithm.set(algorithm_list[0])
            
            # Ocultar todos los menús
            for menu in self.search_algorithm_menus.values():
                menu.pack_forget()

            # Mostrar el menú correspondiente al tipo de búsqueda seleccionado
            if algorithm_type in self.search_algorithm_menus:
                self.search_algorithm_menu = self.search_algorithm_menus[algorithm_type]
                self.search_algorithm_menu.pack(padx="10", fill="x")
                
                # Establecer el primer elemento como seleccionado
                algorithms_for_type = search_algorithms.get(algorithm_type, [])
                if algorithms_for_type:
                    self.selected_algorithm.set(algorithms_for_type[0])

        options_1.trace_add("write", search)

        # Botón de inicio del algoritmo
        boton_inicio = tk.Button(self.right_canvas, text="Iniciar", bg="indianred", fg="black")
        boton_inicio.pack()
        boton_inicio.config(font=('Helvatica', 12))


    def resize_image(self, image, size):
        return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))

    def right_canvas_resize(self, event):
        # Manejar el evento de redimensionar el Canvas
        new_size = (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4))
        self.photo = self.resize_image(Image.open("resources/images/firefighter.png"), new_size)
        self.first_label.config(image=self.photo)

    def dibujar_matriz(self, event=None):

        # Eliminar dibujos anteriores
        self.canvas_matriz.delete("all")

        # Número de filas y columnas en la matriz
        rows = 10
        columns = 10

        # Tamaño de cada rectángulo en el Canvas
        rectangle_width = self.canvas_matriz.winfo_width() // columns
        rentangle_height = self.canvas_matriz.winfo_height() // rows

        
        for row in range(rows):
            for column in range(columns):

                # Calcular coordenadas de la celda
                x1 = column * rectangle_width
                y1 = row * rentangle_height
                x2 = x1 + rectangle_width
                y2 = y1 + rentangle_height

                # Color y texto para el rectángulo
                texto = ""
                if matriz[row][column] == 0:
                    color = "white"
                elif matriz[row][column] == 1:
                    color = "#767171"
                elif matriz[row][column] == 2:
                    color = "#ED7D31"
                elif matriz[row][column] == 3:
                    color = "#FF0000"
                    texto = "1L"
                elif matriz[row][column] == 4:
                    color = "#FF0000"
                    texto = "2L"
                elif matriz[row][column] == 5:
                    color = "#00B050"
                elif matriz[row][column] == 6:
                    color = "#00B0F0"

                # Dibujar rectángulos en el Canvas
                self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                x_centro, y_centro = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas_matriz.create_text(x_centro, y_centro, text=texto, fill="black", font=("Helvetica", 14))

if __name__ == "__main__":
    app = mainInterface()
    app.mainloop()
