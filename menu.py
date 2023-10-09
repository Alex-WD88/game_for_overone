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
        pg.draw.rect(self.screen, (255, 255, 255), (100, 300, 300, 50), 3)
        pg.draw.rect(self.screen, (255, 255, 255), (100, 300, self.volume * 300, 50))
        pg.draw.circle(self.screen, (255, 255, 255), (int(100 + self.volume * 300), 325), 15)
        self.draw_text(self.screen, "Громкость", (255, 255, 255), 100, 260)
        self.draw_text(self.screen, f"{int(self.volume * 100)}%", (255, 255, 255), 420, 310)

    def handle_input(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if 100 <= mouse_x <= 400 and 300 <= mouse_y <= 350 and mouse_pressed:
            self.volume = (mouse_x - 100) / 300
            self.volume = max(0, min(1, int(self.volume)))
        return self.volume

    def render(self, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                self.screen.blit(self.font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.screen.blit(self.font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        punkt = 0
        while done:
            self.screen.fill((0, 100, 200))

            mp = pg.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(punkt)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    # if event.key == pg.K_ESCAPE:
                    # sys.exit()
                    # done = False
                    if event.key == pg.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pg.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        self.draw_slider()
                        volume = self.handle_input()
                        self.ambient.set_volume(volume)
                    elif punkt == 2:
                        sys.exit()

            pg.display.flip()
