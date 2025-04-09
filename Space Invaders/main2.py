import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Cargar imágenes desde la carpeta "imagenes"
img_path = os.path.join("imagenes")
NAVE_IMG = pygame.image.load(os.path.join(img_path, "nave.png"))
GREEN_ALIEN_IMG = pygame.image.load(os.path.join(img_path, "green.png"))
RED_ALIEN_IMG = pygame.image.load(os.path.join(img_path, "red.png"))
YELLOW_ALIEN_IMG = pygame.image.load(os.path.join(img_path, "yellow.png"))

# Redimensionar imágenes si es necesario
NAVE_IMG = pygame.transform.scale(NAVE_IMG, (50, 50))
GREEN_ALIEN_IMG = pygame.transform.scale(GREEN_ALIEN_IMG, (40, 40))
RED_ALIEN_IMG = pygame.transform.scale(RED_ALIEN_IMG, (40, 40))
YELLOW_ALIEN_IMG = pygame.transform.scale(YELLOW_ALIEN_IMG, (40, 40))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Configuración del reloj y FPS
clock = pygame.time.Clock()
FPS = 60

# Clase para la nave del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = NAVE_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5
        self.lives = 3
        self.score = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:  # Mover a la izquierda
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:  # Mover a la derecha
            self.rect.x += self.speed
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase para los aliens
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_type, level=1):
        super().__init__()
        self.alien_type = alien_type
        self.level = level
        
        # Configurar tipo de alien
        if alien_type == "green":
            self.image = GREEN_ALIEN_IMG
            self.value = 10
            self.health = 1
            self.shoot_chance = 0.001 + (level * 0.0005)  # Aumenta con el nivel
        elif alien_type == "yellow":
            self.image = YELLOW_ALIEN_IMG
            self.value = 20
            self.health = 1
            self.shoot_chance = 0.003 + (level * 0.001)  # Disparan más a menudo
        elif alien_type == "red":
            self.image = RED_ALIEN_IMG
            self.value = 30
            self.health = 2  # Los rojos tienen 2 vidas
            self.shoot_chance = 0.005 + (level * 0.0015)  # Los más peligrosos
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1 para derecha, -1 para izquierda
        self.base_speed = 1 + (0.2 * level)  # Velocidad base que aumenta con el nivel
        self.speed = self.base_speed
        
    def update(self):
        self.rect.x += self.direction * self.speed
        
    def reverse_and_down(self):
        self.direction *= -1
        self.rect.y += 20
        
    def shoot(self):
        # Probabilidad de disparo basada en el tipo y nivel
        if random.random() < self.shoot_chance:
            alien_bullet = AlienBullet(self.rect.centerx, self.rect.bottom, self.alien_type)
            all_sprites.add(alien_bullet)
            alien_bullets.add(alien_bullet)
            
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True  # El alien está muerto
        else:
            # Parpadeo o cambio visual para indicar daño
            temp = self.image.copy()
            temp.fill((255, 200, 200), special_flags=pygame.BLEND_MULT)
            self.image = temp
            return False  # El alien sigue vivo

# Clase para las balas del jugador
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Clase para las balas de los aliens
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_type):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        
        # Color de bala según tipo de alien
        if alien_type == "green":
            self.image.fill(GREEN)
            self.speed = 5
        elif alien_type == "yellow":
            self.image.fill(YELLOW)
            self.speed = 7
        elif alien_type == "red":
            self.image.fill(RED)
            self.speed = 9
        else:
            self.image.fill(WHITE)
            self.speed = 5
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Clase para las barreras
class Barrier:
    def __init__(self, x, y):
        self.blocks = pygame.sprite.Group()
        self.create_barrier(x, y)
        
    def create_barrier(self, x, y):
        for row in range(4):
            for col in range(8):
                block = BarrierBlock(x + col * 10, y + row * 10)
                self.blocks.add(block)
                all_sprites.add(block)
                
class BarrierBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3
        
    def hit(self):
        self.health -= 1
        if self.health == 2:
            self.image.fill((0, 200, 0))  # Verde más oscuro
        elif self.health == 1:
            self.image.fill((0, 150, 0))  # Verde aún más oscuro
        elif self.health <= 0:
            self.kill()

# Función para crear la flota de aliens según el nivel
def create_aliens(level):
    aliens = pygame.sprite.Group()
    rows = 5  # Número estándar de filas
    cols = 11  # Número estándar de columnas
    
    # Definir tipos de aliens según nivel
    if level == 1:
        # Oleada 1: Todos verdes
        alien_types = ["green"] * rows
    elif level == 2:
        # Oleada 2: Dos filas superiores amarillas, resto verdes
        alien_types = ["yellow", "yellow"] + ["green"] * (rows - 2)
    elif level == 3:
        # Oleada 3: Todos amarillos
        alien_types = ["yellow"] * rows
    elif level == 4:
        # Oleada 4: Mezcla de verdes y rojos
        alien_types = ["red", "red"] + ["green"] * (rows - 2)
    elif level == 5:
        # Oleada 5: Rojos y amarillos
        alien_types = ["red", "red"] + ["yellow"] * (rows - 2)
    elif level == 6:
        # Oleada 6: Mayoría rojos
        alien_types = ["red"] * (rows - 1) + ["yellow"]
    else:
        # Oleada 7+: Todos rojos (máxima dificultad)
        alien_types = ["red"] * rows
    
    # Crear la flota según la configuración
    spacing_x = 55
    spacing_y = 45
    start_x = 50
    start_y = 50
    
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            alien_type = alien_types[row]
            
            # Ajustar dificultad para niveles más altos
            actual_level = min(level, 10)  # Limitar el nivel para no hacer aliens imposibles
            alien = Alien(x, y, alien_type, actual_level)
            aliens.add(alien)
            all_sprites.add(alien)
            
    return aliens

# Función para comprobar si los aliens llegan al límite lateral
def check_fleet_edges(aliens):
    for alien in aliens:
        if alien.rect.right >= WIDTH or alien.rect.left <= 0:
            change_fleet_direction(aliens)
            return

def change_fleet_direction(aliens):
    for alien in aliens:
        alien.reverse_and_down()

# Función para mostrar texto en pantalla
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para mostrar la pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "SPACE INVADERS", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Usa A y D para moverte, ESPACIO para disparar", 22, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presiona cualquier tecla para comenzar", 18, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Función para mostrar la pantalla de game over
def show_game_over_screen(score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Puntuación final: {score}", 22, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presiona cualquier tecla para jugar de nuevo", 18, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Función para el nivel completado
def show_level_complete(level, score):
    screen.fill(BLACK)
    draw_text(screen, f"¡OLEADA {level} COMPLETADA!", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Puntuación: {score}", 22, WIDTH // 2, HEIGHT // 2)
    
    # Mostrar características de la siguiente oleada
    if level == 1:
        info = "Siguiente oleada: Aliens verdes y amarillos"
    elif level == 2:
        info = "Siguiente oleada: Todos amarillos, más rápidos"
    elif level == 3:
        info = "Siguiente oleada: Aliens verdes y rojos (2 vidas)"
    elif level == 4:
        info = "Siguiente oleada: Aliens rojos y amarillos, más peligrosos"
    elif level == 5:
        info = "Siguiente oleada: Mayoría de aliens rojos"
    else:
        info = "Siguiente oleada: ¡Aliens elite! Máxima dificultad"
    
    draw_text(screen, info, 20, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text(screen, "Presiona cualquier tecla para continuar", 18, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Mostrar información sobre cada tipo de alien
def show_alien_info():
    screen.fill(BLACK)
    draw_text(screen, "INFORMACIÓN DE ALIENS", 42, WIDTH // 2, 30)
    
    # Alien Verde
    screen.blit(GREEN_ALIEN_IMG, (100, 100))
    draw_text(screen, "Alien Verde", 22, 250, 100)
    draw_text(screen, "Puntos: 10", 18, 250, 130)
    draw_text(screen, "Salud: 1", 18, 250, 150)
    draw_text(screen, "Disparo: Lento", 18, 250, 170)
    
    # Alien Amarillo
    screen.blit(YELLOW_ALIEN_IMG, (100, 230))
    draw_text(screen, "Alien Amarillo", 22, 250, 230)
    draw_text(screen, "Puntos: 20", 18, 250, 260)
    draw_text(screen, "Salud: 1", 18, 250, 280)
    draw_text(screen, "Disparo: Medio", 18, 250, 300)
    
    # Alien Rojo
    screen.blit(RED_ALIEN_IMG, (100, 360))
    draw_text(screen, "Alien Rojo", 22, 250, 360)
    draw_text(screen, "Puntos: 30", 18, 250, 390)
    draw_text(screen, "Salud: 2", 18, 250, 410)
    draw_text(screen, "Disparo: Rápido", 18, 250, 430)
    
    draw_text(screen, "Presiona cualquier tecla para comenzar", 18, WIDTH // 2, HEIGHT - 50)
    
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Función principal del juego
def game_loop():
    level = 1
    game_over = False
    running = True
    
    # Crear grupos de sprites
    global all_sprites, bullets, aliens, barriers, alien_bullets
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    alien_bullets = pygame.sprite.Group()
    barriers = []
    
    # Crear el jugador
    player = Player()
    all_sprites.add(player)
    
    # Crear aliens
    aliens = create_aliens(level)
    
    # Crear barreras
    for i in range(4):
        barrier = Barrier(100 + i * 200, 450)
        barriers.append(barrier)
    
    # Bucle principal del juego
    while running:
        clock.tick(FPS)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
        
        if not game_over:
            # Actualizar
            all_sprites.update()
            
            # Verificar si los aliens llegan a los bordes
            check_fleet_edges(aliens)
            
            # Disparos de aliens
            for alien in aliens:
                alien.shoot()
            
            # Colisiones de balas del jugador con aliens
            hits = pygame.sprite.groupcollide(bullets, aliens, True, False)
            for bullet in hits:
                for alien in hits[bullet]:
                    if alien.hit():  # Si el alien muere
                        player.score += alien.value
                        alien.kill()
            
            # Colisiones de balas de aliens con el jugador
            hits = pygame.sprite.spritecollide(player, alien_bullets, True)
            if hits:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
            
            # Colisiones de balas con barreras
            for barrier in barriers:
                for block in barrier.blocks:
                    hits = pygame.sprite.spritecollide(block, bullets, True)
                    for hit in hits:
                        block.hit()
                    
                    hits = pygame.sprite.spritecollide(block, alien_bullets, True)
                    for hit in hits:
                        block.hit()
            
            # Colisiones de aliens con el jugador o la parte inferior
            for alien in aliens:
                if alien.rect.bottom > HEIGHT - 50:
                    game_over = True  # Game over si los aliens llegan abajo
                if pygame.sprite.collide_rect(alien, player):
                    game_over = True  # Game over si un alien toca al jugador
            
            # Verificar si se han eliminado todos los aliens
            if len(aliens) == 0:
                # Mostrar pantalla de nivel completado
                show_level_complete(level, player.score)
                
                # Subir de nivel y reiniciar aliens
                level += 1
                aliens = create_aliens(level)
                
                # Reiniciar barreras
                for barrier in barriers:
                    for block in barrier.blocks:
                        block.kill()
                barriers = []
                for i in range(4):
                    barrier = Barrier(100 + i * 200, 450)
                    barriers.append(barrier)
                
                # Limpiar balas
                for bullet in bullets:
                    bullet.kill()
                for bullet in alien_bullets:
                    bullet.kill()
                
                # Aumentar velocidad del jugador cada 2 niveles para darle ventaja
                if level % 2 == 0 and player.speed < 8:
                    player.speed += 0.5
        
        # Dibujar
        screen.fill(BLACK)
        
        # Dibujar todos los sprites
        all_sprites.draw(screen)
        
        # Mostrar información en pantalla
        draw_text(screen, f"Puntuación: {player.score}", 24, WIDTH // 2, 10)
        draw_text(screen, f"Vidas: {player.lives}", 24, 50, 10)
        draw_text(screen, f"Oleada: {level}", 24, WIDTH - 50, 10)
        
        if game_over:
            show_game_over_screen(player.score)
            return
        
        # Actualizar pantalla
        pygame.display.flip()

# Bucle principal
def main():
    show_start_screen()
    show_alien_info()  # Mostrar información sobre los diferentes tipos de aliens
    while True:
        game_loop()

if __name__ == "__main__":
    main()