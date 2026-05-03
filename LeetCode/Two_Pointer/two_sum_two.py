

def twoSum(numbers, target):

    idx = 0
    max_seen = None
    while idx < len(numbers)-1:

        if max_seen != None and max_seen >= numbers[idx]:
            idx +=1
            continue

        idy = len(numbers)-1
        max_loop_seen = None
        while idx < idy:

            if max_loop_seen != None and max_loop_seen <= numbers[idy]:
                idy -=1
                continue

            print(f"{numbers[idx]} + {numbers[idy]}")
            if numbers[idx] + numbers[idy] == target:
                return [idx+1,idy+1]
            max_loop_seen = numbers[idy]
            idy-=1

        max_seen = numbers[idx]
        idx +=1

    return -1

numbers = [2,7,11,15]
target = 9
print(twoSum(numbers,target))