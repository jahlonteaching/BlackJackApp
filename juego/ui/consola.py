import sys
import time

from juego.mundo.modelo import BlackJack


class UIConsola:

    def __init__(self):
        self.blackjack: BlackJack | None = None
        self.opciones = {
            "1": self.iniciar_nuevo_juego,
            "0": self.salir
        }

    @staticmethod
    def mostrar_menu():
        titulo = " BLACK JACK "
        print(f"\n{titulo:_^30}")
        print("1. Iniciar nuevo juego")
        print("0. Salir")
        print(f"{'_':_^30}")

    def ejecutar_app(self):
        print("\nBIENVENIDO A UN NUEVO JUEGO DE BLACKJACK")
        self.registrar_usuario()
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print(f"{opcion} no es una opción válida")

    def registrar_usuario(self):
        nombre: str = input("¿Cuál es tu nombre?: ")
        self.blackjack = BlackJack(nombre_usuario=nombre)

    def recibir_apuesta_jugador(self):
        while True:
            apuesta = input("¿Cuántas fichas deseas apostar?: ")
            if apuesta.isdigit():
                apuesta = int(apuesta)
                if self.blackjack.jugador.tiene_fichas(apuesta):
                    return apuesta
                else:
                    print("No tienes suficientes fichas para realizar esa apuesta")
            else:
                print("Por favor ingresa un valor numérico")

    def iniciar_nuevo_juego(self):
        if self.blackjack.jugador.fichas == 0:
            print("¡LO SENTIMOS! NO TIENES FICHAS PARA JUGAR")
            return

        apuesta: int = self.recibir_apuesta_jugador()
        self.blackjack.iniciar_nuevo_juego(apuesta)
        self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.jugador.mano)

        if not self.blackjack.usuario_tiene_blackjack():
            self.hacer_jugada_del_jugador()
        else:
            fichas_jugador = self.blackjack.finalizar_juego()
            print(f"¡¡¡BLACKJACK!!!\n!FELICITACIONES {self.blackjack.jugador.nombre.upper()}! HAS GANADO EL JUEGO\n")
            print(f"AHORA TIENES {fichas_jugador} FICHAS")

    def hacer_jugada_del_jugador(self):
        while not self.blackjack.usuario_perdio():
            respuesta = input("¿Quieres otra carta? s(si), n(no): ")
            if respuesta == 's':
                self.blackjack.dar_carta_a_jugador()
                self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.jugador.mano)
            elif respuesta == 'n':
                break

        if self.blackjack.usuario_perdio():
            print("\nHAS PERDIDO EL JUEGO\n")
            fichas_jugador = self.blackjack.finalizar_juego(ganador=False)
            print(f"AHORA TIENES {fichas_jugador} FICHAS")
        else:
            self.ejecutar_turno_de_la_casa()

    def ejecutar_turno_de_la_casa(self):
        print("\nAHORA ES EL TURNO DE LA CASA\n")
        self.blackjack.destapar_mano_de_la_casa()
        self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.jugador.mano)

        time.sleep(3)

        while not self.blackjack.la_casa_perdio() and self.blackjack.la_casa_puede_pedir():
            print("\nLA CASA PIDE UNA CARTA\n")
            time.sleep(1)
            self.blackjack.dar_carta_a_la_casa()
            self.mostrar_manos(self.blackjack.casa.mano, self.blackjack.jugador.mano)
            time.sleep(2.5)

        print("\nLA CASA TERMINA SU JUGADA\n")
        time.sleep(1)

        print(f"{' RESULTADO ':-^20}")
        ganador = True
        if self.blackjack.la_casa_perdio():
            print(f"\n¡FELICITACIONES {self.blackjack.jugador.nombre.upper()}! HAS GANADO EL JUEGO\n")
        else:
            if self.blackjack.casa.mano > self.blackjack.jugador.mano:
                print("\nLO SENTIMOS, ¡LA CASA GANA!\n")
                ganador = False
            else:
                print(f"\n¡FELICITACIONES {self.blackjack.jugador.nombre.upper()}! HAS GANADO EL JUEGO\n")

        fichas_jugador = self.blackjack.finalizar_juego(ganador)
        print(f"AHORA TIENES {fichas_jugador} FICHAS")

    @staticmethod
    def mostrar_manos(mano_casa, mano_jugador):
        print(f"\n{'MANO DE LA CASA':<15}\n{str(mano_casa):<15}")
        print(f"{'VALOR: ' + str(mano_casa.calcular_valor()):<15}\n")
        print(f"\n{'TU MANO':<15}\n{str(mano_jugador):<15}")
        print(f"{'VALOR: ' + str(mano_jugador.calcular_valor()):<15}\n")

    @staticmethod
    def salir():
        print("\nGRACIAS POR JUGAR BLACKJACK. VUELVA PRONTO")
        sys.exit(0)
