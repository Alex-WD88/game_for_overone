class Enemy:
    def __init__(self, x, y, speed, enemy, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.img_enemy = enemy
        self.rect = self.img_enemy.get_rect()
        self.rect.width -= 10
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.img_enemy, (self.x, self.y))

    def get_rect(self):
        return self.rect
