import pygame


class Bullet:

    def __init__(self,x,y):

        self.x = x
        self.y = y

        self.speed = 10

        self.width = 20
        self.height = 10

        self.active = True


    def update(self,enemies):

        self.x += self.speed


        rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


        for enemy in enemies[:]:

            if rect.colliderect(enemy.get_rect()):

                enemies.remove(enemy)

                self.active = False



    def draw(self,screen,camera_x,camera_y):

        pygame.draw.rect(
            screen,
            (255,200,0),
            (
                self.x-camera_x,
                self.y-camera_y,
                self.width,
                self.height
            )
        )

    