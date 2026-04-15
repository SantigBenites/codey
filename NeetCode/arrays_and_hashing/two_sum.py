
def two_sum(numbers, target):
    map = {}

    for ix, i in enumerate(numbers):
        for ij, j in enumerate(numbers):
            if ij!=ix:
                map[i+j] = (ix,ij)

    return map[target]


print(two_sum([3,2,4], 6))
print(two_sum([2,7,11,15],9))
print(two_sum([3,3],6))