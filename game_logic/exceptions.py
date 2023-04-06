class OutOfBoardException(Exception):
    """Позиция вне рамок доски"""


class IllegalMoveException(Exception):
    """Невозможный ход"""


class SamePositionException(Exception):
    """Несколько фигур на одной позиции"""


class WrongAbilityException(Exception):
    """У фигуры нет такой абилки"""
