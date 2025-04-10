from re import A
import pygame
import sys
import os
import time
import json

ancho_pantalla = 700
alto_pantalla = 800




pygame.init()
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Space invaders")
reloj = pygame.time.Clock()

seleccion_menu = 0

nave_img = pygame.image.load("imagenes/nave.png")
nave_img_chica = pygame.transform.scale(nave_img, (65, 65))

alien_verde = pygame.image.load("imagenes/green.png")
alien_verde_chico = pygame.transform.scale(alien_verde, (65, 65))

alien_amarillo = pygame.image.load("imagenes/yellow.png")
alien_amarillo_chico = pygame.transform.scale(alien_amarillo, (65, 65))

alien_rojo = pygame.image.load("imagenes/red.png")
alien_rojo_chico = pygame.transform.scale(alien_rojo, (65, 65))


alien_azul = pygame.image.load("imagenes/blue.png")
alien_azul_chico = pygame.transform.scale(alien_azul, (65, 65))

bala_img = pygame.image.load("imagenes/bala.png")






rojo = (255, 0, 0)
negro = (0, 0, 0)
verde = (0, 255, 0)
blanco = (255, 255, 255)

fuente = pygame.font.Font('PressStart2P-Regular.ttf', 20)



class boton:
    def __init__(self, texto, ancho, alto, posicion, color, color_texto):
        self.rectangulo = pygame.Rect(posicion, (ancho, alto))
        self.color_rect = color 
        self.texto_original = texto
        self.color_texto_default = color_texto
        self.color_texto_hover = blanco
        self.texto = fuente.render(self.texto_original, True, self.color_texto_default)
        self.texto_centrado = self.texto.get_rect(center=self.rectangulo.center)
        
    def actualizar_texto(self, mouseX, mouseY):
            if self.rectangulo.collidepoint(mouseX, mouseY):
                self.texto = fuente.render(self.texto_original, True, self.color_texto_hover)
            else:
                self.texto = fuente.render(self.texto_original, True, self.color_texto_default)

    def dibujar_boton(self, mouseX, mouseY):
        self.actualizar_texto(mouseX, mouseY)
        pygame.draw.rect(pantalla, self.color_rect, self.rectangulo, border_radius=12)
        pantalla.blit(self.texto, self.texto_centrado)
        
        

    

boton1 = boton("Jugar", 200, 60, ((ancho_pantalla-200)/2, 200), negro, verde)
boton2 = boton("Multijugador", 200, 60, ((ancho_pantalla-200)/2, 300), negro, verde)
boton3 = boton("Ranking", 200, 60, ((ancho_pantalla-200)/2, 400), negro, verde)
boton4 = boton("Opciones", 200, 60, ((ancho_pantalla-200)/2, 500), negro, verde)
boton5 = boton("Salir", 200, 60, ((ancho_pantalla-200)/2, 600), negro, verde)





class nave:
    def __init__(self, imagen, ancho, alto, velocidad, disparo):
        self.nave_imagen = imagen
        self.nave_velocidad_x = 0
        self.velocidad = velocidad
        self.disparo = disparo
        self.cuadrado = pygame.Rect(ancho - imagen.get_width()//2, alto - imagen.get_height()//2, imagen.get_width(), imagen.get_height())
        


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


        





def menu(mouseX, mouseY):
    pantalla.fill(negro)
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
        
        pantalla.fill(negro)
        
        jugador.actualizar()
        pantalla.blit(nave_img_chica, jugador.cuadrado)
        
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



