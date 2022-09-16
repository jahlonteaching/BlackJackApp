from dataclasses import dataclass, field
import random
from typing import Optional, ClassVar

CORAZON = "\u2764"
TREBOL = "\u2663"
DIAMANTE = "\u2666"
ESPADA = "\u2660"
OCULTA = "\u25AE"


@dataclass
class Carta:
    VALORES: ClassVar[list[str]] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    PINTAS: ClassVar[list[str]] = [CORAZON, TREBOL, DIAMANTE, ESPADA]
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
        self.recoger_cartas()

    def recoger_cartas(self):
        for pinta in Carta.PINTAS:
            for valor in Carta.VALORES:
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
