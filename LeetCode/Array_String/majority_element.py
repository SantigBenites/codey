def majorityElement(nums):

    e = nums[0]
    c = 0

    for x in nums:

        if c == 0:
            e = x
            c = 1
        elif e == x:
            c += 1
        else:
            c -= 1
    
    return e


nums = [1,1,1,1,1,2,2]
print(majorityElement(nums))