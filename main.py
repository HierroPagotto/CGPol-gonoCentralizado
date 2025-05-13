import tkinter as tk
import math
from tkinter import ttk

class PoligonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho NP2 - Polígono")
        self.root.geometry("800x600")
        
        # Tamanho do canvas
        self.canvas_width = 500
        self.canvas_height = 400
        
        # Parâmetros do polígono
        self.num_lados = 5
        self.raio = 100
        self.centro_x = self.canvas_width // 2
        self.centro_y = self.canvas_height // 2
        
        # Configuração da interface
        self.criar_interface()
        
        # Desenhar o polígono inicial
        self.atualizar_poligono()
        
    def criar_interface(self):
        # Frame principal dividido em área de desenho e controles
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de desenho
        canvas_frame = ttk.LabelFrame(main_frame, text="Área de Desenho", padding=10)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles
        controls_frame = ttk.LabelFrame(main_frame, text="Controles", padding=10, width=200)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Controle do número de lados
        lados_frame = ttk.LabelFrame(controls_frame, text="Número de Lados", padding=5)
        lados_frame.pack(fill=tk.X, pady=5)
        
        self.lados_var = tk.IntVar(value=5)
        lados_scale = ttk.Scale(lados_frame, from_=3, to=50, orient=tk.HORIZONTAL, variable=self.lados_var, command=self.mudar_lados)
        lados_scale.pack(fill=tk.X)
        
        self.lados_label = ttk.Label(lados_frame, text=f"Lados: {self.lados_var.get()}")
        self.lados_label.pack()
        
        # Controle de raio
        raio_frame = ttk.LabelFrame(controls_frame, text="Raio", padding=5)
        raio_frame.pack(fill=tk.X, pady=5)
        
        self.raio_var = tk.IntVar(value=100)
        raio_scale = ttk.Scale(raio_frame, from_=10, to=150, orient=tk.HORIZONTAL, variable=self.raio_var, command=self.mudar_raio)
        raio_scale.pack(fill=tk.X)
        
        self.raio_label = ttk.Label(raio_frame, text=f"Raio: {self.raio_var.get()}")
        self.raio_label.pack()
    
    def calcular_vertices(self):
        vertices = []
        for i in range(self.num_lados):
            # Ângulo para cada vértice
            angulo = 2 * math.pi * i / self.num_lados
            x = self.raio * math.cos(angulo)
            y = self.raio * math.sin(angulo)
            vertices.append((x + self.centro_x, y + self.centro_y))
        
        return vertices
    
    def desenhar_poligono(self, vertices):
        # Limpar canvas
        self.canvas.delete("all")
        
        # Desenhar eixos
        self.canvas.create_line(0, self.centro_y, self.canvas_width, self.centro_y, fill="lightgray", dash=(4, 4))
        self.canvas.create_line(self.centro_x, 0, self.centro_x, self.canvas_height, fill="lightgray", dash=(4, 4))
        
        # Desenhar o polígono usando linhas
        if len(vertices) >= 3:  # Precisa de pelo menos 3 pontos para formar uma figura
            for i in range(len(vertices)):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % len(vertices)]  # próximo vértice (ou o primeiro, se for o último vértice)
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

    def atualizar_poligono(self):
        vertices = self.calcular_vertices()
        self.desenhar_poligono(vertices)
    
    def mudar_lados(self, valor):
        self.num_lados = int(float(valor))
        self.lados_label.config(text=f"Lados: {self.num_lados}")
        self.atualizar_poligono()
    
    def mudar_raio(self, valor):
        self.raio = int(float(valor))
        self.raio_label.config(text=f"Raio: {self.raio}")
        self.atualizar_poligono()

# Função principal
def main():
    root = tk.Tk()
    app = PoligonoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()