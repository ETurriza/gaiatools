from .query import query
from .plot import plot_sky, plot_hr, plot_clusters, hdbscan
from .filters import filter_by_band, filter_by_distance
from pandas import DataFrame
class StarCatalog:
    def __init__ (self, data):
        """
        Args:
        data (DataFrame): Gaia star catalog.
        """
        self.data = data
    @classmethod
    def from_region(cls, ra:float, dec:float, radius:float, limit: int=2000):
        """
    Queries the Gaia DR3 catalog for stars in a circular region of the sky.

    Args:
       ra (float): Right ascension of the center in degrees (0-360).
    dec (float): Declination of the center in degrees (-90 to 90).
    radius (float): Search radius in degrees.
    limit (int): Maximum number of stars to retrieve. Default is 2000.

    Returns:
    StarCatalog: New catalog instance with the queried stars.
    """
        data = query(ra, dec, radius, limit)
        return cls(data)
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f"The catalog has {len(self)} stars"
    
    def plot_sky(self):
        """Generates an interactive 3D sky map of the catalog stars."""
        plot_sky(self.data)


    def plot_hr(self):
        """Generates an interactive Hertzsprung-Russell diagram for the catalog stars."""
        plot_hr(self.data)

    def plot_clusters(self, result):
        """
        Plots detected stellar clusters on a 2D sky map.

        Args:
        result (DataFrame): Output from hdbscan() with a 'Cluster' column.
"""
        plot_clusters(result)

    def hdbscan(self, min_cluster_size=15):
        """
    Detects stellar clusters using HDBSCAN.

    Args:
    min_cluster_size (int): Minimum number of stars to form a cluster. Default is 15.

    Returns:
    DataFrame: Catalog with an additional 'Cluster' column.
"""
        return hdbscan(self.data, min_cluster_size=15)
    
    def filter_by_band( self, band:str, min_mag=None, max_mag=None):
        """
    Filters catalog stars by apparent magnitude in a given band.

    Args:
    band (str): Column name of the photometric band.
    min_mag (float, optional): Minimum magnitude.
    max_mag (float, optional): Maximum magnitude.

    Returns:
    DataFrame: Filtered catalog.
"""
        return filter_by_band(band=band, results = self.data, min_mag=min_mag, max_mag= max_mag )
    
    def filter_by_distance(self, min_parallax=None, max_parallax=None):
        """
    Filters catalog stars by parallax.

    Args:
    min_parallax (float, optional): Minimum parallax in mas.
    max_parallax (float, optional): Maximum parallax in mas.

    Returns:
    DataFrame: Filtered catalog.
"""
        return filter_by_distance(results=self.data,min_parallax=min_parallax, max_parallax= max_parallax)
    
    def get_cluster(self, results:DataFrame, cluster_id:int) -> "StarCatalog":
        """
    Extracts a specific cluster as a new StarCatalog instance.

    Args:
    results (DataFrame): Output from hdbscan() with a 'Cluster' column.
    cluster_id (int): ID of the cluster to extract.

    Returns:
    StarCatalog: New catalog containing only stars from the specified cluster.
"""
        newCluster = results[results["Cluster"] == cluster_id]
        return StarCatalog(newCluster)
