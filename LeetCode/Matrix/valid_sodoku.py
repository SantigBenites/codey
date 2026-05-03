


def isValidSudoku(board):

    rows = [[False] * 9 for _ in range(9)]
    cols = [[False] * 9 for _ in range(9)]
    boxes = [[False] * 9 for _ in range(9)]

    for row in range(9):
        for col in range(9):
            if board[row][col] != ".":

                num = ord(board[row][col]) - ord("1")
                boxIndex = (row // 3) * 3 + (col // 3)
                if rows[row][num] != False or cols[col][num] != False or boxes[boxIndex][num] != False:
                    return False
                rows[row][num], cols[col][num], boxes[boxIndex][num] = True, True, True



    return True


board = [["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
print(isValidSudoku(board))