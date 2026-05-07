
def findMinArrowShots(points):

    points.sort()
    merged = []
    prev = points[0]

    for idx in range(1,len(points)):

        if points[idx][0] <= prev[1]:
            prev[0] = max(prev[0], points[idx][0])
            prev[1] = min(prev[1], points[idx][1])
        else:
            merged.append(prev)
            prev = points[idx]

    merged.append(prev)
    return len(merged)




points = [[1,2],[2,3],[3,4],[4,5]]
print(findMinArrowShots(points))