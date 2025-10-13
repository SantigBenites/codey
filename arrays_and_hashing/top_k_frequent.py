from typing import List
from collections import Counter

def topKFrequent(nums: List[int], k: int) -> List[int]:

    n = len(nums)
    mp = Counter(nums)
    freq = list(mp.items())
    freq.sort(key=lambda x: (x[1], x[0]), reverse=True)
    
    res = []
    for i in range(k):
        res.append(freq[i][0])
        
    return res


print(topKFrequent(nums = [7,7], k = 1))
