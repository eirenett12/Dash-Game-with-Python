import pygame
import Button listenr

TINGGI_LAYAR = 500
LEBAR_LAYAR = 700

screen = pygame.display.set.mode((TINGGI_LAYAR, LEBAR_LAYAR))
pygame.display.set_caption('Button Demo')


# game_loop
register_img = pygame.image.load('nama_folder/register.png')
login_img = pygame.image.load('nama_folder/login.png')

class Button():
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        #draw button on screen
        screen.blit(self. image, (self.rect.x, self.rect.y))


register_button = Button(100, 200, register_img)
exit_button = Button(100, 200, exit_img)

run = True
while run:

    screen.fill((202, 228, 241))

    register_button.draw()
    exit_button.draw()

