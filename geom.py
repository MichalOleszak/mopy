import pandas as pd
import math


def get_parallelizing_rotation(near_table_path, angle_method="PLANAR"):
    """
    Compute rotation angle to be applied to each rectangle defined as a single row of near_table,
    so that the rotated polygon's longer side is parallel to the near feature line given in near_table.
    :param near_table_path: String; path to the CSV file as returned by arcpy.GenerateNearTable_analysis()
    :param angle_method: Method that was used by arcpy.GenerateNearTable_analysis() to generate near_table;
    "PLANAR" or "GEODESIC"
    :return: A list with required rotation angles.
    """
    # Read in near table data
    near_table = pd.read_csv(near_table_path, sep=";")
    # Extract & clean angles of the line connecting rectangle's centroid and nearest point on the near feature line
    angles = near_table.loc[near_table["NEAR_RANK"] == 1].NEAR_ANGLE.tolist()
    angles = [float(a) for a in [b.replace(",", ".") for b in angles]]
    # Compute required rotation angles
    if angle_method == "PLANAR":
        req_rot = [a + 360 if a < 0 else a for a in angles]
    elif angle_method == "GEODESIC":
        raise Exception("Method GEODESIC is not supported yet. Recompute near_table using PLANAR method.")
    else:
        raise Exception("Unsupported angle_method provided. Available methods are 'PLANAR' and 'GEODESIC'.")
    return req_rot


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
        raise Exception("Lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


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
    x = x - x_c
    y = y - y_c
    if units == "degrees":
        angle = math.radians(angle)
    x_r = (x * math.cos(angle)) - (y * math.sin(angle)) + x_c
    y_r = (x * math.sin(angle)) + (y * math.cos(angle)) + y_c
    return x_r, y_r
