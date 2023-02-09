import pygame, sys, random

pygame.init()

screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()
speed = 2.5
bg_speed = 1.5

pygame.display.set_caption("Flappy Bird")

favicon = pygame.image.load("images/player.png")
pygame.display.set_icon(favicon)

background_image = pygame.image.load("images/background.png")
background_x = 0

ground_image = pygame.image.load("images/ground.png")
ground_x = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("images/player.png").convert_alpha(), pygame.image.load("images/player2.png").convert_alpha(), pygame.image.load("images/player3.png").convert_alpha()]
        self.image_index = 0
        self.x = 100
        self.y = 310
        self.w = 57
        self.h = 40
        self.dy = 0
        self.max_y = 20
        
        self.rect = self.images[0].get_rect()
        self.mask = pygame.mask.from_surface(self.images[0])
    
    def animation(self):
        self.image_index += 1
        if self.image_index == 3:
            self.image_index = 0
        self.rect = self.images[self.image_index].get_rect()
        self.mask = pygame.mask.from_surface(self.images[self.image_index])
    
    def draw(self):
        screen.blit(self.images[self.image_index], (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/pipe.png").convert_alpha()
        self.image2 = pygame.image.load("images/pipe_2.png").convert_alpha()
        self.x = 400
        self.y = y
        self.w = 66
        self.h = 600
        self.space = 85
        
        self.rect = self.image1.get_rect()
        self.mask = pygame.mask.from_surface(self.image1)
    
    def updateCollision(self, image_index):
        if image_index == 0:
            self.rect = pygame.Rect(self.x, self.y - 600 - self.space, self.w, self.h)
        else:
            self.rect = pygame.Rect(self.x, self.y + self.space, self.w, self.h)
    
    def draw(self):
        screen.blit(self.image1, (self.x, self.y + self.space))
        screen.blit(self.image2, (self.x, self.y - 600 - self.space))
    
    def move(self):
        self.x -= speed

pipes = []
pipe_timer = 0
player = Player()
player_animation_timer = 0
score = 0

keydown_fly = False
gameover = False
start = False
keylock = False

while True:
    keydown_fly = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not keylock:
                keydown_fly = True
                start = True
                if gameover:
                    gameover = False
                    start = False
                    score = 0
                    player = Player()
                    pipes = []
                    speed = 2.5
                    bg_speed = 1.5
    
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (400 + background_x, 0))
    background_x -= bg_speed
    
    if background_x <= -400:
        background_x = 0
    
    if pipe_timer ==100:
        pipes.append(Pipe(random.randint(300, 400)))
        pipe_timer = 0
        score += 1
    
    for index, item in enumerate(pipes):
        if item.x <= -70:
            pipes.pop(index)
        
        item.updateCollision(0)
        collide1 = pygame.sprite.collide_mask(item, player)
        item.updateCollision(1)
        collide2 = pygame.sprite.collide_mask(item, player)
        
        if collide1 or collide2:
            gameover = True
            keylock = True
        
        item.draw()
        item.move()
    
    if player.y + player.h >= 612:
        gameover = True
    if player.y < 0:
        gameover = True
    
    screen.blit(ground_image, (ground_x, 612))
    screen.blit(ground_image, (400 + ground_x, 612))
    ground_x -= speed
    
    if player_animation_timer == 6:
        player.animation()
        player_animation_timer = 0
    
    if not gameover:
        if start:
            if keydown_fly:
                player.dy = -10
            else:
                player.dy += 0.6
    
        player.y += player.dy
    
        if player.dy >= player.max_y:
            player.dy = player.max_y
    
        if ground_x <= -400:
            ground_x = 0
    
        if start:
            pipe_timer += 1

        player_animation_timer += 1
    else:
        if player.y < 612 and start:
            player.dy += 0.6
            player.y += player.dy
        elif start:
            keylock = False
    
    player.draw()
    
    font = pygame.font.SysFont("arial", 30, True, False)
    text = font.render(str(score), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = 200
    text_rect.y = 20
    screen.blit(text, text_rect)
    
    if not start:
        font = pygame.font.SysFont("arial", 30, True, False)
        text = font.render("Press Space", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = 200
        text_rect.y = 500
        screen.blit(text, text_rect)
    
    if gameover:
        font = pygame.font.SysFont("arial", 30, True, False)
        text = font.render("Game Over!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = 200
        text_rect.y = 500
        screen.blit(text, text_rect)
    
    if gameover:
        speed = 0
        bg_speed = 0
            
    pygame.display.update()
    clock.tick(60)
