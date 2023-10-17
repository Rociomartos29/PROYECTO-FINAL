
import os
import pygame as pg
from . import ANCHO, ALTO


class Nave(pg.sprite.Sprite):
    def __init__(self):
        self.imagenes = []
        margen = 25
        
        
        ruta_image = os.path.join('animacion', 'image', 'nave.png')
        self.imagenes.append(pg.image.load(ruta_image))
        self.rect = self.imagenes.get_rect()
        self.rect = margen
        

    def update(self):

        self.comprobar_teclas()
    


    def comprobar_teclas(self):
        velocidad = 10
        teclas = pg.key.get_pressed()
        if teclas[pg.K_LEFT]:
            self.rect.x -= velocidad
        if teclas[pg.K_RIGHT]:
            self.rect.x += velocidad



class Obtaculos(pg.sprite.Sprite):
    def __init__(self):
        self.images = []

        ruta_meteoro1 = 'animacion', 'image', 'meteorito.jpg'
        ruta_meteorito2 = 'animacion', 'image', 'meteoro.jpeg'