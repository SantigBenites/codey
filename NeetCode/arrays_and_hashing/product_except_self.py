from typing import List


def multiply_array(nums: List[int]) -> int:
    result = 1
    for x in nums:
        result *= x
    return result

def productExceptSelf(nums: List[int]) -> List[int]:

    output = []
    for val in  nums:
        new_array = nums[:]
        new_array.remove(val)
        output.append(multiply_array(new_array))

    return output

nums = [1,2,4,6]
nums2 =[-1,0,1,2,3]

print(productExceptSelf(nums))
print(productExceptSelf(nums2))