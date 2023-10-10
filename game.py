import pygame as pg
import os
import character
import enemy as en
import menu

# позиция персонажа по x
pos_x = 150

PLAYER_SPEED = 3
FORCE_JUMP = 15
ENEMY_SPEED = 6

# корреляция fps
divider = 100

# Скорость игры
FPS = 60

# Размеры игрового окна
win = win_width, win_height = 960, 540

WHITE = (255, 255, 255)
FON = (134, 168, 207)
TITLE = (38, 66, 90)
RES = (225, 203, 215)

score = 0

img_size = 45, 64
img_size_en = 32, 32

# Позиции по оси Y
pos_y = 410
pos_y_en = 425

pg.init()
clock = pg.time.Clock()

# само окно
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("overone Game")
icon_path = os.path.join('images', 'icon.png')
icon = pg.image.load(icon_path).convert_alpha()
pg.display.set_icon(icon)

# шрифт
font = pg.font.Font('fonts/vcr-osd-mono.ttf', 30)
walk_right = [
    pg.transform.scale(pg.image.load(f'images/player/w_{i + 1}.png'),
                       img_size).convert_alpha() for i in range(4)
]
walk_left = [pg.transform.flip(walk_right[i], True, False) for i in range(4)]

# музыка окружения
volume = 0.03
ambient = pg.mixer.Sound('sounds/ambient/bk_m.mp3')
ambient.set_volume(volume)

# задник
bg_imgs = []
for i in range(1, 7):
    bg_img = pg.transform.scale(pg.image.load(f'images/background/bg_{i}.png'), win).convert_alpha()
    bg_imgs.append(bg_img)

bg_x = [0, 0, 0, 0, 0, 0]

# враг
img_enemy = pg.transform.scale(pg.image.load('images/ghost.png'), img_size_en).convert_alpha()
enemy_list_in_game = []

# таймер появления врагов
enemy_timer = pg.USEREVENT + 1
pg.time.set_timer(enemy_timer, 2500)  # в данном случае 2,5 секунды

lose_font = font.render('Вы проиграли', False, TITLE)
restart_font = font.render('Перезагрузить уровень?', False, RES)
restart_font_rect = restart_font.get_rect(topleft=(180, 200))


def draw_text(screen, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


player = character.Character(pos_x, pos_y, FORCE_JUMP, PLAYER_SPEED, divider, screen, walk_left, walk_right)
enemies = []

# создаем меню
punkts = [(120, 140, u'Играть', (250, 250, 30), (250, 30, 250), 0),
          (120, 210, u'Настройка звука', (250, 250, 30), (250, 30, 250), 1),
          (120, 280, u'Выход', (250, 250, 30), (250, 30, 250), 2)]
game = menu.Menu(punkts, font, screen, volume, draw_text, ambient)

# подкласс настройки
punkts2 = [(120, 140, u'Настройка звука', (250, 250, 30), (250, 30, 250), 0),
(120, 280, u'Назад', (250, 250, 30), (250, 30, 250), 1)]
settings = menu.SettingsMenu(punkts2, font, screen, volume, draw_text, ambient)

# Игровой цикл
running = True
gameplay = True
game.menu()
while running:

    dt = clock.tick(FPS)
    fps = clock.get_fps()

    screen.blit(bg_imgs[0], (bg_x[0], 0))
    for i in range(1, len(bg_imgs)):
        screen.blit(bg_imgs[i], (bg_x[i], 0))
        screen.blit(bg_imgs[i], (bg_x[i] + win_width, 0))

    if gameplay:
        ambient.play()
        keys = pg.key.get_pressed()
        player.update(keys, dt)
        player.draw(keys)
        score += 1 / 10
        draw_text(screen, f'Счет: {int(score)}', WHITE, 10, 10)
        # print(int(score))
        # print(fps)

        for enemy in enemies:
            enemy.update()
            enemy.draw()

            if player.get_rect().colliderect(enemy.get_rect()):
                # print('enemy touch you')
                gameplay = False

            if enemy.x < -10:
                enemies.remove(enemy)

        for i in range(1, len(bg_imgs)):
            speed = i
            if speed == 1:
                speed = len(bg_imgs) - 1
            bg_x[i] -= speed
            if bg_x[i] <= -win_width:
                bg_x[i] = 0

    else:
        ambient.stop()
        screen.fill(FON)
        screen.blit(lose_font, (180, 100))
        screen.blit(restart_font, restart_font_rect)
        gameplay = False
        # game.menu()
        mouse = pg.mouse.get_pos()
        if restart_font_rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            pos_x = 150
            pos_y = 410
            score = 0
            player.x = pos_x
            player.y = pos_y
            gameplay = True
            enemies.clear()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                # running = False
                game.menu()
        elif event.type == pg.USEREVENT + 1:
            enemies.append(en.Enemy(win_width + 2, pos_y_en, ENEMY_SPEED, img_enemy, screen))

    pg.display.flip()

pg.quit()
