def jump(nums):

    n = len(nums)
    if n == 1:
        return 0

    current_jump = 0
    farthest_jump = 0
    jumps = 0

    for x in range(n - 1):

        farthest_jump = max(farthest_jump, x + nums[x])
        print(f"index : {x} furthestjump: {farthest_jump}")
        
        if x == current_jump:

            print(f"making jump")

            current_jump = farthest_jump
            jumps = jumps +1



    return jumps


nums = [4,1,0,5,0,0,0,2]
print(jump(nums))