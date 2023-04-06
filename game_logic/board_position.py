from game_logic.exceptions import OutOfBoardException


class BoardPosition:
    """класс представляющий координаты фигуры"""
    BOARD_LEN = 8

    def __init__(self, x: int, y: int):
        self.check_coords_in_board(x, y)
        self.x = x
        self.y = y

    def check_coords_in_board(self, x: int, y: int) -> None:
        if x not in range(0, self.BOARD_LEN):
            raise OutOfBoardException
        if y not in range(0, self.BOARD_LEN):
            raise OutOfBoardException

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Position ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()
