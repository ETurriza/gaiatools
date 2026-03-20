from .query import query
from .plot import plot_sky, plot_hr, plot_clusters, dbscan
from .filters import filter_by_band, filter_by_distance
from pandas import DataFrame
class StarCatalog:
    def __init__ (self, data):
        self.data = data
    @classmethod
    def from_region(cls, ra:float, dec:float, radius:float, limit: int=2000):
        data = query(ra, dec, radius, limit)
        return cls(data)
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f"The catalog has {len(self)} stars"
    
    def plot_sky(self):
        plot_sky(self.data)


    def plot_hr(self):
        plot_hr(self.data)

    def plot_clusters(self, result):
        plot_clusters(result)

    def dbscan(self, eps=0.3, min_samples=15):
        return dbscan(self.data, eps=eps, min_samples=min_samples)
    
    def filter_by_band( self, band:str, min_mag=None, max_mag=None):
        return filter_by_band(band=band, results = self.data, min_mag=min_mag, max_mag= max_mag )
    
    def filter_by_distance(self, min_parallax=None, max_parallax=None):
        return filter_by_distance(results=self.data,min_parallax=min_parallax, max_parallax= max_parallax)
    
    def get_cluster(self, results:DataFrame, cluster_id:int) -> "StarCatalog":
        newCluster = results[results["Cluster"] == cluster_id]
        return StarCatalog(newCluster)
