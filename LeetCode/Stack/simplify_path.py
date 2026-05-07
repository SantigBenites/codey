


def simplifyPath(path):

    stack = []
    print(path.split("/"))

    for word in path.split("/"):
        print(word)
        if word == "":
            continue
        elif word == ".." and len(stack) >= 1:
            stack.pop()
        elif word == "..":
            continue
        elif word == ".":
            continue
        else:
            stack.append(word)

        print(stack)

    return "/" + "/".join(stack)



path = "/../"
print(simplifyPath(path))
