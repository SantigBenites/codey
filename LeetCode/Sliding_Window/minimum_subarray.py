


def minSubArrayLen(target, nums):

    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(len(nums)):

        current_sum += nums[right]
        while current_sum >= target:
            min_len = min(min_len, right - left +1)
            current_sum -= nums[left]
            left +=1

    return min_len



target = 7
nums = [2,3,1,2,4,3]

print(minSubArrayLen(target,nums))