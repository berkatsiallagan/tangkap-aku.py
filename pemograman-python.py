import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen constants
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangkap Aku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

# Game settings
FPS = 120
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 100, 20
player_speed = 18

# Falling objects
object_width, object_height = 30, 30
base_object_speed = 5
object_speed_increment = 0.2  # Reduced speed increment for smoother difficulty
cooldown = 3000  # 3 seconds to increase speed

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

# File for best score
best_score_file = "best_score.txt"

# Load sounds
try:
    catch_sound = pygame.mixer.Sound("catch.wav") if os.path.exists("catch.wav") else None
    miss_sound = pygame.mixer.Sound("miss.wav") if os.path.exists("miss.wav") else None
    bg_music = "funny-bgm-240795.mp3" if os.path.exists("funny-bgm-240795.mp3") else None
    
    if bg_music:
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
except:
    # If sound files don't exist or there's an error, continue without sound
    catch_sound = miss_sound = bg_music = None

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)  # Border
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, math.pi * 2)
        self.life = random.randint(20, 40)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        
    def draw(self, surface):
        alpha = min(255, self.life * 6)
        color = (*self.color[:3], alpha) if len(self.color) == 4 else self.color
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

def load_best_score():
    if os.path.exists(best_score_file):
        with open(best_score_file, "r") as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def save_best_score(best_score):
    with open(best_score_file, "w") as file:
        file.write(str(best_score))

def draw_text(surface, text, position, color=BLACK, font_size=36, align="center"):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    
    if align == "center":
        text_rect = text_surface.get_rect(center=position)
    elif align == "topleft":
        text_rect = text_surface.get_rect(topleft=position)
    elif align == "topright":
        text_rect = text_surface.get_rect(topright=position)
    
    surface.blit(text_surface, text_rect)
    return text_rect

def create_particles(x, y, color, count=15):
    return [Particle(x, y, color) for _ in range(count)]

def show_menu():
    screen.fill(WHITE)
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Tangkap Aku", True, BLUE)
    title_shadow = title_font.render("Tangkap Aku", True, (100, 100, 255))
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    # Draw shadow first
    screen.blit(title_shadow, (title_rect.x+3, title_rect.y+3))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instructions = [
        "Gunakan tombol kiri dan kanan atau mouse",
        "Tangkap benda yang jatuh untuk mendapatkan poin",
        "Hindari kehabisan nyawa!"
    ]
    
    for i, line in enumerate(instructions):
        draw_text(screen, line, (WIDTH//2, HEIGHT//2 + i*40), BLACK, 24)
    
    # Buttons
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 + 150, 200, 50, "Mulai", GREEN, (100, 255, 100))
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 220, 200, 50, "Keluar", RED, (255, 100, 100))
    
    # Footer
    footer_text = "Dibuat oleh Kelompok PBL-115"
    draw_text(screen, footer_text, (WIDTH//2, HEIGHT - 30), GRAY, 20)
    
    # Credits (smaller text)
    credits = [
        "Berkat Tua Siallagan | Adhyca Hafeez Wibowo",
        "Nayla Nur Nabila | Suci Aqila Nst",
        "Hermansa | Ray Refaldo"
    ]
    
    for i, credit in enumerate(credits):
        draw_text(screen, credit, (WIDTH//2, HEIGHT - 80 + i*20), GRAY, 16)
    
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            start_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
            
            if start_button.is_clicked(mouse_pos, event):
                return PLAYING
            if exit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
        
        start_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def show_game_over(score, best_score):
    screen.fill(WHITE)
    
    # Game Over text
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    game_over_shadow = game_over_font.render("GAME OVER", True, (200, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    screen.blit(game_over_shadow, (game_over_rect.x+3, game_over_rect.y+3))
    screen.blit(game_over_text, game_over_rect)
    
    # Score display
    draw_text(screen, f"Skor Anda: {score}", (WIDTH//2, HEIGHT//3 + 70), BLACK, 36)
    draw_text(screen, f"Skor Tertinggi: {best_score}", (WIDTH//2, HEIGHT//3 + 120), BLACK, 36)
    
    # Buttons
    retry_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Coba Lagi", GREEN, (100, 255, 100))
    menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, "Menu Utama", BLUE, (100, 100, 255))
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 190, 200, 50, "Keluar", RED, (255, 100, 100))
    
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            retry_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
            
            if retry_button.is_clicked(mouse_pos, event):
                return PLAYING
            if menu_button.is_clicked(mouse_pos, event):
                return MENU
            if exit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
        
        retry_button.draw(screen)
        menu_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def show_pause_screen():
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Pause text
    pause_font = pygame.font.Font(None, 72)
    pause_text = pause_font.render("PAUSE", True, WHITE)
    pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(pause_text, pause_rect)
    
    # Buttons
    resume_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Lanjutkan", GREEN, (100, 255, 100), WHITE)
    menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, "Menu Utama", BLUE, (100, 100, 255), WHITE)
    
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    return PLAYING
                
            resume_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
            
            if resume_button.is_clicked(mouse_pos, event):
                return PLAYING
            if menu_button.is_clicked(mouse_pos, event):
                return MENU
        
        resume_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def game_loop():
    # Game variables
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 50
    score = 0
    lives = 5
    object_speed = base_object_speed
    last_speed_increase = pygame.time.get_ticks()
    use_cursor = False
    game_state = PLAYING
    particles = []
    best_score = load_best_score()
    
    # Single falling object
    falling_object = {
        'x': random.randint(0, WIDTH - object_width),
        'y': -object_height,
        'speed': object_speed,
        'color': random.choice([RED, BLUE, YELLOW, PURPLE, ORANGE])
    }
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                use_cursor = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSED
                elif event.key == pygame.K_p:
                    game_state = PAUSED if game_state == PLAYING else PLAYING
        
        if game_state == PLAYING:
            # Player controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
                use_cursor = False
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed
                use_cursor = False
            
            # Mouse control
            if use_cursor:
                mouse_x, _ = pygame.mouse.get_pos()
                player_x = mouse_x - player_width // 2
                player_x = max(0, min(WIDTH - player_width, player_x))
            
            # Update falling object
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            obj_rect = pygame.Rect(falling_object['x'], falling_object['y'], object_width, object_height)
            
            falling_object['y'] += falling_object['speed']
                
            # Check if object is caught
            if player_rect.colliderect(obj_rect):
                score += 1
                particles.extend(create_particles(
                    falling_object['x'] + object_width//2, 
                    falling_object['y'] + object_height//2, 
                    falling_object['color']
                ))
                if catch_sound:
                    catch_sound.play()
                
                # Reset object
                falling_object['y'] = -object_height
                falling_object['x'] = random.randint(0, WIDTH - object_width)
                falling_object['color'] = random.choice([RED, BLUE, YELLOW, PURPLE, ORANGE])
            
            # Check if object missed
            elif falling_object['y'] > HEIGHT:
                lives -= 1
                particles.extend(create_particles(
                    falling_object['x'] + object_width//2, 
                    HEIGHT, 
                    (255, 0, 0, 128)
                ))
                if miss_sound:
                    miss_sound.play()
                
                # Reset object
                falling_object['y'] = -object_height
                falling_object['x'] = random.randint(0, WIDTH - object_width)
                falling_object['color'] = random.choice([RED, BLUE, YELLOW, PURPLE, ORANGE])
                
                if lives <= 0:
                    if score > best_score:
                        best_score = score
                        save_best_score(best_score)
                    game_state = GAME_OVER
            
            # Gradually increase difficulty
            current_time = pygame.time.get_ticks()
            if current_time - last_speed_increase > cooldown:
                object_speed += object_speed_increment
                falling_object['speed'] = object_speed
                last_speed_increase = current_time
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for p in particles:
                p.update()
        
        # Drawing
        screen.fill(WHITE)
        
        # Draw particles
        for p in particles:
            p.draw(screen)
        
        # Draw player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height), border_radius=5)
        pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height), 2, border_radius=5)  # Border
        
        # Draw falling object
        pygame.draw.rect(screen, falling_object['color'], (falling_object['x'], falling_object['y'], object_width, object_height), border_radius=5)
        pygame.draw.rect(screen, BLACK, (falling_object['x'], falling_object['y'], object_width, object_height), 1, border_radius=5)  # Border
        
        # Draw HUD
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 60))
        pygame.draw.line(screen, BLACK, (0, 60), (WIDTH, 60), 2)
        
        draw_text(screen, f"Skor: {score}", (20, 30), BLACK, 32, "topleft")
        draw_text(screen, f"Nyawa: {lives}", (WIDTH//2, 30), BLACK, 32)
        draw_text(screen, f"Tertinggi: {best_score}", (WIDTH - 20, 30), BLACK, 32, "topright")
        
        # Draw speed indicator
        speed_percentage = min(100, (object_speed - base_object_speed) / (base_object_speed * 3) * 100)
        pygame.draw.rect(screen, RED, (20, HEIGHT - 30, 200 * (speed_percentage/100), 20))
        pygame.draw.rect(screen, BLACK, (20, HEIGHT - 30, 200, 20), 1)
        draw_text(screen, "Kecepatan", (120, HEIGHT - 20), BLACK, 16)
        
        # Draw pause hint
        if random.random() < 0.01 and game_state == PLAYING:  # Occasionally show hint
            draw_text(screen, "Tekan ESC atau P untuk pause", (WIDTH//2, HEIGHT - 20), GRAY, 20)
        
        pygame.display.flip()
        
        # Handle game states
        if game_state == GAME_OVER:
            next_state = show_game_over(score, best_score)
            if next_state == PLAYING:
                # Reset game
                player_x = WIDTH // 2 - player_width // 2
                score = 0
                lives = 5
                object_speed = base_object_speed
                falling_object['speed'] = object_speed
                last_speed_increase = pygame.time.get_ticks()
                falling_object['y'] = -object_height
                falling_object['x'] = random.randint(0, WIDTH - object_width)
                falling_object['color'] = random.choice([RED, BLUE, YELLOW, PURPLE, ORANGE])
                game_state = PLAYING
            elif next_state == MENU:
                return MENU
        elif game_state == PAUSED:
            next_state = show_pause_screen()
            if next_state == PLAYING:
                game_state = PLAYING
            elif next_state == MENU:
                return MENU
        
        clock.tick(FPS)

# Main game loop
def main():
    current_state = MENU
    
    while True:
        if current_state == MENU:
            current_state = show_menu()
        elif current_state == PLAYING:
            current_state = game_loop()
        elif current_state == GAME_OVER:
            current_state = show_game_over(0, load_best_score())

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()