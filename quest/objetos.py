import random
import os
import pygame as pg
from . import ANCHO, ALTO, TIEMPO_MAX, ALTO_MARCADOR,VEL_MAX, VEL_MIN_Y



class Nave(pg.sprite.Sprite):
    def __init__(self, vidas_iniciales=3):
        self.TIEMPO_MAX_EXPLOSION = 100
        self.imagenes = []
        margen = 750
        centro_imagen=40
        
        ruta_image = os.path.join('animacion', 'image', 'nave_buena.png')
        self.imagenes=  pg.image.load(ruta_image)
        self.rect = self.imagenes.get_rect(midbottom=(ANCHO-margen, ALTO/2+centro_imagen))
        self.mask = pg.mask.from_surface(self.imagenes)
        ruta_explosion = os.path.join('animacion', 'image', 'explosion.png')
        self.imagen_explosion = pg.image.load(ruta_explosion)
        self.rect_explosion = self.imagen_explosion.get_rect()
        ruta_explosion2 = os.path.join('animacion', 'image', 'explosion2.png')
        self.explosion2 = pg.image.load(ruta_explosion2)
        self.rect_explosion2 = self.explosion2.get_rect()

        self.vidas = vidas_iniciales
        rutavida = os.path.join('animacion', 'image','vida.png')
        self.vida_image = [pg.image.load(rutavida) for _ in range(self.vidas)]
        self.rect_vida = self.vida_image[0].get_rect()
        self.rect_vida.topleft = (10, 10)
        self.vidas_eliminadas = 0
        rutasonido= os.path.join('animacion', 'explosion.wav')
        self.explosion_sound = pg.mixer.Sound(rutasonido)
        self.tiempo_recuperacion = 0
        self.imagen_original = pg.image.load(ruta_image)

        self.estado = "normal"
        self.tiempo_explosion = 0
        self.obstaculo = Obstaculo()
        self.vel_y = 0


    def pintar_vidas(self, pantalla):
        for i, imagen_vida in enumerate(self.vida_image):
            x = ANCHO - (i + 1) * (self.rect_vida.width + 5)  # Ajustado para que las vidas estén en la esquina superior derecha
            y = 10
            pantalla.blit(imagen_vida, (x, y))
        print(f"Vida {i}: {x}, {y}")

    def inicializar_velocidades(self):
        self.vel_x = random.randint(-VEL_MAX, VEL_MAX)
        self.vel_y = random.randint(-VEL_MAX, VEL_MIN_Y)

    def update(self):
        if self.estado == "explosion":
            self.image = self.imagen_explosion  # Cambia la imagen a la de explosión
            self.tiempo_explosion += 1
            if self.tiempo_explosion >= self.TIEMPO_MAX_EXPLOSION:
                self.estado = "normal"  # Cambia el estado a normal
                self.tiempo_explosion = 0
                self.image = self.imagen_original
        self.comprobar_teclas()

        if pg.sprite.collide_mask(self, self.obstaculo):
                self.inicializar_velocidades()
        
    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
            self.vidas_eliminadas += 1
            
        
    def comprobar_colisiones(self, grupo_obstaculos):
        # Verifica la colisión con los obstáculos
        colisiones = pg.sprite.spritecollide(self, grupo_obstaculos, False)
        if colisiones:
            self.estado = "explosion"
            # Cambiar la imagen a la de explosión
            self.image = self.imagen_explosion

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
        self.mask = pg.mask.from_surface(self.image)

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
        self.valor = 0
        fuente = 'sysfont.otf'
        ruta = os.path.join('animacion', fuente)
        self.tipo_letra = pg.font.Font(ruta, 36)

    def aumentar(self, incremento):
        self.valor += incremento

    def pintar(self, pantalla):
        cadena = str(self.valor)
        texto = self.tipo_letra.render(cadena, True, (230, 189, 55))
        pos_x = 20
        pos_y = 10
        pantalla.blit(texto, (pos_x, pos_y))