



def maxArea(height):


    idx = 0
    idy = len(height)-1
    max_water = 0
    while idx < idy:
        volume = min(height[idy],height[idx]) * abs(idx - idy)
        max_water = max(max_water,volume)

        if height[idx] < height[idy]:
            idx +=1
        else:
            idy -=1

    return max_water


n = [1,8,6,2,5,4,8,3,7]
print(maxArea(n))