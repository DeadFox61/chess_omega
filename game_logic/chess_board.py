from game_logic.figures import Figure
from game_logic.board_position import BoardPosition
from game_logic.constants import FigureColor
from game_logic.figure_abilities import Ability
from game_logic.exceptions import SamePositionException


class BoardFigure:
    """Шахматная фигура на доске"""
    def __init__(self, figure: Figure, position: BoardPosition, color: FigureColor):
        self.figure = figure
        self.position = position
        self.color = color
        self.is_dead = False


class ChessBoard:
    """Представляет из себя состояние доски"""
    def __init__(self, figures: list[BoardFigure] | None = None):
        if figures is None:
            self.figures = []
        else:
            self.check_figures_position_collision(figures)
            self.figures = figures

    def get_figure_by_position(self, position: BoardPosition) -> BoardFigure | None:
        for figure in self.figures:
            if not figure.is_dead and figure.position == position:
                return figure
        return None

    def check_figures_position_collision(self, figures: list[BoardFigure]) -> None:
        for figure1 in figures:
            for figure2 in figures:
                if figure1 != figure2 and figure1.position == figure2.position:
                    raise SamePositionException

    def perform_action(self, figure: BoardFigure, ability: Ability, to_position: BoardPosition) -> None:
        ability.perform(self, figure, to_position)
