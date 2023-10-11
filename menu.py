import pygame as pg
import sys


class Menu:
    def __init__(self, punkts, font, screen, volume, draw_text, ambient):
        self.punkts = punkts
        self.font = font
        self.screen = screen
        self.volume = volume
        self.draw_text = draw_text
        self.ambient = ambient

    def draw_slider(self):
        x = 100
        y = 300
        h = 50
        w = 300
        pg.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 3)
        pg.draw.rect(self.screen, (255, 255, 255), (x, y, self.volume * w, h))
        pg.draw.circle(self.screen, (255, 255, 255), (int(x + self.volume * y), w + h / 2), 15)
        self.draw_text(self.screen, "Громкость", (255, 255, 255), x, y - 40)
        self.draw_text(self.screen, f"{int(self.volume * 100)}%", (255, 255, 255), x + w + 10, w + 10)

    def handle_input(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if 100 <= mouse_x <= 400 and 300 <= mouse_y <= 350 and mouse_pressed:
            self.volume = (mouse_x - 100) / 300
            self.volume = max(0.0, min(1.0, self.volume))
        return float(self.volume)

    def render(self, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                self.screen.blit(self.font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.screen.blit(self.font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        punkt = 0
        toggle = False
        while done:
            self.screen.fill((0, 100, 200))
            mp = pg.mouse.get_pos()

            if toggle:
                self.draw_slider()
                volume = self.handle_input()
                self.ambient.set_volume(volume)
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
                    if punkt == 1:
                        toggle = True
                    elif punkt == 2:
                        sys.exit()

            pg.display.flip()
