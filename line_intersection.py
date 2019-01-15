def line_intersection(line1, line2):
    """
    Calculate intersection point of two lines on Cartesian plane.
    :param line1: A tuple of two lists of x and y coordinates.
    :param line2: A tuple of two lists of x and y coordinates.
    :return: A tuple; x and y coordinates of the intersection point.
    """
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('Lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y