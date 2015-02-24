import time

# Find the index of the point at 'ti' seconds from the current time
def find(points, ti):
    index = binarySearch(points, ti)
    # If the point were found outside of the point list, or a non exact match, the index is shifted
    # one step to the left to avoid unspecified problems with time
    if index >= len(points) or points[index][0] != ti:
        index = index - 1

    return index

# Binary search algorithm for finding the point whose time is 'x' or if 'x' can't be found, the point
# to the rigth of point closest to 'x'
def binarySearch(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be >= 0')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid][0] < x: hi = mid
        else: lo = mid+1
    return lo
