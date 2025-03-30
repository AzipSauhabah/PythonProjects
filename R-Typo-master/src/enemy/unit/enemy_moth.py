import os
import pygame
from src.enemy.unit.enemy import Enemy

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Moth(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0, start_angle=180):
        """A single moth unit that usually flies in packs."""
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)
        self.images = self.load_images(start_angle)
        self.rect = self.image.get_rect(x=x, y=y)
        self.animation_counter = animation_counter
        self.hp = 3
        self.can_shoot = False
        self.idle_animation = False

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(project_root_dir, path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_images(self, start_angle=180):
        """Load all images for future use based on the starting angle."""
        images = []
        if start_angle == 180:
            for i in range(4):
                if i == 2:
                    images.append([False, self.load_image("sprites/enemy_moth_225.gif")])
                images.append([False, self.load_image(f"sprites/enemy_moth_{i * 30 + 180}.gif")])
            self.image = images[4][1]
        elif start_angle == 90:
            for i in range(4):
                if i == 2:
                    images.append([False, self.load_image("sprites/enemy_moth_135.gif")])
                images.append([False, self.load_image(f"sprites/enemy_moth_{i * 30 + 90}.gif")])
            self.image = images[4][1]
        return images
