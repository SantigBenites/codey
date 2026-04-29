from collections import Counter, defaultdict
import random

count = Counter()
for x in range(0,100):

    count[x] = random.randint(0,100)

dic = defaultdict(list)
for x in range(0,100):

    if x < 20:
        dic["sub20"].append(x)
    elif x < 50 :
        dic["sub50"].append(x)
    elif x < 70:
        dic["sub70"].append(x)
    else:
        dic["sub100"].append(x)

print(count)
print(dic)