import math
import os
import pygame
from src.enemy.weapon.enemy_wpn import EnemyWeapon

ANIMATION_STEP = 3  # Time between each animation sprite

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class EnemyWeaponMissile(EnemyWeapon):
    def __init__(self, x, y, t1, play_sound=True, random_aim=0):
        """Creates a missile that launches upward and falls down."""
        super().__init__(x, y, 0, 0, play_sound)
        self.random_aim = random_aim
        self.t1 = t1
        self.shoot_images = self.load_images()
        self.animation_counter = 0
        self.x0, self.y0 = x, y

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(project_root_dir, path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_images(self):
        """Load all images for future use."""
        shoot_images = []
        for i in range(7):
            if i == 2:
                shoot_images.append(self.load_image("sprites/enemy_transformer_wpn_135.gif"))
            if i == 5:
                shoot_images.append(self.load_image("sprites/enemy_transformer_wpn_225.gif"))
            shoot_images.append(self.load_image(f"sprites/enemy_transformer_wpn_{i * 30 + 90}.gif"))
        self.image = shoot_images[0]
        return shoot_images

    def draw(self, surface):
        """Draws to screen."""
        if self.animation_counter < self.t1:
            self.update_animation_frame()
            self.move()
            self.animation_counter += 1
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def update_animation_frame(self):
        """Update the current frame of animation based on the counter."""
        frames = [
            (0, 25, 0), (25, 35, 1), (35, 43, 2), (42, 50, 3),
            (50, 51, 4), (51, 59, 5), (59, 67, 6), (67, 77, 7)
        ]
        for start, end, index in frames:
            if start <= self.animation_counter < end:
                self.image = self.shoot_images[index]
        if self.animation_counter >= self.x1:
            self.image = self.shoot_images[8]

    def move(self):
        """Move the missiles in an upside-down parabola trajectory with some randomness."""
        t = self.animation_counter
        self.rect.x -= 1
        if 0 <= t < (50 + self.random_aim):
            self.rect.y -= math.sqrt(math.sqrt(abs(50 - t)))
        else:
            self.rect.y += math.sqrt(math.sqrt(abs(t - 50)))
