def removeElement(nums, val):

    fend_removal = 0
    original_length = len(nums)
    idx = 0
    while idx <= len(nums)-1 - fend_removal:

        if nums[idx] == val:

            nums.append(nums.pop(idx))
            fend_removal += 1
        else:
            idx +=1

    nums = nums[:len(nums)-fend_removal]
    return original_length-fend_removal

nums = [0,1,2,2,3,0,4,2]
val = 2
print(removeElement(nums,val))
print(nums)