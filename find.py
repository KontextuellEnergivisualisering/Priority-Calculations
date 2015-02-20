import time

def find(points, ti):
    index = binarySearch(points, ti)
    # print("index before = "+str(index))
    if index >= len(points) or points[index][0] != ti:
        index = index - 1

    # print("length = "+str(len(points)))
    # print("index after = "+str(index))
    # print("time = "+str(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(ti))))
    return index

def binarySearch(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid][0] < x: hi = mid
        else: lo = mid+1
    return lo

# Returns the average difference in SECONDS between the latest 'num' number of points
# def findSampleDiff(points, num):
#     mySum = 0
#     num = num if num < len(points) else (len(points) - 1)
#     diff = 0
#     if num > 1:
#         for i in range(num):
#             mySum = mySum + (points[i][0] - points[i + 1][0])
#
#         diff = mySum / num
#     else:
#         diff = 0
#
#     print("diff = "+str(diff))
#
#     return diff
