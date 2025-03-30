import os
import pygame
from src.enemy.weapon.enemy_wpn import EnemyWeapon

ANIMATION_STEP = 3  # Time between each animation sprite

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class EnemyWeaponBeam(EnemyWeapon):
    def __init__(self, x, y, target_x, target_y, play_sound=True, random_aim=0):
        """Creates a circular red bullet used by regular mobs/enemies."""
        super().__init__(x, y, target_x, target_y, play_sound)
        self.random_aim = random_aim
        self.shoot_images = self.load_images()

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(project_root_dir, path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_images(self):
        """Load all images for future use."""
        shoot_images = []
        for i in range(3):
            shoot_images.append(self.load_image(f"sprites/enemy_boss_wpn2_shoot{i + 1}.gif"))
        self.image = shoot_images[0]
        return shoot_images

    def draw(self, surface):
        """Draws to screen."""
        self.animation_counter += 1
        self.update_animation()
        surface.blit(self.image, (self.rect.x - 15, self.rect.y))
        self.move()

    def update_animation(self):
        """Update the animation frames."""
        for i in range(len(self.shoot_images)):
            if self.animation_counter > (i + 1) * ANIMATION_STEP:
                self.image = self.shoot_images[i]
        if self.animation_counter > ANIMATION_STEP * 3:
            self.animation_counter = 0

    def move(self):
        """Move the beam in the -x direction with a random y offset."""
        self.rect.x -= 4
        self.rect.y += self.random_aim
        self.move_counter += 2
        if self.rect.x < self.oos_x or self.rect.y < self.oos_y:
            self.out_of_screen = True
