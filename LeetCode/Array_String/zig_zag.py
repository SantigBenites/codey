def convert(s, numRows):

    if numRows == 1:
        return s

    rows = [[] for _ in range(numRows)]

    current_row = 0
    reverse = False
    for letter in s:

        if current_row == numRows-1:
            reverse = True
        if current_row == 0:
            reverse = False

        rows[current_row].append(letter)

        if reverse:
            current_row -= 1
        else:
            current_row += 1
        

    return "".join(sum(rows, []))


s = "AB" 
numRows = 1

print(convert(s,numRows))