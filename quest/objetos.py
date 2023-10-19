
import os
import pygame as pg
from . import ANCHO, ALTO


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
        if teclas[pg.K_LEFT]:
            self.rect.x -= velocidad
            if self.rect.left < 0:
                self.rect.left = 0
        if teclas[pg.K_RIGHT]:
            self.rect.x += velocidad
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO



class Obtaculos(pg.sprite.Sprite):
    def __init__(self):
        self.images = []

        ruta_meteoro1 = 'animacion', 'image', 'meteorito.jpg'
        ruta_meteorito2 = 'animacion', 'image', 'meteoro.jpeg'