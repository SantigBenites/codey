import math
def evalRPN(tokens):

    stack = []

    for val in tokens:

        if val in ["+","-","*","/"]:
            val1 = int(stack.pop())
            val2 = int(stack.pop())
            if val == "+":
                stack.append(val1 + val2)
            if val == "-":
                stack.append(val1 - val2)
            if val == "*":
                stack.append(val1 * val2)
            if val == "/":
                stack.append(int(float(val2) / val1))
        else:
            stack.append(val)
        
        print(stack)

    return str(stack[0])

tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
print(evalRPN(tokens))