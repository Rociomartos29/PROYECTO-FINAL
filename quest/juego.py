import pygame as pg
from . import ALTO, ANCHO
from .pantallas import Portada, Historia, Nivel1
class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        portada = Portada(self.pantalla)
        historia = Historia(self.pantalla)
        nivel1 = Nivel1(self.pantalla)
        self.escenas = [
            portada,
            historia,
            nivel1
        ]
    
    def Jugar(self):
        for escena in self.escenas:
            he_acabado = escena.bucle_principal()
            if he_acabado:
                print('La escena me pide que acabe el juego')
                break

        pg.quit()
