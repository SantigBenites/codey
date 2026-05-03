


def spiralOrder(matrix):

    res = []
    m, n = len(matrix), len(matrix[0])

    top = 0
    bottom = m-1
    left = 0
    right = n-1

    while top <= bottom and left <= right:

        for i in range(left,right+1):
            res.append(matrix[top][i])
        top +=1

        for i in range(top,bottom+1):
            res.append(matrix[i][right])
        right -=1
        
        if top <= bottom:
            for i in range(right,left-1,-1):
                res.append(matrix[bottom][i])
            bottom -=1

        if left <= right:
            for i in range(bottom,top-1,-1):
                res.append(matrix[i][left])
            left +=1

    return res



matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
print(spiralOrder(matrix))