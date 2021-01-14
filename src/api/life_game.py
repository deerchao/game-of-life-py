import copy
import rgb_color
from py_linq import Enumerable


class LifeGame:
    """Conway's Life Game"""

    # In the game board we record colors of cells as intgers(0xRRGGBB), 0 means dead.
    def __init__(self, board):
        # initialState and mutations define all the states through history
        self.initialState = board
        # [(generation, row, column, color),...]
        self.mutations = []

        # board for current state, nextBoard for use when ticking
        # They got switched in every tick
        self.board = copy.deepcopy(board)
        self.nextBoard = copy.deepcopy(board)
        self.rowCount = len(board)
        self.columnCount = len(board[0])

        # increased after every tick
        self.generation = 0
        # increased after every input
        self.version = 0

    def print(self):
        for row in self.board:
            for cell in row:
                print(f"{cell:6x}", end=' ')
            print()
        print(f"--------------------^{self.generation}^----------------------")

    def update_cell(self, r, c, color):
        if 0 <= r < self.rowCount and \
           0 <= c < self.columnCount and \
           0 < color < 0xffffff:
            self.board[r][c] = color
            self.mutations.append((self.generation, r, c, color))
            self.version += 1

    # todo make this 1000+ times faster
    def tick(self):
        for r in range(0, self.rowCount):
            for c in range(0, self.columnCount):
                liveNeighbors = self.count_alive_neighbors(r, c)

                nextStatus = self.board[r][c]

                if self.board[r][c]:
                    if liveNeighbors < 2:
                        # rule 1: Any live cell with fewer than two live neighbors dies
                        nextStatus = 0
                    elif liveNeighbors > 3:
                        # rule 3: Any live cell with more than three live neighbors dies
                        nextStatus = 0
                    else:
                        # rule 2: Any live cell with two or three live neighbors lives on to the next generation
                        pass
                else:
                    if liveNeighbors == 3:
                        # rule 4: Any dead cell with exactly three live neighbors becomes a live cell
                        # When a dead cell revives by rule #4 it will be given a color that is the average of its neighbors (that revive it)
                        nextStatus = self.get_average_neighbor_color(r, c)

                self.nextBoard[r][c] = nextStatus

        self.board, self.nextBoard = self.nextBoard, self.board
        self.generation += 1

    def count_alive_neighbors(self, r, c):
        neighbors = self.get_neighbors(r, c)

        return Enumerable(neighbors).count(lambda x: self.board[x[0]][x[1]] != 0)

    def get_average_neighbor_color(self, r, c):
        neighbors = Enumerable(self.get_neighbors(r, c))

        colors = neighbors.select(lambda x: self.board[x[0]][x[1]]).where(lambda x: x != 0).to_list()
        return rgb_color.average(colors)

    def get_neighbors(self, r, c):
        # p for previous
        pr = r-1 if r > 0 else self.rowCount-1
        pc = c-1 if c > 0 else self.columnCount-1

        # n for next
        nr = (r+1) % self.rowCount
        nc = (c+1) % self.columnCount

        return [
            (pr, pc), (pr, c), (pr, nc),
            (r, pc), (r, nc),
            (nr, pc), (nr, c), (nr, nc)
        ]


if __name__ == '__main__':
    board = [
        [0xff0000, 0xff00, 0xff, 0, 0, 0, 0, 0, 0, 0],
        [0xff00, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff00ff, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff0000, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff00ff, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff00, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0xff, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    game = LifeGame(board)

    for t in range(10):
        game.print()
        print()
        game.tick()
