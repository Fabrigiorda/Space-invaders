from tokenize import group
from numpy import imag
import pygame
import sys
import os
import time
import json
import random

#Tamaño pantalla
ancho_pantalla = 1000
alto_pantalla = 750

pygame.init()
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Space invaders")
reloj = pygame.time.Clock()

seleccion_menu = 0
fondo = pygame.image.load("imagenes/fondo.png")
fondo2 = pygame.transform.scale(fondo, (1000, 1000))
#Carga de imagenes
logo = pygame.image.load("imagenes/logo.png")
logo_grande = pygame.transform.scale(logo, (500, 448))

nave_img = pygame.image.load("imagenes/nave.png")
nave_img_chica = pygame.transform.scale(nave_img, (70, 94))

alien_verde = pygame.image.load("imagenes/verde.png")
alien_verde_chico = pygame.transform.scale(alien_verde, (75, 75))

alien_amarillo = pygame.image.load("imagenes/amarillo.png")
alien_amarillo_chico = pygame.transform.scale(alien_amarillo, (75, 75))

alien_rojo = pygame.image.load("imagenes/rojo.png")
alien_rojo_chico = pygame.transform.scale(alien_rojo, (75, 75))

alien_azul = pygame.image.load("imagenes/azul.png")
alien_azul_chico = pygame.transform.scale(alien_azul, (75, 75))

bala_img = pygame.image.load("imagenes/bala.png")
bala_alien_img = pygame.image.load("imagenes/bala_alien.png")

corazon_img = pygame.image.load("imagenes/corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (30, 30))

#Colores y fuentes
rojo = (255, 0, 0)
negro = (0, 0, 0)
verde = (0, 255, 0)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)

fuente = pygame.font.Font('PressStart2P-Regular.ttf', 20)
fuente2 = pygame.font.Font('PressStart2P-Regular.ttf', 24)
#defino la clase boton

class boton:
    #Parametros de la clase boton
    def __init__(self, texto, ancho, alto, posicion, color, color_texto):
        self.rectangulo = pygame.Rect(posicion, (ancho, alto))
        self.color_rect = color 
        self.texto_original = texto
        self.color_texto_default = color_texto
        self.color_texto_hover = blanco
        self.texto = fuente.render(self.texto_original, True, self.color_texto_default)
        self.texto_centrado = self.texto.get_rect(center=self.rectangulo.center)
        

    #Actualizar el texto para cuando el mouse pase por el boton
    def actualizar_texto(self, mouseX, mouseY):
            if self.rectangulo.collidepoint(mouseX, mouseY):
                self.texto = fuente2.render(self.texto_original, True, self.color_texto_hover)
            else:
                self.texto = fuente.render(self.texto_original, True, self.color_texto_default)
            self.texto_centrado = self.texto.get_rect(center=self.rectangulo.center)
            

    #Dibujar el boton
    def dibujar_boton(self, mouseX, mouseY):
        self.actualizar_texto(mouseX, mouseY)
        pygame.draw.rect(pantalla, self.color_rect, self.rectangulo, border_radius=12)
        pantalla.blit(self.texto, self.texto_centrado)
        
        

    
#Defino cada boton del juego y que caracteristicas quiero de estos
boton1 = boton("Jugar", 200, 60, ((ancho_pantalla-200)/2, 450), negro, amarillo)
boton2 = boton("Multijugador", 200, 60, ((ancho_pantalla-200)/2, 550), negro, amarillo)
boton3 = boton("Ranking", 200, 60, ((ancho_pantalla-200)/2, 650), negro, amarillo)
boton4 = boton("Opciones", 200, 60, ((ancho_pantalla-200)/2, 750), negro, amarillo)
boton5 = boton("Salir", 200, 60, ((ancho_pantalla-200)/2, 850), negro, amarillo)
boton6 = boton("Nave", 150, 50, (30, 30), negro, amarillo)

#Defino la clase nave
class nave:
    #Pongo los parametros de la nave
    def __init__(self, imagen, ancho, alto, velocidad, disparo):
        self.nave_imagen = imagen
        self.nave_velocidad_x = 0
        self.velocidad = velocidad
        self.disparo = disparo
        self.cuadrado = pygame.Rect(ancho - imagen.get_width()//2, alto - imagen.get_height()//2 - 10, imagen.get_width(), imagen.get_height())
        self.vidas = 3

    #funcion para poder mover la nave
    def actualizar(self):
        self.nave_velocidad_x = 0 
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_a]:
            self.nave_velocidad_x = -self.velocidad
        elif tecla[pygame.K_d]:
            self.nave_velocidad_x = self.velocidad
        self.cuadrado.x += self.nave_velocidad_x

        if self.cuadrado.left < 0:
            self.cuadrado.left = 0
        if self.cuadrado.right > ancho_pantalla:
            self.cuadrado.right = ancho_pantalla
        
    def dibujar_vidas(self):
        texto_vidas = fuente.render("Vidas:", True, blanco)
        pantalla.blit(texto_vidas, (20, alto_pantalla - 40))
        for i in range(self.vidas):
            pantalla.blit(corazon_img, (120 + i * 40, alto_pantalla - 40))


#defino la clase de disparo de la nave
class disparo:
    def __init__(self, x, y, velocidad, es_alien=False):
        self.imagen = bala_alien_img if es_alien else bala_img
        self.velocidad = velocidad
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y if not es_alien else y
        self.activo = True
        self.es_alien = es_alien

    def actualizar(self):
        if self.es_alien:
            self.rect.y += self.velocidad  # Balas de aliens van hacia abajo
        else:
            self.rect.y -= self.velocidad  # Balas del jugador van hacia arriba
            
        if self.rect.bottom < 0 or self.rect.top > alto_pantalla:
            self.activo = False

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


#Defino la clase de el alien
class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, velocidad, velocidad_x, vidas, tipo, velocidad_disparo):
        super().__init__()
        imagen_path = "imagenes/" + color + ".png"
        self.imagen = pygame.image.load(imagen_path).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (65, 65))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = velocidad
        self.velocidad_x = velocidad_x
        self.vidas = vidas
        self.tipo = tipo
        self.shooting_speed = velocidad_disparo
        self.max_speed = 10 if tipo == "rojo" else 8 if tipo == "azul" else 5
        self.columna = 0  # Se asignará después

    def mover(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0 or self.rect.right > ancho_pantalla:
            self.velocidad_x = -self.velocidad_x
            self.rect.y += 20


def crear_aliens(nivel):
    aliens = []
    filas = 5
    columnas = 8
    distancia_x = 100
    distancia_y = 70
    
    # Configuración base para todos los aliens
    tipo = "verde"  # tipo por defecto
    velocidad_base = 2  # velocidad base
    velocidad_disparo = 1000  # velocidad de disparo base (más alto = más lento)
    vidas = 1  # vidas por defecto
    
    # Configuración específica para cada nivel
    if nivel == 1:
        # Todos verdes normales
        tipo = "verde"
        velocidad_base = 2
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 2:
        # Todos verdes un poco más rápidos
        tipo = "verde"
        velocidad_base = 3
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 3:
        # Todos amarillos
        tipo = "amarillo"
        velocidad_base = 2
        velocidad_disparo = 800  # Disparan más rápido
        vidas = 1
    elif nivel == 4:
        # Todos amarillos un poco más rápido
        tipo = "amarillo"
        velocidad_base = 3
        velocidad_disparo = 800
        vidas = 1
    elif nivel == 5:
        # Todos rojos
        tipo = "rojo"
        velocidad_base = 4  # Se mueven más rápido
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 6:
        # Todos verdes con 2 vidas
        tipo = "verde"
        velocidad_base = 2  # Velocidad del nivel 1
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 7:
        # Todos verdes con 2 vidas y velocidad del nivel 2
        tipo = "verde"
        velocidad_base = 3
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 8:
        # Todos amarillos con velocidad del nivel 3 y 2 vidas
        tipo = "amarillo"
        velocidad_base = 2
        velocidad_disparo = 800
        vidas = 2
    elif nivel == 9:
        # Todos amarillos con 2 vidas y velocidad del nivel 4
        tipo = "amarillo"
        velocidad_base = 3
        velocidad_disparo = 800
        vidas = 2
    elif nivel == 10:
        # Todos rojos con velocidad un poco más alta y 2 vidas
        tipo = "rojo"
        velocidad_base = 5
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 11:
        # Todos rojos con la misma velocidad que nivel 5 pero 3 vidas
        tipo = "rojo"
        velocidad_base = 4
        velocidad_disparo = 1000
        vidas = 3
    elif nivel >= 12:
        # Todos azules que van aumentando velocidad o disparo en niveles alternos
        tipo = "azul"
        # Base de velocidad y disparo como nivel 1 verde
        velocidad_base = 2 + (nivel - 12) // 2  # Aumenta cada 2 niveles
        velocidad_disparo = 1000 - ((nivel - 12) % 2) * 50  # Alterna entre 1000 y 950, luego 900, etc.
        # Evitar que la velocidad o disparos sean excesivos
        velocidad_base = min(velocidad_base, 8)  # Máximo de velocidad
        velocidad_disparo = max(velocidad_disparo, 400)  # Mínimo tiempo entre disparos
        vidas = 2

    # Organizar aliens en filas y columnas
    aliens_por_columna = {}  # Para rastrear qué aliens están en cada columna
    
    for fila in range(filas):
        for columna in range(columnas):
            x = 100 + columna * distancia_x
            y = 50 + fila * distancia_y
            velocidad_x = velocidad_base
            
            # Ajuste para los aliens rojos (más rápidos)
            if tipo == "rojo":
                velocidad_x += 1
            
            nuevo_alien = Alien(tipo, x, y, velocidad_base, velocidad_x, vidas, tipo, velocidad_disparo)
            nuevo_alien.columna = columna
            aliens.append(nuevo_alien)
            
            # Registrar este alien en su columna
            if columna not in aliens_por_columna:
                aliens_por_columna[columna] = []
            aliens_por_columna[columna].append(nuevo_alien)
    
    return aliens


ancho_logo = logo_grande.get_width()

def menu(mouseX, mouseY):
    pantalla.fill(negro)
    pantalla.blit(logo_grande, ((ancho_pantalla - ancho_logo)/2, 10))
    boton1.dibujar_boton(mouseX, mouseY)
    boton2.dibujar_boton(mouseX, mouseY)
    boton3.dibujar_boton(mouseX, mouseY)
    boton4.dibujar_boton(mouseX, mouseY)
    boton5.dibujar_boton(mouseX, mouseY)
    boton6.dibujar_boton(mouseX, mouseY)



def obtener_aliens_mas_bajos(aliens):
    # Diccionario para rastrear el alien más bajo de cada columna
    aliens_mas_bajos = {}
    
    for alien in aliens:
        columna = alien.columna
        if columna not in aliens_mas_bajos or alien.rect.y > aliens_mas_bajos[columna].rect.y:
            aliens_mas_bajos[columna] = alien
    
    return list(aliens_mas_bajos.values())


nivel = 1

def jugar_solo():
    global nivel
    jugador = nave(nave_img_chica, ancho_pantalla // 2, alto_pantalla - 40, 7, True)
    puntuacion = 0
    
    juego_activo = True
    
    balas = []
    balas_aliens = []
    puede_disparar = True
    ultimo_disparo = 0
    tiempo_entre_disparos = 0 #antes 400
    ultimo_disparo_alien = 0
    tiempo_entre_disparos_alien = 1000  # Base para disparos aliens
    
    aliens = crear_aliens(nivel)
    
    # Para el parpadeo cuando la nave es golpeada
    invulnerable = False
    tiempo_invulnerable = 0
    duracion_invulnerable = 2000  # 2 segundos de invulnerabilidad
    parpadeo = False
    ultimo_parpadeo = 0
    intervalo_parpadeo = 200  # 200ms entre parpadeos

    while juego_activo:
        tiempo_actual = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    juego_activo = False
                elif event.key == pygame.K_SPACE and puede_disparar and tiempo_actual - ultimo_disparo > tiempo_entre_disparos:
                    nueva_bala = disparo(jugador.cuadrado.centerx, jugador.cuadrado.top, 10)
                    balas.append(nueva_bala)
                    ultimo_disparo = tiempo_actual
                    
        pantalla.blit(fondo2, (0, 0))
        
        jugador.actualizar()
        
        # Control de invulnerabilidad y parpadeo
        if invulnerable:
            if tiempo_actual - tiempo_invulnerable > duracion_invulnerable:
                invulnerable = False
            
            # Efecto de parpadeo
            if tiempo_actual - ultimo_parpadeo > intervalo_parpadeo:
                parpadeo = not parpadeo
                ultimo_parpadeo = tiempo_actual
            
            if not parpadeo:
                pantalla.blit(nave_img_chica, jugador.cuadrado)
        else:
            pantalla.blit(nave_img_chica, jugador.cuadrado)
        
        # Movimiento de aliens
        for alien in aliens[:]:
            alien.mover()
            pantalla.blit(alien.imagen, alien.rect)

            # Colisión con balas del jugador
            for bala in balas[:]:
                if alien.rect.colliderect(bala.rect):
                    alien.vidas -= 1
                    if alien.vidas <= 0:
                        aliens.remove(alien)
                        # Puntuación según el tipo de alien
                        if alien.tipo == "verde":
                            puntuacion += 10
                        elif alien.tipo == "amarillo":
                            puntuacion += 20
                        elif alien.tipo == "rojo":
                            puntuacion += 30
                        elif alien.tipo == "azul":
                            puntuacion += 40
                    balas.remove(bala)
                    break
        
        # Obtener aliens más bajos para disparar
        aliens_disparadores = obtener_aliens_mas_bajos(aliens)
        
        # Sistema de disparo aleatorio para aliens
        if tiempo_actual - ultimo_disparo_alien > tiempo_entre_disparos_alien and aliens_disparadores:
            # Elegir un alien aleatorio de los que están más abajo para disparar
            alien_disparador = random.choice(aliens_disparadores)
            
            # Ajustar la velocidad de disparo según el tipo de alien
            velocidad_bala = 5
            if alien_disparador.tipo == "amarillo":
                velocidad_bala = 6  # Amarillos disparan más rápido
            
            nueva_bala_alien = disparo(alien_disparador.rect.centerx, alien_disparador.rect.bottom, velocidad_bala, True)
            balas_aliens.append(nueva_bala_alien)
            ultimo_disparo_alien = tiempo_actual
        
        # Actualizar balas del jugador
        for bala in balas[:]:
            bala.actualizar()
            if bala.activo:
                bala.dibujar(pantalla)
            else:
                balas.remove(bala)
        
        # Actualizar balas de aliens
        for bala_alien in balas_aliens[:]:
            bala_alien.actualizar()
            if bala_alien.activo:
                bala_alien.dibujar(pantalla)
                # Revisar si golpea al jugador
                if not invulnerable and bala_alien.rect.colliderect(jugador.cuadrado):
                    jugador.vidas -= 1
                    balas_aliens.remove(bala_alien)
                    
                    # Activar invulnerabilidad
                    invulnerable = True
                    tiempo_invulnerable = tiempo_actual
                    
                    # Si no quedan vidas, terminar el juego
                    if jugador.vidas <= 0:
                        juego_activo = False
            else:
                balas_aliens.remove(bala_alien)
        
        # Si no quedan aliens, pasar al siguiente nivel
        if not aliens:
            nivel += 1
            aliens = crear_aliens(nivel)
            # Reset de balas
            balas = []
            balas_aliens = []
        
        # Información de juego
        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, blanco)
        texto_nivel = fuente.render(f"Oleada: {nivel}", True, blanco)
        
        # Mostrar el tipo de alien de la oleada actual
        tipo_alien = ""
        if nivel <= 2 or nivel == 6 or nivel == 7:
            tipo_alien = "Verdes"
        elif nivel == 3 or nivel == 4 or nivel == 8 or nivel == 9:
            tipo_alien = "Amarillos"
        elif nivel == 5 or nivel == 10 or nivel == 11:
            tipo_alien = "Rojos"
        elif nivel >= 12:
            tipo_alien = "Azules"
            
        texto_tipo = fuente.render(f"Aliens: {tipo_alien}", True, blanco)
        
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_nivel, (ancho_pantalla - 200, 20))
        pantalla.blit(texto_tipo, (ancho_pantalla // 2 - 100, 20))
        
        # Dibujar vidas
        jugador.dibujar_vidas()
        
        pygame.display.update()
        reloj.tick(60)


def multijugador():
    pass

def ranking():
    pass

def opciones():
    pass

def personalizar():
    global nave_img_chica
    naves = [f for f in os.listdir("imagenes") if f.startswith("nave") and f.endswith(".png")]
    naves.sort()  # Ensure consistent order
    indice_actual = 0

    if not os.path.exists("borradas"):
        os.makedirs("borradas")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                # Flecha izquierda
                if boton_izquierda.rectangulo.collidepoint(mouseX, mouseY):
                    indice_actual = (indice_actual - 1) % len(naves)
                # Flecha derecha
                elif boton_derecha.rectangulo.collidepoint(mouseX, mouseY):
                    indice_actual = (indice_actual + 1) % len(naves)
                # Botón seleccionar
                elif boton_seleccionar.rectangulo.collidepoint(mouseX, mouseY):
                    nave_img_chica = pygame.image.load(f"imagenes/{naves[indice_actual]}")
                    nave_img_chica = pygame.transform.scale(nave_img_chica, (70, 94))
                    return
                # Botón eliminar
                elif boton_eliminar.rectangulo.collidepoint(mouseX, mouseY):
                    if naves[indice_actual] != "nave.png":
                        os.remove(f"imagenes/{naves[indice_actual]}")
                        naves.pop(indice_actual)
                        if not naves:
                            return
                        indice_actual %= len(naves)

        pantalla.fill(negro)
        pantalla.blit(fondo2, (0, 0))

        # Mostrar nave actual
        nave_actual = pygame.image.load(f"imagenes/{naves[indice_actual]}")
        nave_actual = pygame.transform.scale(nave_actual, (150, 200))
        pantalla.blit(nave_actual, ((ancho_pantalla - 150) // 2, (alto_pantalla - 200) // 2))

        # Dibujar botones
        boton_izquierda.dibujar_boton(*pygame.mouse.get_pos())
        boton_derecha.dibujar_boton(*pygame.mouse.get_pos())
        boton_seleccionar.dibujar_boton(*pygame.mouse.get_pos())
        boton_eliminar.dibujar_boton(*pygame.mouse.get_pos())

        pygame.display.update()
        reloj.tick(60)

# Crear botones para personalizar
boton_izquierda = boton("<", 50, 50, (ancho_pantalla // 2 - 150, alto_pantalla // 2), negro, amarillo)
boton_derecha = boton(">", 50, 50, (ancho_pantalla // 2 + 100, alto_pantalla // 2), negro, amarillo)
boton_seleccionar = boton("Seleccionar", 200, 50, ((ancho_pantalla - 200) // 2, alto_pantalla // 2 + 250), negro, amarillo)
boton_eliminar = boton("Eliminar", 150, 50, (ancho_pantalla - 200, 20), negro, rojo)


while True:
    for evento in pygame.event.get():   
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouseX, mouseY = pygame.mouse.get_pos()
    menu(mouseX, mouseY)
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if boton1.rectangulo.collidepoint(mouseX, mouseY):
            jugar_solo()
        elif boton2.rectangulo.collidepoint(mouseX, mouseY):
            multijugador()
        elif boton3.rectangulo.collidepoint(mouseX, mouseY):
            ranking()
        elif boton4.rectangulo.collidepoint(mouseX, mouseY):
            opciones()
        elif boton5.rectangulo.collidepoint(mouseX, mouseY):
            pygame.quit()
            sys.exit()
        elif boton6.rectangulo.collidepoint(mouseX, mouseY):
            personalizar()
    pygame.display.update()
    reloj.tick(60)