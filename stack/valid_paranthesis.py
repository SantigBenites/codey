

def isValid(s: str) -> bool:

    pairs = {')':'(', '}':'{', ']':'['}

    stack = []
    for x in s:
        if x in ['(', '{', '[']:
            stack.append(x)
        if x in [')', '}', ']']:
            if len(stack) == 0:
                return False
            char = stack.pop()
            if pairs[x] != char:
                return False

    if len(stack) == 0:
        return True
    else:
        return False

s1 = "[]"
s2 = "([{}])"
s3 = "[(])"

print(isValid(s1))
print(isValid(s2))
print(isValid(s3))