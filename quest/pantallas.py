import os
import random
import pygame as pg
from . import ALTO, ANCHO, FPS, COLOR_DE_TEXTO, TIEMPO_ANIMACION_NAVE
from .objetos import Nave, Obstaculo, Marcador
import sqlite3
pg.mixer.init()
pg.init()


class Principal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        print ('Esto es un metodo vacio')

    def mostrar_mensaje(self, mensaje):
        fuente = pg.font.Font(None, 36)
        texto_renderizado = fuente.render(mensaje, True, (255, 255, 255))  
        pos_x = (ANCHO - texto_renderizado.get_width()) // 2
        pos_y = ALTO // 2
        self.pantalla.blit(texto_renderizado, (pos_x, pos_y))
        pg.display.flip()
    


class Portada(Principal):

    def __init__(self, pantalla):
        super().__init__(pantalla)
        
        ruta = os.path.join( 'animacion','image',
                         'portada.png')
        self.animacion = pg.image.load(ruta)

        ruta_font = os.path.join('animacion', 
                                 'sysfont.otf')
        self.tipo = pg.font.Font(ruta_font, 35)
        self.reiniciar_juego = False 


    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
                    self.reiniciar_juego = True  


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
        self.explosion_sound = pg.mixer.Sound(os.path.join('animacion', 'explosion.wav'))
        self.explosion_sound.set_volume(1.0)
        self.grupo_obstaculos = pg.sprite.Group()
        self.tiempo_maximo = 30000
        self.tiempo_nivel2 = 30000
        self.max_obstaculos = 10
        self.obstaculos_generados = 0
        self.generacion_activa = True
        self.marcador = Marcador()
        self.puntuacion = 0
        self.tiempo_inicial = pg.time.get_ticks()
        self.fondo = pg.image.load(os.path.join('animacion', 'image', 'fondo1.png'))
        self.tiempo_anterior_generacion = 0
        self.nivel_completado = False
        self.juego_iniciado = False
        self.game_over = False
        self.sonido_reproducido = False
        self.ultima_colision = None
        self.salir = False  
        self.colisiones = 0 
        self.reiniciar_juego = False  
 

    def bucle_principal(self):
        while not self.salir:
            tiempo_inicial = pg.time.get_ticks()
            tiempo_transcurrido = 0

            while not self.salir:
                self.reloj.tick(FPS)
                tiempo_actual = pg.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicial

                for evento in pg.event.get():
                    if evento.type == pg.QUIT:
                        self.salir = True
                    if not self.nivel_completado:
                        if not self.juego_iniciado:
                            if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                                self.juego_iniciado = True
                        else:
                            if tiempo_transcurrido >= self.tiempo_maximo or self.obstaculos_generados >= self.max_obstaculos:
                                self.nivel_completado = True
                                self.generacion_activa = False

                self.jugador.update()
                self.comprobar_colisiones()
                if self.colisiones >= 3:  
                    self.regresar_a_portada()

                self.grupo_obstaculos.update()
                self.pintar_fondo()
                self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

                if self.generacion_activa and self.obstaculos_generados < self.max_obstaculos:
                    self.generar_obstaculo()

                self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

                if self.jugador.estado == "explosion":
                    self.jugador.explosion_sound.play()
                    self.pantalla.blit(self.jugador.imagen_explosion, self.jugador.rect)
                else:
                    self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

                if tiempo_transcurrido >= self.tiempo_nivel2:
                    self.pasar_a_nivel2()

                self.jugador.explosion_sound.set_volume(1.0)

                self.grupo_obstaculos.draw(self.pantalla)
                self.comprobar_obstaculos_salidos()
                self.marcador.pintar(self.pantalla)
                self.jugador.pintar_vidas(self.pantalla)

                pg.display.flip()

            if self.colisiones >= 3:
                self.regresar_a_portada()  # Vuelve a la portada después de 3 colisiones

        if self.jugador.vidas <= 0:
            self.game_over = True

    def comprobar_colisiones(self):
        if not self.game_over:
            colisiones = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)

            for obstaculo in colisiones:
                if obstaculo != self.ultima_colision:
                    self.jugador.eliminar_vida()
                    self.explosion_sound.play()
                    self.ultima_colision = obstaculo
                    self.marcador.puntuacion = self.puntuacion
                    obstaculo.kill()
                    self.colisiones += 1 

            golpeadas = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)
            esquivados = len(self.grupo_obstaculos) - len(golpeadas)

            if esquivados > 0:
                vidas_eliminar = min(len(golpeadas), self.jugador.vidas - self.jugador.vidas_eliminadas)
                self.jugador.vidas_eliminadas += vidas_eliminar
                self.marcador.aumentar(len(self.grupo_obstaculos))
                self.jugador.vel_y = -self.jugador.vel_y

    def regresar_a_portada(self):
        portada = Portada(self.pantalla)
        portada.bucle_principal()

        
        if portada.reiniciar_juego:
            self.__init__(self.pantalla)  
            self.bucle_principal()  

        self.salir = True

    def generar_obstaculo(self):
        if self.generacion_activa and len(self.grupo_obstaculos) < self.max_obstaculos:
            tiempo_actual = pg.time.get_ticks()

            if tiempo_actual - self.tiempo_anterior_generacion >= 2000:
                obstaculo = Obstaculo()
                self.grupo_obstaculos.add(obstaculo)
                self.obstaculos_generados += 1
                self.tiempo_anterior_generacion = tiempo_actual

            if tiempo_actual - self.tiempo_inicial >= 30000:
                self.generacion_activa = False

    def comprobar_obstaculos_salidos(self):
        obstaculos_a_eliminar = [obstaculo for obstaculo in self.grupo_obstaculos if obstaculo.rect.right < 0]
        self.puntuacion += len(obstaculos_a_eliminar) * 10
        self.grupo_obstaculos.remove(obstaculos_a_eliminar)
        self.marcador.puntuacion = self.puntuacion

        if self.obstaculos_generados >= self.max_obstaculos and not self.grupo_obstaculos:
            self.pasar_a_nivel2()

    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    def pasar_a_nivel2(self):
        nivel2 = Nivel2(self.pantalla)
        nivel2.bucle_principal()
        self.salir = True
class Nivel2(Principal):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        pg.mixer.init()
        self.jugador = Nave()
        
        self.grupo_obstaculos = pg.sprite.Group()
        
        self.obstaculos_generados = 0
        self.generacion_activa = True
        self.marcador = Marcador()
        self.puntuacion = 0
        self.tiempo_inicial = pg.time.get_ticks()
        self.planeta_mostrado = False
        self.tiempo_maximo = 30000
        self.tiempo_nivel2 = 30000
        self.max_obstaculos = 10

        self.planeta = pg.image.load(os.path.join('animacion', 'image', 'planeta.png'))
        self.rect_planeta = self.planeta.get_rect()
        self.rect_planeta.right = ANCHO  
        self.rect_planeta.centery = ALTO // 2  

        self.fondo = pg.image.load(os.path.join('animacion', 'image', 'fondo2.png'))
        self.explosion_sound = pg.mixer.Sound(os.path.join('animacion', 'explosion.wav'))
        self.explosion_sound.set_volume(1.0)
        self.tiempo_anterior_generacion = 0
        self.nivel_completado = False
        self.juego_iniciado = False
        self.planeta_aparecido = False  
        self.nave_aterrizando = False  
        self.angulo_giro = 0
        self.velocidad_giro = 1
        self.nave_y = 0
        self.game_over = False
        self.sonido_reproducido = False
        self.ultima_colision = None
        self.salir = False  
        self.colisiones = 0 
        self.reiniciar_juego = False
        self.esperando_tecla = False  
        self.tecla_presionada = False
    def generar_obstaculo(self):
        if len(self.grupo_obstaculos) < self.max_obstaculos:
            obstaculo = Obstaculo()
            self.grupo_obstaculos.add(obstaculo)

    def bucle_principal(self):
        salir = False
        tiempo_inicial = pg.time.get_ticks()
        tiempo_transcurrido_planeta = 0
        planeta_mostrado = False

        while not salir:
            self.reloj.tick(FPS)
            tiempo_actual = pg.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicial
            angulo_giro = 0
            tecla_presionada = False

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

            
            if not self.nivel_completado:
                if not self.juego_iniciado:
                   
                    for evento in pg.event.get():
                        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                            self.juego_iniciado = True

            if not self.nave_aterrizando:
                self.generar_obstaculo()  

            # Lógica del juego
            self.comprobar_colisiones()
            if self.colisiones >= 3:
                self.regresar_a_portada()

            #
            self.grupo_obstaculos.update()
            for obstaculo in self.grupo_obstaculos.copy():
                if obstaculo.rect.right < 0:
                    self.grupo_obstaculos.remove(obstaculo)

            self.grupo_obstaculos.update()
            self.pintar_fondo()

            
            if not self.game_over and not self.nave_aterrizando:
                self.jugador.update()

            if not planeta_mostrado:
                if not self.nivel_completado:
                    if tiempo_transcurrido >= self.tiempo_nivel2:
                        if self.obstaculos_generados >= self.max_obstaculos:
                            self.planeta_aparecido = True
                            self.mostrar_planeta()
                            planeta_mostrado = True

            
            if self.jugador.estado == "explosion":
                self.jugador.explosion_sound.play()
                self.pantalla.blit(self.jugador.imagen_explosion, self.jugador.rect)
            else:
                self.pantalla.blit(self.jugador.imagenes, self.jugador.rect)

            if not self.nivel_completado:
                if tiempo_transcurrido >= self.tiempo_nivel2:
                    if self.obstaculos_generados >= self.max_obstaculos:
                        self.nave_aterrizando = True
                        if not self.planeta_aparecido:
                            self.pantalla.blit(self.planeta, self.rect_planeta)
                            self.rect_planeta.right = ANCHO  
                            self.rect_planeta.centery = ALTO // 2
                            self.planeta_aparecido = True

            self.grupo_obstaculos.draw(self.pantalla)

            self.marcador.pintar(self.pantalla)
            self.jugador.pintar_vidas(self.pantalla)

            pg.display.flip()

        if self.colisiones >= 3:
            self.regresar_a_portada()  

        if self.jugador.vidas <= 0:
            self.game_over = True

        self.pasar_al_final()

    def eliminar_obstaculos(self):
        self.grupo_obstaculos.empty()  
        self.obstaculos_generados = 0

    def regresar_a_portada(self):
        portada = Portada(self.pantalla)
        portada.bucle_principal()

        if portada.reiniciar_juego:
            self.__init__(self.pantalla) 
            self.bucle_principal()  

        self.salir = True


    def comprobar_obstaculos_salidos(self):
        obstaculos_a_eliminar = [obstaculo for obstaculo in self.grupo_obstaculos if obstaculo.rect.right < 0]

        for obstaculo in obstaculos_a_eliminar:
            obstaculo.kill()

        
        if len(self.grupo_obstaculos) < self.max_obstaculos and not self.generacion_activa:
            self.generacion_activa = True

    def mostrar_planeta(self):
        self.pantalla.blit(self.planeta, self.rect_planeta)
        self.rect_planeta.left = ANCHO // 2  
        self.rect_planeta.centery = ALTO // 2  

    def comprobar_colisiones(self):
        if not self.game_over:
            colisiones = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)

            for obstaculo in colisiones:
                if obstaculo != self.ultima_colision:
                    self.jugador.eliminar_vida()
                    self.explosion_sound.play()
                    self.ultima_colision = obstaculo
                    self.marcador.puntuacion = self.puntuacion
                    obstaculo.kill()
                    self.colisiones += 1  

            golpeadas = pg.sprite.spritecollide(self.jugador, self.grupo_obstaculos, False, pg.sprite.collide_mask)
            esquivados = len(self.grupo_obstaculos) - len(golpeadas)

            if esquivados > 0:
                vidas_eliminar = min(len(golpeadas), self.jugador.vidas - self.jugador.vidas_eliminadas)
                self.jugador.vidas_eliminadas += vidas_eliminar
                self.marcador.aumentar(len(self.grupo_obstaculos))
                self.jugador.vel_y = -self.jugador.vel_y

    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho)
        pos_y = (ALTO - alto)
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    def pasar_al_final(self):
        nivel_final = Final(self.pantalla, self.puntuacion)  
        nivel_final.bucle_principal()
        self.salir = True
class Final(Principal):
    def __init__(self, pantalla, puntuacion):
        super().__init__(pantalla)
        self.fondo = pg.image.load(os.path.join('animacion', 'image', 'records.png'))
        self.conexion = sqlite3.connect("records.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_records()
        self.puntuacion = puntuacion 


    def crear_tabla_records(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    jugador TEXT,
                    puntuacion INTEGER
                )
            """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de registros: {e}")

    def bucle_principal(self):
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

            self.pintar_fondo()
            self.mostrar_records()
            
            pg.display.flip()

        self.conexion.close()  
        pg.quit()

    def insertar_record(self, jugador, puntuacion):
        try:
            self.cursor.execute("INSERT INTO records (jugador, puntuacion) VALUES (?, ?)", (jugador, puntuacion))
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar el registro: {e}")

    def mostrar_records(self):
        try:
            self.cursor.execute("SELECT jugador, puntuacion FROM records ORDER BY puntuacion DESC")
            records = self.cursor.fetchall()
            y = 100  
            for i, record in enumerate(records):
                jugador, puntuacion = record
                texto = f"#{i + 1}: Jugador: {jugador}, Puntuación: {puntuacion}"
                self.mostrar_texto(texto, y)
                y += 30  

          
            self.mostrar_texto(f"Tu puntuación: {self.puntuacion}", y)
        except sqlite3.Error as e:
            print(f"Error al consultar los registros: {e}")

    def mostrar_texto(self, texto, y):
        fuente = pg.font.Font(None, 36)
        texto_renderizado = fuente.render(texto, True, COLOR_DE_TEXTO)
        pos_x = (ANCHO - texto_renderizado.get_width()) // 2
        self.pantalla.blit(texto_renderizado, (pos_x, y))

    def pintar_fondo(self):
        ancho, alto = self.fondo.get_size()
        pos_x = (ANCHO - ancho) // 2
        pos_y = (ALTO - alto) // 2
        self.pantalla.blit(self.fondo, (pos_x, pos_y))

    