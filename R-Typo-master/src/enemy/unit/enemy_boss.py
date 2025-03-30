import os
import random
import pygame
from pygame.locals import *
from src.enemy.unit.enemy import Enemy
from src.enemy.weapon.enemy_beam import EnemyWeaponBeam

ANIMATION_STEP = 15  # Time between each animation sprite

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Boss(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=60, animation_counter=0):
        """The boss enemy unit."""
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)
        self.hp = 120
        self.can_shoot = True
        self.idle_animation = True
        self.stand_y = y - 14
        self.idle_y = y
        self.invincible = True
        self.images = self.load_images()
        self.rect = self.image.get_rect(x=x, y=y)
        self.animation_counter = animation_counter

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(project_root_dir, path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_images(self):
        """Load all images for future use."""
        images = []
        for i in range(3):
            images.append([False, self.load_image(f"sprites/enemy_boss{i+1}.gif")])
        self.image = images[0][1]
        return images

    def draw(self, surface):
        """Draws to screen."""
        if not self.dead:
            self.handle_alive_animation(surface)
        else:
            self.handle_death_animation(surface)

    def handle_alive_animation(self, surface):
        """Handle the animation when the enemy is alive."""
        self.animation_counter += 1
        if self.hit_animation:
            self.hit_timer()
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        if not self.hit_animation:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y), None, BLEND_RGBA_ADD)

    def handle_death_animation(self, surface):
        """Handle the animation when the enemy is dead."""
        dead_step = 10
        if self.dead_counter == 0 and not self.mute:
            self.death_sound.play()
        self.dead_counter += 2
        self.move(-1, 0, bypass=True)
        for i in range(len(self.dead_images)):
            if (i + 1) * dead_step < self.dead_counter < (i + 2) * dead_step:
                self.image = self.dead_images[i]
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        if self.dead_counter < self.dead_counter_max:
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self, target_x, target_y, charged=False):
        """Shoot a projectile at the unit."""
        if self.can_shoot and 0 < self.rect.x - target_x < 800:
            pygame.mixer.Sound(file="sounds/player_wpn2_shoot.ogg").play()
            return EnemyWeaponBeam(self.rect.x, self.rect.y, target_x, target_y, random_aim=random.randint(-1, 1))

    def move(self, x, y, bypass=False):
        """Move the enemy if the enemy is not dead."""
        if not self.dead or bypass:
            self.image = self.images[0][1] if x > 0 else self.images[1][1]
            self.rect.x += x
            self.rect.y += y
