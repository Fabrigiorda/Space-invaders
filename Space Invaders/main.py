from tokenize import group
from numpy import imag
import pygame
import sys
import os
import time
import json



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




#Defino la clase nave
class nave:
    #Pongo los parametros de la nave
    def __init__(self, imagen, ancho, alto, velocidad, disparo):
        self.nave_imagen = imagen
        self.nave_velocidad_x = 0
        self.velocidad = velocidad
        self.disparo = disparo
        self.cuadrado = pygame.Rect(ancho - imagen.get_width()//2, alto - imagen.get_height()//2 - 10, imagen.get_width(), imagen.get_height())
        

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
        



#defino la clase de disparo de la nave
class disparo:
    def __init__(self, x, y, velocidad):
        self.imagen = bala_img
        self.velocidad = velocidad
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.activo = True

    def actualizar(self):
        self.rect.y -= self.velocidad
        if self.rect.bottom < 0:
            self.activo = False

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)




#Defino la clase de el alien verde
class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        imagen_path = "imagenes/" + color + ".png"
        self.imagen = pygame.image.load(imagen_path).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (65, 65))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)



def crear_aliens():
    aliens = []
    filas = 5
    columnas = 8
    distancia_x = 100
    distancia_y = 70
    for fila in range(filas):
        for columna in range(columnas):
            x = 100 + columna * distancia_x
            y = 50 + fila * distancia_y
            alien = Alien("rojo", x, y)
            aliens.append(alien)
    return aliens




ancho_logo = logo_grande.get_width()


def menu(mouseX, mouseY):
    pantalla.fill(negro)
    pantalla.blit(logo, ((ancho_pantalla - ancho_logo)/2, 10))
    boton1.dibujar_boton(mouseX, mouseY)
    boton2.dibujar_boton(mouseX, mouseY)
    boton3.dibujar_boton(mouseX, mouseY)
    boton4.dibujar_boton(mouseX, mouseY)
    boton5.dibujar_boton(mouseX, mouseY)











def jugar_solo():
    jugador = nave(nave_img_chica, ancho_pantalla // 2, alto_pantalla - 40, 7, True)
    puntuacion = 0
    nivel = 1
    juego_activo = True
    
    balas = []
    puede_disparar = True
    ultimo_disparo = 0
    tiempo_entre_disparos = 400 
    
    aliens = crear_aliens()


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
        pantalla.blit(nave_img_chica, jugador.cuadrado)
        
        for alien in aliens:
            pantalla.blit(alien.imagen, alien.rect)
                
        
        for bala in balas[:]:  
            bala.actualizar()
            if bala.activo:
                bala.dibujar(pantalla)
            else:
                balas.remove(bala)  
        
        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, blanco)
        texto_nivel = fuente.render(f"Oleada: {nivel}", True, blanco)
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_nivel, (ancho_pantalla - 200, 20))


        
        pygame.display.update()
        reloj.tick(60)
    

def multijugador():
    pass

def ranking():
    pass

def opciones():
    pass



while True:
    for evento in pygame.event.get():   
        if evento.type == pygame.quit:
            pygame.quit()

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

    
    


    pygame.display.update()
    reloj.tick(60)



