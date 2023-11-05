import pygame as pg
from quest.pantallas import Portada, Historia, Nivel1, Nivel2, Final
from quest import ALTO, ANCHO

def main():
    pg.mixer.init()

    pg.init()
    

    pantalla = pg.display.set_mode((ANCHO, ALTO))
    pg.display.set_caption("Tu juego")

    portada = Portada(pantalla)
    historia = Historia(pantalla)
    nivel1 = Nivel1(pantalla)
    nivel2 = Nivel2(pantalla)
    puntuacion = nivel1.puntuacion
    final = Final(pantalla, puntuacion)
    

    while True:
        portada.bucle_principal()
        historia.bucle_principal()
        nivel1.bucle_principal()
        nivel2.bucle_principal()
        final.bucle_principal()

pg.quit()

if __name__ == "__main__":
    main()
