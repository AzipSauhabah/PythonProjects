import os
import math
import pygame
from pygame.locals import *

ANIMATION_STEP = 3  # Time between each animation sprite

class EnemyWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x=0, target_y=0, play_sound=True):
        """Creates a circular red bullet used by regular mobs/enemies."""
        super().__init__()
        self.image = self.load_image("sprites/enemy_wpn1_shoot1.gif")
        self.shoot_images = self.load_images()
        self.mask = pygame.mask.from_surface(self.image, 0)
        self.rect = self.image.get_rect(x=x, y=y + 35)
        self.setup_trajectory(target_x, target_y)
        self.initialize_variables()

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(os.path.dirname(__file__), '../../..', path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_images(self):
        """Load all images for future use."""
        shoot_images = []
        for i in range(4):
            shoot_images.append(self.load_image(f"sprites/enemy_wpn1_shoot{i+1}.gif"))
        return shoot_images

    def setup_trajectory(self, target_x, target_y):
        """Calculate angle/trajectory of projectile."""
        self.x0, self.y0 = self.rect.x, self.rect.y  # Store origin coordinates
        x1, y1 = target_x - self.x0, target_y - self.y0
        magnitude = math.sqrt(x1 ** 2 + y1 ** 2)
        self.x1, self.y1 = x1 / magnitude, y1 / magnitude

    def initialize_variables(self):
        """Initialize variables for the weapon."""
        self.move_counter = 0
        self.charging = False
        self.draw_impact = False
        self.dead = False
        self.oos_x, self.oos_y = -1, -1
        self.animation_counter = 0
        self.impact_counter = 0
        self.damage = 1
        self.out_of_screen = False

    def draw(self, surface):
        """Draws to screen."""
        self.animation_counter += 1
        self.update_animation()
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.move()

    def update_animation(self):
        """Update the animation frames."""
        for i in range(len(self.shoot_images)):
            if self.animation_counter > (i + 1) * ANIMATION_STEP:
                self.image = self.shoot_images[i]
        if self.animation_counter > ANIMATION_STEP * 5:
            self.animation_counter = 0

    def move(self):
        """Move the projectile in the calculated trajectory."""
        self.rect.x = self.x0 + self.x1 * self.move_counter
        self.rect.y = self.y0 + self.y1 * self.move_counter
        self.move_counter += 2
        if self.rect.x < self.oos_x or self.rect.y < self.oos_y:
            self.out_of_screen = True

    def impact(self, surface):
        """Responsible for impact effects, i.e. animation and rectangle adjustments."""
        self.damage = 0  # Prevent damage from triggering multiple times
        impact_step = 2
        if self.out_of_screen:
            self.dead = True
        elif not self.dead:
            self.impact_counter += 1
            for i in range(len(self.impact_images)):
                if i * impact_step < self.impact_counter < (i + 1) * impact_step:
                    self.image = self.impact_images[i]
            if self.draw_impact:
                surface.blit(self.image, (self.rect.x + 15, self.rect.y - 10))
            if self.impact_counter > 6:
                self.dead = True

    def load_impact_images(self):
        """Load all images for the impact animation."""
        self.impact_images = []
        for i in range(4):
            self.impact_images.append(self.load_image(f"sprites/enemy_wpn1_impact{i+1}.gif"))
