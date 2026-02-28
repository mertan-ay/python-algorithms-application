from typing import List, Sequence, Iterator


class Solver:
    """
    Backtracking solver for the 8-piece block puzzle.
    The board is represented as a 1D list with a padded border.
    """

    def __init__(self) -> None:
        self.board: List[int] = [-1] * 82
        self.free: List[bool] = [True] * 8
        self.solution_count: int = 0

        # Create border (blocked cells)
        for i in range(9):
            self.board[i * 9 + 8] = 99
        for i in range(72, 81):
            self.board[i] = 99

        self.standen = [4, 2, 8, 4, 4, 1, 4, 4]

        self.pieces: List[Sequence[Sequence[int]]] = [
            # Rood
            [
                [1,9,10,19,20,28,29],
                [1,9,10,17,18,26,27],
                [1,9,10,11,12,20,21],
                [1,7,8,9,10,16,17],
            ],
            # Paars
            [
                [1,2,3,9,10,11,12],
                [1,9,10,18,19,27,28],
            ],
            # Geel
            [
                [1,9,10,18,19,17,16],
                [1,9,10,18,19,20,21],
                [1,2,3,11,12,20,21],
                [1,2,3,9,10,18,19],
                [1,2,9,10,11,18,27],
                [9,18,27,19,20,28,29],
                [1,2,9,10,11,20,29],
                [9,18,27,16,17,25,26],
            ],
            # Groen
            [
                [9,18,19,20,21,12,3],
                [9,18,1,2,3,12,21],
                [1,2,11,20,29,28,27],
                [1,2,9,18,27,28,29],
            ],
            # Roze
            [
                [1,2,9,10,11,19,28],
                [1,9,10,18,19,11,12],
                [1,9,10,18,19,7,8],
                [9,17,18,19,26,27,28],
            ],
            # Zwart
            [
                [9,18,27,36,17,26,35],
            ],
            # Blauw
            [
                [1,2,9,10,11,18,19],
                [1,2,9,10,11,19,20],
                [1,9,10,8,19,11,20],
                [1,9,10,18,19,8,17],
            ],
            # Licht-Groen
            [
                [1,9,10,17,18,19,20],
                [1,2,3,10,11,19,20],
                [9,18,27,7,8,16,17],
                [9,18,27,10,11,19,20],
            ],
        ]

    def fits(self, piece: int, orientation: int, start: int) -> bool:
        if self.board[start] != -1:
            return False
        for offset in self.pieces[piece][orientation]:
            if self.board[start + offset] != -1:
                return False
        return True

    def place(self, piece: int, orientation: int, start: int) -> None:
        self.board[start] = piece
        for offset in self.pieces[piece][orientation]:
            self.board[start + offset] = piece
        self.free[piece] = False

    def remove(self, piece: int, orientation: int, start: int) -> None:
        self.board[start] = -1
        for offset in self.pieces[piece][orientation]:
            self.board[start + offset] = -1
        self.free[piece] = True

    def next_empty(self, start: int) -> int:
        i = start
        while self.board[i] != -1:
            i += 1
        return i

    def solve(self, start: int = 0) -> Iterator[List[int]]:
        for piece in range(8):
            if not self.free[piece]:
                continue

            for orientation in range(self.standen[piece]):
                if not self.fits(piece, orientation, start):
                    continue

                self.place(piece, orientation, start)
                nxt = self.next_empty(start)

                if nxt != 81:
                    yield from self.solve(nxt)
                else:
                    yield self.board.copy()

                self.remove(piece, orientation, start)


def format_board(board: List[int]) -> str:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
    lines = []
    for r in range(8):
        line = "".join(labels[board[r * 9 + c]] for c in range(8))
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    solver = Solver()
    for i, solution in enumerate(solver.solve(0), start=1):
        print(format_board(solution))
        print(f"\nSolution #{i}\n")


if __name__ == "__main__":
    main()