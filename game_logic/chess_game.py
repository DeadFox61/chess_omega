from game_logic.chess_board import ChessBoard, BoardFigure
from game_logic.figure_abilities import Ability
from game_logic.board_position import BoardPosition
from game_logic.constants import FigureColor


class ChessGame:
    """Класс управления игрой"""
    def __init__(self, board: ChessBoard, time_units: int):
        self.white_time = time_units
        self.black_time = time_units
        self.board = board

    def perform_move(self, figure: BoardFigure, ability: Ability, to_position: BoardPosition, time_units: int):
        if figure.color == FigureColor.WHITE:
            self.white_time -= time_units
        elif figure.color == FigureColor.BLACK:
            self.black_time -= time_units
