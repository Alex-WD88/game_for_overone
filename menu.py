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
        self.volume = volume
        self.draw_text = draw_text
        self.ambient = ambient

    def draw_slider(self, x, y, h, w, r):
        pg.draw.rect(self.screen, (self.colorF), (x, y, self.volume * w, h))
        pg.draw.rect(self.screen, (self.colorS), (x, y, w, h), 2)
        pg.draw.circle(self.screen, (self.colorFS), (int(x + self.volume * w), int(y + h / 2)), r)
        self.draw_text(self.screen, "Громкость", (self.colorS), x, y - 40)
        self.draw_text(self.screen, f"{int(self.volume * 100)}%", (self.colorS), x + w + 20, y)

    def handle_input(self, x, y, h, w):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if x - 10 <= mouse_x <= x + w + 10 and y - 5 <= mouse_y <= y + h + 5 and mouse_pressed:
            self.volume = (mouse_x - x) / w
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

    def menu(self):
        done = True
        punkt = -1
        toggle = False
        x = 440
        y = 210
        h = 30
        w = 300
        r = 15
        while done:
            if self.back_img == None:
                surf = pg.Surface(self.win)
                surf.fill((0, 0, 0))
                surf.set_alpha(6000)
                self.screen.blit(surf, (0, 0))
            else:
                self.screen.blit(self.back_img, (0, 0))
            mp = pg.mouse.get_pos()

            if toggle:
                self.draw_text(self.screen, "Настройка звука", (self.colorS), 120, 210)
                self.draw_slider(x, y, h, w, r)
                volume = self.handle_input(x, y, h, w)
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
                    self.render(punkt)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        toggle = True
                    elif punkt == len(self.punkts) + 1:
                        toggle = False
                    elif punkt == 2:
                        sys.exit()

            pg.display.flip()
