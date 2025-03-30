import os
import pygame
from pygame.locals import *
from src.enemy.weapon.enemy_wpn import EnemyWeapon

ANIMATION_COUNTER_MAX = 200  # Time after which animation is looped (back to the starting animation)
DEAD_COUNTER_MAX = 70  # Time after which the death animation ends

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, eid=0, animation_counter_max=30, dead_counter_max=60, animation_counter=0):
        """A basic enemy unit."""
        super().__init__()
        self.id = eid
        self.hp = 1
        self.dead = False
        self.can_shoot = True
        self.mute = False
        self.idle_animation = True
        self.facing = 'left'
        self.invincible = False
        self.image = self.load_image("sprites/black.gif")
        self.images, self.dead_images = [], []
        self.load_images()
        self.load_dead_images()
        self.death_sound = pygame.mixer.Sound(self.load_sound_path('sounds/enemy_dead.wav'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_counter = animation_counter
        self.dead_counter = 0
        self.animation_counter_max = animation_counter_max
        self.dead_counter_max = dead_counter_max
        self.hit_counter = 0
        self.hit_animation = False
        self.out_of_screen = False

    def load_image(self, path):
        """Load an image and set the colorkey to black."""
        image_path = os.path.join(os.path.dirname(__file__), '../../..', path)
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_sound_path(self, path):
        """Construct the path for sound files."""
        return os.path.join(os.path.dirname(__file__), '../../..', path)

    def draw(self, surface):
        """Draw the enemy to the screen."""
        if not self.dead:
            self.animate()
            self.update_rect()
            self.image.set_colorkey(pygame.Color(0, 0, 0))
            self.draw_image(surface)
        else:
            self.handle_death(surface)

    def animate(self):
        """Handle the enemy's animation."""
        animation_step = 15
        self.animation_counter += 1
        if self.hit_animation:
            self.hit_timer()
        if self.idle_animation:
            self.update_animation_frames()

    def update_animation_frames(self):
        """Update the animation frames."""
        animation_step = 15
        for i in range(len(self.images) + 1):
            if i == len(self.images) and self.animation_counter > (i + 1) * animation_step:
                self.image = self.images[0][1]
            elif self.animation_counter > (i + 1) * animation_step and not self.images[i][0]:
                self.images[i][0] = True
                self.image = self.images[i][1]
        if self.animation_counter > self.animation_counter_max:
            self.animation_counter = 0
            for i in range(len(self.images)):
                self.images[i][0] = False

    def update_rect(self):
        """Update the rect to fix moving hitboxes."""
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect(x=x, y=y)

    def draw_image(self, surface):
        """Blit the image to the surface."""
        if not self.hit_animation:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y), None, pygame.BLEND_RGBA_ADD)

    def handle_death(self, surface):
        """Handle the death animation."""
        dead_step = 10
        if self.dead_counter == 0 and not self.mute:
            self.death_sound.play()
        self.dead_counter += 2
        self.move(-1, 0, bypass=True)
        for i in range(len(self.dead_images)):
            if (i + 1) * dead_step < self.dead_counter < (i + 2) * dead_step:
                self.image = self.dead_images[i]
        if self.dead_counter < self.dead_counter_max:
            self.image.set_colorkey(pygame.Color(0, 0, 0))
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def death(self, sound=True):
        """Kill the enemy."""
        self.dead = True
        self.can_shoot = False
        if not sound:
            self.mute = True

    def shoot(self, target_x, target_y, charged=False):
        """Shoot a projectile at the unit."""
        if self.facing == 'right':
            if self.can_shoot and -800 < self.rect.x - target_x < 0:
                return EnemyWeapon(self.rect.x + self.image.get_width(), self.rect.y, target_x, target_y)
        elif self.facing == 'left':
            if self.can_shoot and 0 < self.rect.x - target_x < 800:
                return EnemyWeapon(self.rect.x, self.rect.y, target_x, target_y)

    def move(self, x, y, bypass=False):
        """Move the enemy."""
        if self.dead_counter == 0 or bypass:
            self.rect.x += x
            self.rect.y += y

    def hit_timer(self):
        """Handle the hit animation timer."""
        self.hit_counter += 1
        if self.hit_counter > 5:
            self.hit_counter = 0
            self.hit_animation = False

    def take_damage(self, damage):
        """Handle damage taken by the enemy."""
        self.hp -= damage
        if self.hp <= 0:
            self.death()
        elif not self.hit_animation:
            self.hit_animation = True

    def pause(self):
        """Pause the idle animation."""
        self.idle_animation = False

    def unpause(self):
        """Unpause the idle animation."""
        self.idle_animation = True

    def flip_sprite(self):
        """Flip the sprite from left to right or vice versa."""
        self.facing = 'right' if self.facing == 'left' else 'left'
        self.load_images()

    def load_images(self):
        """Load all images for future use."""
        pass

    def load_dead_images(self):
        """Load all images for the death animation."""
        self.dead_images = []
        for i in range(6):
            self.dead_images.append(self.load_image(f"sprites/enemy_dead{i + 1}.gif"))
