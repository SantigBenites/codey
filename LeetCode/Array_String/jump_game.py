
def canJump(nums):

    gas = 0

    for x in nums:

        if gas < 0:
            return False
        elif x > gas:
            gas = x
        gas -= 1

    return True
        


nums = [3,2,1,0,4]
print(canJump(nums))