"""R-Typo Project
Azip Sauhabah
"""

import os
import sys
import pygame

# Add the 'src' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Construct the path dynamically
current_dir = os.path.dirname(__file__)
music_path = os.path.join(current_dir, 'sounds', 'music', 'medley.mp3')

from src import game
from src.player.unit import Player

FPS = 60

# A hack to get pyinstaller to work
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

def initialize_pygame():
    pygame.init()
    pygame.mixer.init()

def create_window(width, height):
    return pygame.display.set_mode((width, height))

def load_assets():
    assets = {
        'r_type_logo': pygame.image.load(os.path.join(current_dir, "img/main_logo.png")).convert(),
        'enter_logo': pygame.image.load(os.path.join(current_dir, "img/x-Enter.gif")).convert(),
        'bg': pygame.image.load(os.path.join(current_dir, "img/space_bg.png")),
        'start_sound': pygame.mixer.Sound(os.path.join(current_dir, 'sounds/start.ogg')),
    }
    assets['r_type_logo'].set_colorkey(pygame.Color(0, 0, 0))
    return assets

def setup_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, 0.2)  # loop music

def main():
    initialize_pygame()
    window_size = (800, 600)
    surface = create_window(window_size[0], window_size[1])
    pygame.display.set_caption("R-Typo")

    setup_music(music_path)
    assets = load_assets()
    ship = Player(window_size[0] // 2 - 30, window_size[1] // 2 - 15)
    fps_clock = pygame.time.Clock()

    # Counters / timers
    text_timer, start_timer = 0, 0
    scroll_x = 0
    game_ready = False

    # Alpha screen (for smooth fade-in/fade-outs)
    alpha_surface = pygame.Surface(window_size)
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)
    alpha = 0

    while True:
        surface.fill((0, 0, 0))
        surface.blit(assets['bg'], (scroll_x, 0))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 800, 200))
        pygame.draw.rect(surface, (0, 0, 0), (0, 400, 800, 200))
        surface.blit(assets['r_type_logo'], (window_size[0] / 2 - assets['r_type_logo'].get_width() / 2, window_size[1] / 4 - assets['r_type_logo'].get_height() / 2 - 50))

        ship.draw(surface)

        text_timer += 1
        if text_timer < 50:
            surface.blit(assets['enter_logo'], (window_size[0] / 2 - assets['enter_logo'].get_width() / 2, window_size[1] / 2 - assets['enter_logo'].get_height() / 2 + 200))
        elif text_timer > 100:
            text_timer = 0

        scroll_x -= 1
        if scroll_x < -800:
            scroll_x = 0

        if game_ready:
            ship.move(surface, 10, 0, bypass_wall=True)  # animation
            start_timer += 1  # start countdown until game mode
            text_timer = 1  # don't blink the text anymore
            if start_timer == 100:
                pygame.mixer.music.fadeout(1000)
            if 200 > start_timer > 100:
                alpha += 5
                alpha_surface.set_alpha(alpha)  # fade out
            elif start_timer >= 200:
                game.start_level(surface)
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # enter key
                    game_ready = True
                    assets['start_sound'].play()
                    start_timer = 0

        surface.blit(alpha_surface, (0, 0))
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()
