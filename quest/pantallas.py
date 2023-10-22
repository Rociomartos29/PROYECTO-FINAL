import os
import pygame as pg
from . import ALTO, ANCHO, FPS, COLOR_DE_TEXTO
from .objetos import Nave

class Principal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        print ('Esto es un metodo vacio')


class Portada(Principal):

    def __init__(self, pantalla):
        super().__init__(pantalla)
        
        ruta = os.path.join( 'animacion','image',
                         'portada.png')
        self.animacion = pg.image.load(ruta)

        ruta_font = os.path.join('animacion', 
                                 'sysfont.otf')
        self.tipo = pg.font.Font(ruta_font, 35)

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True

            self.pintar_animacion()
            self.pintar_mensaje()
            pg.display.flip()

    def pintar_animacion(self):
        ancho, alto = self.animacion.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.animacion, (pos_x, pos_y))

    def pintar_mensaje(self):
        mensaje = 'Pulsa Espacio para comenzar'
        texto = self.tipo.render(mensaje, True, COLOR_DE_TEXTO)
        pos_x = (ANCHO - texto.get_width())
        pos_y = ALTO / 4 * 3
        self.pantalla.blit(texto, (pos_x, pos_y))

class Historia(Principal):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        
        ruta = os.path.join( 'animacion','image',
                         'Historia.png')
        self.historia = pg.image.load(ruta)

        ruta_font = os.path.join('animacion', 
                                 'sysfont.otf')
        self.tipo = pg.font.Font(ruta_font, 35)


    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True

            self.pintar_historia()
            self.pintar_mensaje()
            pg.display.flip()

    def pintar_historia(self):
        ancho, alto = self.historia.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.historia, (pos_x, pos_y))

    def pintar_mensaje(self):
        mensaje = 'Pulsa Espacio para comenzar'
        texto = self.tipo.render(mensaje, True, COLOR_DE_TEXTO)
        pos_x = (ANCHO/ 4*3 - texto.get_width())
        pos_y = ALTO / 4 * 3
        self.pantalla.blit(texto, (pos_x, pos_y))


class Nivel1(Principal):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.jugador = Nave()
        #self.meteoritos = Obtaculos()
        #todos_los_obstaculos = pg.sprite.Group()
        #todos_los_obstaculos.add(self.meteoritos)
        #todos_los_obstaculos.update()
        ruta_fondo = os.path.join('animacion', 'image', 'fondo2.png')
        self.fondo = pg.image.load(ruta_fondo)


        
        
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        juego_iniciado = False
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return  True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    juego_iniciado = True
            
            
            self.jugador.update()
            self.pintar_fondo()
            self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)
            '''self.pintar_obtaculos()'''
            
            
            #self.pantalla.blit(self.jugador.image, self.jugador.rect)
            pg.display.flip()

    def pintar_fondo(self):
        
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    '''def pintar_obtaculos(self):
        filas = 4
        columnas = 6
        margen_superior = 20

        for fila in range(filas):   # 0-3
            for col in range(columnas):
                # por aquí voy a pasar filas*columnas = 24 veces
                margen_izquierdo = (ANCHO - columnas * self.meteoritos.rect.width) / 2
                # x = ancho_lad * col
                # y = alto_lad * fila
                self.meteoritos.rect.x = self.meteoritos.rect.width * col + margen_izquierdo
                self.meteoritos.rect.y = self.meteoritos.rect.height * fila + margen_superior
                self.meteoritos.add(self.meteoritos)
                print (self.meteoritos.rect)

            self.meteoritos.generar_meteorito()
            self.meteoritos.update()


        self.pantalla.blit(self.meteoritos)'''
    


class Nivel2:
    pass

class Final:
    pass
        