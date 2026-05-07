


def summaryRanges(nums):

    if nums == []:
        return nums
    if len(nums) == 1:
        return [str(nums[0])]

    ranges = []
    current_start = nums[0]
    current_end = nums[0]
    for idx in range(1,len(nums)):

        if nums[idx-1] + 1 == nums[idx]:
            current_end = nums[idx]
        else:
            string = str(current_start) + "->" + str(current_end) if current_start != current_end else str(current_end)
            ranges.append(string)
            current_start = nums[idx]
            current_end = nums[idx]


    string = str(current_start) + "->" + str(current_end) if current_start != current_end else str(current_end)
    if string not in ranges:
        ranges.append(string)
    return ranges



nums = []
print(summaryRanges(nums))