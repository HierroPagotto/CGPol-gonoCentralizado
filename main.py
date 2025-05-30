import tkinter as tk
import math
from tkinter import ttk

class PoligonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho NP2 - Polígono")
        self.root.geometry("1000x600")

        # Configurações iniciais
        self.canvas_width = 600
        self.canvas_height = 500
        self.centro_x = self.canvas_width // 2
        self.centro_y = self.canvas_height // 2
        
        # Parâmetros da figura
        self.num_lados = 5
        self.raio = 100
        self.tipo_figura = "poligono"
        
        # Transformações
        self.transl_x = self.transl_y = self.angulo = self.cisalhamento = 0
        self.escala = 1

        self.criar_interface()
        self.atualizar_poligono()

    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas para desenho
        canvas_frame = ttk.LabelFrame(main_frame, text="Área de Desenho", padding=10)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Painel de controles
        controls_frame = ttk.LabelFrame(main_frame, text="Controles", padding=10, width=300)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Tipo de figura
        tipo_frame = ttk.LabelFrame(controls_frame, text="Tipo de Figura")
        tipo_frame.pack(fill=tk.X, pady=5)
        self.tipo_var = tk.StringVar(value="poligono")
        for tipo in ["poligono", "circulo", "elipse"]:
            ttk.Radiobutton(tipo_frame, text=tipo.capitalize(), variable=self.tipo_var, 
                            value=tipo, command=self.atualizar_poligono).pack(anchor=tk.W)

        # Controle de lados
        lados_frame = ttk.LabelFrame(controls_frame, text="Lados")
        lados_frame.pack(fill=tk.X, pady=5)
        self.lados_var = tk.IntVar(value=5)
        ttk.Scale(lados_frame, from_=3, to=100, orient=tk.HORIZONTAL, 
                 variable=self.lados_var, command=self.mudar_lados).pack(fill=tk.X)
        self.lados_label = ttk.Label(lados_frame, text="Lados: 5")
        self.lados_label.pack()

        # Controle de raio
        raio_frame = ttk.LabelFrame(controls_frame, text="Raio")
        raio_frame.pack(fill=tk.X, pady=5)
        self.raio_var = tk.IntVar(value=100)
        ttk.Scale(raio_frame, from_=10, to=200, orient=tk.HORIZONTAL, 
                variable=self.raio_var, command=self.mudar_raio).pack(fill=tk.X)
        self.raio_label = ttk.Label(raio_frame, text="Raio: 100")
        self.raio_label.pack()

        # Controles de transformação
        self.criar_slider(controls_frame, "Translação X", -200, 200, 0, 
                         lambda val: self.atualizar_param("transl_x", val))
        self.criar_slider(controls_frame, "Translação Y", -200, 200, 0, 
                         lambda val: self.atualizar_param("transl_y", val))
        self.criar_slider(controls_frame, "Rotação (graus)", 0, 360, 0, 
                         lambda val: self.atualizar_param("angulo", math.radians(float(val))))
        self.criar_slider(controls_frame, "Escala", 0.1, 3.0, 1.0, 
                         lambda val: self.atualizar_param("escala", val))
        self.criar_slider(controls_frame, "Cisalhamento X", -2, 2, 0, 
                         lambda val: self.atualizar_param("cisalhamento", val))

    def criar_slider(self, parent, label, minval, maxval, default, callback):
        frame = ttk.LabelFrame(parent, text=label)
        frame.pack(fill=tk.X, pady=5)
        var = tk.DoubleVar(value=default)
        ttk.Scale(frame, from_=minval, to=maxval, variable=var, 
                 orient=tk.HORIZONTAL, command=callback).pack(fill=tk.X)

    def atualizar_param(self, param, val):
        setattr(self, param, float(val))
        self.atualizar_poligono()

    def mudar_lados(self, val):
        self.num_lados = int(float(val))
        self.lados_label.config(text=f"Lados: {self.num_lados}")
        self.atualizar_poligono()

    def mudar_raio(self, val):
        self.raio = int(float(val))
        self.raio_label.config(text=f"Raio: {self.raio}")
        self.atualizar_poligono()

    def calcular_vertices(self):
        lados = self.num_lados if self.tipo_var.get() != "elipse" else 100
        vertices = []
        
        for i in range(lados):
            angulo = 2 * math.pi * i / lados
            rx = self.raio
            ry = self.raio * (0.6 if self.tipo_var.get() == "elipse" else 1)

            # Coordenadas iniciais
            x = rx * math.cos(angulo)
            y = ry * math.sin(angulo)

            # Aplicar transformações: escala, cisalhamento, rotação e translação
            x *= self.escala
            y *= self.escala
            
            x += self.cisalhamento * y
            
            x_rot = x * math.cos(self.angulo) - y * math.sin(self.angulo)
            y_rot = x * math.sin(self.angulo) + y * math.cos(self.angulo)
            
            x_final = x_rot + self.centro_x + self.transl_x
            y_final = y_rot + self.centro_y + self.transl_y

            vertices.append((x_final, y_final))

        return vertices

    def atualizar_poligono(self):
        vertices = self.calcular_vertices()
        self.canvas.delete("all")
        
        # Desenhar eixos de referência
        self.canvas.create_line(0, self.centro_y, self.canvas_width, self.centro_y, 
                               fill="gray", dash=(4, 4))
        self.canvas.create_line(self.centro_x, 0, self.centro_x, self.canvas_height, 
                               fill="gray", dash=(4, 4))
        
        # Desenhar o polígono
        for i in range(len(vertices)):
            self.canvas.create_line(vertices[i], vertices[(i + 1) % len(vertices)], 
                                   fill="blue", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    PoligonoApp(root)
    root.mainloop()