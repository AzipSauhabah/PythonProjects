import os
import random
import pygame
from pygame.locals import *
from src.enemy.unit.enemy import Enemy
from src.enemy.weapon.enemy_missile import EnemyWeaponMissile

ANIMATION_STEP = 15  # Time between each animation sprite

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class MissileBot(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        """Creates a MissileBot, capable of shooting missiles upward."""
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)
        self.hp = 6
        self.can_shoot = False
        self.idle_animation = True
        self.launch_animation = False
        self.stand_y = y - 28
        self.idle_y = y
        self.y0 = y
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
        if self.facing == 'right':
            for i in range(3):
                images.append([False, self.load_image(f"sprites/enemy_giru{i+1}r.gif")])
            images.append([False, self.load_image("sprites/enemy_giru2r.gif")])
        else:
            for i in range(6):
                images.append([False, self.load_image(f"sprites/enemy_transformer{i+1}.gif")])
            for i in range(4):
                images.append([False, self.load_image(f"sprites/enemy_transformer_launch{i+1}.gif")])
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
        animation_step = 10
        self.animation_counter += 1
        if self.hit_animation:
            self.hit_timer()

        if self.idle_animation:
            self.update_idle_animation(animation_step)
        else:
            self.update_launch_animation(animation_step)

        self.update_rect()
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        self.blit_image(surface)

    def update_idle_animation(self, animation_step):
        """Update the idle animation frames."""
        for i in range(len(self.images) + 1):
            if i == len(self.images) and self.animation_counter > (i + 1) * animation_step:
                self.image = self.images[0][1]
            elif self.animation_counter > (i + 1) * animation_step and not self.images[i][0]:
                self.images[i][0] = True
                self.image = self.images[i][1]
        if self.animation_counter >= self.animation_counter_max:
            self.animation_counter = 0
            for i in range(len(self.images)):
                self.images[i][0] = False

    def update_launch_animation(self, animation_step):
        """Update the launch animation frames."""
        for i in range(6, len(self.images)):
            if self.animation_counter > (i + 1) * animation_step and not self.images[i][0]:
                self.images[i][0] = True
                self.image = self.images[i][1]
                if i == 6:
                    self.rect.y = self.y0 - 11
                elif i >= 7:
                    self.rect.y = self.y0 - 35
        if self.animation_counter > 150:
            self.can_shoot = True

    def update_rect(self):
        """Update the rect to fix moving hitboxes."""
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect(x=x, y=y)

    def blit_image(self, surface):
        """Blit the image to the surface."""
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
        if self.can_shoot and -800 < self.rect.x - target_x < 800:
            return EnemyWeaponMissile(self.rect.x + 30, self.rect.y - 50, 150, random_aim=random.randint(0, 4) * 5)

    def flip_sprite(self):
        """Flip the sprite from right to left or left to right. Also changes the facing."""
        self.facing = 'right' if self.facing == 'left' else 'left'
        self.images = self.load_images()

    def siege_mode(self):
        """Allows attacks to commence once in siege mode."""
        self.unpause()
        self.idle_animation = False
