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
    import pandas as pd
    near_table = pd.read_csv(near_table_path, sep=";")
    # Extract & clean angles of the line connecting rectangle's centroid and nearest point on the near feature line
    angles = near_table.loc[near_table['NEAR_RANK'] == 1].NEAR_ANGLE.tolist()
    angles = [float(a) for a in [b.replace(',', '.') for b in angles]]
    # Compute required rotation angles
    if angle_method == "PLANAR":
        reqrot = [-a for a in [b + 360 if b < 0 else b for b in angles]]
    elif angle_method == "GEODESIC":
        raise Exception("Method GEODESIC is not supported yet. Recompute near_table using PLANAR method.")
    else:
        raise Exception("Unsupported angle_method provided. Available methods are 'PLANAR' and 'GEODESIC'.")
    return(reqrot)


