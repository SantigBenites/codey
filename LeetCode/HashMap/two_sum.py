


def twoSum(nums, target):

    ret = {}
    for idx,x in enumerate(nums):
        
        if target-x in ret:
            return idx, ret[target-x]
        else:
            ret[x] = idx

    return -1




nums = [3,3]
target = 6
print(twoSum(nums,target))