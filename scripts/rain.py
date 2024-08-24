import pygame

class Drop:
    def __init__(self, image, pos=(0, 0), size=(2, 4), weight=1):
        self.size = list(size)
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.weight = weight
    
    def update(self, tilemap=None):
        self.rect.x = self.rect.x - 2
        self.rect.y = self.rect.y + self.size[1]
        entity_rect = self.rect
        if tilemap:
            for tile in tilemap.physics_tiles_around((self.rect.x, self.rect.y)):
                if entity_rect.colliderect(tile):
                    return True
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))