from astroquery.gaia import Gaia 

def query(ra: float, dec: float, radius: float):
    """
    The following code communicate directly with the GAIA API in order to retrieve the desired information when given an specific area in the sky. 

    Args: 
    ra (float): Right ascension, defines the horizontal position of a star in the sky
    dec (float): Declination, latitud of the star
    radius (float): Defines the perimter of the zone thats going to be explored

    Returns: 
    DataFrame: Information of all the stars in the defined zone
"""
    query = f"""SELECT source_id, ra, dec, phot_g_mean_mag,phot_bp_mean_mag, phot_rp_mean_mag, parallax, pmra, pmdec 
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(
       POINT('ICRS', {ra}, {dec}),
        CIRCLE('ICRS', {ra}, {dec}, {radius})
    ) = 1"""
    job = Gaia.launch_job(query)
    results = job.get_results()
    results = results.to_pandas()

    return results
