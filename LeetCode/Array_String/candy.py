
def candy(ratings):

    candy_arr = [1] * len(ratings)
    
    print("Forwards")

    for x in range(1,len(ratings)) :
        if ratings[x] > ratings[x-1]:
            candy_arr[x] = candy_arr[x-1] + 1
        print(candy_arr)

    print("Backwards")

    for x in range(len(ratings)-2,-1,-1) :
        if ratings[x] > ratings[x+1]:
            candy_arr[x] = max(candy_arr[x], candy_arr[x+1] + 1)
        print(candy_arr)

    return sum(candy_arr)



ratings = [1,0,2]
# [2,1,2]
print(candy(ratings))
