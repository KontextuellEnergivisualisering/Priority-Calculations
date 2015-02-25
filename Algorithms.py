def min(points, lastHourData):
    min = -1
    if not isinstance(points[0][1], int):
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
        return [min, "min", 3]
    else:
        return []

def max(points, lastHourData):
    max = -1
    if not isinstance(points[0][1], int):
        for a in points:
            if a[1].find("max") != -1:
                max = a[0]

    if max == -1:
        max = lastHourData[0][2]

    change = 0
    print("max: "+str(max))
    for n in points:
        if n[2] > max:
            max = n[2]
            change = 1

    if change == 1:
        return [max, "max", 3]
    else:
        return []
