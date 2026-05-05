


def containsNearbyDuplicate(nums, k):

    pairs = {}
    for idx,val in enumerate(nums):

        if val in pairs and abs(pairs[val] - idx) <= k:
            return True

        pairs[val] = idx

    return False



nums = [1,2,3,1]
k = 3

print(containsNearbyDuplicate(nums,k))