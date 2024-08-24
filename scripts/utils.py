import pygame
import os
import math

PATH = 'data/images/'
def load_image(path):
    img = pygame.image.load(PATH + path)
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(PATH + path), key=len):
        images.append(load_image(path + '/' + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True) -> None:
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def img(self):
        return self.images[int(self.frame) // self.img_dur]
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

class ImageButton:
    def __init__(self, x, y, width, height, text, image, font_size=45, hover_image=None, sound=None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.transform.scale(image, (self.width, self.height))

        if hover_image:
            self.hover_image = pygame.transform.scale(hover_image, (self.width, self.height))
        else:
            self.hover_image = None


        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = sound

        self.is_hovered = False

        self.current_image = image

        self.font_size = font_size
    
    def render(self, surf):
        surf.blit(self.current_image, self.rect.topleft)

        font = pygame.font.Font('data/Font/ofont.ru_Fixedsys.ttf', self.font_size)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surf.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_image = self.hover_image if self.is_hovered and self.hover_image else self.image
    
    def handle_event(self):
        if self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

class Bullet:
    def __init__(self, anim, pos, size, direction):
        self.animation = anim
        self.velocity = [3, 0]
        self.pos = list(pos)
        self.direction = direction
        self.flip = False if self.direction == 1 else True
        self.size = list(size)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap):
        tile_loc = str(int(self.pos[0] // tilemap.tile_size)) + ';' + str(int(self.pos[1] // tilemap.tile_size))
        if tile_loc in tilemap.tilemap:
            return True
        
        self.pos[0] += self.velocity[0] * self.direction
        self.pos[1] += self.velocity[1]

        self.animation.update()
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
class Projectile:
    def __init__(self, img, pos, degree, speed=1, leave=60) -> None:
        self.pos = list(pos)
        self.leave = leave
        self.img = img

        self.velocity = [math.cos(degree) * speed, math.sin(degree) * speed]
    
    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.leave -= 1
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))