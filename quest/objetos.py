import random
import os
import pygame as pg
from . import ANCHO, ALTO, TIEMPO_MAX


class Nave(pg.sprite.Sprite):
    def __init__(self):
        self.imagenes = []
        margen = 750
        centro_imagen=40
        
        ruta_image = os.path.join('animacion', 'image', 'nave_buena.png')
        self.imagenes=  pg.image.load(ruta_image)
        self.rect = self.imagenes.get_rect(midbottom=(ANCHO-margen, ALTO/2+centro_imagen))
        
        

    def update(self):

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








        
class Obtaculos(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.images = []

            ruta_meteoro = os.path.join('animacion', 'image', 'meteorito.jpg')
            self.meteoro = pg.image.load(ruta_meteoro)
            self.rect = self.meteoro.get_rect()
            ruta_meteorito = os.path.join('animacion', 'image', 'meteoro.jpeg')
            self.meteorito = pg.image.load(ruta_meteorito)
            self.rect2 = self.meteorito.get_rect()
            self.tiempo_inicial = pg.time.get_ticks()
            self.tiempo_max = TIEMPO_MAX

        def generar_meteorito(self):
            tiempo_actual = pg.time.get_ticks()
            if tiempo_actual - self.tiempo_inicial < self.tiempo_max:
                 if random.randrange(100) < 2:
                    self.tiempo_inicial = tiempo_actual

        