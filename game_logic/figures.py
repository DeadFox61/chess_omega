from abc import ABC, abstractmethod
from game_logic.figure_abilities import (
    Ability,
    RookMoveAbility,
    BishopMoveAbility,
    KnightMoveAbility,
    QueenMoveAbility,
    KingMoveAbility,
    PawnMoveAbility,
)


class Figure(ABC):
    """Абстрактный класс фигуры"""
    abilities = []


class RookFigure(Figure):
    abilities = [
        RookMoveAbility
    ]


class BishopFigure(Figure):
    abilities = [
        BishopMoveAbility
    ]


class KnightFigure(Figure):
    abilities = [
        KnightMoveAbility
    ]


class QueenFigure(Figure):
    abilities = [
        QueenMoveAbility
    ]


class KingFigure(Figure):
    abilities = [
        KingMoveAbility
    ]


class PawnFigure(Figure):
    abilities = [
        PawnMoveAbility
    ]
