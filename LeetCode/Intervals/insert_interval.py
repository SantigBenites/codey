

def insert(intervals, newInterval):

    result = []
    i = 0
    
    # Iterate through intervals and add non-overlapping intervals before newInterval
    while i < len(intervals) and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    
    # Add merged newInterval
    result.append(newInterval)
    
    # Add non-overlapping intervals after newInterval
    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    
    return result

# [3,8] - prev
# [12,16]
# [1,2]

intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]
newInterval = [4,8]
print(insert(intervals,newInterval))