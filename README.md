# gaiatools

`gaiatools` is a Python library that simplifies access to the ESA Gaia DR3 stellar catalog by building on top of `astroquery`. It allows users to retrieve stars from any region of the sky, filter them by brightness and distance, generate interactive Hertzsprung-Russell diagrams and 3D sky maps, detect stellar clusters using HDBSCAN, and cross-match with the NASA Exoplanet Archive to identify stars with confirmed exoplanets.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ETurriza/gaiatools/blob/main/tutorial.ipynb)

## Installation

```bash
pip install gaiatools
```

## Usage

### Query a region of the sky

```python
from gaiatools import StarCatalog

catalog = StarCatalog.from_region(ra=56.75, dec=24.12, radius=2.0, limit=2000)
print(catalog)
```

### Filter stars

```python
# By brightness
bright = catalog.filter_by_band("phot_g_mean_mag", max_mag=18)

# By distance
nearby = catalog.filter_by_distance(min_parallax=2)
```

### Hertzsprung-Russell Diagram

```python
catalog.plot_hr()
```

### 3D Sky Map

```python
catalog.plot_sky()
```

### Stellar Cluster Detection

```python
clusters = catalog.hdbscan()
catalog.plot_clusters(clusters)
```

### Cross-match with NASA Exoplanet Archive

```python
from gaiatools.exoplanets import get_exoplanets, crossmatch

exoplanets = get_exoplanets()
matches = crossmatch(catalog.data, exoplanets)
```

### Visualize a Planetary System

```python
from gaiatools.exoplanets import plot_system

plot_system("55 Cnc", exoplanets)
```

## Requirements

- Python >= 3.10
- pandas
- numpy
- plotly
- astroquery
- scikit-learn >= 1.3
- astropy
- requests

## License

MIT
