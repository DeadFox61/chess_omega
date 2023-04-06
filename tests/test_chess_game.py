import unittest

from game_logic.board_position import BoardPosition
from game_logic.chess_board import ChessBoard, BoardFigure
from game_logic.constants import FigureColor
from game_logic.chess_game import ChessGame
from game_logic.exceptions import (
    OutOfBoardException,
    IllegalMoveException,
    SamePositionException,
    WrongAbilityException,
)
from game_logic.figure_abilities import (
    RookMoveAbility,
    BishopMoveAbility,
    KnightMoveAbility,
    QueenMoveAbility,
    KingMoveAbility,
    PawnMoveAbility,
)
from game_logic.figures import (
    RookFigure,
    BishopFigure,
    KnightFigure,
    QueenFigure,
    KingFigure,
    PawnFigure,
)


class TestBoardPosition(unittest.TestCase):
    def test_create(self):
        pos = BoardPosition(0, 0)

    def test_out_of_board(self):
        with self.assertRaises(OutOfBoardException):
            pos = BoardPosition(0, 8)


class TestBoardFigure(unittest.TestCase):
    def test_create_with_rook(self):
        rook = RookFigure()
        board_figure = BoardFigure(
            figure=rook, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        self.assertEqual(board_figure.figure, rook)


class TestChessBoard(unittest.TestCase):
    def test_create(self):
        board = ChessBoard()

    def test_create_with_empty_data(self):
        board = ChessBoard()
        self.assertEqual(board.figures, [])

    def test_create_with_one_rook(self):
        rook = RookFigure()
        rook_figure = BoardFigure(
            figure=rook, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[rook_figure])
        self.assertEqual(board.figures, [rook_figure])

    def test_create_figures_in_same_position(self):
        rook_figure = RookFigure()
        board_rook_figure1 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_rook_figure2 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        with self.assertRaises(SamePositionException):
            board = ChessBoard(figures=[board_rook_figure1, board_rook_figure2])

    def test_create_one_rook_and_legal_move(self):
        rook_figure = RookFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure])
        rook_move_ability = RookMoveAbility()
        board.perform_action(
            figure=board_rook_figure,
            ability=rook_move_ability,
            to_position=BoardPosition(0, 1),
        )
        self.assertEqual(board_rook_figure.position, BoardPosition(0, 1))

    def test_capturing_rook_with_rook(self):
        rook_figure = RookFigure()
        board_rook_figure1 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_rook_figure2 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 1), color=FigureColor.BLACK
        )
        board = ChessBoard(figures=[board_rook_figure1, board_rook_figure2])
        rook_move_ability = RookMoveAbility()
        board.perform_action(
            figure=board_rook_figure1,
            ability=rook_move_ability,
            to_position=BoardPosition(0, 1),
        )
        self.assertEqual(board_rook_figure1.position, BoardPosition(0, 1))
        self.assertEqual(board_rook_figure2.is_dead, True)

    def test_capturing_same_color_rook(self):
        rook_figure = RookFigure()
        board_rook_figure1 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_rook_figure2 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 1), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure1, board_rook_figure2])
        rook_move_ability = RookMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_rook_figure1,
                ability=rook_move_ability,
                to_position=BoardPosition(0, 1),
            )

    def test_moving_rook_to_cell_not_on_same_line(self):
        rook_figure = RookFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure])
        rook_move_ability = RookMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_rook_figure,
                ability=rook_move_ability,
                to_position=BoardPosition(1, 1),
            )

    def test_moving_rook_through_another_rook(self):
        rook_figure = RookFigure()
        board_rook_figure1 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_rook_figure2 = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 1), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure1, board_rook_figure2])
        rook_move_ability = RookMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_rook_figure1,
                ability=rook_move_ability,
                to_position=BoardPosition(0, 2),
            )

    def test_doing_wrong_ability(self):
        rook_figure = RookFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure])
        rook_move_bishop = BishopMoveAbility()
        with self.assertRaises(WrongAbilityException):
            board.perform_action(
                figure=board_rook_figure,
                ability=rook_move_bishop,
                to_position=BoardPosition(0, 1),
            )

    def test_create_and_move_bishop(self):
        bishop_figure = BishopFigure()
        board_bishop_figure = BoardFigure(
            figure=bishop_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_bishop_figure])
        bishop_move_ability = BishopMoveAbility()
        board.perform_action(
            figure=board_bishop_figure,
            ability=bishop_move_ability,
            to_position=BoardPosition(1, 1),
        )
        self.assertEqual(board_bishop_figure.position, BoardPosition(1, 1))

    def test_capturing_rook_with_bishop(self):
        rook_figure = RookFigure()
        bishop_figure = BishopFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_bishop_figure = BoardFigure(
            figure=bishop_figure, position=BoardPosition(1, 1), color=FigureColor.BLACK
        )
        board = ChessBoard(figures=[board_rook_figure, board_bishop_figure])
        bishop_move_ability = BishopMoveAbility()
        board.perform_action(
            figure=board_bishop_figure,
            ability=bishop_move_ability,
            to_position=BoardPosition(0, 0),
        )
        self.assertEqual(board_bishop_figure.position, BoardPosition(0, 0))
        self.assertEqual(board_rook_figure.is_dead, True)

    def test_capturing_same_color_rook_with_bishop(self):
        rook_figure = RookFigure()
        bishop_figure = BishopFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_bishop_figure = BoardFigure(
            figure=bishop_figure, position=BoardPosition(1, 1), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure, board_bishop_figure])
        bishop_move_ability = BishopMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_bishop_figure,
                ability=bishop_move_ability,
                to_position=BoardPosition(0, 0),
            )

    def test_create_and_move_bishop_on_different_diagonal(self):
        bishop_figure = BishopFigure()
        board_bishop_figure = BoardFigure(
            figure=bishop_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_bishop_figure])
        bishop_move_ability = BishopMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_bishop_figure,
                ability=bishop_move_ability,
                to_position=BoardPosition(1, 2),
            )

    def test_bishop_moving_over_another_figure(self):
        rook_figure = RookFigure()
        bishop_figure = BishopFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(1, 1), color=FigureColor.WHITE
        )
        board_bishop_figure = BoardFigure(
            figure=bishop_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure, board_bishop_figure])
        bishop_move_ability = BishopMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_bishop_figure,
                ability=bishop_move_ability,
                to_position=BoardPosition(2, 2),
            )

    def test_knight_legal_move(self):
        knight_figure = KnightFigure()
        board_knight_figure = BoardFigure(
            figure=knight_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_knight_figure])
        knight_move_ability = KnightMoveAbility()
        board.perform_action(
            figure=board_knight_figure,
            ability=knight_move_ability,
            to_position=BoardPosition(1, 2),
        )
        self.assertEqual(board_knight_figure.position, BoardPosition(1, 2))

    def test_capturing_rook_with_knight(self):
        rook_figure = RookFigure()
        knight_figure = KnightFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_knight_figure = BoardFigure(
            figure=knight_figure, position=BoardPosition(1, 2), color=FigureColor.BLACK
        )
        board = ChessBoard(figures=[board_rook_figure, board_knight_figure])
        bishop_move_ability = KnightMoveAbility()
        board.perform_action(
            figure=board_knight_figure,
            ability=bishop_move_ability,
            to_position=BoardPosition(0, 0),
        )
        self.assertEqual(board_knight_figure.position, BoardPosition(0, 0))
        self.assertEqual(board_rook_figure.is_dead, True)

    def test_capturing_same_color_rook_with_knight(self):
        rook_figure = RookFigure()
        knight_figure = KnightFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_knight_figure = BoardFigure(
            figure=knight_figure, position=BoardPosition(1, 2), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_rook_figure, board_knight_figure])
        bishop_move_ability = KnightMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_knight_figure,
                ability=bishop_move_ability,
                to_position=BoardPosition(0, 0),
            )
        self.assertEqual(board_knight_figure.position, BoardPosition(1, 2))
        self.assertEqual(board_rook_figure.is_dead, False)

    def test_capturing_rook_with_knight_on_illegal_pos(self):
        rook_figure = RookFigure()
        knight_figure = KnightFigure()
        board_rook_figure = BoardFigure(
            figure=rook_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board_knight_figure = BoardFigure(
            figure=knight_figure, position=BoardPosition(1, 3), color=FigureColor.BLACK
        )
        board = ChessBoard(figures=[board_rook_figure, board_knight_figure])
        bishop_move_ability = KnightMoveAbility()
        with self.assertRaises(IllegalMoveException):
            board.perform_action(
                figure=board_knight_figure,
                ability=bishop_move_ability,
                to_position=BoardPosition(0, 0),
            )
        self.assertEqual(board_knight_figure.position, BoardPosition(1, 3))
        self.assertEqual(board_rook_figure.is_dead, False)

    def test_moving_queen_vertical(self):
        queen_figure = QueenFigure()
        board_queen_figure = BoardFigure(
            figure=queen_figure, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[board_queen_figure])
        queen_move_ability = QueenMoveAbility()
        board.perform_action(
            figure=board_queen_figure,
            ability=queen_move_ability,
            to_position=BoardPosition(4, 0),
        )
        self.assertEqual(board_queen_figure.position, BoardPosition(4, 0))


class TestRookAbilities(unittest.TestCase):
    def test_create(self):
        ability = RookMoveAbility()


class TestChessGame(unittest.TestCase):
    def test_create_with_one_rook(self):
        rook = RookFigure()
        rook_figure = BoardFigure(
            figure=rook, position=BoardPosition(0, 0), color=FigureColor.WHITE
        )
        board = ChessBoard(figures=[rook_figure])
        game = ChessGame(board=board, time_units=150)

        self.assertEqual(game.board, board)
        self.assertEqual(game.board.figures[0], rook_figure)
