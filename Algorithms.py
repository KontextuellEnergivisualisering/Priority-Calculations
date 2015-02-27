# Calculates the minimum power in the combined list with old data ('points') and new data ('lastHourData')
def min(points, lastHourData):
    min = -1
    # Check if points are from database
    if not isinstance(points[0][1], int):
        # If points come from database, loop through every point until a point with 'min'
        # is found, this points value will be the current minimum to compare to
        for a in points:
            if a[1].find("min") != -1:
                min = a[0]

    if min == -1:
        min = lastHourData[0][2]

    change = 0

    for n in lastHourData:
        if n[2] < min:
            min = n[2]
            change = 1

    if change == 1:
        return [min, "min", 3, int(time.time())]
    else:
        return []

# Calculates the minimum power in the combined list with old data ('points') and new data ('lastHourData')
def max(points, lastHourData):
    max = -1
    # Check if points are from database
    if not isinstance(points[0][1], int):
        # If points come from database, loop through every point until a point with 'max'
        # is found, this points value will be the current maximum to compare to
        for a in points:
            if a[1].find("max") != -1:
                max = a[0]

    if max == -1:
        max = lastHourData[0][2]

    change = 0
    for n in points:
        if n[2] > max:
            max = n[2]
            change = 1

    if change == 1:
        return [max, "max", 3, int(time.time())]
    else:
        return []
