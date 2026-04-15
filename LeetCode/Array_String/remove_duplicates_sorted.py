def removeDuplicates(nums):

    idx = 0

    while idx < len(nums)-2:
        
        if nums[idx] == nums[idx+1]:

            while len(nums) > idx+2 and nums[idx+1] == nums[idx+2]:
                nums.pop(idx+1)
                print(f"{idx} - {len(nums)} {nums}")
        
        idx +=1

    return len(nums)


nums = [1,2,2,2]
print(removeDuplicates(nums))
print(nums)