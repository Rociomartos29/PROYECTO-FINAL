import random
import os
import pygame as pg
from . import ANCHO, ALTO, TIEMPO_MAX



class Nave(pg.sprite.Sprite):
    def __init__(self):
        self.TIEMPO_MAX_EXPLOSION = 100
        self.imagenes = []
        margen = 750
        centro_imagen=40
        
        ruta_image = os.path.join('animacion', 'image', 'nave_buena.png')
        self.imagenes=  pg.image.load(ruta_image)
        self.rect = self.imagenes.get_rect(midbottom=(ANCHO-margen, ALTO/2+centro_imagen))
        ruta_explosion = os.path.join('animacion', 'image', 'principio_explosion.png')
        self.imagen_explosion = pg.image.load(ruta_explosion)
        self.rect_explosion = self.imagen_explosion.get_rect()
        ruta_explosion2 = os.path.join('animacion', 'image', 'explosion2.png')
        self.explosion2 = pg.image.load(ruta_explosion2)
        self.rect_explosion2 = self.explosion2.get_rect()
        self.estado = "normal"
        self.tiempo_explosion = 0
        

    def update(self):
        if self.estado == "explosion":
            self.tiempo_explosion += 1
        if self.tiempo_explosion >= self.TIEMPO_MAX_EXPLOSION:  # Define TIEMPO_MAX_EXPLOSION
            self.estado = "normal"
            self.tiempo_explosion = 0

        self.comprobar_teclas()
    


    def comprobar_teclas(self):
        velocidad = 10
        teclas = pg.key.get_pressed()
        if teclas[pg.K_UP]:
            self.rect.y -= velocidad
            if self.rect.top < 0:
                self.rect.top = 0
        if teclas[pg.K_DOWN]:
            self.rect.y += velocidad
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO








        
class Obstaculo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        ruta_meteoro = os.path.join('animacion', 'image','meteorito1.png')
        self.image = pg.image.load(ruta_meteoro)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = random.randint(0, ALTO - self.rect.height)
        self.velocidad = random.randint(2, 5)

        ruta_meteorito = os.path.join('animacion', 'image', 'meteorito1.png')
        self.image2 =  pg.image.load(ruta_meteorito)
        self.rect1 = self.image2.get_rect()
        self.rect1.x = ANCHO
        self.rect1.y = random.randint(0, ALTO - self.rect1.height)

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.rect.x = ANCHO
            self.rect.y = random.randint(0, ALTO - self.rect.height)


        

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
        pantalla.blit(self.image2, self.rect1)


class Marcador:
    def __init__(self):
        self.puntuacion = 0

    def incrementar_puntuacion(self, puntos):
        self.puntuacion += puntos

    def obtener_puntuacion(self):
        return self.puntuacion