from .query import query
class StarCatalog:
    def __init__ (self, data):
        self.data = data
    @classmethod
    def from_region(cls, ra:float, dec:float, radius:float):
        data = query(ra, dec, radius)
        return cls(data)
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f"The catalog has {len(self)} stars"