import os
import pygame
from src.enemy.unit.enemy import Enemy

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class SitBot(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        """A sitting robot that looks like the Predator from Alien vs. Predator. It is tanky, with high HP."""
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)
        self.images = self.load_images()
        self.rect = self.image.get_rect(x=x, y=y)
        self.hp = 15
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
            images.append(
                [False, self.load_image(f"sprites/enemy_sitbot_stand{i+1}.gif")]
            )
        self.image = images[0][1]
        return images
