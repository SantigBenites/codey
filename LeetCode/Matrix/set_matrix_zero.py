
def setZeroes(matrix):
    row = len(matrix)
    col = len(matrix[0])

    zero_row = []
    zero_col = []

    for i in range(row):
        for j in range(col):
            if matrix[i][j] == 0:
                zero_row.append(i)
                zero_col.append(j)

    for i in range(row):
        for j in range(col):

            if i in zero_row or j in zero_col:
                matrix[i][j] = 0


matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
setZeroes(matrix)
print(matrix)