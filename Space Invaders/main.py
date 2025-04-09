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


def menu(mouseX, mouseY):
    pantalla.fill(negro)
    boton1.dibujar_boton(mouseX, mouseY)
    boton2.dibujar_boton(mouseX, mouseY)
    boton3.dibujar_boton(mouseX, mouseY)
    boton4.dibujar_boton(mouseX, mouseY)
    boton5.dibujar_boton(mouseX, mouseY)

def jugar_solo():
    pass

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



