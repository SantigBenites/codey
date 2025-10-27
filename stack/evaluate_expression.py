from typing import List
from collections import defaultdict


def evalRPN(tokens: List[str]) -> int:

    while tokens:

        current_stack = []
        char = tokens.pop(0)
        if char.isnumeric():

            current_stack.append(int(char))
            
        else:
            
            if char == "+":
                base += second_value
            elif char == "-":
                base -= second_value
            elif char == "*":
                base *= second_value
            elif char == "/":
                base = int(second_value / base)
            else:
                return

input = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
print(evalRPN(input))