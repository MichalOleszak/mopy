def rotate_point(x, y, x_c=0, y_c=0, angle=0, units="degrees"):
    """
    Rotate a point on the Cartesian plane around another point
    by the chosen angle.
    :param x: x coordinate of the point to be rotated
    :param y: y coordinate of the point to be rotated
    :param x_c: x coordinate of the center of rotation
    :param y_c: y coordinate of the center of rotation
    :param angle: angle of rotation
    :param units: "degrees" or "radians"
    :return: x and y coordinates of the rotated point
    """
    import math
    x = x - x_c
    y = y - y_c
    if units == "degrees":
        angle = math.radians(angle)
    x_r = (x * math.cos(angle)) - (y * math.sin(angle)) + x_c
    y_r = (x * math.sin(angle)) + (y * math.cos(angle)) + y_c
    return x_r, y_r





