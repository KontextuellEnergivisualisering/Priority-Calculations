def find(points):
    return findSampleDiff(points, 5)

# Returns the 
def findSampleDiff(points, num):
    mySum = 0
    num = num if num < len(points) else (len(points) - 1)
    diff = 0
    if num > 1:
        print(points[0][0])
        print(points[1][0])
        for i in range(num):
            mySum = mySum + (points[i][0] - points[i + 1][0])

        diff = mySum / num
    else:
        diff = 0

    return diff
