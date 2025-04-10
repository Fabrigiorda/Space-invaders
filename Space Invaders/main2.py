import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Configuración del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = 300  # milisegundos

    def update(self):
        # Movimiento lateral
        self.velocidad_x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -7
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 7
        self.rect.x += self.velocidad_x
        
        # Limitar al área de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            self.ultimo_disparo = ahora
            return Bala(self.rect.centerx, self.rect.top, -10)  # -10 es la velocidad hacia arriba
        return None

# Clase para los aliens
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 2
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = random.randint(3000, 8000)  # Disparo aleatorio entre 3 y 8 segundos

    def update(self):
        self.rect.x += self.velocidad_x

    def cambiar_direccion(self):
        self.velocidad_x *= -1
        self.rect.y += 20  # Bajar cuando toca el borde
    
    def disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            self.ultimo_disparo = ahora
            self.cadencia_disparo = random.randint(3000, 8000)  # Resetear tiempo aleatorio
            return Bala(self.rect.centerx, self.rect.bottom, 5)  # 5 es la velocidad hacia abajo
        return None

# Clase para los escudos
class Escudo(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ALTO - 100  # Posición vertical fija
        self.salud = 5

    def recibir_daño(self):
        self.salud -= 1
        # Cambiar el color/tamaño según el daño recibido
        self.image = pygame.Surface((100 - (5 - self.salud) * 10, 20))
        self.image.fill((0, 0, min(255, 50 + 50 * self.salud)))
        if self.salud <= 0:
            self.kill()

# Clase para las balas
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        if velocidad_y < 0:  # Si es disparo del jugador
            self.image.fill(VERDE)
        else:  # Si es disparo de alien
            self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = velocidad_y

    def update(self):
        self.rect.y += self.velocidad_y
        # Eliminar si sale de la pantalla
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill()

# Iniciar juego
def iniciar_juego():
    # Crear sprites
    todos_los_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    balas_jugador = pygame.sprite.Group()
    balas_aliens = pygame.sprite.Group()
    escudos = pygame.sprite.Group()
    
    # Crear jugador
    jugador = Jugador()
    todos_los_sprites.add(jugador)
    
    # Crear aliens (5 filas de 8 aliens)
    for fila in range(5):
        for columna in range(8):
            alien = Alien(100 + columna * 70, 50 + fila * 60)
            aliens.add(alien)
            todos_los_sprites.add(alien)
    
    # Crear escudos (4 escudos distribuidos)
    for i in range(4):
        escudo = Escudo(100 + i * 200)
        escudos.add(escudo)
        todos_los_sprites.add(escudo)
    
    # Configuración del juego
    clock = pygame.time.Clock()
    puntuacion = 0
    running = True
    game_over = False
    font = pygame.font.SysFont(None, 36)
    
    # Bucle principal del juego
    while running:
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    nueva_bala = jugador.disparar()
                    if nueva_bala:
                        balas_jugador.add(nueva_bala)
                        todos_los_sprites.add(nueva_bala)
                elif event.key == pygame.K_r and game_over:
                    return iniciar_juego()  # Reiniciar juego
        
        if not game_over:
            # Actualizar
            todos_los_sprites.update()
            
            # Comprobar si los aliens deben cambiar de dirección
            for alien in aliens:
                if alien.rect.left <= 0 or alien.rect.right >= ANCHO:
                    for a in aliens:
                        a.cambiar_direccion()
                    break
            
            # Aliens disparan aleatoriamente
            for alien in aliens:
                disparo = alien.disparar()
                if disparo:
                    balas_aliens.add(disparo)
                    todos_los_sprites.add(disparo)
            
            # Colisiones entre balas del jugador y aliens
            colisiones_aliens = pygame.sprite.groupcollide(aliens, balas_jugador, True, True)
            for alien in colisiones_aliens:
                puntuacion += 10
            
            # Colisiones entre balas y escudos
            colisiones_escudos_balas_jugador = pygame.sprite.groupcollide(escudos, balas_jugador, False, True)
            for escudo in colisiones_escudos_balas_jugador:
                escudo.recibir_daño()
            
            colisiones_escudos_balas_aliens = pygame.sprite.groupcollide(escudos, balas_aliens, False, True)
            for escudo in colisiones_escudos_balas_aliens:
                escudo.recibir_daño()
            
            # Colisiones entre balas de aliens y jugador
            colisiones_jugador = pygame.sprite.spritecollide(jugador, balas_aliens, True)
            if colisiones_jugador:
                game_over = True
            
            # Comprobar si los aliens llegaron al jugador
            for alien in aliens:
                if alien.rect.bottom >= jugador.rect.top:
                    game_over = True
                    break
            
            # Victoria si no quedan aliens
            if len(aliens) == 0:
                game_over = True
        
        # Dibujar
        pantalla.fill(NEGRO)
        todos_los_sprites.draw(pantalla)
        
        # Mostrar puntuación
        texto_puntuacion = font.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (10, 10))
        
        # Mostrar mensaje de fin de juego
        if game_over:
            if len(aliens) == 0:
                mensaje = "¡HAS GANADO!"
            else:
                mensaje = "GAME OVER"
            texto_game_over = font.render(mensaje, True, BLANCO)
            texto_reiniciar = font.render("Presiona 'R' para reiniciar", True, BLANCO)
            pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 50))
            pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 50))
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar velocidad del juego
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    iniciar_juego()