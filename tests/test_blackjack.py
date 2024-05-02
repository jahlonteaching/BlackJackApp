import pytest
import inspect

import juego.mundo.modelo

from juego.mundo.modelo import CORAZON, DIAMANTE, TREBOL, ESPADA, OCULTA

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


@pytest.fixture()
def not_visible_carta():
    return Carta(pinta=CORAZON, valor="A", visible=False)


class TestCarta:

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    def test_class_decorated_with_dataclass(self, carta):
        assert hasattr(carta, "__dataclass_fields__")

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "constant_name, constant_value",
        [("VALORES", ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]),
         ("PINTAS", [CORAZON, TREBOL, DIAMANTE, ESPADA])])
    def test_class_has_constants_with_value(self, carta, constant_name, constant_value):
        assert hasattr(carta, constant_name)
        assert getattr(carta, constant_name) == constant_value

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("pinta", str), ("valor", str), ("visible", bool)]
    )
    def test_class_has_attributes(self, carta, attribute_name, attribute_type):
        assert hasattr(carta, attribute_name)
        assert isinstance(getattr(carta, attribute_name), attribute_type)

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    def test_class_visible_attribute_default_value(self, carta):
        assert carta.visible is True

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("mostrar", None, []),
         ("ocultar", None, []),
         ("calcular_valor", int, [True]),
         ("es_letra", bool, []),
         ("__str__", str, [])]
    )
    def test_class_has_methods(self, carta, method_name, expected_return_type, args):
        assert hasattr(carta, method_name)
        method = getattr(carta, method_name)
        assert inspect.ismethod(method)
        assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    def test_mostrar_method_changes_visible_attribute_to_true(self, not_visible_carta):
        not_visible_carta.mostrar()
        assert not_visible_carta.visible is True

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    def test_ocultar_method_changes_visible_attribute_to_false(self, carta):
        carta.ocultar()
        assert carta.visible is False

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "as_como_11, expected_value",
        [(True, 11), (False, 1)]
    )
    def test_calcular_valor_method_returns_11_or_1_for_as(self, carta, as_como_11, expected_value):
        carta.valor = "A"
        assert carta.calcular_valor(as_como_11) == expected_value

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "value, expected_return",
        [("J", 10), ("Q", 10), ("K", 10), ("2", 2), ("10", 10)]
    )
    def test_calcular_valor_method_returns_expected_value(self, carta, value, expected_return):
        carta.valor = value
        assert carta.calcular_valor() == expected_return

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "value, expected_return",
        [("A", True), ("J", True), ("Q", True), ("K", True), ("2", False), ("10", False)]
    )
    def test_es_letra_method_returns_true_for_A_J_Q_K(self, carta, value, expected_return):
        carta.valor = value
        assert carta.es_letra() == expected_return

    @pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
    @pytest.mark.parametrize(
        "valor, pinta, visible, expected_return",
        [("A", CORAZON, True, f"A{CORAZON}"),
         ("A", CORAZON, False, f"{OCULTA}"),
         ("J", TREBOL, True, f"J{TREBOL}"),
         ("Q", DIAMANTE, True, f"Q{DIAMANTE}"),
         ("K", ESPADA, True, f"K{ESPADA}"),
         ("2", CORAZON, True, f"2{CORAZON}"),
         ("10", DIAMANTE, True, f"10{DIAMANTE}")]
    )
    def test_str_method_returns_expected_string(self, carta, valor, pinta, visible, expected_return):
        carta.valor = valor
        carta.pinta = pinta
        carta.visible = visible
        assert str(carta) == expected_return


@pytest.fixture()
def baraja():
    return Baraja()


@pytest.fixture()
def empty_baraja():
    baraja = Baraja()
    baraja.cartas = []
    return baraja


class TestBaraja:

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_class_not_decorated_with_dataclass(self, baraja):
        assert not hasattr(baraja, "__dataclass_fields__")

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_class_has_attribute_cartas(self, baraja):
        assert hasattr(baraja, "cartas")
        assert isinstance(baraja.cartas, list)

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("reiniciar", None, []),
         ("revolver", None, []),
         ("tiene_cartas", bool, []),
         ("repartir", Carta, [True])]
    )
    def test_class_has_methods(self, baraja, method_name, expected_return_type, args):
        assert hasattr(baraja, method_name)
        method = getattr(baraja, method_name)
        assert inspect.ismethod(method)
        assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_reiniciar_method_called_on_init(self, baraja):
        for pinta in Carta.PINTAS:
            for valor in Carta.VALORES:
                assert Carta(pinta, valor) in baraja.cartas

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_reiniciar_method_adds_52_cards_to_cartas_attribute(self, baraja):
        baraja.reiniciar()
        assert len(baraja.cartas) == 52

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_revolver_method_shuffles_cartas_attribute(self, baraja):
        baraja.reiniciar()
        original_cartas = baraja.cartas.copy()
        baraja.revolver()
        assert original_cartas != baraja.cartas
        assert len(original_cartas) == len(baraja.cartas)

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_tiene_cartas_method_returns_true_if_cartas_attribute_has_elements(self, baraja):
        baraja.reiniciar()
        assert baraja.tiene_cartas() is True

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_tiene_cartas_method_returns_false_if_cartas_attribute_is_empty(self, empty_baraja):
        assert empty_baraja.tiene_cartas() is False

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_repartir_method_returns_carta_instance(self, baraja):
        baraja.reiniciar()
        assert isinstance(baraja.repartir(), Carta)

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_repartir_method_returns_carta_instance_with_visible_attribute_true(self, baraja):
        baraja.reiniciar()
        assert baraja.repartir().visible is True

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_repartir_method_returns_carta_instance_with_visible_attribute_false(self, baraja):
        baraja.reiniciar()
        assert baraja.repartir(oculta=True).visible is False

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_repartir_method_returns_none_if_cartas_attribute_is_empty(self, empty_baraja):
        assert empty_baraja.repartir() is None

    @pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
    def test_repartir_method_removes_carta_from_cartas_attribute(self, baraja):
        baraja.reiniciar()
        carta = baraja.repartir()
        assert carta not in baraja.cartas


@pytest.fixture()
def mano():
    return Mano()


class TestMano:

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_class_not_decorated_with_dataclass(self, mano):
        assert not hasattr(mano, "__dataclass_fields__")

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("cartas", list), ("cantidad_ases", int)]
    )
    def test_class_has_attributes(self, mano, attribute_name, attribute_type):
        assert hasattr(mano, attribute_name)
        assert isinstance(getattr(mano, attribute_name), attribute_type)

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "attribute_name, expected_default_value",
        [("cartas", []), ("cantidad_ases", 0)]
    )
    def test_attributes_default_values_on_init(self, mano, attribute_name, expected_default_value):
        assert getattr(mano, attribute_name) == expected_default_value

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("limpiar", None, []),
         ("agregar_carta", None, [Carta(pinta=CORAZON, valor="A")]),
         ("calcular_valor", int, []),
         ("__gt__", bool, [Mano()]),
         ("__str__", str, [])]
    )
    def test_class_has_methods(self, mano, method_name, expected_return_type, args):
        assert hasattr(mano, method_name)
        method = getattr(mano, method_name)
        assert inspect.ismethod(method)
        assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_limpiar_method_clears_cartas_attribute(self, mano):
        mano.cartas = [Carta(pinta=CORAZON, valor="A")]
        mano.limpiar()
        assert mano.cartas == []

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_limpiar_method_resets_cantidad_ases_attribute(self, mano):
        mano.cantidad_ases = 2
        mano.limpiar()
        assert mano.cantidad_ases == 0

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_agregar_carta_method_adds_carta_to_cartas_attribute(self, mano):
        carta = Carta(pinta=CORAZON, valor="A")
        mano.agregar_carta(carta)
        assert carta in mano.cartas

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_agregar_carta_method_increments_cantidad_ases_attribute(self, mano):
        carta = Carta(pinta=CORAZON, valor="A")
        mano.agregar_carta(carta)
        assert mano.cantidad_ases == 1

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_agregar_carta_method_adds_as_to_end_of_cartas_attribute(self, mano):
        carta = Carta(pinta=CORAZON, valor="A")
        mano.agregar_carta(carta)
        assert mano.cartas[-1] == carta

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    def test_agregar_carta_method_adds_non_as_to_beginning_of_cartas_attribute(self, mano):
        carta = Carta(pinta=CORAZON, valor="2")
        mano.agregar_carta(carta)
        assert mano.cartas[0] == carta

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "cartas, expected_return",
        [([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="2")], 13),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="K")], 21),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="A")], 12),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="2")], 4),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="K")], 12),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="A", visible=False)], "--")]
    )
    def test_calcular_valor_method_returns_expected_value(self, mano, cartas, expected_return):
        mano.cartas = cartas
        assert mano.calcular_valor() == expected_return

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "cartas, expected_return",
        [([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="K")], True),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="2")], False),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="2")], False),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="A")], False),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="A")], False),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="Q")], True),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="J")], True),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="10")], True)]
    )
    def test_es_blackjack_method_returns_expected_value(self, mano, cartas, expected_return):
        mano.cartas = cartas
        assert mano.es_blackjack() == expected_return

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "other_cartas, expected_return",
        [([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="K")], False),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="2")], True),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="2")], True),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="A")], True),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="A")], True),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="Q")], False),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="J")], False),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="10")], False)]
    )
    def test_gt_method_returns_expected_value(self, mano, other_cartas, expected_return):
        mano.cartas = [Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="K")]
        other_mano = Mano()
        other_mano.cartas = other_cartas
        assert (mano > other_mano) == expected_return

    @pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
    @pytest.mark.parametrize(
        "cartas, expected_return",
        [([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="K")], f"{"A"+CORAZON:^5}{"K"+CORAZON:^5}"),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="2")], f"{"A"+CORAZON:^5}{"2"+CORAZON:^5}"),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="2")], f"{"2"+CORAZON:^5}{"2"+CORAZON:^5}"),
         ([Carta(pinta=CORAZON, valor="2"), Carta(pinta=CORAZON, valor="A")], f"{"2"+CORAZON:^5}{"A"+CORAZON:^5}"),
         ([Carta(pinta=TREBOL, valor="A"), Carta(pinta=CORAZON, valor="A")], f"{"A"+TREBOL:^5}{"A"+CORAZON:^5}"),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=ESPADA, valor="Q")], f"{"A"+CORAZON:^5}{"Q"+ESPADA:^5}"),
         ([Carta(pinta=DIAMANTE, valor="A"), Carta(pinta=CORAZON, valor="J")], f"{"A"+DIAMANTE:^5}{"J"+CORAZON:^5}"),
         ([Carta(pinta=CORAZON, valor="A"), Carta(pinta=CORAZON, valor="10")], f"{"A"+CORAZON:^5}{"10"+CORAZON:^5}")]
    )
    def test_str_method_returns_expected_value(self, mano, cartas, expected_return):
        mano.cartas = cartas
        assert str(mano) == expected_return
