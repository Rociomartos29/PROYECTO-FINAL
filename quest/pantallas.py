import os
import random
import pygame as pg
from . import ALTO, ANCHO, FPS, COLOR_DE_TEXTO
from .objetos import Nave, Obstaculo, Marcador

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
        self.meteorito = Obstaculo()
        self.grupo_obstaculos = pg.sprite.Group()  
        self.tiempo_maximo = 30000
        ruta_fondo = os.path.join('animacion', 'image', 'fondo2.png')
        self.fondo = pg.image.load(ruta_fondo)

        #Obstaculos
        self.tiempo_generacion = 30000
        self.max_obstaculos = 10
        self.tiempo_actual = pg.time.get_ticks()
        self.tiempo_anterior_generacion = pg.time.get_ticks()
        self.tiempo_inicial = pg.time.get_ticks()
        self.ultimo_tiempo_generacion = self.tiempo_inicial
        self.generacion_activa = True
        self.obstaculos_generados = 0 

        self.marcador = Marcador()
        self.obstaculos_salidos = 0



    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        juego_iniciado = False
        tiempo_transcurrido = 0
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    juego_iniciado = True


            
            self.jugador.update()

            # Verifica colisiones entre la nave y los obstáculos
            if pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_rect):
                # La nave ha colisionado, cambia su imagen a explosión
                self.jugador.estado = "explosion"
                self.jugador.image = self.jugador.imagen_explosion
            self.grupo_obstaculos.update()

            self.pintar_fondo()
            

            self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)
            self.grupo_obstaculos.draw(self.pantalla)  
            tiempo_transcurrido = self.tiempo_actual - self.tiempo_inicial
            if self.generacion_activa and len(self.grupo_obstaculos) < 6:
                self.generar_obstaculo()
                if self.obstaculos_generados >= 10:
                    self.generacion_activa = False
                

            self.comprobar_obstaculos_salidos()
            
            puntuacion_actual = self.marcador.obtener_puntuacion()
            print(f'Puntuación actual: {puntuacion_actual}')

            colisiones = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)
            if colisiones:
                # La nave ha colisionado, cambia su imagen a explosión
                self.jugador.estado = "explosion"
                self.jugador.image = self.jugador.imagen_explosion


            pg.display.flip()

    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    def generar_obstaculo(self):
        if self.generacion_activa and len(self.grupo_obstaculos) < 6:
            obstaculo = Obstaculo()
            self.grupo_obstaculos.add(obstaculo)
            self.obstaculos_generados += 1

    def comprobar_obstaculos_salidos(self):
        obstaculos_a_eliminar = []
        for obstaculo in self.grupo_obstaculos:
            if obstaculo.rect.right < 0:
                # Incrementa la puntuación y marca el obstáculo para eliminación
                self.marcador.incrementar_puntuacion(10)
                obstaculos_a_eliminar.append(obstaculo)
        # Elimina los obstáculos marcados
        for obstaculo in obstaculos_a_eliminar:
            self.grupo_obstaculos.remove(obstaculo)




class Nivel2:
    pass

class Final:
    pass
        