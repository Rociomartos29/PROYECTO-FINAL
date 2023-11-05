import random
import os
import pygame as pg
from . import ANCHO, ALTO, TIEMPO_MAX, ALTO_MARCADOR,VEL_MAX, VEL_MIN_Y
pg.mixer.init()





class Nave(pg.sprite.Sprite):
    def __init__(self, vidas_iniciales=3):
        pg.sprite.Sprite.__init__(self)

        self.TIEMPO_MAX_EXPLOSION = 100
        self.imagenes = []
        margen = 750
        centro_imagen = 40

        ruta_image = os.path.join('animacion', 'image', 'nave_buena.png')
        self.imagenes = pg.image.load(ruta_image)
        self.rect = self.imagenes.get_rect(midbottom=(ANCHO - margen, ALTO / 2 + centro_imagen))
        self.mask = pg.mask.from_surface(self.imagenes)
        ruta_explosion = os.path.join('animacion', 'image', 'explosion.png')
        self.imagen_explosion = pg.image.load(ruta_explosion)
        self.rect_explosion = self.imagen_explosion.get_rect()
        ruta_explosion2 = os.path.join('animacion', 'image', 'explosion2.png')
        self.explosion2 = pg.image.load(ruta_explosion2)
        self.rect_explosion2 = self.explosion2.get_rect()
        self.game_over = False
        

        self.vidas = vidas_iniciales
        self.vida_image = [pg.image.load(os.path.join('animacion', 'image', 'vida.png'))for _ in range(vidas_iniciales)]
        self.rect_vida = self.vida_image[0].get_rect()
        self.rect_vida.topleft = (ANCHO - 10 - self.rect_vida.width, 10)
        rutasonido = os.path.join('animacion', 'explosion.wav')
        self.explosion_sound = pg.mixer.Sound(rutasonido)
        self.tiempo_recuperacion = 0
        self.imagen_original = pg.image.load(ruta_image)
        self.mask = pg.mask.from_surface(self.imagenes)
        self.vidas_mostradas = vidas_iniciales  
        self.vidas_eliminadas = 0

        self.estado = "normal"
        self.tiempo_explosion = 0
        self.obstaculo = Obstaculo()
        self.vel_y = 0
        self.girado = False
        self.nave_giro_completo = False
        self.nave_avanzando = False

    def eliminar_vida(self):
        if self.vidas_eliminadas < self.vidas:
            self.vidas_eliminadas += 1
        else:
            
            self.game_over = True

    def pintar_vidas(self, pantalla):
        x = ANCHO - 10  # Alinea con el borde derecho
        y = 10

        vidas_actuales = self.vida_image[:self.vidas - self.vidas_eliminadas]

        total_width = len(vidas_actuales) * (self.rect_vida.width + 5)
        x -= total_width  

        for vida in vidas_actuales:
            if x + self.rect_vida.width < ANCHO:
                pantalla.blit(vida, (x, y))
            x += self.rect_vida.width + 5


    def inicializar_velocidades(self):
        self.vel_x = random.randint(-VEL_MAX, VEL_MAX)
        self.vel_y = random.randint(-VEL_MAX, VEL_MIN_Y)

    def update(self):
        if self.estado == "explosion":
            self.image = self.imagen_explosion  
            self.tiempo_explosion += 1
            if self.tiempo_explosion >= self.TIEMPO_MAX_EXPLOSION:
                self.estado = "normal"  
                self.tiempo_explosion = 0
                self.image = self.imagen_original
                self.explosion_sound.play()
        self.comprobar_teclas()

        if pg.sprite.collide_mask(self, self.obstaculo):
            self.inicializar_velocidades()

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
            self.vidas_eliminadas += 1
            if self.vidas_eliminadas <= len(self.vida_image):
                del self.vida_image[-1]
            else:
                print("No se eliminó una imagen de vida.")

    def reiniciar_vidas(self):
        self.max_vidas_mostradas = self.vidas

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
        self.mask = pg.mask.from_surface(self.image)

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
        ruta = os.path.abspath(os.path.join('animacion', 'sysfont.otf'))
        self.tipo_letra = pg.font.Font(ruta, 36)
        self.puntuacion = 0
    def aumentar(self, incremento):
        self.valor += incremento

    def pintar(self, pantalla):
        cadena = str(self.valor)
        texto = self.tipo_letra.render(cadena, True, (230, 189, 55))
        pos_x = 20
        pos_y = 10
        pantalla.blit(texto, (pos_x, pos_y))