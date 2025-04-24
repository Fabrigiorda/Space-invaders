from numpy import imag
import pygame
import sys
import os
import time
import json
import random

# Configuración pantalla
ancho_pantalla = 1000
alto_pantalla = 1000

pygame.init()
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Space invaders")
reloj = pygame.time.Clock()

seleccion_menu = 0
fondo = pygame.image.load("imagenes/fondo.png")
fondo2 = pygame.transform.scale(fondo, (1000, 1000))

# Carga de imágenes
logo = pygame.image.load("imagenes/logo.png")
logo_grande = pygame.transform.scale(logo, (500, 448))

nave_img = pygame.image.load("imagenes/nave.png")
nave_img_chica = pygame.transform.scale(nave_img, (70, 94))

# Cargar imagen de la segunda nave para jugador 2
nave_img_2 = pygame.image.load("imagenes/nave2.png")
nave_img_chica_2 = pygame.transform.scale(nave_img_2, (70, 94))

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

# Colores y fuentes
rojo = (255, 0, 0)
negro = (0, 0, 0)
verde = (0, 255, 0)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)

fuente = pygame.font.Font('PressStart2P-Regular.ttf', 20)
fuente2 = pygame.font.Font('PressStart2P-Regular.ttf', 24)

# Carga de sonidos
sonido_click = pygame.mixer.Sound("sonidos/click.wav")
sonido_hover = pygame.mixer.Sound("sonidos/hoover.wav")
musica_menu = "sonidos/menu.wav"
musica_partida = "sonidos/partida.wav"
sonido_enemigo_golpeado = pygame.mixer.Sound("sonidos/soundenemyhit.wav")
sonido_game_over = pygame.mixer.Sound("sonidos/soundgameover.wav")
sonido_jugador_golpeado = pygame.mixer.Sound("sonidos/soundplayerhit.wav")
sonido_disparo = pygame.mixer.Sound("sonidos/soundshootregular.wav")
sonido_inicio_nivel = pygame.mixer.Sound("sonidos/soundstartlevel.wav")
sonido_disparo_nave = pygame.mixer.Sound("sonidos/Laser1.wav")


# Reproducir música del menú
pygame.mixer.music.load(musica_menu)
pygame.mixer.music.play(-1)  # Repetir indefinidamente

# Variables de volumen
volumen_musica = 0.5
volumen_sonidos = 0.5

# Configurar volúmenes iniciales
pygame.mixer.music.set_volume(volumen_musica)
sonido_click.set_volume(volumen_sonidos)
sonido_hover.set_volume(volumen_sonidos)
sonido_enemigo_golpeado.set_volume(volumen_sonidos)
sonido_game_over.set_volume(volumen_sonidos)
sonido_jugador_golpeado.set_volume(volumen_sonidos)
sonido_disparo.set_volume(volumen_sonidos)
sonido_inicio_nivel.set_volume(volumen_sonidos)
sonido_disparo_nave.set_volume(volumen_sonidos)


# Variable para controlar si la música del menú ya está reproduciéndose
musica_menu_reproduciendo = False

class Boton:
    def __init__(self, texto, ancho, alto, posicion, color, color_texto):
        self.rectangulo = pygame.Rect(posicion, (ancho, alto))
        self.color_rect = color 
        self.texto_original = texto
        self.color_texto_default = color_texto
        self.color_texto_hover = blanco
        self.texto = fuente.render(self.texto_original, True, self.color_texto_default)
        self.texto_centrado = self.texto.get_rect(center=self.rectangulo.center)
        self.hover_sonado = False  # Controla si el sonido de hover ya se reprodujo
        
    def actualizar_texto(self, mouseX, mouseY):
        if self.rectangulo.collidepoint(mouseX, mouseY):
            if not self.hover_sonado:
                sonido_hover.play()  # Reproducir sonido al pasar el mouse una sola vez
                self.hover_sonado = True
            self.texto = fuente2.render(self.texto_original, True, self.color_texto_hover)
        else:
            self.texto = fuente.render(self.texto_original, True, self.color_texto_default)
            self.hover_sonado = False  # Resetear para permitir reproducir el sonido nuevamente
        self.texto_centrado = self.texto.get_rect(center=self.rectangulo.center)
            
    def dibujar_boton(self, mouseX, mouseY):
        self.actualizar_texto(mouseX, mouseY)
        pygame.draw.rect(pantalla, self.color_rect, self.rectangulo, border_radius=12)
        pantalla.blit(self.texto, self.texto_centrado)
    
# Definición de botones
boton1 = Boton("Jugar", 200, 60, ((ancho_pantalla-200)/2, 450), negro, amarillo)
boton2 = Boton("Multijugador", 200, 60, ((ancho_pantalla-200)/2, 550), negro, amarillo)
boton3 = Boton("Ranking", 200, 60, ((ancho_pantalla-200)/2, 650), negro, amarillo)
boton4 = Boton("Opciones", 200, 60, ((ancho_pantalla-200)/2, 750), negro, amarillo)
boton5 = Boton("Salir", 200, 60, ((ancho_pantalla-200)/2, 850), negro, amarillo)

class Nave:
    def __init__(self, imagen, ancho, alto, velocidad, disparo):
        self.nave_imagen = imagen
        self.nave_velocidad_x = 0
        self.velocidad = velocidad
        self.disparo = disparo
        self.cuadrado = pygame.Rect(ancho - imagen.get_width()//2, alto - imagen.get_height()//2 - 10, imagen.get_width(), imagen.get_height())
        self.vidas = 3

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

class Disparo:
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
        self.velocidad_disparo = velocidad_disparo
        self.max_velocidad = 10 if tipo == "rojo" else 8 if tipo == "azul" else 5
        self.columna = 0
        self.cambiar_direccion = False

    def mover(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0 or self.rect.right > ancho_pantalla:
            self.cambiar_direccion = True
            self.rect.y += 10

def crear_aliens(nivel):
    aliens = []
    filas = 5
    columnas = 8
    distancia_x = 100
    distancia_y = 70
    
    # Configuración base para todos los aliens
    tipo = "verde"
    velocidad_base = 2
    velocidad_disparo = 1000
    vidas = 1
    
    # Configuración específica para cada nivel
    if nivel == 1:
        tipo = "verde"
        velocidad_base = 2
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 2:
        tipo = "verde"
        velocidad_base = 3
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 3:
        tipo = "amarillo"
        velocidad_base = 2
        velocidad_disparo = 800
        vidas = 1
    elif nivel == 4:
        tipo = "amarillo"
        velocidad_base = 3
        velocidad_disparo = 800
        vidas = 1
    elif nivel == 5:
        tipo = "rojo"
        velocidad_base = 4
        velocidad_disparo = 1000
        vidas = 1
    elif nivel == 6:
        tipo = "verde"
        velocidad_base = 2
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 7:
        tipo = "verde"
        velocidad_base = 3
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 8:
        tipo = "amarillo"
        velocidad_base = 2
        velocidad_disparo = 800
        vidas = 2
    elif nivel == 9:
        tipo = "amarillo"
        velocidad_base = 3
        velocidad_disparo = 800
        vidas = 2
    elif nivel == 10:
        tipo = "rojo"
        velocidad_base = 5
        velocidad_disparo = 1000
        vidas = 2
    elif nivel == 11:
        tipo = "rojo"
        velocidad_base = 4
        velocidad_disparo = 1000
        vidas = 3
    elif nivel >= 12:
        tipo = "azul"
        velocidad_base = 2 + (nivel - 12) // 2
        velocidad_disparo = 1000 - ((nivel - 12) % 2) * 50
        velocidad_base = min(velocidad_base, 8)
        velocidad_disparo = max(velocidad_disparo, 400)
        vidas = 1

    aliens_por_columna = {}
    
    for fila in range(filas):
        for columna in range(columnas):
            x = 100 + columna * distancia_x
            y = 50 + fila * distancia_y
            velocidad_x = velocidad_base
            
            if tipo == "rojo":
                velocidad_x += 1
            
            nuevo_alien = Alien(tipo, x, y, velocidad_base, velocidad_x, vidas, tipo, velocidad_disparo)
            nuevo_alien.columna = columna
            aliens.append(nuevo_alien)
            
            if columna not in aliens_por_columna:
                aliens_por_columna[columna] = []
            aliens_por_columna[columna].append(nuevo_alien)
    
    return aliens

ancho_logo = logo_grande.get_width()

def menu(mouseX, mouseY):
    global musica_menu_reproduciendo
    if not musica_menu_reproduciendo:
        pygame.mixer.music.load(musica_menu)
        pygame.mixer.music.play(-1)  # Repetir indefinidamente
        musica_menu_reproduciendo = True

    pantalla.fill(negro)
    pantalla.blit(logo_grande, ((ancho_pantalla - ancho_logo)/2, 10))
    boton1.dibujar_boton(mouseX, mouseY)
    boton2.dibujar_boton(mouseX, mouseY)
    boton3.dibujar_boton(mouseX, mouseY)
    boton4.dibujar_boton(mouseX, mouseY)
    boton5.dibujar_boton(mouseX, mouseY)

def obtener_aliens_mas_bajos(aliens):
    aliens_mas_bajos = {}
    
    for alien in aliens:
        columna = alien.columna
        if columna not in aliens_mas_bajos or alien.rect.y > aliens_mas_bajos[columna].rect.y:
            aliens_mas_bajos[columna] = alien
    
    return list(aliens_mas_bajos.values())

nivel = 1

class Escudo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.golpes = 0
        self.max_golpes = 7

    def dibujar(self):
        if self.golpes < self.max_golpes:
            pygame.draw.rect(pantalla, verde, self.rect)

    def recibir_dano(self):
        self.golpes += 1
        if self.golpes >= self.max_golpes:
            return True
        return False

class Corazon:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.imagen = corazon_img
        self.velocidad = 2

    def actualizar(self):
        self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.imagen, self.rect)

def mostrar_contador(tiempo):
    """Muestra un contador en el centro de la pantalla."""
    pantalla.fill(negro)
    texto_contador = fuente.render(f"{tiempo}", True, blanco)
    pantalla.blit(texto_contador, ((ancho_pantalla - texto_contador.get_width()) // 2, alto_pantalla // 2))
    pygame.display.update()
    reloj.tick(60)

def guardar_puntuacion(nombre, puntos, modo):
    """Guarda la puntuación en el archivo JSON bajo la sección correspondiente."""
    ranking_path = "ranking.json"
    try:
        with open(ranking_path, "r") as archivo:
            contenido = archivo.read().strip()
            ranking = json.loads(contenido) if contenido else {}
    except (FileNotFoundError, json.JSONDecodeError):
        ranking = {}

    if modo not in ranking:
        ranking[modo] = []

    ranking[modo].append({"nombre": nombre, "puntos": puntos})
    with open(ranking_path, "w") as archivo:
        json.dump(ranking, archivo, indent=4)

def mostrar_mensaje_perdida(puntuacion):
    """Muestra un mensaje de pérdida y permite guardar los puntos."""
    pygame.mixer.music.stop()  # Detener toda la música
    pantalla.fill(negro)
    texto_perdiste = fuente2.render("PERDISTE", True, rojo)
    texto_puntos = fuente.render(f"Tus puntos fueron: {puntuacion}", True, blanco)
    texto_guardar = fuente.render("¿Deseas guardar tus puntos? (S/N)", True, blanco)
    pantalla.blit(texto_perdiste, ((ancho_pantalla - texto_perdiste.get_width()) // 2, alto_pantalla // 3))
    pantalla.blit(texto_puntos, ((ancho_pantalla - texto_puntos.get_width()) // 2, alto_pantalla // 3 + 50))
    pantalla.blit(texto_guardar, ((ancho_pantalla - texto_guardar.get_width()) // 2, alto_pantalla // 3 + 100))
    pygame.display.update()

    guardar_puntos = None
    while guardar_puntos is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    guardar_puntos = True
                elif evento.key == pygame.K_n:
                    guardar_puntos = False

    if guardar_puntos:
        pantalla.fill(negro)
        texto_ingresa_nombre = fuente.render("Ingresa tu nombre:", True, blanco)
        pantalla.blit(texto_ingresa_nombre, ((ancho_pantalla - texto_ingresa_nombre.get_width()) // 2, alto_pantalla // 3))
        pygame.display.update()

        nombre = ""
        ingresando_nombre = True
        while ingresando_nombre:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nombre:
                        ingresando_nombre = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode

            pantalla.fill(negro)
            pantalla.blit(texto_ingresa_nombre, ((ancho_pantalla - texto_ingresa_nombre.get_width()) // 2, alto_pantalla // 3))
            texto_nombre = fuente.render(nombre, True, blanco)
            pantalla.blit(texto_nombre, ((ancho_pantalla - texto_nombre.get_width()) // 2, alto_pantalla // 3 + 50))
            pygame.display.update()

        guardar_puntuacion(nombre, puntuacion, "jugar solo")

    # Volver al menú y reproducir música del menú
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.play(-1)

def mostrar_mensaje_perdida_multijugador(puntuacion1, puntuacion2):
    """Muestra un mensaje de pérdida para multijugador y permite guardar los puntos."""
    pantalla.fill(negro)
    texto_perdiste = fuente2.render("PERDISTE", True, rojo)
    texto_guardar = fuente.render("¿Desean guardar sus puntos? (S/N)", True, blanco)
    pantalla.blit(texto_perdiste, ((ancho_pantalla - texto_perdiste.get_width()) // 2, alto_pantalla // 3))
    pantalla.blit(texto_guardar, ((ancho_pantalla - texto_guardar.get_width()) // 2, alto_pantalla // 3 + 50))
    pygame.display.update()

    guardar_puntos = None
    while guardar_puntos is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    guardar_puntos = True
                elif evento.key == pygame.K_n:
                    guardar_puntos = False

    if guardar_puntos:
        nombres = []
        for i in range(2):
            pantalla.fill(negro)
            texto_ingresa_nombre = fuente.render(f"Ingresa tu nombre Jugador {i + 1}:", True, blanco)
            pantalla.blit(texto_ingresa_nombre, ((ancho_pantalla - texto_ingresa_nombre.get_width()) // 2, alto_pantalla // 3))
            pygame.display.update()

            nombre = ""
            ingresando_nombre = True
            while ingresando_nombre:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN and nombre:
                            ingresando_nombre = False
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre = nombre[:-1]
                        else:
                            nombre += evento.unicode

                pantalla.fill(negro)
                pantalla.blit(texto_ingresa_nombre, ((ancho_pantalla - texto_ingresa_nombre.get_width()) // 2, alto_pantalla // 3))
                texto_nombre = fuente.render(nombre, True, blanco)
                pantalla.blit(texto_nombre, ((ancho_pantalla - texto_nombre.get_width()) // 2, alto_pantalla // 3 + 50))
                pygame.display.update()

            nombres.append(nombre)

        nombre_combinado = f"{nombres[0]} y {nombres[1]}"
        puntuacion_total = puntuacion1 + puntuacion2
        guardar_puntuacion(nombre_combinado, puntuacion_total, "multijugador")

def mostrar_menu_pausa():
    """Muestra el menú de pausa con opciones."""
    overlay = pygame.Surface((ancho_pantalla, alto_pantalla))
    overlay.set_alpha(128)  # Opacidad baja
    overlay.fill(negro)
    pantalla.blit(overlay, (0, 0))

    # Opciones del menú de pausa
    texto_reanudar = fuente.render("Reanudar", True, blanco)
    texto_opciones = fuente.render("Opciones", True, blanco)
    texto_salir = fuente.render("Salir", True, blanco)

    pantalla.blit(texto_reanudar, ((ancho_pantalla - texto_reanudar.get_width()) // 2, alto_pantalla // 3))
    pantalla.blit(texto_opciones, ((ancho_pantalla - texto_opciones.get_width()) // 2, alto_pantalla // 3 + 50))
    pantalla.blit(texto_salir, ((ancho_pantalla - texto_salir.get_width()) // 2, alto_pantalla // 3 + 100))

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Reanudar el juego
                    return "reanudar"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if texto_reanudar.get_rect(center=((ancho_pantalla) // 2, alto_pantalla // 3)).collidepoint(mouseX, mouseY):
                    return "reanudar"
                elif texto_opciones.get_rect(center=((ancho_pantalla) // 2, alto_pantalla // 3 + 50)).collidepoint(mouseX, mouseY):
                    return "opciones"
                elif texto_salir.get_rect(center=((ancho_pantalla) // 2, alto_pantalla // 3 + 100)).collidepoint(mouseX, mouseY):
                    # Cambiar a música del menú
                    pygame.mixer.music.load(musica_menu)
                    pygame.mixer.music.play(-1)
                    return "salir"

def jugar_solo():
    for i in range(3, 0, -1):
        sonido_inicio_nivel.play()  # Reproducir sonido de inicio de nivel
        mostrar_contador(i)
        time.sleep(1)
    pygame.mixer.music.load(musica_partida)
    pygame.mixer.music.play(-1)  # Repetir indefinidamente
    global nivel
    nivel = 1
    puntuacion = 0
    jugador = Nave(nave_img_chica, ancho_pantalla // 2, alto_pantalla - 40, 7, True)
    juego_activo = True
    balas = []
    balas_aliens = []
    corazones = []
    puede_disparar = True
    ultimo_disparo = 0
    tiempo_entre_disparos = 400
    ultimo_disparo_alien = 0
    tiempo_entre_disparos_alien = 1000
    aliens = crear_aliens(nivel)

    escudos = [
        Escudo(150, alto_pantalla - 200),
        Escudo(350, alto_pantalla - 200),
        Escudo(550, alto_pantalla - 200),
        Escudo(750, alto_pantalla - 200),
    ]

    invulnerable = False
    tiempo_invulnerable = 0
    duracion_invulnerable = 2000
    parpadeo = False
    ultimo_parpadeo = 0
    intervalo_parpadeo = 200

    while juego_activo:
        tiempo_actual = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    opcion = mostrar_menu_pausa()
                    if opcion == "reanudar":
                        continue
                    elif opcion == "opciones":
                        opciones()
                    elif opcion == "salir":
                        return  # Salir al menú principal

        pantalla.blit(fondo2, (0, 0))
        jugador.actualizar()

        if invulnerable:
            if tiempo_actual - tiempo_invulnerable > duracion_invulnerable:
                invulnerable = False

            if tiempo_actual - ultimo_parpadeo > intervalo_parpadeo:
                parpadeo = not parpadeo
                ultimo_parpadeo = tiempo_actual

            if not parpadeo:
                pantalla.blit(nave_img_chica, jugador.cuadrado)
        else:
            pantalla.blit(nave_img_chica, jugador.cuadrado)

        for escudo in escudos[:]:
            escudo.dibujar()
            for bala_alien in balas_aliens[:]:
                if escudo.rect.colliderect(bala_alien.rect):
                    if escudo.recibir_dano():
                        escudos.remove(escudo)
                    balas_aliens.remove(bala_alien)

        cambiar_direccion_global = False
        for alien in aliens[:]:
            alien.mover()
            if alien.cambiar_direccion:
                cambiar_direccion_global = True
                alien.cambiar_direccion = False
            pantalla.blit(alien.imagen, alien.rect)

            for bala in balas[:]:
                if alien.rect.colliderect(bala.rect):
                    sonido_enemigo_golpeado.play()  # Reproducir sonido al golpear un enemigo
                    alien.vidas -= 1
                    if alien.vidas <= 0:
                        aliens.remove(alien)
                        puntuacion += 10 if alien.tipo == "verde" else 20 if alien.tipo == "amarillo" else 30 if alien.tipo == "rojo" else 40
                        if random.random() < 0.04:
                            drop_x = max(0, min(alien.rect.centerx, ancho_pantalla - 25))
                            drop_y = max(0, min(alien.rect.centery, alto_pantalla - 25))
                            corazones.append(Corazon(drop_x, drop_y))
                    balas.remove(bala)
                    break

        if cambiar_direccion_global:
            for alien in aliens:
                alien.velocidad_x = -alien.velocidad_x
                alien.rect.y += 10

        aliens_disparadores = obtener_aliens_mas_bajos(aliens)
        if tiempo_actual - ultimo_disparo_alien > tiempo_entre_disparos_alien and aliens_disparadores:
            alien_disparador = random.choice(aliens_disparadores)
            sonido_disparo_nave.play()  # Reproducir sonido al disparar el alien
            nueva_bala_alien = Disparo(alien_disparador.rect.centerx, alien_disparador.rect.bottom, 5, True)
            balas_aliens.append(nueva_bala_alien)
            ultimo_disparo_alien = tiempo_actual

        for bala in balas[:]:
            bala.actualizar()
            if bala.activo:
                bala.dibujar(pantalla)
            else:
                balas.remove(bala)

        for bala_alien in balas_aliens[:]:
            bala_alien.actualizar()
            if bala_alien.activo:
                bala_alien.dibujar(pantalla)
                if bala_alien.rect.colliderect(jugador.cuadrado) and not invulnerable:
                    sonido_jugador_golpeado.play()  # Reproducir sonido al golpear al jugador
                    jugador.vidas -= 1
                    balas_aliens.remove(bala_alien)
                    invulnerable = True
                    tiempo_invulnerable = tiempo_actual
                    if jugador.vidas <= 0:
                        sonido_game_over.play()  # Reproducir sonido de game over
                        juego_activo = False
                        mostrar_mensaje_perdida(puntuacion)
            else:
                balas_aliens.remove(bala_alien)

        for corazon in corazones[:]:
            corazon.actualizar()
            if corazon.rect.colliderect(jugador.cuadrado) and jugador.vidas < 3:
                jugador.vidas += 1
                corazones.remove(corazon)
            elif corazon.rect.top > alto_pantalla:
                corazones.remove(corazon)
            else:
                corazon.dibujar()

        if not aliens:
            nivel += 1
            for i in range(3, 0, -1):
                mostrar_contador(i)
                time.sleep(1)
            aliens = crear_aliens(nivel)
            balas = []
            balas_aliens = []

        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, blanco)
        texto_nivel = fuente.render(f"Oleada: {nivel}", True, blanco)
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_nivel, (ancho_pantalla - 200, 20))
        jugador.dibujar_vidas()

        # Dibujar vidas en la parte superior central
        texto_vidas = fuente.render("Vidas:", True, blanco)
        pantalla.blit(texto_vidas, ((ancho_pantalla - texto_vidas.get_width()) // 2 - 50, 20))
        for i in range(jugador.vidas):
            pantalla.blit(corazon_img, ((ancho_pantalla // 2) + i * 40, 20))

        pygame.display.update()
        reloj.tick(60)

def multijugador():
    """Modo multijugador del juego."""
    for i in range(3, 0, -1):
        sonido_inicio_nivel.play()  # Reproducir sonido de inicio de nivel
        mostrar_contador(i)
        time.sleep(1)
    
    pygame.mixer.music.load(musica_partida)
    pygame.mixer.music.play(-1)  # Repetir indefinidamente

    global nivel
    nivel = 1
    puntuacion1 = 0
    puntuacion2 = 0
    
    jugadores = [
        Nave(nave_img_chica, ancho_pantalla // 3, alto_pantalla - 40, 7, True),
        Nave(nave_img_chica_2, 2 * ancho_pantalla // 3, alto_pantalla - 40, 7, True)
    ]
    
    juego_activo = True
    balas = []
    balas_aliens = []
    corazones = [[], []]
    puede_disparar = [True, True]
    ultimo_disparo = [0, 0]
    tiempo_entre_disparos = 400
    ultimo_disparo_alien = 0
    tiempo_entre_disparos_alien = 1000
    aliens = crear_aliens(nivel)
    freeze_timer = 0
    piercing_bullets = [False, False]

    escudos = [
        Escudo(150, alto_pantalla - 200),
        Escudo(350, alto_pantalla - 200),
        Escudo(550, alto_pantalla - 200),
        Escudo(750, alto_pantalla - 200),
    ]

    invulnerable = [False, False]
    tiempo_invulnerable = [0, 0]
    duracion_invulnerable = 2000
    parpadeo = [False, False]
    ultimo_parpadeo = [0, 0]
    intervalo_parpadeo = 200

    while juego_activo:
        tiempo_actual = pygame.time.get_ticks()

        if freeze_timer > 0 and tiempo_actual - freeze_timer > 5000:
            freeze_timer = 0
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    opcion = mostrar_menu_pausa()
                    if opcion == "reanudar":
                        continue
                    elif opcion == "opciones":
                        opciones()
                    elif opcion == "salir":
                        return  # Salir al menú principal
                elif evento.key == pygame.K_w and puede_disparar[0] and tiempo_actual - ultimo_disparo[0] > tiempo_entre_disparos:
                    sonido_disparo_nave.play()  # Reproducir sonido al disparar el jugador 1
                    nueva_bala = Disparo(jugadores[0].cuadrado.centerx, jugadores[0].cuadrado.top, 10)
                    nueva_bala.piercing = piercing_bullets[0]
                    balas.append(nueva_bala)
                    ultimo_disparo[0] = tiempo_actual
                elif evento.key == pygame.K_UP and puede_disparar[1] and tiempo_actual - ultimo_disparo[1] > tiempo_entre_disparos:
                    sonido_disparo_nave.play()  # Reproducir sonido al disparar el jugador 2
                    nueva_bala = Disparo(jugadores[1].cuadrado.centerx, jugadores[1].cuadrado.top, 10)
                    nueva_bala.piercing = piercing_bullets[1]
                    balas.append(nueva_bala)
                    ultimo_disparo[1] = tiempo_actual

        pantalla.blit(fondo2, (0, 0))

        teclas = pygame.key.get_pressed()
        for i, jugador in enumerate(jugadores):
            if jugador.vidas > 0:
                if i == 0:  # Controles del jugador 1 (WASD)
                    jugador.nave_velocidad_x = 0
                    if teclas[pygame.K_a]:
                        jugador.nave_velocidad_x = -jugador.velocidad
                    elif teclas[pygame.K_d]:
                        jugador.nave_velocidad_x = jugador.velocidad
                elif i == 1:  # Controles del jugador 2 (Flechas)
                    jugador.nave_velocidad_x = 0
                    if teclas[pygame.K_LEFT]:
                        jugador.nave_velocidad_x = -jugador.velocidad
                    elif teclas[pygame.K_RIGHT]:
                        jugador.nave_velocidad_x = jugador.velocidad

                jugador.cuadrado.x += jugador.nave_velocidad_x
                if jugador.cuadrado.left < 0:
                    jugador.cuadrado.left = 0
                if jugador.cuadrado.right > ancho_pantalla:
                    jugador.cuadrado.right = ancho_pantalla

                if invulnerable[i]:
                    if tiempo_actual - tiempo_invulnerable[i] > duracion_invulnerable:
                        invulnerable[i] = False
                    if tiempo_actual - ultimo_parpadeo[i] > intervalo_parpadeo:
                        parpadeo[i] = not parpadeo[i]
                        ultimo_parpadeo[i] = tiempo_actual
                    if not parpadeo[i]:
                        pantalla.blit(jugador.nave_imagen, jugador.cuadrado)
                else:
                    pantalla.blit(jugador.nave_imagen, jugador.cuadrado)
            else:
                puede_disparar[i] = False

        # Actualizar balas de aliens
        for bala_alien in balas_aliens[:]:
            bala_alien.actualizar()
            if bala_alien.activo:
                bala_alien.dibujar(pantalla)
                hit_players = False
                for i, jugador in enumerate(jugadores):
                    if jugador.vidas > 0 and bala_alien.rect.colliderect(jugador.cuadrado):
                        sonido_jugador_golpeado.play()  # Reproducir sonido al golpear al jugador
                        jugador.vidas -= 1
                        invulnerable[i] = True
                        tiempo_invulnerable[i] = tiempo_actual
                        hit_players = True
                if hit_players:
                    balas_aliens.remove(bala_alien)
            else:
                balas_aliens.remove(bala_alien)

        # Verificar si ambos jugadores están muertos
        if all(jugador.vidas <= 0 for jugador in jugadores):
            sonido_game_over.play()  # Reproducir sonido de game over
            juego_activo = False
            mostrar_mensaje_perdida_multijugador(puntuacion1, puntuacion2)

        # Dibujar y actualizar escudos
        for escudo in escudos[:]:
            escudo.dibujar()
            for bala_alien in balas_aliens[:]:
                if escudo.rect.colliderect(bala_alien.rect):
                    if escudo.recibir_dano():
                        escudos.remove(escudo)
                    balas_aliens.remove(bala_alien)

        # Mover y dibujar aliens
        cambiar_direccion_global = False
        for alien in aliens[:]:
            if freeze_timer == 0:
                alien.mover()
                if alien.cambiar_direccion:
                    cambiar_direccion_global = True
                    alien.cambiar_direccion = False
            pantalla.blit(alien.imagen, alien.rect)

            for bala in balas[:]:
                if alien.rect.colliderect(bala.rect):
                    sonido_enemigo_golpeado.play()  # Reproducir sonido al golpear un enemigo
                    alien.vidas -= 1
                    if alien.vidas <= 0:
                        aliens.remove(alien)
                        puntuacion1 += 10 if alien.tipo == "verde" else 20 if alien.tipo == "amarillo" else 30 if alien.tipo == "rojo" else 40
                        if random.random() < 0.04:
                            drop_x = max(0, min(alien.rect.centerx, ancho_pantalla - 25))
                            drop_y = max(0, min(alien.rect.centery, alto_pantalla - 25))
                            corazones[random.randint(0, 1)].append(Corazon(drop_x, drop_y))
                    if not bala.piercing:
                        balas.remove(bala)
                    break

        if cambiar_direccion_global:
            for alien in aliens:
                alien.velocidad_x = -alien.velocidad_x
                alien.rect.y += 10

        # Disparos de aliens
        aliens_disparadores = obtener_aliens_mas_bajos(aliens)
        if tiempo_actual - ultimo_disparo_alien > tiempo_entre_disparos_alien and aliens_disparadores:
            alien_disparador = random.choice(aliens_disparadores)
            sonido_disparo_nave.play()  # Reproducir sonido al disparar el alien
            nueva_bala_alien = Disparo(alien_disparador.rect.centerx, alien_disparador.rect.bottom, 5, True)
            balas_aliens.append(nueva_bala_alien)
            ultimo_disparo_alien = tiempo_actual

        # Actualizar balas de jugadores
        for bala in balas[:]:
            bala.actualizar()
            if bala.activo:
                bala.dibujar(pantalla)
            else:
                balas.remove(bala)

        # Actualizar y dibujar corazones
        for i, jugador_corazones in enumerate(corazones):
            for corazon in jugador_corazones[:]:
                corazon.actualizar()
                if jugadores[i].vidas > 0 and corazon.rect.colliderect(jugadores[i].cuadrado) and jugadores[i].vidas < 3:
                    jugadores[i].vidas += 1
                    jugador_corazones.remove(corazon)
                elif corazon.rect.top > alto_pantalla:
                    jugador_corazones.remove(corazon)
                else:
                    corazon.dibujar()

        # Dibujar vidas de jugadores
        for i, jugador in enumerate(jugadores):
            texto_vidas = fuente.render(f"Jugador {i + 1}:", True, blanco)
            pantalla.blit(texto_vidas, ((ancho_pantalla - texto_vidas.get_width())/ 2  -100, alto_pantalla - 950 - i * 30))
            for j in range(jugador.vidas):
                pantalla.blit(corazon_img, ((ancho_pantalla - texto_vidas.get_width())/ 2 +100 + j * 40, alto_pantalla - 955 - i * 30))

        # Verificar si todos los aliens fueron eliminados
        if not aliens:
            nivel += 1
            for i in range(3, 0, -1):  
                mostrar_contador(i)
                time.sleep(1)  
            aliens = crear_aliens(nivel)
            balas = []
            balas_aliens = []

        # Mostrar información del juego
        texto_puntos = fuente.render(f"Puntos: {puntuacion1}", True, blanco)
        texto_nivel = fuente.render(f"Oleada: {nivel}", True, blanco)
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_nivel, (ancho_pantalla - 200, 20))

        # Dibujar vidas en la parte superior central
        for i, jugador in enumerate(jugadores):
            texto_vidas = fuente.render(f"Jugador {i + 1}:", True, blanco)
            pantalla.blit(texto_vidas, ((ancho_pantalla - texto_vidas.get_width()) // 2 - 100, 20 + i * 30))
            for j in range(jugador.vidas):
                pantalla.blit(corazon_img, ((ancho_pantalla // 2) + j * 40, 20 + i * 30))

        pygame.display.update()
        reloj.tick(60)

def ranking():
    """Muestra la pantalla de ranking con mejores puntuaciones."""
    ejecutando = True
    while ejecutando:
        pantalla.fill(negro)
        
        # Título
        texto_ranking = pygame.font.Font('PressStart2P-Regular.ttf', 36).render("Ranking", True, blanco)
        pantalla.blit(texto_ranking, ((ancho_pantalla - texto_ranking.get_width()) // 2, alto_pantalla // 10))
        
        # Texto "Un jugador" y "Multijugador"
        texto_un_jugador = fuente.render("Un jugador", True, blanco)
        texto_multijugador = fuente.render("Multijugador", True, blanco)
        pantalla.blit(texto_un_jugador, (ancho_pantalla // 4 - texto_un_jugador.get_width() // 2, alto_pantalla // 5))
        pantalla.blit(texto_multijugador, (3 * ancho_pantalla // 4 - texto_multijugador.get_width() // 2, alto_pantalla // 5))

        # Cargar y mostrar rankings desde JSON
        try:
            with open("ranking.json", "r") as archivo:
                datos_ranking = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            datos_ranking = {"jugar solo": [], "multijugador": []}

        # Ordenar y mostrar top 10 de rankings individuales
        y_offset = alto_pantalla // 5 + 50
        top_solo = sorted(datos_ranking.get("jugar solo", []), key=lambda x: x["puntos"], reverse=True)[:10]
        for i, entrada in enumerate(top_solo):
            texto = fuente.render(f"Top {i + 1}: {entrada['nombre']} - {entrada['puntos']}", True, blanco)
            pantalla.blit(texto, (ancho_pantalla // 4 - texto.get_width() // 2 - 50, y_offset))
            y_offset += 30

        # Ordenar y mostrar top 10 de rankings multijugador
        y_offset = alto_pantalla // 5 + 50
        top_multijugador = sorted(datos_ranking.get("multijugador", []), key=lambda x: x["puntos"], reverse=True)[:10]
        for i, entrada in enumerate(top_multijugador):
            texto = fuente.render(f"Top {i + 1}: {entrada['nombre']} - {entrada['puntos']}", True, blanco)
            pantalla.blit(texto, (3 * ancho_pantalla // 4 - texto.get_width() // 2 - 50, y_offset))
            y_offset += 30

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Volver al menú principal
                    ejecutando = False

        pygame.display.update()
        reloj.tick(60)

def opciones():
    """Muestra el menú de opciones con controles de volumen."""
    global volumen_musica, volumen_sonidos
    ejecutando = True

    while ejecutando:
        pantalla.fill(negro)

        # Títulos
        texto_opciones = fuente2.render("Opciones", True, blanco)
        pantalla.blit(texto_opciones, ((ancho_pantalla - texto_opciones.get_width()) // 2, 50))

        # Controles de volumen
        texto_musica = fuente.render("Volumen Música", True, blanco)
        texto_sonidos = fuente.render("Volumen Sonidos", True, blanco)
        pantalla.blit(texto_musica, ((ancho_pantalla - texto_musica.get_width()) // 2, 150))
        pantalla.blit(texto_sonidos, ((ancho_pantalla - texto_sonidos.get_width()) // 2, 250))

        # Dibujar barras de volumen debajo del texto
        barra_musica = pygame.Rect((ancho_pantalla - 400) // 2, 180, 400, 20)
        barra_sonidos = pygame.Rect((ancho_pantalla - 400) // 2, 280, 400, 20)
        pygame.draw.rect(pantalla, blanco, barra_musica)
        pygame.draw.rect(pantalla, blanco, barra_sonidos)

        # Indicadores de volumen
        indicador_musica = pygame.Rect(barra_musica.x + int(volumen_musica * barra_musica.width), barra_musica.y - 5, 10, 30)
        indicador_sonidos = pygame.Rect(barra_sonidos.x + int(volumen_sonidos * barra_sonidos.width), barra_sonidos.y - 5, 10, 30)
        pygame.draw.rect(pantalla, amarillo, indicador_musica)
        pygame.draw.rect(pantalla, amarillo, indicador_sonidos)

        # Botón para volver al menú
        texto_volver = fuente.render("Volver", True, blanco)
        boton_volver = pygame.Rect((ancho_pantalla - texto_volver.get_width()) // 2, 400, texto_volver.get_width() + 20, texto_volver.get_height() + 10)
        pygame.draw.rect(pantalla, rojo, boton_volver)
        pantalla.blit(texto_volver, (boton_volver.x + 10, boton_volver.y + 5))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if barra_musica.collidepoint(mouseX, mouseY):
                    volumen_musica = (mouseX - barra_musica.x) / barra_musica.width
                    pygame.mixer.music.set_volume(volumen_musica)
                elif barra_sonidos.collidepoint(mouseX, mouseY):
                    volumen_sonidos = (mouseX - barra_sonidos.x) / barra_sonidos.width
                    # Ajustar el volumen de todos los sonidos
                    sonido_click.set_volume(volumen_sonidos)
                    sonido_hover.set_volume(volumen_sonidos)
                    sonido_enemigo_golpeado.set_volume(volumen_sonidos)
                    sonido_game_over.set_volume(volumen_sonidos)
                    sonido_jugador_golpeado.set_volume(volumen_sonidos)
                    sonido_disparo.set_volume(volumen_sonidos)
                    sonido_inicio_nivel.set_volume(volumen_sonidos)
                    sonido_disparo_nave.set_volume(volumen_sonidos)
                elif boton_volver.collidepoint(mouseX, mouseY):
                    ejecutando = False

# Bucle principal del juego
while True:
    for evento in pygame.event.get():   
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    posX_raton, posY_raton = pygame.mouse.get_pos()
    menu(posX_raton, posY_raton)
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if boton1.rectangulo.collidepoint(posX_raton, posY_raton):
            jugar_solo()
        elif boton2.rectangulo.collidepoint(posX_raton, posY_raton):
            multijugador()
        elif boton3.rectangulo.collidepoint(posX_raton, posY_raton):
            ranking()
        elif boton4.rectangulo.collidepoint(posX_raton, posY_raton):
            opciones()
        elif boton5.rectangulo.collidepoint(posX_raton, posY_raton):
            pygame.quit()
            sys.exit()
    pygame.display.update()
    reloj.tick(60)