

def hIndex(citations):
    

    for value in range(len(citations),0,-1):
        count = 0

        for cit in citations:

            if cit >= value:
                count += 1

        if value <= count:
            return value
    return 0


citations = [0,0]
print(hIndex(citations))