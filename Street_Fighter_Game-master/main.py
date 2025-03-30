# Street Fighter Game
# By: Azip Sauhabah
# Date: 27/10/2024
# Version: 1.0
# Description: This is the main file for the Street Fighter Game.

import pygame
from pygame import mixer
from fighter import Fighter
import os

# Initialize Pygame and Mixer
def init_game():
    pygame.init()
    mixer.init()

# Set up the game window
def create_game_window(width, height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Street Fighter!")
    return screen

# Load assets dynamically
def load_assets():
    current_dir = os.path.dirname(__file__)
    
    assets = {
        "music": os.path.join(current_dir, 'assets', 'audio', 'music.mp3'),
        "sword_fx": os.path.join(current_dir, "assets", "audio", "sword.wav"),
        "staff_fx": os.path.join(current_dir, "assets", "audio", "magic.wav"),
        "bg_image": os.path.join(current_dir, "assets", "images", "background", "background.jpg"),
        "warrior_sheet": os.path.join(current_dir, "assets", "images", "warrior", "Sprites", "warrior.png"),
        "wizard_sheet": os.path.join(current_dir, "assets", "images", "wizard", "Sprites", "wizard.png"),
        "victory_img": os.path.join(current_dir, "assets", "images", "icons", "victory.png"),
        "count_font": os.path.join(current_dir, "assets", "fonts", "turok.ttf"),
        "score_font": os.path.join(current_dir, "assets", "fonts", "turok.ttf")
    }
    
    return assets

# Load and play music
def setup_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

# Load sound effects
def load_sounds(sword_fx_path, staff_fx_path):
    sword_fx = pygame.mixer.Sound(sword_fx_path)
    sword_fx.set_volume(0.75)
    staff_fx = pygame.mixer.Sound(staff_fx_path)
    staff_fx.set_volume(0.75)
    return sword_fx, staff_fx

# Load images
def load_images(assets):
    bg_image = pygame.image.load(assets["bg_image"]).convert_alpha()
    warrior_sheet = pygame.image.load(assets["warrior_sheet"]).convert_alpha()
    wizard_sheet = pygame.image.load(assets["wizard_sheet"]).convert_alpha()
    victory_img = pygame.image.load(assets["victory_img"]).convert_alpha()
    return bg_image, warrior_sheet, wizard_sheet, victory_img

# Load fonts
def load_fonts(assets):
    count_font = pygame.font.Font(assets["count_font"], 80)
    score_font = pygame.font.Font(assets["score_font"], 30)
    return count_font, score_font

# Draw text
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Draw background
def draw_bg(screen, bg_image, width, height):
    scaled_bg = pygame.transform.scale(bg_image, (width, height))
    screen.blit(scaled_bg, (0, 0))

# Draw fighter health bar
def draw_health_bar(screen, health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, (400 * ratio), 30))

# Main game loop
def game_loop(screen, clock, fps, assets):
    WARRIOR_DATA = [162, 4, [72, 56]]
    WIZARD_DATA = [250, 3, [112, 107]]
    score = [0, 0]
    round_over = False
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    ROUND_OVER_COOLDOWN = 2000
    
    setup_music(assets["music"])
    sword_fx, staff_fx = load_sounds(assets["sword_fx"], assets["staff_fx"])
    bg_image, warrior_sheet, wizard_sheet, victory_img = load_images(assets)
    count_font, score_font = load_fonts(assets)
    
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, [10, 8, 1, 7, 7, 3, 7], sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, [8, 8, 1, 8, 8, 3, 7], staff_fx)
    
    run = True
    while run:
        clock.tick(fps)
        draw_bg(screen, bg_image, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_health_bar(screen, fighter_1.health, 20, 20)
        draw_health_bar(screen, fighter_2.health, 580, 20)
        draw_text(screen, "P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text(screen, "P2: " + str(score[1]), score_font, RED, 580, 60)
        
        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(screen, str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
        
        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, [10, 8, 1, 7, 7, 3, 7], sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, [8, 8, 1, 8, 8, 3, 7], staff_fx)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    
    pygame.quit()

# Run the game
if __name__ == "__main__":
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    FPS = 60
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    
    init_game()
    screen = create_game_window(SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    assets = load_assets()
    game_loop(screen, clock, FPS, assets)
