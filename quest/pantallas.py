import os
import random
import pygame as pg
from . import ALTO, ANCHO, FPS, COLOR_DE_TEXTO
from .objetos import Nave, Obstaculo, Marcador
import sqlite3
pg.mixer.init()


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
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        self.jugador = Nave()
        self.grupo_obstaculos = pg.sprite.Group()
        self.tiempo_maximo = 30000
        ruta_fondo = os.path.join('animacion', 'image', 'fondo1.png')
        self.fondo = pg.image.load(ruta_fondo)
        self.tiempo_inicial = pg.time.get_ticks()
        self.tiempo_nivel2 = 30000

            # Obstáculos
        self.max_obstaculos = 10
        self.tiempo_anterior_generacion = 0
        self.obstaculos_generados = 0
        self.generacion_activa = True
        self.marcador = Marcador()
        self.puntuacion = 0
        self.tiempo_inicial  = 0
        tiempo_nivel2 = 30000

    def bucle_principal(self):
        salir = False
        juego_iniciado = False
        nivel_completado = False
        tiempo_inicial = pg.time.get_ticks()

        while not salir:
            self.reloj.tick(FPS)
            tiempo_actual = pg.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicial

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if not nivel_completado:
                    if not juego_iniciado:
                        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                            juego_iniciado = True
                    else:
                        if tiempo_transcurrido >= self.tiempo_maximo or self.obstaculos_generados >= self.max_obstaculos:
                            nivel_completado = True
                            self.generacion_activa = False

            self.jugador.update()

            if pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask):
                self.jugador.estado = "explosion"
                self.jugador.image = self.jugador.imagen_explosion

            self.grupo_obstaculos.update()
            self.pintar_fondo()
            self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)
            if self.generacion_activa and self.obstaculos_generados < self.max_obstaculos:
                self.generar_obstaculo()

            if self.generacion_activa and len(self.grupo_obstaculos) < 6:
                self.generar_obstaculo()
                if self.obstaculos_generados >= self.max_obstaculos:
                    self.generacion_activa = False

            if self.jugador.estado == "explosion":
                self.jugador.explosion_sound.play()
                self.pantalla.blit(self.jugador.imagen_explosion, self.jugador.rect)
            else:
                self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

            if tiempo_transcurrido >= self.tiempo_nivel2:
                self.pasar_a_nivel2()

            self.grupo_obstaculos.draw(self.pantalla)
            self.generar_obstaculo()
            self.comprobar_colisiones()
            self.comprobar_obstaculos_salidos()
            self.marcador.pintar(self.pantalla)
            self.jugador.pintar_vidas(self.pantalla)

            pg.display.flip()

    def comprobar_colisiones(self):
        colisiones = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)

        for obstaculo in self.grupo_obstaculos:
            if pg.sprite.collide_mask(self.jugador, obstaculo):
                self.puntuacion += 10

        if pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, True, pg.sprite.collide_mask):
            self.jugador.perder_vida()
            if self.jugador.vidas <= 0:
                self.jugador.vidas = 3
                self.jugador.estado = "normal"
                self.jugador.tiempo_explosion = 0
            self.jugador.image = self.jugador.imagen_original
            self.jugador.explosion_sound.play() 

    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    def generar_obstaculo(self):
        if self.generacion_activa and len(self.grupo_obstaculos) < self.max_obstaculos:
            tiempo_actual = pg.time.get_ticks()
            
            # Controla la velocidad de generación (cada 2 segundos)
            if tiempo_actual - self.tiempo_anterior_generacion >= 2000:
                obstaculo = Obstaculo()
                self.grupo_obstaculos.add(obstaculo)
                self.obstaculos_generados += 1
                self.tiempo_anterior_generacion = tiempo_actual
                
            # Detener la generación de obstáculos después de 30 segundos
            if tiempo_actual - self.tiempo_inicial >= 30000:  # 30 segundos
                self.generacion_activa = False

    def comprobar_obstaculos_salidos(self):
        obstaculos_a_eliminar = []

        for obstaculo in self.grupo_obstaculos:
            if obstaculo.rect.right < 0:
                self.puntuacion += 10
                obstaculos_a_eliminar.append(obstaculo)

        for obstaculo in obstaculos_a_eliminar:
            self.grupo_obstaculos.remove(obstaculo)

        self.marcador.puntuacion = self.puntuacion

        if self.obstaculos_generados >= self.max_obstaculos and len(self.grupo_obstaculos) == 0:
            self.pasar_a_nivel2()

    def pasar_a_nivel2(self):
        nivel2 = Nivel2(self.pantalla)
        nivel2.bucle_principal()


class Nivel2(Principal):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        self.jugador = Nave()
        self.grupo_obstaculos = pg.sprite.Group()
        self.tiempo_maximo = 30000
        ruta_fondo = os.path.join('animacion', 'image', 'fondo2.png')
        self.fondo = pg.image.load(ruta_fondo)
        self.tiempo_inicial = pg.time.get_ticks()
        self.tiempo_nivel2 = 30000
        self.jugador_girado = False
        self.nivel2_iniciado = False
        self.tiempo_transcurrido = 0  # Agregamos esta variable
        self.tiempo_actual = pg.time.get_ticks()
        # Obstáculos
        self.max_obstaculos = 10
        self.tiempo_anterior_generacion = 0
        self.obstaculos_generados = 0
        self.generacion_activa = True
        self.marcador = Marcador()
        self.puntuacion = 0

    def bucle_principal(self):
        salir = False
        juego_iniciado = False
        nivel_completado = False
        tiempo_inicial = pg.time.get_ticks()

        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

                if not nivel_completado:
                    if not juego_iniciado:
                        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                            juego_iniciado = True
                    else:
                        if self.tiempo_transcurrido >= self.tiempo_nivel2:
                            resultado_nivel2 = self.pasar_a_nivel2()
                            if resultado_nivel2 == "Final":
                                return "Final"



            self.jugador.update()
            if pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask):
                self.jugador.estado = "explosion"
                self.jugador.image = self.jugador.imagen_explosion

            self.grupo_obstaculos.update()
            self.pintar_fondo()
            self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)
            if self.generacion_activa and self.obstaculos_generados < self.max_obstaculos:
                self.generar_obstaculo()

            if self.generacion_activa and len(self.grupo_obstaculos) < 6:
                self.generar_obstaculo()
                if self.obstaculos_generados >= self.max_obstaculos:
                    self.generacion_activa = False

            if self.jugador.estado == "explosion":
                self.jugador.explosion_sound.play()
                self.pantalla.blit(self.jugador.imagen_explosion, self.jugador.rect)
            else:
                self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

            if not self.nivel2_iniciado:
                self.tiempo_transcurrido = self.tiempo_actual - tiempo_inicial

            if self.tiempo_transcurrido >= self.tiempo_maximo:
                self.jugador_girar_nave()
                self.marcador.puntuacion = self.puntuacion
                self.marcador.pintar(self.pantalla)
                nivel_completado = True

            if nivel_completado:
                self.mostrar_planeta()
                self.mostrar_mensaje("Pulsa Espacio para continuar")

            if self.tiempo_transcurrido >= self.tiempo_nivel2:
                self.pasar_a_final()

            self.grupo_obstaculos.draw(self.pantalla)
            self.generar_obstaculo()
            self.comprobar_colisiones()
            self.comprobar_obstaculos_salidos()
            self.marcador.pintar(self.pantalla)
            self.jugador.pintar_vidas(self.pantalla)

            if nivel_completado:
                self.mostrar_planeta()
                self.mostrar_mensaje("Pulsa Espacio para continuar")

            if self.tiempo_transcurrido >= self.tiempo_nivel2:
                return "Final"

            self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)
            self.grupo_obstaculos.draw(self.pantalla)
            self.generar_obstaculo()
            pg.display.flip()
        pg.quit()
    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))


    def mostrar_planeta(self):
        ruta_planeta = os.path.join('animacion', 'image', 'planeta.png')
        planeta = pg.image.load(ruta_planeta)
        self.pantalla.blit(planeta, (0, ALTO // 2))

    def mostrar_mensaje(self, mensaje):
        fuente = pg.font.Font(None, 36)
        texto = fuente.render(mensaje, True, COLOR_DE_TEXTO)
        pos_x = (ANCHO - texto.get_width()) // 2
        pos_y = ALTO // 2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def jugador_girar_nave(self):
        if not self.jugador_girado:
            # Cargar la imagen de la nave girada 180 grados
            nave_girada = pg.transform.rotate(self.jugador.imagen_original, 180)

            # Obtener el rectángulo original de la imagen
            rect_original = self.jugador.rect

            # Asignar la imagen girada a la nave
            self.jugador.imagenes = nave_girada
            self.jugador.rect = self.jugador.imagenes.get_rect()

            # Centrar el rectángulo en la posición original
            self.jugador.rect.center = rect_original.center

            # Establecer el indicador de que la nave ha girado
            self.jugador_girado = True

    def generar_obstaculo(self):
        if self.generacion_activa and len(self.grupo_obstaculos) < self.max_obstaculos:
            tiempo_actual = pg.time.get_ticks()
            
            # Controla la velocidad de generación (cada 2 segundos)
            if tiempo_actual - self.tiempo_anterior_generacion >= 2000:
                obstaculo = Obstaculo()
                self.grupo_obstaculos.add(obstaculo)
                self.obstaculos_generados += 1
                self.tiempo_anterior_generacion = tiempo_actual
                
            # Detener la generación de obstáculos después de 30 segundos
            if tiempo_actual - self.tiempo_inicial >= 30000:  # 30 segundos
                self.generacion_activa = False

    def comprobar_colisiones(self):
        colisiones = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)

        for obstaculo in self.grupo_obstaculos:
            if pg.sprite.collide_mask(self.jugador, obstaculo):
                self.puntuacion += 10

        if pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, True, pg.sprite.collide_mask):
            self.jugador.perder_vida()
            if self.jugador.vidas <= 0:
                self.jugador.vidas = 3
                self.jugador.estado = "normal"
                self.jugador.tiempo_explosion = 0
            self.jugador.image = self.jugador.imagen_original
            self.jugador.explosion_sound.play()

    def comprobar_obstaculos_salidos(self):
        obstaculos_a_eliminar = []

        for obstaculo in self.grupo_obstaculos:
            if obstaculo.rect.right < 0:
                self.puntuacion += 10
                obstaculos_a_eliminar.append(obstaculo)

        for obstaculo in obstaculos_a_eliminar:
            self.grupo_obstaculos.remove(obstaculo)

        self.marcador.puntuacion = self.puntuacion

        if self.obstaculos_generados >= self.max_obstaculos and len(self.grupo_obstaculos) == 0:
            self.pasar_a_final()

    def pasar_a_final(self):
        final = Final(self.pantalla)
        final.bucle_principal()
class Final(Principal):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

        ruta_fondo = os.path.join('animacion', 'image', 'records.png')
        self.fondo = pg.image.load(ruta_fondo)

        # Crear una conexión a la base de datos (o crear una nueva si no existe)
        self.conexion = sqlite3.connect("records.db")
        self.cursor = self.conexion.cursor()

        # Crear una tabla para almacenar los récords si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                jugador TEXT,
                puntuacion INTEGER
            )
        """)
    def bucle_principal(self):
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

            self.mostrar_records() 
            self.insertar_record("Jugador1", 1000)           
            self.pintar_fondo()
            pg.display.flip()

        # Ejemplo: Insertar un récord en la base de datos
        # Cambia esto a donde desees insertar los récords
        

        # Ejemplo: Mostrar récords en la consola
        

    def insertar_record(self, jugador, puntuacion):
        # Insertar un récord en la base de datos
        self.cursor.execute("INSERT INTO records (jugador, puntuacion) VALUES (?, ?)", (jugador, puntuacion))
        self.conexion.commit()

    def mostrar_records(self):
        # Consultar récords de la base de datos y mostrarlos
        self.cursor.execute("SELECT jugador, puntuacion FROM records ORDER BY puntuacion DESC")
        records = self.cursor.fetchall()

        for i, record in enumerate(records):
            jugador, puntuacion = record
            print(f"#{i + 1}: Jugador: {jugador}, Puntuación: {puntuacion}")



    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))