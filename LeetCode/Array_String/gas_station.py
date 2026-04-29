

def canCompleteCircuit(gas, cost):
    total = 0
    tank = 0
    start = 0

    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff

        if tank < 0:
            start = i + 1
            tank = 0

    return start if total >= 0 else -1

gas = [2,3,4]
cost = [3,4,3]
print(canCompleteCircuit(gas,cost))