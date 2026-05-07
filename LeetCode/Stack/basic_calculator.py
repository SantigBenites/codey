


def calculate(s):


    stack = []
    s = s.replace(" ", "")
    s = s[::-1]
    for x in s:

        stack.append(x)
        if x == "(":
            result = 0
            value = ""
            
            current_number = ""
            while value != ")":
                print(f"val:{value}, res:{result} cur:{current_number}")
                    
                if value == "+" or value == "-":
                    current_number = 0 if current_number == "" else int(current_number)
                    if value == "+":
                        result += current_number + int(stack.pop())
                    if value == "-":
                        result -= current_number + int(stack.pop())
                    current_number = ""
                elif value.isdigit():
                    current_number += value
                value = stack.pop()

                print(stack)

            print(f"Added {result} to stack")
            stack.append(result)
        print(stack)

    if "+" not in s or "-" not in s:
        return stack[0]

    result = 0
    while stack != []:
        value = stack.pop()

        if value == "+" or value == "-":
            if value == "+":
                result += int(stack.pop())
            if value == "-":
                result -= int(stack.pop())
        else:
            result = int(value)


    return result



s = "312312313"
print(calculate(s))