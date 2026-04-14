from pandas import DataFrame
def filter_by_band(band:str, results:DataFrame, min_mag=None, max_mag=None):
    """
Filters stars by apparent magnitude in a given photometric band.

Args:
    band (str): Column name of the band to filter by (e.g. 'phot_g_mean_mag').
    results (DataFrame): Gaia star catalog.
    min_mag (float, optional): Minimum magnitude (exclusive).
    max_mag (float, optional): Maximum magnitude (exclusive).

Returns:
    DataFrame: Filtered catalog.
"""
    if min_mag is not None and max_mag is not None:
        return results[(results[band] < max_mag) & (results[band]> min_mag)]
    elif min_mag is not None:
          return results[results[band] > min_mag]
    else:
         return results[results[band]<max_mag]
    
def filter_by_distance(results:DataFrame, min_parallax=None, max_parallax=None):
     """
Filters stars by parallax, which is inversely proportional to distance.
A higher parallax means a closer star (distance in pc = 1000 / parallax).

Args:
    results (DataFrame): Gaia star catalog.
    min_parallax (float, optional): Minimum parallax in mas.
    max_parallax (float, optional): Maximum parallax in mas.

Returns:
    DataFrame: Filtered catalog.
"""
     if min_parallax is not None and max_parallax is not None:
          return results[(results["parallax"] > min_parallax) & (results["parallax"] < max_parallax)]
     elif min_parallax is not None:
          return results[results["parallax"] >min_parallax]
     else:
          return results[results["parallax"] < max_parallax]