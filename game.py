import pygame as pg
import os
import character
import enemy as en
import menu

# позиция персонажа по x
pos_x = 150

PLAYER_SPEED = 3
FORCE_JUMP = 16
ENEMY_SPEED = 6

# корреляция fps
divider = 100

# Скорость игры
FPS = 60

# Размеры игрового окна
win = win_width, win_height = 960, 540

WHITE = (255, 255, 255)
M_FONTS = (201, 192, 187)
HM_FONTS = (173, 156, 147)
TITLE = (248, 248, 255)
FM_FIELD = (101, 0, 11)
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
death = False
enemies = []

# создаем меню
name_menu = ['Играть', 'Продолжить игру', 'Новая игра']

mainMenu_img = pg.transform.scale(pg.image.load('images/menu/mainMenu.jpg'), win).convert_alpha()
gameOver_img = pg.transform.scale(pg.image.load('images/menu/GameOver.jpg'), win).convert_alpha()
pause_img = pg.transform.scale(pg.image.load('images/menu/pause.jpg'), win).convert_alpha()

punkts = [(120, 140, name_menu[0], (M_FONTS), (HM_FONTS), 0),
          (120, 210, u'Настройка звука', (M_FONTS), (HM_FONTS), 1),
          (120, 280, u'Выход', (M_FONTS), (HM_FONTS), 2)]
punkts_back = [(120, 280, u'назад', (M_FONTS), (HM_FONTS), len(punkts) + 1)]
game = menu.Menu(mainMenu_img, punkts, punkts_back, font, TITLE, FM_FIELD, M_FONTS, screen, win, volume, draw_text,
                 ambient)
for i in range(len(name_menu)):
    if name_menu[i] == name_menu[1]:
        punkts = [(120, 140, name_menu[i], (M_FONTS), (HM_FONTS), 0),
                  (120, 210, u'Настройка звука', (M_FONTS), (HM_FONTS), 1),
                  (120, 280, u'Выход', (M_FONTS), (HM_FONTS), 2)]
        pause = menu.Menu(pause_img, punkts, punkts_back, font, TITLE, FM_FIELD, M_FONTS, screen, win, volume,
                          draw_text, ambient)
    elif name_menu[i] == name_menu[2]:
        punkts = [(120, 140, name_menu[i], (M_FONTS), (HM_FONTS), 0),
                  (120, 210, u'Настройка звука', (M_FONTS), (HM_FONTS), 1),
                  (120, 280, u'Выход', (M_FONTS), (HM_FONTS), 2)]
        gameOver = menu.Menu(gameOver_img, punkts, punkts_back, font, TITLE, FM_FIELD, M_FONTS, screen, win, volume,
                             draw_text, ambient)

# Игровой цикл
running = True
gameplay = True
start = False
game.menu()
while running:

    dt = clock.tick(FPS)
    fps = clock.get_fps()

    screen.blit(bg_imgs[0], (bg_x[0], 0))
    for i in range(1, len(bg_imgs)):
        screen.blit(bg_imgs[i], (bg_x[i], 0))
        screen.blit(bg_imgs[i], (bg_x[i] + win_width, 0))
    keys = pg.key.get_pressed()
    player.draw(keys, start)
    player.update(keys, dt, death)
    death = False
    draw_text(screen, f'Счет: {int(score)}', TITLE, 10, 10)

    if start:
        if gameplay:

            ambient.play()
            score += 1 / 10

            for enemy in enemies:
                enemy.update()
                enemy.draw()
                if player.get_rect().colliderect(enemy.get_rect()):
                    # print('enemy touch you')
                    gameplay = False

                if enemy.x < -10:
                    enemies.pop(0)

            for i in range(1, len(bg_imgs)):
                speed = i
                if speed == 1:
                    speed = len(bg_imgs) - 1
                bg_x[i] -= speed
                if bg_x[i] <= -win_width:
                    bg_x[i] = 0

        else:
            ambient.stop()
            running = False
            death = gameOver.menu()
            if death:
                bg_x = [0, 0, 0, 0, 0, 0]
                score = 0
                player.x = 150
                player.y = 410
                enemies.clear()
                gameplay = True
                running = True
                start = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pause.menu()
            if event.key == pg.K_SPACE:
                start = True
        elif event.type == pg.USEREVENT + 1:
            if len(enemies) == 0:
                enemies.append(en.Enemy(win_width + 2, pos_y_en, ENEMY_SPEED, img_enemy, screen))

    pg.display.flip()

pg.quit()
