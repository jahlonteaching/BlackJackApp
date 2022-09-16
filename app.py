from juego.mundo.modelo import Baraja


if __name__ == "__main__":
    baraja: Baraja = Baraja()
    baraja.revolver()
    while baraja.tiene_cartas():
        print(f"{str(baraja.repartir()):^10}")


