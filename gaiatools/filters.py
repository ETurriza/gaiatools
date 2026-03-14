from pandas import DataFrame
def filter_by_band(band:str, results:DataFrame, min_mag=None, max_mag=None):
    if min_mag is not None and max_mag is not None:
        return results[(results[band] < max_mag) & (results[band]> min_mag)]
    elif min_mag is not None:
          return results[results[band] > min_mag]
    else:
         return results[results[band]<max_mag]
    
def filter_by_distance(results:DataFrame, min_parallax=None, max_parallax=None):
     if min_parallax is not None and max_parallax is not None:
          return results[(results["parallax"] > min_parallax) & (results["parallax"] < max_parallax)]
     elif min_parallax is not None:
          return results[results["parallax"] >min_parallax]
     else:
          return results[results["parallax"] < max_parallax]