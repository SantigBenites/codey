from collections import defaultdict
from typing import List




def trap(height: List[int]) -> int:

    water_level = []
    for idx,x in enumerate(height):

        prefix = max(height[idx:]) if len(height[idx:]) > 0 else 0 
        suffix = max(height[:idx]) if len(height[:idx]) > 0 else 0
        current_level = min(prefix, suffix) - x
        if current_level > 0:
            water_level.append(current_level)

    return sum(water_level)


height = [0,2,0,3,1,0,1,3,2,1]
print(trap(height))