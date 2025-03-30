import os
import pygame
from src.player.weapon.player_wpn import PlayerWeapon
from src.player.weapon.player_wpn_charged import PlayerWeaponCharged

# Define the project root directory globally
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Creates a player unit sprite."""
        super().__init__()
        self.image = self.load_image("sprites/player.gif")
        self.dead_images = self.load_dead_images()
        self.rect = self.image.get_rect(x=x, y=y)
        self.mask = pygame.mask.from_surface(self.image, 0)
        
        # Position to respawn at
        self.respawn_pos = (x, y)
        self.last_pos = (0, 0)  # for wall collision
        self.charged_beam = None
        
        # Variables
        self.dead = False
        self.dead_timer = 0
        self.invincible = False
        self.invincible_animation = False
        self.invincible_timer = 0

    def load_image(self, path):
        """Loads an image and sets the colorkey to black."""
        global project_root_dir  # Access the global project_root_dir
        image_path = os.path.join(project_root_dir, path)
        print(image_path)  # Check the full path
        image = pygame.image.load(image_path).convert()
        image.set_colorkey(pygame.Color(0, 0, 0))
        return image

    def load_dead_images(self):
        """Loads all images for the death animation."""
        return [self.load_image(f"sprites/player_dead{i+1}.gif") for i in range(6)]

    def draw(self, surface):
        """Draws to screen."""
        if not self.dead:
            if self.invincible:
                if self.invincible_animation:
                    self.invincible_timer += 1
                if self.invincible_timer % 5 == 0:
                    surface.blit(self.image, (self.rect.x, self.rect.y))
                if self.invincible_timer > 90:
                    self.invincible = False
                    self.invincible_timer = 0
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            self.animate_death(surface)

    def animate_death(self, surface):
        """Handles the death animation."""
        if self.dead_timer == 0:
            pygame.mixer.Sound('sounds/player_dead.ogg').play()
        self.dead_timer += 1
        death_step = 5
        for i in range(len(self.dead_images)):
            if (i+1) * death_step < self.dead_timer < (i+2) * death_step:
                self.image = self.dead_images[i]
        self.rect.x -= 1
        if self.dead_timer < 35:
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def death(self):
        """Kills the player unit."""
        self.dead = True
        if self.charged_beam:
            self.charged_beam.fail = True
            self.charged_beam.charge_sound.stop()

    def respawn(self):
        """Respawns the player unit at the respawn position with invincibility."""
        self.rect.topleft = self.respawn_pos
        self.dead = False
        self.dead_timer = 0
        self.be_invincible()
        self.image = self.load_image("sprites/player.gif")

    def shoot(self, beam_x, beam_y, charged=False):
        """Shoots a beam."""
        if charged:
            beam = PlayerWeaponCharged(beam_x, beam_y)
            beam.charging = True
            self.charged_beam = beam
        else:
            beam = PlayerWeapon(beam_x, beam_y)
        return beam

    def move(self, surface, x, y, bypass_wall=False):
        """Moves the player by altering the x and y coordinates."""
        if self.dead:
            return

        r_collide = self.rect.right > surface.get_width()
        l_collide = self.rect.left < 0
        t_collide = self.rect.top < 0
        b_collide = self.rect.bottom > surface.get_height() - 40

        if bypass_wall:
            self.rect.move_ip(x, y)
        else:
            if not ((r_collide and x > 0) or (l_collide and x < 0)):
                self.rect.x += x
                if self.charged_beam:
                    self.charged_beam.rect.x += x
            if not ((t_collide and y < 0) or (b_collide and y > 0)):
                self.rect.y += y
                if self.charged_beam:
                    self.charged_beam.rect.y += y

    def be_invincible(self, animation=True):
        """Grant invincibility to the player, with an optional flashing animation."""
        self.invincible = True
        self.invincible_animation = animation
