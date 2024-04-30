import pytest
import inspect

import juego.mundo.modelo

from juego.mundo.modelo import CORAZON, DIAMANTE, TREBOL, ESPADA

module_members = [member[0] for member in inspect.getmembers(juego.mundo.modelo)]
carta_defined = "Carta" in module_members
mano_defined = "Mano" in module_members
baraja_defined = "Baraja" in module_members
jugador_defined = "Jugador" in module_members
casa_defined = "Casa" in module_members
blackjack_defined = "BlackJack" in module_members

if carta_defined:
    from juego.mundo.modelo import Carta

if mano_defined:
    from juego.mundo.modelo import Mano

if baraja_defined:
    from juego.mundo.modelo import Baraja

if jugador_defined:
    from juego.mundo.modelo import Jugador

if casa_defined:
    from juego.mundo.modelo import Casa

if blackjack_defined:
    from juego.mundo.modelo import BlackJack


@pytest.fixture()
def carta():
    return Carta(pinta=CORAZON, valor="A")


class TestCarta:

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    def test_carta_class_decorated_with_dataclass(self, carta):
        assert hasattr(carta, "__dataclass_fields__")

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "constant_name, constant_value",
        [("VALORES", ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]),
         ("PINTAS", [CORAZON, TREBOL, DIAMANTE, ESPADA])])
    def test_carta_class_has_constants_with_value(self, carta, constant_name, constant_value):
        assert hasattr(carta, constant_name)
        assert getattr(carta, constant_name) == constant_value
