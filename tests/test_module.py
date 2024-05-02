import importlib.util
import inspect
import sys

import pytest


MODULE_NAME = "modelo"
CORAZON = "\u2764\uFE0F"
TREBOL = "\u2663\uFE0F"
DIAMANTE = "\u2666\uFE0F"
ESPADA = "\u2660\uFE0F"
OCULTA = "\u25AE\uFE0F"


@pytest.fixture(scope="session", autouse=True)
def module_members(pytestconfig):
    file = pytestconfig.getoption("module_file")
    spec = importlib.util.spec_from_file_location(MODULE_NAME, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[MODULE_NAME] = module
    return inspect.getmembers(module)


@pytest.fixture(scope="session")
def module_members_names(module_members):
    return [item[0] for item in module_members]


@pytest.fixture(scope="session")
def module_members_types(module_members):
    return {item[0]: item[1] for item in module_members}


@pytest.fixture(scope="session")
def modelo_module():
    return importlib.import_module(MODULE_NAME)


@pytest.fixture()
def carta_defined(module_members_names):
    assert "Carta" in module_members_names


@pytest.fixture()
def baraja_defined(module_members_names):
    assert "Baraja" in module_members_names


@pytest.fixture()
def mano_defined(module_members_names):
    assert "Mano" in module_members_names


@pytest.fixture()
def carta(modelo_module):
    return modelo_module.Carta(pinta=CORAZON, valor="A")


@pytest.fixture()
def not_visible_carta(modelo_module):
    return modelo_module.Carta(pinta=CORAZON, valor="A", visible=False)


@pytest.fixture()
def carta_class(modelo_module):
    return modelo_module.Carta


# Carta class tests

@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
def test_carta_class_decorated_with_dataclass(carta):
    assert hasattr(carta, "__dataclass_fields__")


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
@pytest.mark.parametrize(
    "constant_name, constant_value",
    [("VALORES", ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]),
     ("PINTAS", [CORAZON, TREBOL, DIAMANTE, ESPADA])])
def test_carta_class_has_constants_with_value(carta, constant_name, constant_value):
    assert hasattr(carta, constant_name)
    assert getattr(carta, constant_name) == constant_value


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
@pytest.mark.parametrize(
    "attribute_name, attribute_type",
    [("pinta", str), ("valor", str), ("visible", bool)]
)
def test_carta_class_has_attributes(carta, attribute_name, attribute_type):
    assert hasattr(carta, attribute_name)
    assert isinstance(getattr(carta, attribute_name), attribute_type)


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
def test_carta_class_visible_attribute_default_value(carta):
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
def test_carta_class_has_methods(carta, method_name, expected_return_type, args):
    assert hasattr(carta, method_name)
    method = getattr(carta, method_name)
    assert inspect.ismethod(method)
    assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
def test_carta_class_mostrar_method_changes_visible_attribute_to_true(not_visible_carta):
    not_visible_carta.mostrar()
    assert not_visible_carta.visible is True


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
def test_carta_class_ocultar_method_changes_visible_attribute_to_false(carta):
    carta.ocultar()
    assert carta.visible is False


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
@pytest.mark.parametrize(
    "as_como_11, expected_value",
    [(True, 11), (False, 1)]
)
def test_carta_class_calcular_valor_method_returns_11_or_1_for_as(carta, as_como_11, expected_value):
    carta.valor = "A"
    assert carta.calcular_valor(as_como_11) == expected_value


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
@pytest.mark.parametrize(
    "value, expected_return",
    [("J", 10), ("Q", 10), ("K", 10), ("2", 2), ("10", 10)]
)
def test_carta_class_calcular_valor_method_returns_expected_value(carta, value, expected_return):
    carta.valor = value
    assert carta.calcular_valor() == expected_return


@pytest.mark.xfail(not carta_defined, reason="Carta class not defined")
@pytest.mark.parametrize(
    "value, expected_return",
    [("A", True), ("J", True), ("Q", True), ("K", True), ("2", False), ("10", False)]
)
def test_carta_class_es_letra_method_returns_true_for_A_J_Q_K(carta, value, expected_return):
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
def test_carta_class_str_method_returns_expected_string(carta, valor, pinta, visible, expected_return):
    carta.valor = valor
    carta.pinta = pinta
    carta.visible = visible
    assert str(carta) == expected_return


@pytest.fixture()
def baraja(modelo_module):
    return modelo_module.Baraja()


@pytest.fixture()
def empty_baraja(modelo_module):
    baraja_ = modelo_module.Baraja()
    baraja_.cartas = []
    return baraja_

# Baraja class tests


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_not_decorated_with_dataclass(baraja):
    assert not hasattr(baraja, "__dataclass_fields__")


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_has_attribute_cartas(baraja):
    assert hasattr(baraja, "cartas")
    assert isinstance(baraja.cartas, list)


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
@pytest.mark.parametrize(
    "method_name, expected_return_type, args",
    [("reiniciar", None, []),
     ("revolver", None, []),
     ("tiene_cartas", bool, []),
     ("repartir", "carta_class", [True])]
)
def test_baraja_class_has_methods(baraja, method_name, expected_return_type, args, request):
    expected_return_type = request.getfixturevalue(expected_return_type) if isinstance(expected_return_type, str) \
        else expected_return_type
    assert hasattr(baraja, method_name)
    method = getattr(baraja, method_name)
    assert inspect.ismethod(method)
    assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_reiniciar_method_called_on_init(baraja, modelo_module):
    for pinta in modelo_module.Carta.PINTAS:
        for valor in modelo_module.Carta.VALORES:
            assert modelo_module.Carta(pinta, valor) in baraja.cartas


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_reiniciar_method_adds_52_cards_to_cartas_attribute(baraja):
    baraja.reiniciar()
    assert len(baraja.cartas) == 52


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_revolver_method_shuffles_cartas_attribute(baraja):
    baraja.reiniciar()
    original_cartas = baraja.cartas.copy()
    baraja.revolver()
    assert original_cartas != baraja.cartas
    assert len(original_cartas) == len(baraja.cartas)


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_tiene_cartas_method_returns_true_if_cartas_attribute_has_elements(baraja):
    baraja.reiniciar()
    assert baraja.tiene_cartas() is True


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_tiene_cartas_method_returns_false_if_cartas_attribute_is_empty(empty_baraja):
    assert empty_baraja.tiene_cartas() is False


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_repartir_method_returns_carta_instance(baraja, modelo_module):
    baraja.reiniciar()
    assert isinstance(baraja.repartir(), modelo_module.Carta)


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_repartir_method_returns_carta_instance_with_visible_attribute_true(baraja):
    baraja.reiniciar()
    assert baraja.repartir().visible is True


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_repartir_method_returns_carta_instance_with_visible_attribute_false(baraja):
    baraja.reiniciar()
    assert baraja.repartir(oculta=True).visible is False


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_repartir_method_returns_none_if_cartas_attribute_is_empty(empty_baraja):
    assert empty_baraja.repartir() is None


@pytest.mark.xfail(not baraja_defined, reason="Baraja class not defined")
def test_baraja_class_repartir_method_removes_carta_from_cartas_attribute(baraja):
    baraja.reiniciar()
    carta_ = baraja.repartir()
    assert carta_ not in baraja.cartas


@pytest.fixture()
def mano(modelo_module):
    return modelo_module.Mano()


# Mano class tests

@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_not_decorated_with_dataclass(mano):
    assert not hasattr(mano, "__dataclass_fields__")


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "attribute_name, attribute_type",
    [("cartas", list), ("cantidad_ases", int)]
)
def test_mano_class_has_attributes(mano, attribute_name, attribute_type):
    assert hasattr(mano, attribute_name)
    assert isinstance(getattr(mano, attribute_name), attribute_type)


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "attribute_name, expected_default_value",
    [("cartas", []), ("cantidad_ases", 0)]
)
def test_mano_class_attributes_default_values_on_init(mano, attribute_name, expected_default_value):
    assert getattr(mano, attribute_name) == expected_default_value


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "method_name, expected_return_type, args",
    [("limpiar", None, []),
     ("agregar_carta", None, "carta"),
     ("calcular_valor", int, []),
     ("__gt__", bool, "mano"),
     ("__str__", str, [])]
)
def test_mano_class_has_methods(mano, method_name, expected_return_type, args, request):
    args = [request.getfixturevalue(args)] if isinstance(args, str) else args
    assert hasattr(mano, method_name)
    method = getattr(mano, method_name)
    assert inspect.ismethod(method)
    assert method(*args) is None if expected_return_type is None else isinstance(method(*args), expected_return_type)


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_limpiar_method_clears_cartas_attribute(mano, modelo_module):
    mano.cartas = [modelo_module.Carta(pinta=CORAZON, valor="A")]
    mano.limpiar()
    assert mano.cartas == []


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_limpiar_method_resets_cantidad_ases_attribute(mano):
    mano.cantidad_ases = 2
    mano.limpiar()
    assert mano.cantidad_ases == 0


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_agregar_carta_method_adds_carta_to_cartas_attribute(mano, modelo_module):
    carta_ = modelo_module.Carta(pinta=CORAZON, valor="A")
    mano.agregar_carta(carta_)
    assert carta_ in mano.cartas


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_agregar_carta_method_increments_cantidad_ases_attribute(mano, modelo_module):
    carta_ = modelo_module.Carta(pinta=CORAZON, valor="A")
    mano.agregar_carta(carta_)
    assert mano.cantidad_ases == 1


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_agregar_carta_method_adds_as_to_end_of_cartas_attribute(mano, modelo_module):
    carta_ = modelo_module.Carta(pinta=CORAZON, valor="A")
    mano.agregar_carta(carta_)
    assert mano.cartas[-1] == carta_


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
def test_mano_class_agregar_carta_method_adds_non_as_to_beginning_of_cartas_attribute(mano, modelo_module):
    carta_ = modelo_module.Carta(pinta=CORAZON, valor="2")
    mano.agregar_carta(carta_)
    assert mano.cartas[0] == carta_


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "cartas, expected_return",
    [([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "2"}], 13),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "K"}], 21),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "2"}], 4),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "A"}], 13),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "A", "visible": False}], "--")]
)
def test_mano_class_calcular_valor_method_returns_expected_value(mano, modelo_module, cartas, expected_return):
    cartas = [modelo_module.Carta(**carta) for carta in cartas]
    mano.cartas = cartas
    assert mano.calcular_valor() == expected_return


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "cartas, expected_return",
    [([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "K"}], True),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "2"}], False),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "2"}], False),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "A"}], False),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "A"}], False),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "Q"}], True),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "J"}], True),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "10"}], True)]
)
def test_mano_class_es_blackjack_method_returns_expected_value(mano, modelo_module, cartas, expected_return):
    cartas = [modelo_module.Carta(**carta) for carta in cartas]
    mano.cartas = cartas
    assert mano.es_blackjack() == expected_return


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "other_cartas, expected_return",
    [([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "K"}], False),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "2"}], True),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "2"}], True),
     ([{"pinta": CORAZON, "valor": "2"}, {"pinta": CORAZON, "valor": "A"}], True),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "A"}], True),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "Q"}], False),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "J"}], False),
     ([{"pinta": CORAZON, "valor": "A"}, {"pinta": CORAZON, "valor": "10"}], False)]
)
def test_mano_class_gt_method_returns_expected_value(mano, modelo_module, other_cartas, expected_return):
    mano.cartas = [modelo_module.Carta(pinta=CORAZON, valor="A"), modelo_module.Carta(pinta=CORAZON, valor="K")]
    other_mano = modelo_module.Mano()
    other_mano.cartas = [modelo_module.Carta(**carta) for carta in other_cartas]
    assert (mano > other_mano) == expected_return


@pytest.mark.xfail(not mano_defined, reason="Mano class not defined")
@pytest.mark.parametrize(
    "cartas, expected_return",
    [([{"pinta": CORAZON,  "valor": "A"}, {"pinta": CORAZON,  "valor": "K"}], f"{"A"+CORAZON:^5}{"K"+CORAZON:^5}"),
     ([{"pinta": CORAZON,  "valor": "A"}, {"pinta": CORAZON,  "valor": "2"}], f"{"A"+CORAZON:^5}{"2"+CORAZON:^5}"),
     ([{"pinta": CORAZON,  "valor": "2"}, {"pinta": CORAZON,  "valor": "2"}], f"{"2"+CORAZON:^5}{"2"+CORAZON:^5}"),
     ([{"pinta": CORAZON,  "valor": "2"}, {"pinta": CORAZON,  "valor": "A"}], f"{"2"+CORAZON:^5}{"A"+CORAZON:^5}"),
     ([{"pinta": TREBOL,   "valor": "A"},  {"pinta": CORAZON, "valor": "A"}], f"{"A"+TREBOL:^5}{"A"+CORAZON:^5}"),
     ([{"pinta": CORAZON,  "valor": "A"}, {"pinta": ESPADA,   "valor": "Q"}], f"{"A"+CORAZON:^5}{"Q"+ESPADA:^5}"),
     ([{"pinta": DIAMANTE, "valor": "A"}, {"pinta": CORAZON,   "valor": "J"}], f"{"A"+DIAMANTE:^5}{"J"+CORAZON:^5}"),
     ([{"pinta": CORAZON,  "valor": "A"}, {"pinta": CORAZON,  "valor": "10"}], f"{"A"+CORAZON:^5}{"10"+CORAZON:^5}")]
)
def test_mano_class_str_method_returns_expected_value(mano, modelo_module, cartas, expected_return):
    cartas = [modelo_module.Carta(**carta) for carta in cartas]
    mano.cartas = cartas
    assert str(mano) == expected_return
