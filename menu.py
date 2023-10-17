import pygame as pg
import sys


class Menu:
    def __init__(self, back_img, punkts, punkts_back, font, colorS, colorF, colorFS, screen, win, volume, draw_text,
                 ambient):
        self.back_img = back_img
        self.punkts = punkts
        self.punkts_back = punkts_back
        self.font = font
        self.colorS = colorS
        self.colorF = colorF
        self.colorFS = colorFS
        self.screen = screen
        self.win = win
        self.draw_text = draw_text
        self.ambient = ambient
        self.volume = volume
        self.x = 440
        self.y = 210
        self.h = 30
        self.w = 300
        self.r = 15

    def draw_slider(self, volume):
        self.volume = volume
        pg.draw.rect(self.screen, (self.colorF), (self.x, self.y, self.volume * self.w, self.h))
        pg.draw.rect(self.screen, (self.colorS), (self.x, self.y, self.w, self.h), 2)
        pg.draw.circle(self.screen, (self.colorFS), (int(self.x + self.volume * self.w), int(self.y + self.h / 2)),
                       self.r)
        self.draw_text(self.screen, "Громкость", (self.colorS), self.x, self.y - 40)
        self.draw_text(self.screen, f"{int(self.volume * 100)}%", (self.colorS), self.x + self.w + 20, self.y)
        return self.volume

    def handle_input(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.x - 10 <= mouse_x <= self.x + self.w + 10 and self.y - 5 <= mouse_y <= self.y + self.h + 5 and mouse_pressed:
            self.volume = (mouse_x - self.x) / self.w
            self.volume = max(0.0, min(1.0, self.volume))
        return float(self.volume)

    def render(self, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                self.screen.blit(self.font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.screen.blit(self.font.render(i[2], 1, i[3]), (i[0] + 5, i[1] + 5))

    def back_render(self, num_punkt):
        for i in self.punkts_back:
            if num_punkt == i[5]:
                self.screen.blit(self.font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.screen.blit(self.font.render(i[2], 1, i[3]), (i[0] + 5, i[1] + 5))

    def menu(self, main_name, go_name, score, death):
        score = int(score)
        done = True
        punkt = -1
        name = main_name
        toggle = False
        while done:
            if self.back_img == None:
                surf = pg.Surface(self.win)
                surf.fill((0, 0, 0))
                self.screen.blit(surf, (0, 0))
            else:
                self.screen.blit(self.back_img, (0, 0))

            if death:
                self.draw_text(self.screen, 'Вы проиграли', (self.colorS), self.screen.get_width() / 2, 10)
                self.draw_text(self.screen, 'Пройдено: ' + str(score), (self.colorS), self.screen.get_width() / 2, 80)

            mp = pg.mouse.get_pos()

            if toggle:
                self.draw_text(self.screen, "Настройка звука", (self.colorS), 120, 210)
                volume = self.handle_input()
                volume = self.draw_slider(volume)
                self.ambient.set_volume(volume)
                for i in self.punkts_back:
                    if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                        punkt = i[5]
                    else:
                        punkt = -1
                    self.back_render(punkt)
            else:
                for i in self.punkts:
                    if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                        punkt = i[5]
                        name = i[2]
                    self.render(punkt)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        if name == go_name:
                            death = False
                            return death
                        done = False
                    elif punkt == 1:
                        toggle = True
                    elif punkt == len(self.punkts) + 1:
                        toggle = False
                    elif punkt == 2:
                        sys.exit()

            pg.display.flip()
