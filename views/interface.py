import os
import uuid
import tkinter as tk
import numpy as np
import amplitud as amplitud
import profundidad as profundidad
import costo_uniforme as costo
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
    self.resizable(True, True)
    self.image_dict = {}

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
    self.buttons_frame = tk.Frame(self.right_canvas, bg="white")
    self.buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

    algorithm_functions = {
      "Amplitud": amplitud.solve,
      "Costo uniforme": costo.solve, 
      "Profundidad": profundidad.solve,
      "Avara": None,
      "A*": None
    }

    # Función del botón de inicio del algoritmo
    def start_algorithm():
      algorithm = self.selected_algorithm.get()

      if selected_search.get() != "Seleccionar..." and algorithm != "Seleccionar...":
        # Deshabilitar botones
        start_button.config(state=tk.DISABLED)
        restart_button.config(state=tk.DISABLED)

        # Ejecución del algoritmo seleccionado
        if algorithm in algorithm_functions:
          print(f"Prueba {algorithm}:")
          if algorithm_functions[algorithm]: # Eliminar luego, sólo es útil mientras se definen las funciones de los algoritmos
              expanded_nodes, path, depth, cost = algorithm_functions[algorithm](matriz)
              self.agent_movements(path)
              print(f"expanded_nodes: {expanded_nodes}, path: {path}, depth: {depth}, cost: {cost}")
          else:
              print(f"{algorithm} no está implementado todavía.")
        restart_button.config(state=tk.NORMAL)

    # Botón de inicio del algoritmo
    start_button = tk.Button(self.buttons_frame, text="Iniciar", bg="indianred", fg="black", command=start_algorithm)
    start_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    start_button.config(font=('Helvetica', 11))

    # Función para reiniciar la selección del tipo de búsqueda
    def restart():
      global matriz
      start_button.config(state=tk.NORMAL)
      selected_search.set(search_options[0])
      self.selected_algorithm.set("")

      # Optimizar
      with open("resources/map.txt", "r") as archivo:
        lineas = archivo.readlines()
        matriz = np.array([list(map(int, linea.strip().split())) for linea in lineas])
      self.dibujar_matriz(any)

    # Botón de reiniciar
    restart_button = tk.Button(self.buttons_frame, text="Reiniciar", bg="indianred", fg="black", command=restart)
    restart_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    restart_button.config(font=('Helvetica', 11))

    # Crear ventana con los créditos
    def credits():
      credits_window = tk.Toplevel(self)
      credits_window.title("Proyecto #1: Bombero inteligente - Inteligencia artificial")
      credits_window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
      credits_window.config(bg="indianred")

      # Etiqueta para mostrar los créditos
      credits_label = tk.Label(credits_window, text="HECHO POR:\n\nDIEGO FERNANDO VICTORIA - 202125877\nDIEGO.VICTORIA@CORREOUNIVALLE.EDU.CO\n\nJANIERT SEBASTIÁN SALAS - 201941265\nJANIERT.SALAS@CORREOUNIVALLE.EDU.CO\n\nJHON ALEXANDER VALENCIA - 202042426\nJHON.HILAMO@CORREOUNIVALLE.EDU.CO")
      credits_label.config(font=('Helvetica', 10), bg="white")
      credits_label.place(relx=0.5, rely=0.5, anchor="center")
      credits_window.transient(self)
      credits_window.wait_window()

    # Botón de créditos
    credits_button = tk.Button(self.buttons_frame, text="Créditos", bg="indianred", fg="black", command=credits)
    credits_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    credits_button.config(font=('Helvetica', 11))

    # Distribuir uniformemente el espacio en X entre los botones
    self.buttons_frame.columnconfigure(0, weight=1)
    self.buttons_frame.columnconfigure(1, weight=1)

  def resize_first_image(self, image, size):
    return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))

  def right_canvas_resize(self, event):
    # Manejar el evento de redimensionar el Canvas y la imagen
    self.photo = self.resize_first_image(Image.open("resources/images/firefighter.png"), (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4)))
    self.first_label.config(image=self.photo)

  def dibujar_matriz(self, event):

    # Eliminar dibujos anteriores
    self.canvas_matriz.delete("all")
    if hasattr(self, 'label_agent_icon') and self.label_agent_icon:self.label_agent_icon.destroy()
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
        color = "white"
        image_path = None
        if matriz[row][column] == 0: # Casilla libre
          pass
        elif matriz[row][column] == 1: # Obstáculo
          color = "#767171"
        elif matriz[row][column] == 2: # Punto de fuego
          image_path = "resources/images/burning_house.png"
        elif matriz[row][column] == 3: # Cubo de un litro
          image_path = "resources/images/water_cube1.png"
        elif matriz[row][column] == 4: # Cubo de dos litros
          image_path = "resources/images/water_cube2.png"
        elif matriz[row][column] == 5: # Punto de inicio
          image_path = "resources/images/fire_truck.png"
          
          if (x1 == 0 and y1 != 0): # Posición cuando X=0 y Y!=0
            self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(y1 ** 0.35))
          elif (x1 != 0 and y1 == 0): # Posición cuando X!=0 y Y=0
            self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(rectangle_height ** 0.55))
          elif (x1 == 0 and y1 == 0): # Posición cuando X=0 y Y=0
            self.label_agent_icon.place(x=x1 + (rectangle_width * 0.15), y=y1 + round(rectangle_height ** 0.55))
          else: # Posición en cualquier otro caso
            self.label_agent_icon.place(x=x1 + round(x1 ** 0.35), y=y1 + round(y1 ** 0.35))

        elif matriz[row][column] == 6: # Hidrante
          image_path = "resources/images/hydrant.png"
        elif matriz[row][column] == 7: # Fuego apagado
          image_path = "resources/images/house.png"

        # Dibujar rectángulos en el Canvas
        self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        if image_path:
          unique_id = str(uuid.uuid4())  # Generar un identificador único
          image = ImageTk.PhotoImage(Image.open(image_path).resize((round(rectangle_width * 0.9), round(rectangle_height * 0.9)), Image.LANCZOS))
          self.image_dict[unique_id] = image  # Almacenar la imagen en el diccionario
          self.canvas_matriz.create_image(x_center, y_center, anchor=tk.CENTER, image=image)

  def agent_movements(self, movements):

    # Ubicaciones de los puntos de fuego
    fire_positions = [(row, column) for row in range(len(matriz)) for column in range(len(matriz[0])) if matriz[row][column] == 2]
    # Ubicaciones de los cubos de agua
    cube_positions = [(row, column) for row in range(len(matriz)) for column in range(len(matriz[0])) if matriz[row][column] == 3 or matriz[row][column] == 4]

    # Cálculo de posición del agente y longitud movimientos
    agent_x, agent_y = int(self.label_agent_icon.place_info()['x']), int(self.label_agent_icon.place_info()['y'])
    rectangle_width, rectangle_height = self.canvas_matriz.winfo_width() // len(matriz[0]), self.canvas_matriz.winfo_height() // len(matriz)
    
    def move_agent(index):
      nonlocal agent_x, agent_y
      if index < len(movements):
        if movements[index] == 0:  # Movimiento hacia arriba del agente
          agent_y -= rectangle_height
        elif movements[index] == 1: # Movimiento hacia abajo del agente
          agent_y += rectangle_height
        elif movements[index] == 3: # Movimiento hacia la izquierda del agente
          agent_x -= rectangle_width
        elif movements[index] == 2: # Movimiento hacia la derecha del agente
          agent_x += rectangle_width

        # Verificar si el agente pasa sobre un fuego
        if (agent_y // rectangle_height, agent_x // rectangle_width) in fire_positions:
          # Actualizar la matriz y reflejar los cambios en el Canvas
          matriz[agent_y // rectangle_height][agent_x // rectangle_width] = 7  # Cambia el fuego a casilla libre
          self.dibujar_matriz(None)  # Vuelve a dibujar la matriz

        # Verifica si el agente toma un cubo de agua
        elif (agent_y // rectangle_height, agent_x // rectangle_width) in cube_positions: 
          # Actualizar la matriz y reflejar los cambios en el Canvas
          for row in range(len(matriz)):
            for col in range(len(matriz[0])):
              if matriz[row][col] == 3 or matriz[row][col] == 4: # Comprueba si la celda tiene algún cubo de agua
                matriz[row][col] = 0 # Reemplaza los cubos por celdas vacías
          self.dibujar_matriz(None)  # Vuelve a dibujar la matriz

        # Asignar los nuevos valores
        self.label_agent_icon.place(x=agent_x, y=agent_y)

        # Pausa de 1/2 segundo (500 milisegundos) entre cada movimiento
        self.after(500, move_agent, index + 1)
        
    # Iniciar la secuencia de movimientos desde el índice 1 para evitar el None
    move_agent(1)

if __name__ == "__main__":
  app = mainInterface()
  app.mainloop()
  #os.system('cls') # Limpia la terminal
