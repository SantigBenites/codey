
def maxProfit(prices):

    profit = 0
    current_buy =  prices[0]


    for idx in range(1,len(prices)):

        if prices[idx-1] < prices[idx]:
            profit = profit + prices[idx] - current_buy
        current_buy = prices[idx]


    return profit

prices = [7,6,4,3,1]

print(maxProfit((prices)))