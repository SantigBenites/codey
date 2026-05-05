

def isHappy(n):


    squares = set()

    while n != 1 and n not in squares:

        squares.add(n)
    
        sum = 0
        while n != 0:
            digit = n % 10
            sum += digit * digit
            n //= 10

        n = sum

    return n == 1

n = 19
print(isHappy(n))
