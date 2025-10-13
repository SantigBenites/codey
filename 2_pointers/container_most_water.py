from collections import defaultdict
from typing import List


def get_area(x : int,y : int,x_height : int,y_height : int):
    height = y_height if x_height > y_height else x_height
    length = abs(x-y)
    return height * length


def maxArea(heights: List[int]) -> int:

    max = 0

    for idx,x in enumerate(heights):

        for idy,y in enumerate(heights):

            area = get_area(idx,idy,x,y)
            if area > max :
                print(f"{idx},{idy},{x},{y}")
                max = area 

    return max

height = [1,7,2,5,4,7,3,6]
print(maxArea(height))