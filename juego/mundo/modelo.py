from dataclasses import dataclass, field
import random
from typing import Optional

CORAZON = "\u2764\uFE0F"
TREBOL = "\u2663\uFE0F"
DIAMANTE = "\u2666\uFE0F"
ESPADA = "\u2660\uFE0F"
OCULTA = "\u25AE\uFE0F"

VALORES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
PINTAS = [CORAZON, TREBOL, DIAMANTE, ESPADA]


@dataclass
class Carta:
    pinta: str
    valor: str
    _visible: bool = field(init=False, repr=False, default=False)

    @property
    def visible(self) -> bool:
        return self._visible

    def mostrar(self):
        self._visible = True

    def ocultar(self):
        self._visible = False

    def __str__(self) -> str:
        if self.visible:
            return f"{OCULTA}"
        else:
            return f"{self.valor}{self.pinta}"


class Baraja:

    def __init__(self):
        self.cartas = []
        self.inicializar_cartas()

    def inicializar_cartas(self):
        for pinta in PINTAS:
            for valor in VALORES:
                self.cartas.append(Carta(pinta, valor))

    def revolver(self):
        random.shuffle(self.cartas)

    def repartir(self) -> Optional[Carta]:
        if len(self.cartas) > 0:
            return self.cartas.pop()
        else:
            return None

    def tiene_cartas(self) -> bool:
        return len(self.cartas) > 0
