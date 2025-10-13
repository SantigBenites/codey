from typing import List
from collections import defaultdict


def longestConsecutive(nums: List[int]) -> int:
    chains_map = defaultdict()
    nums.sort()
    max = 0

    for n in nums:
    
        if n in chains_map.keys():
            continue
        if n-1 in chains_map.keys():
            new_list = chains_map[n-1]
            new_list.append(n)
            chains_map[n] = new_list 
            del chains_map[n-1]
            
            if len(new_list) > max:
                max = len(new_list)
        else:
            chains_map[n] = [n]
            if 1 > max:
                max = 1

    return max





nums = [2,20,4,10,3,4,5]
print(longestConsecutive(nums))
nums2 = [0,3,2,5,4,6,1,1]
print(longestConsecutive(nums2))
nums2 = [0,3,2,5,4,6,1,1]
print(longestConsecutive(nums2))