from collections import defaultdict

def longestConsecutive(nums):

    nums.sort()
    biggest_substring = 0
    current_sequences = defaultdict(list)
    for x in nums:
        if x+1 in current_sequences:
            continue
        current_sequences[x].append(x)
        current_sequences[x+1] = current_sequences[x]
        del current_sequences[x]
        print(current_sequences)
        biggest_substring = max(biggest_substring,len(current_sequences[x+1]))
        
    return biggest_substring



nums = [1,0,1,2]
print(longestConsecutive(nums))