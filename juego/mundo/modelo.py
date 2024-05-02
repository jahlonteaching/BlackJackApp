import random

from typing import ClassVar
from dataclasses import dataclass, field

CORAZON = "\u2764\uFE0F"
TREBOL = "\u2663\uFE0F"
DIAMANTE = "\u2666\uFE0F"
ESPADA = "\u2660\uFE0F"
OCULTA = "\u25AE\uFE0F"


@dataclass
class Carta:
    VALORES: ClassVar[list[str]] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    PINTAS: ClassVar[list[str]] = [CORAZON, TREBOL, DIAMANTE, ESPADA]
    pinta: str
    valor: str
    visible: bool = True

    def mostrar(self):
        self.visible = True

    def ocultar(self):
        self.visible = False

    def calcular_valor(self, as_como_11=True) -> int:
        if self.valor == "A":
            if as_como_11:
                return 11
            else:
                return 1
        elif self.valor in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.valor)

    def es_letra(self) -> bool:
        return self.valor in ["A", "J", "Q", "K"]

    def __str__(self) -> str:
        if not self.visible:
            return f"{OCULTA}"
        else:
            return f"{self.valor}{self.pinta}"


class Baraja:

    def __init__(self):
        self.cartas: list[Carta] = []
        self.reiniciar()

    def reiniciar(self):
        self.cartas.clear()
        for pinta in Carta.PINTAS:
            for valor in Carta.VALORES:
                self.cartas.append(Carta(pinta, valor))

    def revolver(self):
        random.shuffle(self.cartas)

    def tiene_cartas(self) -> bool:
        return len(self.cartas) > 0

    def repartir(self, oculta=False) -> Carta | None:
        if self.tiene_cartas():
            carta = self.cartas.pop()
            if oculta:
                carta.ocultar()
            return carta
        else:
            return None


class Mano:

    def __init__(self):
        self.cartas: list[Carta] = []
        self.cantidad_ases: int = 0

    def limpiar(self):
        self.cartas.clear()
        self.cantidad_ases = 0

    def agregar_carta(self, carta: Carta):
        if carta.valor == "A":
            self.cartas.append(carta)
            self.cantidad_ases += 1
        else:
            self.cartas.insert(0, carta)

    def calcular_valor(self) -> int | str:

        for carta in self.cartas:
            if not carta.visible:
                return "--"

        valor_mano = 0

        for carta in self.cartas[:-self.cantidad_ases]:
            valor_mano += carta.calcular_valor()

        for carta in self.cartas[-self.cantidad_ases:]:
            as_como_11 = valor_mano < 11
            valor_mano += carta.calcular_valor(as_como_11)

        return valor_mano

    def es_blackjack(self) -> bool:
        if len(self.cartas) > 2:
            return False
        else:
            return self.cartas[0].valor == "A" and self.cartas[1].valor in ["10", "J", "Q", "K"] \
                   or self.cartas[1].valor == "A" and self.cartas[0].valor in ["10", "J", "Q", "K"]

    def __gt__(self, other) -> bool:
        return self.calcular_valor() > other.calcular_valor()

    def __str__(self) -> str:
        str_mano = ""
        for carta in self.cartas:
            str_mano += f"{str(carta):^5}"

        return str_mano


@dataclass
class Jugador:
    nombre: str
    fichas: int = field(init=False, default=100)
    mano: Mano = field(init=False, default=Mano())

    def recibir_carta(self, carta: Carta):
        self.mano.agregar_carta(carta)

    def agregar_fichas(self, fichas: int):
        self.fichas += fichas

    def tiene_fichas(self, apuesta: int) -> bool:
        return self.fichas >= apuesta


@dataclass
class Casa:
    mano: Mano = field(init=False, default=Mano())

    def recibir_carta(self, carta: Carta):
        self.mano.agregar_carta(carta)


class BlackJack:

    def __init__(self, nombre_usuario: str):
        self.apuesta_actual: int = 0
        self.baraja: Baraja = Baraja()
        self.jugador: Jugador = Jugador(nombre_usuario)
        self.casa: Casa = Casa()

    def iniciar_nuevo_juego(self, apuesta: int):
        self.apuesta_actual = apuesta
        self.jugador.mano.limpiar()
        self.casa.mano.limpiar()
        self.baraja.reiniciar()
        self.repartir_manos()

    def repartir_manos(self):
        self.baraja.revolver()

        # Repartir la mano del usuario
        self.jugador.recibir_carta(self.baraja.repartir())
        self.jugador.recibir_carta(self.baraja.repartir())

        # Repartir la mano de la casa
        self.casa.recibir_carta(self.baraja.repartir())
        self.casa.recibir_carta(self.baraja.repartir(oculta=True))

    def dar_carta_a_jugador(self):
        self.jugador.recibir_carta(self.baraja.repartir())

    def usuario_perdio(self) -> bool:
        return self.jugador.mano.calcular_valor() > 21

    def la_casa_perdio(self) -> bool:
        valor = self.casa.mano.calcular_valor()
        if type(valor) is int:
            return valor > 21
        else:
            return False

    def la_casa_puede_pedir(self) -> bool:
        valor_mano_casa = self.casa.mano.calcular_valor()
        return valor_mano_casa <= self.jugador.mano.calcular_valor() and valor_mano_casa < 16

    def destapar_mano_de_la_casa(self):
        for carta in self.casa.mano.cartas:
            carta.mostrar()

    def dar_carta_a_la_casa(self):
        self.casa.recibir_carta(self.baraja.repartir())

    def usuario_tiene_blackjack(self) -> bool:
        return self.jugador.mano.es_blackjack()

    def finalizar_juego(self, ganador=True) -> int:
        if ganador:
            self.jugador.agregar_fichas(self.apuesta_actual)
        else:
            self.jugador.agregar_fichas(-self.apuesta_actual)

        return self.jugador.fichas
