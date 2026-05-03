



def lengthOfLongestSubstring(s):

    if len(s) == 0:
        return 0
    if len(s) == 1:
        return 1

    left = 0
    max_size = 0
    for right in range(len(s)+1):
        x = s[left:right]
        print(f"{s} : {x[:]} {right}:{left}")
        if len(set(x)) == len(x):
            max_size = max(len(x),max_size)
        elif len(x) > len(set(x)):
            left +=1

    return max_size


s = "au"
print(lengthOfLongestSubstring(s))