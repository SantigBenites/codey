


def productExceptSelf(nums):
    n = len(nums)
    output = [1] * n

    # Prefix pass
    print("Forwards")
    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]
        print(output)

    # Suffix pass
    print("Backwards")
    suffix = 1
    for i in range(n-1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]
        print(output)

    return output


nums = [1,2,3,4]
print(productExceptSelf(nums))