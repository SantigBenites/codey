import random as random
import time

list_size = 10
original_list = []
for _ in range(list_size):
    num = random.randint(0,100) # create random num and append
    original_list.append(num)

print(f"Original list {original_list}")
original_list.append(-1)

for x in range(len(original_list)+1):
    print(f"{original_list}")
    for y in range(0, len(original_list)-x-1):
        if original_list[y] > original_list[y+1]:
            original_list[y], original_list[y + 1] = original_list[y + 1], original_list[y]

print(f"Post Sort list {original_list}")