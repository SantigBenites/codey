def rotate(nums, k):
    k = k % len(nums)
    if k != 0:
        nums[k:], nums[:k] = nums[:-k], nums[-k:] 


nums = [-1,-100,3,99]
k = 2


rotate(nums,k)
print(nums)
