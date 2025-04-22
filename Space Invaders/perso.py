import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 1000, 700
GRIS_CLARO = (220, 220, 220)
GRIS = (180, 180, 180)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Tamaño de la cuadrícula
CELDA = 40
MARGEN = 1

# Colores para las piezas
COLORES = {
    "rojo": (255, 0, 0),
    "naranja": (255, 165, 0),
    "amarillo": (255, 255, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "azul_claro": (0, 191, 255),
    "morado": (128, 0, 128),
    "blanco": (255, 255, 255),
    "gris": (128, 128, 128),
    "negro": (30, 30, 30),
    "marron": (165, 42, 42)
}

class Pieza:
    def __init__(self, color, tipo="bloque"):
        self.color = color
        self.tipo = tipo  # "bloque" o "cañon"
    
    def dibujar(self, superficie, x, y, tamaño):
        if self.tipo == "bloque":
            pygame.draw.rect(superficie, COLORES[self.color], (x + MARGEN, y + MARGEN, tamaño - 2*MARGEN, tamaño - 2*MARGEN))
            pygame.draw.rect(superficie, NEGRO, (x + MARGEN, y + MARGEN, tamaño - 2*MARGEN, tamaño - 2*MARGEN), 2)
        elif self.tipo == "cañon":
            pygame.draw.rect(superficie, COLORES[self.color], (x + MARGEN + 5, y + MARGEN, tamaño - 2*MARGEN - 10, tamaño - 2*MARGEN))
            pygame.draw.rect(superficie, NEGRO, (x + MARGEN + 5, y + MARGEN, tamaño - 2*MARGEN - 10, tamaño - 2*MARGEN), 2)

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Constructor de Naves")
        
        # Configuración del área de construcción
        self.ancho_barra_lateral = 200
        self.ancho_area_construccion = ANCHO - self.ancho_barra_lateral
        
        # Número de celdas en la cuadrícula
        self.filas = (ALTO - 120) // CELDA
        self.columnas = (self.ancho_area_construccion - 40) // CELDA
        
        # Matriz para almacenar las piezas colocadas
        self.cuadricula = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Pieza seleccionada actualmente
        self.pieza_seleccionada = None
        
        # Catálogo de piezas disponibles
        self.catalogo_piezas = self.crear_catalogo()
        
        # Contador de cañones colocados
        self.canones_colocados = 0
        
        # Fuente para textos
        self.fuente = pygame.font.SysFont("Arial", 24)
        
    def crear_catalogo(self):
        # Bloques en diferentes colores
        bloques = [
            Pieza("rojo"), Pieza("naranja"), Pieza("amarillo"),
            Pieza("verde"), Pieza("azul"), Pieza("azul_claro"),
            Pieza("morado"), Pieza("blanco"), Pieza("gris"),
            Pieza("negro"), Pieza("azul_claro"), Pieza("marron")
        ]
        
        # Cañones en diferentes colores
        canones = [
            Pieza("rojo", "cañon"), Pieza("naranja", "cañon"), Pieza("amarillo", "cañon"),
            Pieza("verde", "cañon"), Pieza("azul", "cañon"), Pieza("azul_claro", "cañon"),
            Pieza("morado", "cañon"), Pieza("blanco", "cañon"), Pieza("marron", "cañon")
        ]
        
        return {"bloques": bloques, "canones": canones}
    
    def dibujar_barra_lateral(self):
        # Fondo de la barra lateral
        pygame.draw.rect(self.pantalla, GRIS, (0, 0, self.ancho_barra_lateral, ALTO))
        
        # Título "Piezas"
        texto_piezas = self.fuente.render("Piezas", True, NEGRO)
        self.pantalla.blit(texto_piezas, (50, 20))
        
        # Dibujar bloques disponibles
        filas_bloques = 4
        columnas_bloques = 3
        for i in range(filas_bloques):
            for j in range(columnas_bloques):
                indice = i * columnas_bloques + j
                if indice < len(self.catalogo_piezas["bloques"]):
                    x = j * (CELDA + 10) + 30
                    y = i * (CELDA + 10) + 60
                    self.catalogo_piezas["bloques"][indice].dibujar(self.pantalla, x, y, CELDA)
        
        # Título "Cañones"
        texto_canones = self.fuente.render("Cañones", True, NEGRO)
        self.pantalla.blit(texto_canones, (50, 250))
        
        # Dibujar cañones disponibles
        filas_canones = 3
        columnas_canones = 3
        for i in range(filas_canones):
            for j in range(columnas_canones):
                indice = i * columnas_canones + j
                if indice < len(self.catalogo_piezas["canones"]):
                    x = j * (CELDA + 10) + 30
                    y = i * (CELDA + 10) + 290
                    self.catalogo_piezas["canones"][indice].dibujar(self.pantalla, x, y, CELDA)
    
    def dibujar_area_construccion(self):
        # Fondo del área de construcción
        pygame.draw.rect(self.pantalla, BLANCO, (self.ancho_barra_lateral, 0, self.ancho_area_construccion, ALTO))
        
        # Dibujar la cuadrícula
        for fila in range(self.filas):
            for columna in range(self.columnas):
                x = columna * CELDA + self.ancho_barra_lateral + 20
                y = fila * CELDA + 20
                pygame.draw.rect(self.pantalla, GRIS_CLARO, (x, y, CELDA, CELDA), 1)
                
                # Dibujar pieza si existe en esa posición
                if self.cuadricula[fila][columna]:
                    self.cuadricula[fila][columna].dibujar(self.pantalla, x, y, CELDA)
        
        # Botón Finalizar
        boton_x = self.ancho_barra_lateral + (self.ancho_area_construccion - 300) // 2
        boton_y = ALTO - 100
        pygame.draw.rect(self.pantalla, ROJO, (boton_x, boton_y, 300, 70))
        texto_finalizar = self.fuente.render("FINALIZAR", True, BLANCO)
        self.pantalla.blit(texto_finalizar, (boton_x + 100, boton_y + 20))
    
    def obtener_celda_desde_coordenadas(self, pos_x, pos_y):
        # Verificar si está en el área de construcción
        if pos_x > self.ancho_barra_lateral + 20 and pos_x < ANCHO - 20:
            if pos_y > 20 and pos_y < 20 + self.filas * CELDA:
                columna = (pos_x - self.ancho_barra_lateral - 20) // CELDA
                fila = (pos_y - 20) // CELDA
                if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                    return (fila, columna)
        return None
    
    def obtener_pieza_seleccionada(self, pos_x, pos_y):
        # Verificar si hizo clic en un bloque
        filas_bloques = 4
        columnas_bloques = 3
        for i in range(filas_bloques):
            for j in range(columnas_bloques):
                indice = i * columnas_bloques + j
                if indice < len(self.catalogo_piezas["bloques"]):
                    x = j * (CELDA + 10) + 30
                    y = i * (CELDA + 10) + 60
                    if x <= pos_x <= x + CELDA and y <= pos_y <= y + CELDA:
                        return Pieza(list(COLORES.keys())[indice % len(COLORES)], "bloque")
        
        # Verificar si hizo clic en un cañón
        filas_canones = 3
        columnas_canones = 3
        for i in range(filas_canones):
            for j in range(columnas_canones):
                indice = i * columnas_canones + j
                if indice < len(self.catalogo_piezas["canones"]):
                    x = j * (CELDA + 10) + 30
                    y = i * (CELDA + 10) + 290
                    if x <= pos_x <= x + CELDA and y <= pos_y <= y + CELDA:
                        return Pieza(list(COLORES.keys())[indice % len(COLORES)], "cañon")
        
        return None
    
    def verificar_boton_finalizar(self, pos_x, pos_y):
        boton_x = self.ancho_barra_lateral + (self.ancho_area_construccion - 300) // 2
        boton_y = ALTO - 100
        if boton_x <= pos_x <= boton_x + 300 and boton_y <= pos_y <= boton_y + 70:
            return True
        return False
    
    def guardar_nave(self):
        # Determinar los límites del dibujo
        min_fila, max_fila, min_columna, max_columna = self.filas, 0, self.columnas, 0
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.cuadricula[fila][columna]:
                    min_fila = min(min_fila, fila)
                    max_fila = max(max_fila, fila)
                    min_columna = min(min_columna, columna)
                    max_columna = max(max_columna, columna)
        
        # Si no hay piezas colocadas, no guardar nada
        if min_fila > max_fila or min_columna > max_columna:
            print("No hay piezas para guardar.")
            return
        
        # Calcular el tamaño del dibujo
        ancho_dibujo = (max_columna - min_columna + 1) * CELDA
        alto_dibujo = (max_fila - min_fila + 1) * CELDA
        
        # Crear una superficie para el dibujo
        superficie_nave = pygame.Surface((ancho_dibujo, alto_dibujo), pygame.SRCALPHA)
        superficie_nave.fill((0, 0, 0, 0))  # Transparente
        
        # Dibujar las piezas en la superficie
        for fila in range(min_fila, max_fila + 1):
            for columna in range(min_columna, max_columna + 1):
                if self.cuadricula[fila][columna]:
                    x = (columna - min_columna) * CELDA
                    y = (fila - min_fila) * CELDA
                    self.cuadricula[fila][columna].dibujar(superficie_nave, x, y, CELDA)
        
        # Buscar el siguiente nombre disponible
        if not os.path.exists("imagenes"):
            os.makedirs("imagenes")
        indice = 1
        while os.path.exists(f"imagenes/nave{indice}.png"):
            indice += 1
        nombre_archivo = f"imagenes/nave{indice}.png"
        
        # Guardar la imagen
        pygame.image.save(superficie_nave, nombre_archivo)
        print(f"Nave guardada como '{nombre_archivo}'")
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    
                    # Verificar si hizo clic en la barra lateral
                    if pos_x < self.ancho_barra_lateral:
                        self.pieza_seleccionada = self.obtener_pieza_seleccionada(pos_x, pos_y)
                    
                    # Verificar si hizo clic en el área de construcción
                    elif self.pieza_seleccionada:
                        celda = self.obtener_celda_desde_coordenadas(pos_x, pos_y)
                        if celda:
                            fila, columna = celda
                            
                            # Si es un cañón y ya hay uno colocado, no permitir colocar otro
                            if self.pieza_seleccionada.tipo == "cañon" and self.canones_colocados >= 1:
                                # Reemplazar el cañón existente
                                for f in range(self.filas):
                                    for c in range(self.columnas):
                                        if self.cuadricula[f][c] and self.cuadricula[f][c].tipo == "cañon":
                                            self.cuadricula[f][c] = None
                                            self.canones_colocados -= 1
                            
                            # Colocar la pieza
                            self.cuadricula[fila][columna] = Pieza(self.pieza_seleccionada.color, self.pieza_seleccionada.tipo)
                            
                            # Actualizar contador de cañones
                            if self.pieza_seleccionada.tipo == "cañon":
                                self.canones_colocados += 1
                    
                    # Verificar si hizo clic en el botón finalizar
                    if self.verificar_boton_finalizar(pos_x, pos_y):
                        if self.canones_colocados >= 1:
                            self.guardar_nave()
                        else:
                            print("Debes colocar al menos un cañón para finalizar.")
            
            # Limpiar pantalla
            self.pantalla.fill(BLANCO)
            
            # Dibujar elementos
            self.dibujar_barra_lateral()
            self.dibujar_area_construccion()
            
            # Actualizar pantalla
            pygame.display.flip()
            reloj.tick(30)

# Iniciar juego
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()