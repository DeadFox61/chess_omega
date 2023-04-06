from __future__ import annotations
from abc import ABC, abstractmethod

from game_logic.exceptions import IllegalMoveException, WrongAbilityException
from game_logic.board_position import BoardPosition

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_logic.chess_board import ChessBoard, BoardFigure
    from game_logic.board_position import BoardPosition


class Ability(ABC):
    @abstractmethod
    def perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition | None = None) -> None:
        """Применяет абилку к доске"""
        pass

    def check_ability(self, figure: BoardFigure):
        if self.__class__ not in figure.figure.abilities:
            raise WrongAbilityException


class MoveAbility(Ability):
    @abstractmethod
    def is_can_perform(self, board: ChessBoard, from_pos: BoardPosition, to_pos: BoardPosition) -> bool:
        """Проверка возможности передвинуть фигуру или побить другую"""

    def perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition | None = None) -> None:
        """Передвигает фигуру"""
        self.check_ability(figure)
        if self.is_can_perform(board, figure, to_pos):
            to_figure = board.get_figure_by_position(to_pos)
            figure.position = to_pos
            if to_figure is not None:
                to_figure.is_dead = True
        else:
            raise IllegalMoveException


class RookMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        to_figure = board.get_figure_by_position(to_pos)
        if to_figure is not None:
            if to_figure.color == figure.color:
                return False

        if to_pos.x != figure.position.x and to_pos.y != figure.position.y:
            return False

        if to_pos.x == figure.position.x:
            if to_pos.y < figure.position.y:
                bad_y_range = range(to_pos.y + 1, figure.position.y)
            else:
                bad_y_range = range(figure.position.y + 1, to_pos.y)
            for curr_figure in board.figures:
                if curr_figure.position.x == figure.position.x and curr_figure.position.y in bad_y_range:
                    return False

        if to_pos.y == figure.position.y:
            if to_pos.x < figure.position.x:
                bad_x_range = range(to_pos.x + 1, figure.position.x)
            else:
                bad_x_range = range(figure.position.x + 1, to_pos.x)
            for curr_figure in board.figures:
                if curr_figure.position.y == figure.position.y and curr_figure.position.x in bad_x_range:
                    return False
        return True


class BishopMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        to_figure = board.get_figure_by_position(to_pos)
        if to_figure is not None:
            if to_figure.color == figure.color:
                return False

        if abs(to_pos.x - figure.position.x) != abs(to_pos.y - figure.position.y):
            return False

        move_range = range(1, abs(to_pos.x - figure.position.x)+1)
        bad_positions = [BoardPosition(x=figure.position.x+i, y=figure.position.y+i) for i in move_range]
        for curr_figure in board.figures:
            if curr_figure.position in bad_positions:
                return False

        return True


class KnightMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        to_figure = board.get_figure_by_position(to_pos)
        if to_figure is not None:
            if to_figure.color == figure.color:
                return False

        x_diff = abs(to_pos.x - figure.position.x)
        y_diff = abs(to_pos.y - figure.position.y)

        if not ((x_diff == 1 and y_diff == 2) or (x_diff == 2 and y_diff == 1)):
            return False

        return True


class QueenMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        return True


class KingMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        return True


class PawnMoveAbility(MoveAbility):
    def is_can_perform(self, board: ChessBoard, figure: BoardFigure, to_pos: BoardPosition) -> bool:
        return True
