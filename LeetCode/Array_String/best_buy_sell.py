def maxProfit(prices):


    profit = 0
    min_buy = prices[0]

    for idx in range(0,len(prices)):

        if prices[idx] < min_buy:
            min_buy = prices[idx]

        if prices[idx] - min_buy > profit:
            profit =  prices[idx] - min_buy

    return profit

prices = [7,1,5,3,6,4]

print(maxProfit(prices))