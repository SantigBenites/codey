



def rotate(matrix):

    row = len(matrix)
    col = len(matrix[0])
    for i in range(row):
        for j in range(i+1,col):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for k in range(row):
        matrix[k].reverse()

    print(matrix)


matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
#        [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
rotate(matrix)