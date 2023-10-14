import pygame as pg


class Character:
    def __init__(self, x, y, force, speed, divider, screen, walk_left, walk_right):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.is_jumping = False
        self.force = force
        self.jump_count = force
        self.anim_count = 0
        self.walk_left = walk_left
        self.walk_right = walk_right
        self.delta_time = 0
        self.divider = divider

    def update(self, keys, delta_time, is_jump):
        self.delta_time = delta_time
        if keys[pg.K_LEFT] and self.x > 50:
            self.x -= self.speed
        elif keys[pg.K_RIGHT] and self.x < 200:
            self.x += self.speed

        if not self.is_jumping:
            if keys[pg.K_UP]:
                self.is_jumping = True
        else:
            if self.jump_count >= -self.force:
                if self.jump_count > 0:
                    self.y -= self.jump_count * 0.5
                else:
                    self.y += self.jump_count * -0.5
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.force

    def draw(self, keys):
        self.anim_count += self.delta_time / self.divider
        if self.anim_count >= len(self.walk_left):
            self.anim_count = 0

        index = int(self.anim_count)

        if keys[pg.K_LEFT]:
            self.screen.blit(self.walk_left[index], (self.x, self.y))
        elif keys[pg.K_UP]:
            self.screen.blit(self.walk_right[0], (self.x, self.y))
        else:
            self.screen.blit(self.walk_right[index], (self.x, self.y))

    def get_rect(self):
        return self.walk_left[0].get_rect(topleft=(self.x, self.y))
