import copy


class LifeGame:
    """Conway's Life Game"""

    # In the game board we record colors of cells as intgers(0xRRGGBB), 0 means dead.
    def __init__(self, board):
        # board for current state, nextBoard for use when ticking
        # They got switched in every tick
        self.board = board
        self.nextBoard = copy.deepcopy(board)
        self.rowCount = len(board)
        self.columnCount = len(board[0])
        # increased after every tick
        self.generation = 0

    def print(self):
        for row in self.board:
            for cell in row:
                print(f"{cell:6x}", end=' ')
            print()
        print(f"--------------------^{self.generation}^----------------------")

    def updateBoard(self, r, c, color):
        if 0 <= r < self.rowCount and \
           0 <= c < self.columnCount and \
           0 < color < 0xffffff:
            self.board[r][c] = color

    def tick(self):
        for r in range(0, self.rowCount):
            for c in range(0, self.columnCount):
                liveNeighbors = self.countAliveNeighbors(r, c)

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
                        nextStatus = self.getAverageNeighborColor(r, c)
                
                self.nextBoard[r][c] = nextStatus
        
        self.board, self.nextBoard = self.nextBoard, self.board
        self.generation += 1

    def countAliveNeighbors(self, r, c):
        neighbors = self.getNeighbors(r, c)

        count = 0

        for neighbor in neighbors:
            row, col = neighbor
            count += 1 if self.board[row][col] != 0 else 0

        return count

    def getAverageNeighborColor(self, r, c):
        neighbors = self.getNeighbors(r, c)

        red = 0
        green = 0
        blue = 0
        count = 0
        
        for neighbor in neighbors:
            row, col = neighbor
            state = self.board[row][col]
            red += (state & 0xff0000) >> 16
            green += (state & 0xff00) >> 8
            blue += state & 0xff
            count += 1 if state != 0 else 0

        if count == 0:
            return 0
        
        red /= count
        green /= count
        blue /= count

        average = (int(red) << 16) + (int(green) << 8) + int(blue)
        return average
      
    def getNeighbors(self, r, c):
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

