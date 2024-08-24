import pygame

class Sword:
    def __init__(self, pos, sound):
        self.pos = list[pos]
        self.size = [0, 0]
        self.sound = sound

        self.combat1 = 0
        self.combat2 = 0
        self.combat3 = 0

        self.hit = False
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def strike(self, hero):
        if not self.combat1:
            self.sound.play()
            self.combat1 = 25
            hero.combat1 = 25
            self.size = [21, 36]
        
        elif not self.combat2 and 11 > self.combat1 > 0:
            self.sound.play()
            self.combat2 = 25
            self.combat1 = 25
            hero.combat2 = 25
            hero.combat1 = 25
            self.size = [25, 36]
        
        elif not self.combat3 and 11 > self.combat2 > 0:
            self.sound.play()
            self.combat3 = 50
            self.combat2 = 50
            self.combat1 = 50
            hero.combat3 = 50
            hero.combat2 = 50
            hero.combat1 = 50
            self.size = [28, 36]
    
    def update(self, hero):
        self.combat1 = max(0, self.combat1 - 1)
        self.combat2 = max(0, self.combat2 - 1)
        self.combat3 = max(0, self.combat3 - 1)

        hero.combat1 = max(0, hero.combat1 - 1)
        hero.combat2 = max(0, hero.combat2 - 1)
        hero.combat3 = max(0, hero.combat3 - 1)

        self.hit = False

        if 23 > self.combat1 > 13:
            self.hit = True
        
        if 23 > self.combat2 > 13:
            self.hit = True
        
        if 38 > self.combat3 > 17:
            self.hit = True

