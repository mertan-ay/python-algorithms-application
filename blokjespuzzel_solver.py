from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List, Sequence


Offsets = Sequence[int]
Orientations = Sequence[Offsets]


@dataclass(frozen=True)
class Solution:
    board: List[int]  # copy of internal board state


class BlokjespuzzelSolver:
    """
    Backtracking solver (depth-first search) for an 8x8 block puzzle.
    Board is represented as a 1D list with a padded border to simplify bounds checks.
    """

    def __init__(self) -> None:
        # 8x8 playable area, but stored in a 9-wide grid with last column as border
        # plus a bottom border row -> total length 82 in original student approach
        self.vakje: List[int] = [-1] * 82
        self.vrij: List[bool] = [True] * 8
        self.opl: int = 0

        # Maak een rand van bezette vakjes (99 = border/blocked)
        for i in range(9):
            self.vakje[i * 9 + 8] = 99
        for i in range(72, 81):
            self.vakje[i] = 99

        # Zwart heeft maar 1 stand om spiegelingen te voorkomen
        self.standen: List[int] = [4, 2, 8, 4, 4, 1, 4, 4]
        # ............Rood, Paars, Geel, Groen, Roze, Zwart, Blauw, Licht-Groen

        # Offsets of the 7 extra squares relative to 'vanaf' (the anchor square)
        self.viertal: List[Orientations] = [
            [  # Rood
                [1, 9, 10, 19, 20, 28, 29],
                [1, 9, 10, 17, 18, 26, 27],
                [1, 9, 10, 11, 12, 20, 21],
                [1, 7, 8, 9, 10, 16, 17],
            ],
            [  # Paars
                [1, 2, 3, 9, 10, 11, 12],
                [1, 9, 10, 18, 19, 27, 28],
            ],
            [  # Geel
                [1, 9, 10, 18, 19, 17, 16],
                [1, 9, 10, 18, 19, 20, 21],
                [1, 2, 3, 11, 12, 20, 21],
                [1, 2, 3, 9, 10, 18, 19],
                [1, 2, 9, 10, 11, 18, 27],
                [9, 18, 27, 19, 20, 28, 29],
                [1, 2, 9, 10, 11, 20, 29],
                [9, 18, 27, 16, 17, 25, 26],
            ],
            [  # Groen
                [9, 18, 19, 20, 21, 12, 3],
                [9, 18, 1, 2, 3, 12, 21],
                [1, 2, 11, 20, 29, 28, 27],
                [1, 2, 9, 18, 27, 28, 29],
            ],
            [  # Roze
                [1, 2, 9, 10, 11, 19, 28],
                [1, 9, 10, 18, 19, 11, 12],
                [1, 9, 10, 18, 19, 7, 8],
                [9, 17, 18, 19, 26, 27, 28],
            ],
            [  # Zwart
                [9, 18, 27, 36, 17, 26, 35],
            ],
            [  # Blauw
                [1, 2, 9, 10, 11, 18, 19],
                [1, 2, 9, 10, 11, 19, 20],
                [1, 9, 10, 8, 19, 11, 20],
                [1, 9, 10, 18, 19, 8, 17],
            ],
            [  # Licht-Groen
                [1, 9, 10, 17, 18, 19, 20],
                [1, 2, 3, 10, 11, 19, 20],
                [9, 18, 27, 7, 8, 16, 17],
                [9, 18, 27, 10, 11, 19, 20],
            ],
        ]

    def past(self, stuk: int, stand: int, vanaf: int) -> bool:
        """Check of a given piece in a given orientation fits starting at cell 'vanaf'."""
        if self.vakje[vanaf] != -1:
            return False

        for offset in self.viertal[stuk][stand]:
            idx = vanaf + offset
            if self.vakje[idx] != -1:
                return False
        return True

    def plaats(self, stuk: int, stand: int, vanaf: int) -> None:
        """Place a piece on the board (mutates state)."""
        self.vakje[vanaf] = stuk
        for offset in self.viertal[stuk][stand]:
            self.vakje[vanaf + offset] = stuk
        self.vrij[stuk] = False

    def neem_weg(self, stuk: int, stand: int, vanaf: int) -> None:
        """Remove a piece from the board (undo place)."""
        self.vakje[vanaf] = -1
        for offset in self.viertal[stuk][stand]:
            self.vakje[vanaf + offset] = -1
        self.vrij[stuk] = True

    def _volgend_vrij_vakje(self, start: int) -> int:
        """Find next empty cell index starting from 'start'."""
        vv = start
        while self.vakje[vv] != -1:
            vv += 1
        return vv

    def oplossingen(self) -> Iterator[Solution]:
        """
        Generate solutions using backtracking.
        Yields copies of the board when a full solution is found.
        """
        yield from self._probeer_zet(0)

    def _probeer_zet(self, vanaf: int) -> Iterator[Solution]:
        for stuk in range(8):
            if self.vrij[stuk]:
                for stand in range(self.standen[stuk]):
                    if self.past(stuk, stand, vanaf):
                        self.plaats(stuk, stand, vanaf)

                        vv = self._volgend_vrij_vakje(vanaf)
                        if vv != 81:
                            yield from self._probeer_zet(vv)
                        else:
                            # Found a complete filling
                            self.opl += 1
                            yield Solution(board=self.vakje.copy())

                        self.neem_weg(stuk, stand, vanaf)

    @staticmethod
    def format_board(board: Sequence[int]) -> str:
        """
        Pretty-print the 8x8 playable area.
        Uses 1..8 labels for the pieces, similar to your original output.
        """
        naam = ["1", "2", "3", "4", "5", "6", "7", "8"]
        lines: List[str] = []
        for r in range(8):
            rij = ""
            for k in range(8):
                rij += naam[board[r * 9 + k]]
            lines.append(rij)
        return "\n".join(lines)


def main() -> None:
    solver = BlokjespuzzelSolver()

    # Voor master-sample is het vaak beter om niet alle oplossingen te printen (kan veel output zijn).
    # Hier printen we wel elke oplossing; pas aan als je liever alleen telt.
    for i, sol in enumerate(solver.oplossingen(), start=1):
        print(BlokjespuzzelSolver.format_board(sol.board))
        print(f"\nOplossing nummer: {i}\n")


if __name__ == "__main__":
    main()