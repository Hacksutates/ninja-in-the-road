import pygame
import random

BLOCKS_FOR_ENEMY = {(-1, 1): 1,
                    (1, 1): -1,}


class Entity:
    def __init__(self, game, e_type, pos, size, max_vel) -> None:
        self.pos = list(pos)
        self.game = game
        self.size = size
        self.type = e_type
        self.velocity = [0, 0]

        self.action = ''
        self.set_action('idle')
        self.flip = False
        self.anim_offset = [0, 0]

        self.last_movement = [0, 0]

        self.min_vel1 = max_vel[0]
        self.min_vel2 = max_vel[1]
        self.max_vel = self.min_vel1

        self.running = False

        self.collision = {'up': False,
                          'down': False,
                          'right': False,
                          'left': False,
                          }
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
    def update(self, tilemap, acceleration=(0, 0)):
        
        self.collision = {'up': False,
                          'down': False,
                          'right': False,
                          'left': False,
                          }
        if not self.running:
            if self.velocity[0] > self.min_vel1 or self.velocity[0] < -self.min_vel1:
                self.max_vel = self.min_vel2
            else:
                self.max_vel = self.min_vel1
        
        self.velocity[0] += acceleration[0] * 0.5
        
        if self.velocity[0] > 0:
            self.velocity[0] = min(self.velocity[0], self.max_vel)
        elif self.velocity[0] < 0:
            self.velocity[0] = max(self.velocity[0], self.max_vel * -1)
        
        if not self.running:
            if self.max_vel > self.min_vel1:
                if self.velocity[0] > 0:
                    self.velocity[0] = min(max(self.velocity[0] - 0.6, 0), self.max_vel)
                elif self.velocity[0] < 0:
                    self.velocity[0] = max(min(self.velocity[0] + 0.6, 0), self.max_vel * -1)


        frame_movement = (self.velocity[0], self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for tile in tilemap.physics_tiles_around(self.pos):
            if entity_rect.colliderect(tile):
                if frame_movement[0] < 0:
                    entity_rect.left = tile.right
                    self.collision['left'] = True
                elif frame_movement[0] > 0:
                    entity_rect.right = tile.left
                    self.collision['right'] = True
                self.pos[0] = entity_rect.x
        
            

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for tile in tilemap.physics_tiles_around(self.pos):
            if entity_rect.colliderect(tile):
                if frame_movement[1] > 0:
                    entity_rect.bottom = tile.top
                    self.collision['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = tile.bottom
                    self.collision['up'] = True
                self.pos[1] = entity_rect.y
        
        if acceleration[0] > 0:
            self.flip = False
        if acceleration[0] < 0:
            self.flip = True

        self.last_movement = acceleration
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collision['down'] or self.collision['up']:
            self.velocity[1] = 0
        
        self.animation.update()

    
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Hero(Entity):
    def __init__(self, game, pos, size) -> None:
        super().__init__(game, 'player', pos, size, max_vel=[3.5, 10])

        self.force = 0

        self.jumps = 1
        self.wall_slide = False
        self.dashing = False
        self.dashing_cd = 10
        self.air_time = 0

        self.killed = False

        self.combat1 = 0
        self.combat2 = 0
        self.combat3 = 0
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, acceleration=(0, 0)):
        super().update(tilemap, acceleration=acceleration)

        self.air_time += 1
        if self.collision['down']:
            self.air_time = 0
            self.jumps = 1

        if acceleration[0] == 0:
            if self.air_time < 5:
                if self.velocity[0] > 0:
                    self.velocity[0] = min(max(self.velocity[0] - 0.5, 0), self.max_vel)
                elif self.velocity[0] < 0:
                    self.velocity[0] = max(min(self.velocity[0] + 0.5, 0), self.max_vel * -1)
            elif self.wall_slide:
                if self.velocity[0] > 0:
                    self.velocity[0] = min(max(self.velocity[0] - 1, 0), self.max_vel)
                elif self.velocity[0] < 0:
                    self.velocity[0] = max(min(self.velocity[0] + 1, 0), self.max_vel * -1)
            else:
                if self.velocity[0] > 0:
                    self.velocity[0] = min(max(self.velocity[0] - 0.1, 0), self.max_vel)
                elif self.velocity[0] < 0:
                    self.velocity[0] = max(min(self.velocity[0] + 0.1, 0), self.max_vel * -1)
        
        self.wall_slide = False
        if self.air_time > 4 and (self.collision['right'] or self.collision['left']):
            self.wall_slide = True
            self.jumps = 1
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collision['right']:
                self.flip = False
            elif self.collision['left']:
                self.flip = True
            self.anim_offset = [0, 0]
            self.set_action('wall_slide')
        

        if self.killed:
            self.set_action('die')
        elif not self.wall_slide:
            if self.combat3 > 0:
                if self.flip:
                    self.anim_offset = [-41, 0]
                self.anim_offset[1] = -11
                self.set_action('combo3')
            elif self.combat2 > 0:
                if self.flip:
                    self.anim_offset = [-36, 0]
                self.anim_offset[1] = 1
                self.set_action('combo2')
            elif self.combat1 > 0:
                if self.flip:
                    self.anim_offset = [-27, 0]
                self.anim_offset[1] = -4
                self.set_action('combo1')
            elif self.velocity[1] > 0.4:
                self.anim_offset = [0, 0]
                self.set_action('fall')
            elif self.air_time > 4:
                self.anim_offset = [0, -3]
                self.set_action('jump')
            elif acceleration[0] != 0:
                self.anim_offset = [0, 6]
                self.set_action('run')
            else:
                self.anim_offset = [0, 0]
                self.set_action('idle')
    
    def jump(self):
        if not self.wall_slide:
            if self.jumps == 1 and self.air_time < 5:
                self.jumps -= 1
                self.velocity[1] = -3
            return True
        else:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 10
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            if not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -10
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        return False
    

class Enemy(Entity):
    def __init__(self, game, pos, size) -> None:
        e_type = 'enemy'
        super().__init__(game, e_type, pos, size, max_vel=[1, 2])

        self.max_vel = 1

        self.running = False
        self.walking = 0
        self.direction = 1
        self.must_direction = 1

        self.angry = 0
        self.shooting = 0
    
    def update(self, tilemap):
        acceleration = [0, 0]

        if self.running:
            self.walking = 0
            self.max_vel = self.min_vel2
            acceleration = [self.direction, 0]
            
        if self.shooting > 0:
            acceleration = [0, 0]
            self.shooting -= 1

        if not self.running:
            if self.walking == 0:
                if random.randint(1, 100) == 100:
                    self.walking = random.randint(40, 200)
                    if self.must_direction != self.direction:
                        self.direction = self.must_direction
                    elif self.collision['left']:
                        self.direction = 1
                    elif self.collision['right']:
                        self.direction = -1
                    else:
                        self.direction = random.choice([-1, 1])
                    acceleration[0] = self.direction
            else:
                acceleration[0] = self.direction
        
        if self.check_under(tilemap, self.pos, self.direction):
            acceleration = [0, 0]
            self.running = False

        super().update(tilemap, acceleration=acceleration)

        if self.check_under(tilemap, self.pos, self.direction):
            self.walking = 0
            self.must_direction = self.direction * -1
        
        if self.collision['left'] or self.collision['right']:
            self.walking = 0
            self.running = False
            self.shooting = 0
            self.angry = 60

        if acceleration[0] == 0:
            if self.velocity[0] > 0:
                self.velocity[0] = min(max(self.velocity[0] - 0.5, 0), self.max_vel)
            elif self.velocity[0] < 0:
                self.velocity[0] = max(min(self.velocity[0] + 0.5, 0), self.max_vel * -1)

        self.walking = max(0, self.walking - 1)

        if self.shooting:
            self.set_action('shoot')    
        elif self.running:
            self.set_action('run')
        elif self.walking:
            self.set_action('walk')
        else:
            self.set_action('idle')

        self.running = False
        self.angry = max(0, self.angry - 1)
    
    def check_under(self, tilemap, pos, direction):
        return str(int((pos[0]) // tilemap.tile_size + direction)) + ';' + str(int((pos[1]) // tilemap.tile_size + 1)) not in tilemap.tilemap
    
    def check_hero(self, hero, tilemap):
        if abs(self.pos[0] - hero.pos[0]) < 200 and abs(self.pos[1] - hero.pos[1]) < 200:
            if not self.angry:
                if self.pos[0] - hero.pos[0] < 0 and self.direction == 1:
                    self.direction = 1
                    self.running = True
                    self.angry = 60
                elif self.pos[0] - hero.pos[0] > 0 and self.direction == -1:
                    self.direction = -1
                    self.running = True
                    self.angry = 60
            else:
                if self.pos[0] - hero.pos[0] < 0:
                    self.direction = 1
                    self.running = True
                    self.angry = 60
                elif self.pos[0] - hero.pos[0] > 0:
                    self.direction = -1
                    self.running = True
                    self.angry = 60

        if abs(self.pos[0] - hero.pos[0]) < 100 and abs(self.pos[1] - hero.pos[1]) < 100:
            if self.angry or (self.pos[0] - hero.pos[0] < 0 and self.direction == 1) or (self.pos[0] - hero.pos[0] > 0 and self.direction == -1):
                if self.shooting in (0, 1) and not (self.collision['left'] or self.collision['right']):
                    self.shooting = 70
                if self.pos[0] - hero.pos[0] < 0:
                    self.flip = False
                else:
                    self.flip = True

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Body:
    def __init__(self, game, pos, flip) -> None:
        self.game = game
        self.pos = list(pos)
        self.flip = flip
        self.action = ''
        self.type = 'enemy'
        self.set_action('die')
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))