import pygame
import os
import random
from tkinter import *
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile
import json
import math
import sys

from scripts.entities import Entity, Hero, Enemy, Body
from scripts.utils import load_image, load_images, Animation, ImageButton, Bullet, Projectile
from scripts.tilemap import Tilemap
from scripts.rain import Drop
from scripts.weapon import Sword
from scripts.levels import Level

RENDER_SCALE = 2.0

class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption('Ninja in the road')

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height - 50), pygame.WINDOWMAXIMIZED)

        self.display = pygame.Surface((self.screen_width // 2, self.screen_height // 2), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = {
            'player/idle': Animation(load_images('player/idle')),
            'player/jump': Animation(load_images('player/jump')),
            'player/fall': Animation(load_images('player/fall')),
            'player/hit': Animation(load_images('player/hit')),
            'player/run': Animation(load_images('player/run')),
            'player/die': Animation(load_images('player/die'), 10),
            'player/combo1': Animation(load_images('player/combo1')),
            'player/combo2': Animation(load_images('player/combo2')),
            'player/combo3': Animation(load_images('player/combo3')),
            'player/wall_slide': Animation(load_images('player/wall_slide')),
            'menu_background': pygame.transform.scale(load_image('SCS_AssetPackage_01/SCS_Background_Nighttime_01.png'), (self.screen_width, self.screen_height)),
            'background': pygame.transform.scale(load_image('SCS_AssetPackage_01/SCS_Background_Nighttime_01.png'), (960, 540)),
            'zavod_0': load_images('tiles/white_zavod_0'),
            'button_start': load_images('btn/start'),
            'drop': load_image('drop.png'),
            'enemy/idle': Animation(load_images('enemy/idle')),
            'enemy/walk': Animation(load_images('enemy/walk')),
            'enemy/run': Animation(load_images('enemy/run')),
            'enemy/shoot': Animation(load_images('enemy/shoot'), img_dur=10),
            'enemy/die': Animation(load_images('enemy/die'), img_dur=10, loop=False),
            'spawners': load_images('tiles/spawners'),
            'bullet': Animation(load_images('bullet'), img_dur=10),
            'projectile': load_image('projectile.png'),
            'line': load_image('line.png'),
            'finish': load_images('tiles/finish'),
        }

        self.sfx = {
            'rain': pygame.mixer.Sound('data/sfx/rain.mp3'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.mp3'),
            'sword': pygame.mixer.Sound('data/sfx/sword.mp3'),
            'die': pygame.mixer.Sound('data/sfx/die.mp3'),
            'bullet_sword': pygame.mixer.Sound('data/sfx/bullet_sword.mp3'),
            'bullet': pygame.mixer.Sound('data/sfx/bullet.mp3'),
            'hero_die': pygame.mixer.Sound('data/sfx/hero_die.mp3'),
        }

        self.sfx['rain'].set_volume(0.2)
        self.sfx['ambience'].set_volume(0.5)
        self.sfx['sword'].set_volume(0.2)
        self.sfx['die'].set_volume(0.1)
        self.sfx['bullet_sword'].set_volume(0.1)
        self.sfx['bullet'].set_volume(0.1)
        self.sfx['hero_die'].set_volume(0.2)

        self.sfx['rain'].play(-1)
        self.sfx['ambience'].play(-1)

        self.tilemap = Tilemap(self)

        self.enemies = []

        self.player = Hero(self, (0, 0), (15, 32))

        self.transition = -30

        self.level_path = None
    
    def main_menu(self):
        buttons = {
            'start': ImageButton((self.screen_width - 150) // 2, (self.screen_height - 50) // 2 - 100, 150, 50, 'start', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            'editor': ImageButton((self.screen_width - 150) // 2, (self.screen_height - 50) // 2, 150, 50, 'editor', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            'leave': ImageButton((self.screen_width - 150) // 2, (self.screen_height - 50) // 2 + 100, 150, 50, 'leave', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            'from directory': ImageButton((self.screen_width - 500) // 2, (self.screen_height - 100) // 2 + 50, 500, 100, 'from directory', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            '1': ImageButton((self.screen_width - 50) // 2 - 100, (self.screen_height - 50) // 2 - 200, 50, 50, '1', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            '2': ImageButton((self.screen_width - 50) // 2, (self.screen_height - 50) // 2 - 200, 50, 50, '2', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            '3': ImageButton((self.screen_width - 50) // 2 + 100, (self.screen_height - 50) // 2 - 200, 50, 50, '3', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            'create new map': ImageButton((self.screen_width - 500) // 2, (self.screen_height - 100) // 2 - 100, 500, 100, 'create new map', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
            'open map': ImageButton((self.screen_width - 500) // 2, (self.screen_height - 100) // 2 + 50, 500, 100, 'open map', self.assets['button_start'][0], hover_image=self.assets['button_start'][1]),
        }

        boxes = {
            'standart levels': pygame.Surface((500, 100)),
        }
        boxes['standart levels'].fill((136, 0, 21))

        text_font = pygame.font.Font('data/Font/ofont.ru_Fixedsys.ttf', 45)
        text_surface = text_font.render('standart levels', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=boxes['standart levels'].get_rect(topleft=((self.screen_width - boxes['standart levels'].get_width()) // 2, (self.screen_height - boxes['standart levels'].get_height()) // 2 - 300)).center)

        levels = False
        
        self.finished = False

        mapping = False

        drops = []

        while True:
            self.screen.blit(self.assets['menu_background'], (0, 0))

            weight = random.randint(1, 2)
            drops.append(Drop(self.assets['drop'], (random.randint(0, int(self.screen_width * 1.5)), 0), (2 * weight, 4 * weight), weight))

            for drop in drops:
                drop.update()
                if self.screen_height < drop.rect.y:
                    drops.remove(drop)
                    continue
                drop.render(self.screen)

            mouse_pos = pygame.mouse.get_pos()

            if levels:
                for name in ('1', '2', '3', 'from directory'):
                    buttons[name].update(mouse_pos)
                    buttons[name].render(self.screen)
                self.screen.blit(boxes['standart levels'], ((self.screen_width - boxes['standart levels'].get_width()) // 2, (self.screen_height - boxes['standart levels'].get_height()) // 2 - 300))
                self.screen.blit(text_surface, text_rect)
            elif mapping:
                for name in ('create new map', 'open map'):
                    buttons[name].update(mouse_pos)
                    buttons[name].render(self.screen)
            else:
                for name in ('start', 'editor', 'leave'):
                    buttons[name].update(mouse_pos)
                    buttons[name].render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if levels:
                        for name in ('1', '2', '3', 'from directory'):
                            buttons[name].handle_event()
                    elif mapping:
                        for name in ('create new map', 'open map'):
                            buttons[name].handle_event()
                    else:
                        for name in ('start', 'editor', 'leave'):
                            buttons[name].handle_event()

                if event.type == pygame.USEREVENT:
                    if event.button == buttons['start']:
                        levels = True
                    elif event.button == buttons['leave']:
                        pygame.quit()
                        sys.exit()
                    elif event.button == buttons['editor']:
                        mapping = True
                    elif event.button == buttons['from directory']:
                        f = askopenfile(initialdir=os.getcwd() + '/data/maps')
                        if f:
                            self.level_path = f.name
                            self.run()
                    elif event.button == buttons['create new map']:
                        self.editor()
                    elif event.button == buttons['open map']:
                        f = askopenfile()
                        if f:
                            self.level_path = f.name
                            self.editor()
                    elif event.button == buttons['1']:
                        self.level_path = 'data/maps/standart/level1.json'
                        self.run()
                    elif event.button == buttons['2']:
                        self.level_path = 'data/maps/standart/level2.json'
                        self.run()
                    elif event.button == buttons['3']:
                        self.level_path = 'data/maps/standart/level3.json'
                        self.run()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def editor(self):
        if self.level_path:
            self.tilemap.load(self.level_path)

        buttons = {
            'save': ImageButton(self.display.get_width() - 85, 10, 70, 20, 'save', self.assets['button_start'][0], font_size=20, hover_image=self.assets['button_start'][1]),
            'continue': ImageButton((self.display.get_width() - 150) // 2, (self.display.get_height() - 50) // 2, 200, 50, 'continue', self.assets['button_start'][0], hover_image=self.assets['button_start'][1], font_size=20),
            'main_menu': ImageButton((self.display.get_width() - 150) // 2, (self.display.get_height() - 50) // 2 - 100, 200, 50, 'go to main menu', self.assets['button_start'][0], hover_image=self.assets['button_start'][1], font_size=20),
            }
        

        active = 0

        scroll = [0, 0]

        movement = [False, False, False, False]

        tile_list = ['zavod_0', 'spawners', 'finish']
        tile_group = 0
        tile_variant = 0

        shift = False

        offgrid = False

        clicking = False

        hovered_btn = False

        right_clicking = False

        paused = False

        while True:
            active = max(0, active - 1)
            if paused:
                mouse_pos = list(pygame.mouse.get_pos())
                mouse_pos[0] = mouse_pos[0] // RENDER_SCALE
                mouse_pos[1] = mouse_pos[1] // RENDER_SCALE

                
                buttons['continue'].update(mouse_pos)
                buttons['continue'].render(self.display)
                buttons['main_menu'].update(mouse_pos)
                buttons['main_menu'].render(self.display)
            else:
                self.display.fill((0, 0, 0))

                scroll[0] += ((movement[1] - movement[0]) * 2)
                scroll[1] += ((movement[3] - movement[2]) * 2)
                
                render_scroll = (int(scroll[0]), int(scroll[1]))

                self.tilemap.render(self.display, render_scroll)

                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)

                tile_pos = (int((mouse_pos[0] + scroll[0]) // self.tilemap.tile_size), int((mouse_pos[1] + scroll[1]) // self.tilemap.tile_size))

                tile_pos = (int(mouse_pos[0] + scroll[0]) // self.tilemap.tile_size, int(mouse_pos[1] + scroll[1]) // self.tilemap.tile_size)
                
                current_tile_img = self.assets[tile_list[tile_group]][tile_variant].copy()
                current_tile_img.set_alpha(100)

                buttons['save'].update(mouse_pos)
                buttons['save'].render(self.display)
                hovered_btn = buttons['save'].is_hovered

                if clicking:
                    if not offgrid and not hovered_btn and not active:
                        self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': tile_list[tile_group], 'variant': tile_variant, 'pos': tile_pos} 
                
                if not offgrid:
                    self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - scroll[0], tile_pos[1] * self.tilemap.tile_size - scroll[1]))
                else:
                    self.display.blit(current_tile_img, mouse_pos)
                
                if right_clicking:
                    tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                    if tile_loc in self.tilemap.tilemap:
                        del self.tilemap.tilemap[tile_loc]
                    else:
                        for tile in self.tilemap.offgrid_tiles:
                            tile_img = self.assets[tile['type']][tile['variant']]
                            tile_rect = pygame.Rect(tile['pos'][0] - scroll[0], tile['pos'][1] - scroll[1], tile_img.get_width(), tile_img.get_height())
                            if tile_rect.collidepoint(mouse_pos):
                                self.tilemap.offgrid_tiles.remove(tile)
                
                self.display.blit(self.assets['line'], (0, 500 - render_scroll[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not active:
                        if not offgrid:
                            clicking = True
                        else:
                            if not hovered_btn:
                                self.tilemap.offgrid_tiles.append({'type': tile_list[tile_group], 'variant': tile_variant, 'pos': (mouse_pos[0] + render_scroll[0], mouse_pos[1] + render_scroll[1])})
                    
                    if event.button == 2:
                        offgrid = not offgrid
                    
                    if event.button == 3:
                        right_clicking = True

                    if shift:
                        if event.button == 4:
                            tile_group = (tile_group - 1) % len(tile_list)
                            tile_variant = 0
                        if event.button == 5:
                            tile_group = (tile_group + 1) % len(tile_list)
                            tile_variant = 0
                    else:
                        if event.button == 4:
                            tile_variant = (tile_variant - 1) % len(self.assets[tile_list[tile_group]])
                        if event.button == 5:
                            tile_variant = (tile_variant + 1) % len(self.assets[tile_list[tile_group]])

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        clicking = False
                    
                    if event.button == 3:
                        right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        movement[1] = True
                    if event.key == pygame.K_a:
                        movement[0] = True
                    if event.key == pygame.K_w:
                        movement[2] = True
                    if event.key == pygame.K_s:
                        movement[3] = True
                    if event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                        shift = True
                    if event.key == pygame.K_t:
                        self.tilemap.auto_tiling()
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        movement[1] = False
                    if event.key == pygame.K_a:
                        movement[0] = False
                    if event.key == pygame.K_w:
                        movement[2] = False
                    if event.key == pygame.K_s:
                        movement[3] = False
                    if event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                        shift = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in buttons.values():
                        button.handle_event()

                if event.type == pygame.USEREVENT:
                    if event.button == buttons['save']:
                        active = 10
                        f = asksaveasfile(initialfile = 'Untitled.json', defaultextension=".json",filetypes=[("Map","*.json")], initialdir='D:/project/Python/ninja_in_the_road/data/maps')
                        if f:
                            json.dump({'tile_size': self.tilemap.tile_size, 'tilemap': self.tilemap.tilemap, 'offgrid': self.tilemap.offgrid_tiles}, f)
                            f.close()

                    if event.button == buttons['continue']:
                        paused = False

                    if event.button == buttons['main_menu']:
                        self.main_menu()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)


    def run(self):
        if self.finished:
            self.main_menu()

        self.tilemap.load(self.level_path)

        buttons = {
            'continue': ImageButton((self.display.get_width() - 150) // 2, (self.display.get_height() - 50) // 2, 200, 50, 'continue', self.assets['button_start'][0], hover_image=self.assets['button_start'][1], font_size=20),
            'main_menu': ImageButton((self.display.get_width() - 150) // 2, (self.display.get_height() - 50) // 2 - 100, 200, 50, 'go to main menu', self.assets['button_start'][0], hover_image=self.assets['button_start'][1], font_size=20),
        }

        self.acceleration = [False, False]

        self.scroll = [0, 0]

        drops = []

        self.enemies.clear()

        sword = Sword([0, 0], self.sfx['sword'])

        paused = False

        bodies = []

        self.kill = 0
        self.player.killed = False

        bullets = []

        projectiles = []

        screenshake = 0

        self.player.pos = [0, 0]

        finish = self.tilemap.extract([('finish', 0)], True)

        if finish:
            finish = pygame.Rect(finish[0]['pos'][0], finish[0]['pos'][1], self.tilemap.tile_size, self.tilemap.tile_size)

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 1:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (10, 29)))

        while True:

            if self.kill:
                    self.kill += 1
                    if self.kill == 2:
                        self.sfx['hero_die'].play()
                        screenshake = 16
                    if self.kill > 10:
                        self.transition += 1
                    if self.kill > 70:
                        self.transition = -30
                        self.kill = 0
                        self.run()

            if paused:
                mouse_pos = list(pygame.mouse.get_pos())
                mouse_pos[0] = mouse_pos[0] // RENDER_SCALE
                mouse_pos[1] = mouse_pos[1] // RENDER_SCALE

                for button in buttons.values():
                    button.update(mouse_pos)
                    button.render(self.display)
            else:
                self.display.blit(self.assets['background'], (0, 0))

                if self.transition < 0:
                    self.transition += 1
                
                screenshake = max(0, screenshake - 1)

                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 20

                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                    
                weight = random.randint(1, 2)
                drops.append(Drop(self.assets['drop'], (random.randint(render_scroll[0], render_scroll[0] + int(self.display.get_width() * 1.5)), render_scroll[1]), (2 * weight, 4 * weight), weight))

                if finish:
                    if finish.colliderect(self.player.rect()):
                        if not self.kill:
                            self.kill = 1
                            self.finished = True

                for drop in drops:
                    kill = drop.update(self.tilemap)
                    if kill or render_scroll[1] + self.display.get_height() < drop.rect.y or render_scroll[1] > drop.rect.y:
                        drops.remove(drop)
                        continue
                    drop.render(self.display, render_scroll)
                
                for body in bodies:
                    body.animation.update()
                    body.render(self.display, render_scroll)

                for enemy in self.enemies:
                    barier_x = [(render_scroll[0] - self.display.get_width() // 2), (render_scroll[0] + self.display.get_width() * 1.5)]
                    barier_y = [(render_scroll[1] - self.display.get_height() // 2), (render_scroll[1] + self.display.get_height() * 1.5)]

                    if barier_x[1] > enemy.pos[0] > barier_x[0] and barier_y[1] > enemy.pos[1] > barier_y[0]:
                        enemy.update(self.tilemap)
                        enemy.render(self.display, render_scroll)

                        if sword.hit and sword.rect().colliderect(enemy.rect()):
                            bodies.append(Body(self, enemy.pos, enemy.flip))
                            self.enemies.remove(enemy)
                            screenshake = 16
                            self.sfx['die'].play()

                        elif enemy.rect().colliderect(self.player.rect()):
                            if not self.kill:
                                self.kill = 1
                                self.player.killed = True
                            
                        elif enemy.shooting == 50:
                            bullets.append(Bullet(self.assets['bullet'].copy(), (enemy.pos[0] if enemy.direction == -1 else enemy.pos[0] + 17, enemy.pos[1] + 11), (2, 2), enemy.direction))
                            self.sfx['bullet'].play()

                        enemy.check_hero(self.player, self.tilemap)

                for bullet in bullets:
                    kill = bullet.update(self.tilemap)
                    if kill or (sword.hit and sword.rect().colliderect(bullet.rect())):
                        for i in range(10):
                            projectiles.append(Projectile(self.assets['projectile'], bullet.pos, random.random() * 360, speed=random.random(), leave=random.random()*30))
                        self.sfx['bullet_sword'].play()
                        bullets.remove(bullet)
                        if sword.hit and not kill:
                            screenshake = 16
                        continue
                    bullet.render(self.display, render_scroll)
                    
                    if bullet.rect().colliderect(self.player.rect()):
                        bullets.remove(bullet)
                        if not self.kill:
                            self.kill = 1
                            self.player.killed = True
                
                for projectile in projectiles:
                    projectile.update()
                    if projectile.leave < 0:
                        projectiles.remove(projectile)
                        continue
                    projectile.render(self.display, render_scroll)
                
                if (sword.combat1 or sword.combat2 or sword.combat3):
                    self.player.update(self.tilemap, (0, 0))
                    self.player.render(self.display, render_scroll)
                    if not self.player.flip:
                        sword.pos[0] = self.player.pos[0] + self.player.animation.img().get_width() // 2
                    else:
                        sword.pos[0] = self.player.pos[0]
                        if sword.combat3:
                            sword.pos[0] -= 41
                        elif sword.combat2:
                            sword.pos[0] -= 36
                        elif sword.combat1:
                            sword.pos[0] -= 30

                    sword.pos[1] = self.player.pos[1]
                    sword.update(self.player)

                elif not self.kill:
                    self.player.update(self.tilemap, (self.acceleration[1] - self.acceleration[0], 0))
                    self.player.render(self.display, render_scroll)
                    if not self.player.flip:
                        sword.pos = [self.player.rect().centerx, self.player.pos[1]]
                    else:
                        sword.pos = [self.player.rect().x - self.player.rect().width // 2, self.player.pos[1]]
                    sword.update(self.player)

                elif self.kill:
                    self.player.update(self.tilemap, (0, 0))
                    self.player.render(self.display, render_scroll)
                    self.player.killed = True

                self.tilemap.render(self.display, render_scroll)

                if self.player.pos[1] > 500 and not self.kill:
                    self.kill = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sword.strike(self.player)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.acceleration[1] = True
                    if event.key == pygame.K_a:
                        self.acceleration[0] = True
                    if event.key in (pygame.K_w, pygame.K_SPACE):
                            if not (sword.combat1 or sword.combat2 or sword.combat3 or self.kill):
                                self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.acceleration[1] = False
                    if event.key == pygame.K_a:
                        self.acceleration[0] = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in buttons.values():
                        button.handle_event()

                if event.type == pygame.USEREVENT:
                    if event.button == buttons['continue']:
                        paused = False

                    if event.button == buttons['main_menu']:
                        self.main_menu()
            
            
            
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 20)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            screenshake_offset = (random.random() * screenshake, random.random() * screenshake)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)

wow = Game().main_menu()