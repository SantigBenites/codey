


def merge(intervals):

    intervals.sort()
    merged = []
    prev = intervals[0]

    for idx in range(1,len(intervals)):

        if intervals[idx][0] <= prev[1]:
            prev[1] = max(prev[1], intervals[idx][1])
        else:
            merged.append(prev)
            prev = intervals[idx]

    merged.append(prev)
    return merged

intervals = [[1,3],[2,6],[8,10],[15,18]]
print(merge(intervals))