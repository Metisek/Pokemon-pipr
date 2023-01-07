from pygame_objects import AbstractWidget, Button, PokemonFrame

from classes import (
    InvalidDataTypeError,
    InvalidDataLineLeghthError,
    NotANumberError
)

from pytest import raises


# Global testing variables

size = (200, 40)
pos = (100, 100)

# Odpuszczam testy sprawdzajace czy dane wartosci są floatami,
# Odpowiednie testy są w test_model_io.py

def test_abstract_widget_init():
    abstract_widget = AbstractWidget(size, pos)
    assert abstract_widget.get_pos() == (100, 100)
    assert abstract_widget.get_size() == (200, 40)


def test_abstract_widget_not_list_or_tuple():
    with raises(InvalidDataTypeError):
        AbstractWidget(22, pos)


def test_abstract_widget_not_too_large_tuple():
    with raises(InvalidDataLineLeghthError):
        AbstractWidget((20, 20, 20), pos)


def test_abstract_widget_tuple_values_not_convertable_to_float():
    with raises(NotANumberError):
        AbstractWidget((20, 'test'), pos)


def test_abstract_widget_tuple_set_pos_typical():
    abstract_widget = AbstractWidget(size, pos)
    abstract_widget._set_pos((20, 30))
    assert abstract_widget.get_pos() == (20, 30)


def test_button_init():
    button = Button("test", size, pos)
    assert button.get_color('frame_inactive') == (200, 208, 218)
    assert button.get_pos() == (100, 100)
    assert button.get_size() == (200, 40)
    assert button.get_button_text() == "test"


def test_button_draw_button_values():
    button = Button("test", size, pos)
    button.get_draw_values()