from typing import List
from collections import defaultdict

def twoSum(self, numbers: List[int], target: int) -> List[int]:
    map = {}

    for ix, i in enumerate(numbers):
        for ij, j in enumerate(numbers):
            if ij!=ix:
                map[i+j] = [ix+1,ij+1]

    map[target].sort()
    return map[target]