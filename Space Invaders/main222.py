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
alto_pantalla = 1000

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

# Load gadget images
gadget_images = [
    pygame.image.load("imagenes/gadget1.png"),  # Freeze
    pygame.image.load("imagenes/gadget2.png"),  # Bomb Bullet
    pygame.image.load("imagenes/gadget3.png"),  # Machine Gun
    pygame.image.load("imagenes/gadget4.png"),  # Piercing Bullets
]

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
        self.piercing = False

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
        self.cambiar_direccion = False  # Flag to indicate direction change

    def mover(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0 or self.rect.right > ancho_pantalla:
            self.cambiar_direccion = True  # Set flag to change direction
            self.rect.y += 10  # Move down less when touching the wall


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
        vidas = 1

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

class Shield:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.hits = 0
        self.max_hits = 7

    def dibujar(self):
        if self.hits < self.max_hits:
            pygame.draw.rect(pantalla, verde, self.rect)

    def recibir_dano(self):
        self.hits += 1
        if self.hits >= self.max_hits:
            return True
        return False

class Gadget:
    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x, y, 25, 25)  # Adjusted size to 25x25
        self.tipo = tipo
        self.imagen = pygame.transform.scale(gadget_images[tipo], (25, 25))  # Scale image to match size
        self.velocidad = 2  # Gadgets fall slower than bullets

    def actualizar(self):
        self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.imagen, self.rect)

class Heart:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.imagen = corazon_img
        self.velocidad = 2

    def actualizar(self):
        self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.imagen, self.rect)

def dibujar_columna_gadgets(gadgets_inventario):
    """Draw the gadget column on the right side of the screen."""
    columna_x = ancho_pantalla - 60
    columna_y = 20
    espacio_entre_gadgets = 50

    for i, gadget in enumerate(gadgets_inventario):
        pantalla.blit(gadget.imagen, (columna_x, columna_y + i * espacio_entre_gadgets))

def seleccionar_gadget(gadgets_inventario):
    """Pause the game and allow the player to select a gadget."""
    seleccion_activa = True
    while seleccion_activa:
        pantalla.fill(negro)
        texto_titulo = fuente.render("Seleccionar Gadget", True, blanco)
        pantalla.blit(texto_titulo, ((ancho_pantalla - texto_titulo.get_width()) // 2, 20))

        # Draw gadgets in the center of the screen
        for i, gadget in enumerate(gadgets_inventario):
            x = (ancho_pantalla - 50) // 2
            y = 100 + i * 70
            pantalla.blit(gadget.imagen, (x, y))
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pygame.Rect(x, y, 50, 50).collidepoint(mouse_x, mouse_y):
                    seleccion_activa = False
                    return gadget.tipo  # Return the selected gadget type

        # Draw a close button
        boton_cerrar = pygame.Rect(20, 20, 50, 50)
        pygame.draw.rect(pantalla, rojo, boton_cerrar)
        texto_cerrar = fuente.render("X", True, blanco)
        pantalla.blit(texto_cerrar, (35, 25))
        if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if boton_cerrar.collidepoint(mouse_x, mouse_y):
                seleccion_activa = False
                return None  # No gadget selected

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        reloj.tick(60)

def jugar_solo():
    global nivel
    nivel = 1  # Reset level
    puntuacion = 0  # Reset score
    jugador = nave(nave_img_chica, ancho_pantalla // 2, alto_pantalla - 40, 7, True)
    juego_activo = True
    balas = []
    balas_aliens = []
    gadgets = []
    corazones = []
    gadgets_inventario = []  # Collected gadgets
    puede_disparar = True
    ultimo_disparo = 0
    tiempo_entre_disparos = 400
    ultimo_disparo_alien = 0
    tiempo_entre_disparos_alien = 1000
    aliens = crear_aliens(nivel)

    # Gadget effects
    freeze_timer = 0
    machine_gun_timer = 0
    piercing_bullets = False

    # Create shields
    shields = [
        Shield(150, alto_pantalla - 200),
        Shield(350, alto_pantalla - 200),
        Shield(550, alto_pantalla - 200),
        Shield(750, alto_pantalla - 200),
    ]

    # For blinking effect when the ship is hit
    invulnerable = False
    tiempo_invulnerable = 0
    duracion_invulnerable = 2000  # 2 seconds of invulnerability
    parpadeo = False
    ultimo_parpadeo = 0
    intervalo_parpadeo = 200  # 200ms between blinks

    while juego_activo:
        tiempo_actual = pygame.time.get_ticks()

        # Handle timers for gadgets
        if freeze_timer > 0 and tiempo_actual - freeze_timer > 5000:
            freeze_timer = 0
        if machine_gun_timer > 0 and tiempo_actual - machine_gun_timer > 7000:
            machine_gun_timer = 0
            tiempo_entre_disparos = 400
        if piercing_bullets and tiempo_actual - machine_gun_timer > 7000:
            piercing_bullets = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    juego_activo = False
                elif event.key == pygame.K_SPACE and puede_disparar and tiempo_actual - ultimo_disparo > tiempo_entre_disparos:
                    nueva_bala = disparo(jugador.cuadrado.centerx, jugador.cuadrado.top, 10)
                    nueva_bala.piercing = piercing_bullets
                    balas.append(nueva_bala)
                    ultimo_disparo = tiempo_actual
                elif event.key == pygame.K_RETURN and gadgets_inventario:
                    gadget_tipo = seleccionar_gadget(gadgets_inventario)
                    if gadget_tipo is not None:
                        gadgets_inventario = [g for g in gadgets_inventario if g.tipo != gadget_tipo]  # Remove used gadget
                        if gadget_tipo == 0:  # Freeze
                            freeze_timer = tiempo_actual
                        elif gadget_tipo == 1:  # Bomb Bullet
                            pass  # Implement bomb bullet logic
                        elif gadget_tipo == 2:  # Machine Gun
                            machine_gun_timer = tiempo_actual
                            tiempo_entre_disparos = 50
                        elif gadget_tipo == 3:  # Piercing Bullets
                            piercing_bullets = True
                            machine_gun_timer = tiempo_actual

        pantalla.blit(fondo2, (0, 0))
        jugador.actualizar()

        # Handle invulnerability and blinking
        if invulnerable:
            if tiempo_actual - tiempo_invulnerable > duracion_invulnerable:
                invulnerable = False

            # Blinking effect
            if tiempo_actual - ultimo_parpadeo > intervalo_parpadeo:
                parpadeo = not parpadeo
                ultimo_parpadeo = tiempo_actual

            if not parpadeo:
                pantalla.blit(nave_img_chica, jugador.cuadrado)
        else:
            pantalla.blit(nave_img_chica, jugador.cuadrado)

        # Draw and update shields
        for shield in shields[:]:
            shield.dibujar()
            for bala_alien in balas_aliens[:]:
                if shield.rect.colliderect(bala_alien.rect):
                    if shield.recibir_dano():
                        shields.remove(shield)
                    balas_aliens.remove(bala_alien)

        # Move and draw aliens
        cambiar_direccion_global = False
        for alien in aliens[:]:
            if freeze_timer == 0:  # Freeze effect
                alien.mover()
                if alien.cambiar_direccion:
                    cambiar_direccion_global = True
                    alien.cambiar_direccion = False  # Reset flag
            pantalla.blit(alien.imagen, alien.rect)

            for bala in balas[:]:
                if alien.rect.colliderect(bala.rect):
                    alien.vidas -= 1
                    if alien.vidas <= 0:
                        aliens.remove(alien)
                        puntuacion += 10 if alien.tipo == "verde" else 20 if alien.tipo == "amarillo" else 30 if alien.tipo == "rojo" else 40
                        # Drop heart or gadget
                        if random.random() < 0.04:  # 4% chance
                            drop_x = max(0, min(alien.rect.centerx, ancho_pantalla - 25))  # Ensure inside screen
                            drop_y = max(0, min(alien.rect.centery, alto_pantalla - 25))
                            if random.random() < 0.5:
                                corazones.append(Heart(drop_x, drop_y))
                            else:
                                gadgets.append(Gadget(drop_x, drop_y, random.randint(0, 3)))
                    if not bala.piercing:
                        balas.remove(bala)
                    break

        # Change direction and move down for all aliens if needed
        if cambiar_direccion_global:
            for alien in aliens:
                alien.velocidad_x = -alien.velocidad_x
                alien.rect.y += 10  # Move all aliens down less

        # Alien shooting logic
        aliens_disparadores = obtener_aliens_mas_bajos(aliens)
        if tiempo_actual - ultimo_disparo_alien > tiempo_entre_disparos_alien and aliens_disparadores:
            alien_disparador = random.choice(aliens_disparadores)
            nueva_bala_alien = disparo(alien_disparador.rect.centerx, alien_disparador.rect.bottom, 5, True)
            balas_aliens.append(nueva_bala_alien)
            ultimo_disparo_alien = tiempo_actual

        # Update player bullets
        for bala in balas[:]:
            bala.actualizar()
            if bala.activo:
                bala.dibujar(pantalla)
            else:
                balas.remove(bala)

        # Update alien bullets
        for bala_alien in balas_aliens[:]:
            bala_alien.actualizar()
            if bala_alien.activo:
                bala_alien.dibujar(pantalla)
                if bala_alien.rect.colliderect(jugador.cuadrado) and not invulnerable:
                    jugador.vidas -= 1
                    balas_aliens.remove(bala_alien)
                    invulnerable = True
                    tiempo_invulnerable = tiempo_actual
                    if jugador.vidas <= 0:
                        juego_activo = False
            else:
                balas_aliens.remove(bala_alien)

        # Update and draw gadgets
        for gadget in gadgets[:]:
            gadget.actualizar()
            if gadget.rect.colliderect(jugador.cuadrado):  # Fix collision detection
                gadgets.remove(gadget)
                gadgets_inventario.append(gadget)  # Add gadget to inventory
            elif gadget.rect.top > alto_pantalla:
                gadgets.remove(gadget)
            else:
                gadget.dibujar()

        # Update and draw hearts
        for heart in corazones[:]:
            heart.actualizar()
            if heart.rect.colliderect(jugador.cuadrado) and jugador.vidas < 3:  # Fix collision detection
                jugador.vidas += 1
                corazones.remove(heart)
            elif heart.rect.top > alto_pantalla:
                corazones.remove(heart)
            else:
                heart.dibujar()

        # Draw gadget column
        dibujar_columna_gadgets(gadgets_inventario)

        # Check if all aliens are defeated
        if not aliens:
            nivel += 1
            aliens = crear_aliens(nivel)
            balas = []
            balas_aliens = []

        # Display game info
        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, blanco)
        texto_nivel = fuente.render(f"Oleada: {nivel}", True, blanco)
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_nivel, (ancho_pantalla - 200, 20))
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