import os
import pygame
from pygame.locals import *
from src.enemy.unit.enemy import Enemy

ANIMATION_STEP = 15  # Time between each animation sprite

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Giru(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        """A walking robot."""
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)
        self.hp = 6
        self.can_shoot = True
        self.idle_animation = True
        self.stand_y = y - 14
        self.idle_y = y
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
            for i in range(3):
                images.append([False, self.load_image(f"sprites/enemy_giru{i+1}.gif")])
            images.append([False, self.load_image("sprites/enemy_giru2.gif")])
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
        stand = False
        self.animation_counter += 1
        if self.hit_animation:
            self.hit_timer()
        if self.idle_animation:
            self.update_animation_frames()
            stand = self.update_stand_y(stand)
            self.update_rect()
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        if not self.hit_animation:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y), None, BLEND_RGBA_ADD)

    def update_animation_frames(self):
        """Update the animation frames."""
        if ANIMATION_STEP > self.animation_counter >= 0:
            self.images[0][0] = True
            self.image = self.images[0][1]
        elif ANIMATION_STEP * 3 > self.animation_counter >= ANIMATION_STEP:
            self.images[1][0] = True
            self.image = self.images[1][1]
        elif ANIMATION_STEP * 4 > self.animation_counter >= ANIMATION_STEP * 3:
            self.images[2][0] = True
            self.image = self.images[2][1]
        elif ANIMATION_STEP * 6 >= self.animation_counter >= ANIMATION_STEP * 4:
            self.images[3][0] = True
            self.image = self.images[3][1]
        if self.animation_counter >= self.animation_counter_max:
            self.animation_counter = 0
            for img in self.images:
                img[0] = False

    def update_stand_y(self, stand):
        """Update the stand_y position."""
        if stand:
            self.rect.y = self.stand_y
            stand = False
        else:
            self.rect.y = self.idle_y
        return stand

    def update_rect(self):
        """Update the rect to fix moving hitboxes."""
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect(x=x, y=y)

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
