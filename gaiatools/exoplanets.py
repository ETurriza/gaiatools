import pandas as pd
import requests
from pandas import DataFrame
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.coordinates import match_coordinates_sky
import plotly.graph_objects as go
import numpy as np

def get_exoplanets()-> DataFrame:
    query = f"""SELECT hostname, ra, dec, pl_name, pl_orbsmax, pl_masse, pl_rade, pl_orbper
    FROM pscomppars """
    response = requests.get('https://exoplanetarchive.ipac.caltech.edu/TAP/sync', params={"query":query, "format":"json"})
    exoplanets=pd.DataFrame(response.json())
    return exoplanets

def crossmatch(gaia_df:DataFrame, exoplanet_df:DataFrame):
    gaia_df = gaia_df.copy()
    gaia_df = gaia_df.dropna(subset=["ra","dec"])
    exoplanet_df= exoplanet_df.dropna(subset=["ra", "dec"])
    exoplanet_df = exoplanet_df.groupby("hostname").first().reset_index()
    gaiaCoord = SkyCoord(ra=gaia_df["ra"].values, dec=gaia_df["dec"].values, unit="deg")
    exoplanetCoord = SkyCoord(ra=exoplanet_df["ra"].values, dec=exoplanet_df["dec"].values, unit="deg")
    estrellaCercana, angular, _ = match_coordinates_sky(gaiaCoord, exoplanetCoord)
    gaia_df.loc[angular < 5*u.arcsec, "pl_name"] = exoplanet_df.iloc[estrellaCercana[angular < 5*u.arcsec]]["pl_name"].values
    print(f"Total estrellas Gaia: {len(gaia_df)}")
    print(f"Total exoplanetas NASA: {len(exoplanet_df)}")
    print(f"Distancia mínima encontrada: {angular.min().to(u.arcsec)}")
    print(f"Matches < 1 arcsec: {(angular < 1*u.arcsec).sum()}")
    if (angular < 5*u.arcsec).sum() == 0:
        print("No se encontraron estrellas con exoplanetas en esta región.")
        return pd.DataFrame()
    return gaia_df[angular < 5*u.arcsec]

def plot_system(starName: str, exoplanet_df: DataFrame):
    planets = exoplanet_df[exoplanet_df["hostname"] == starName]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        name=starName,
        marker=dict(color="yellow", size=15)
    ))
    for _, planet in planets.iterrows():
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter(
        x=planet["pl_orbsmax"] * np.cos(theta),
        y=planet["pl_orbsmax"] * np.sin(theta),
        mode='lines',
        showlegend=False,
        line=dict(color="gray", width=1)
))
        fig.add_trace(go.Scatter(
            x=[planet["pl_orbsmax"]],
            y=[0],
            mode='markers',
            name=planet["pl_name"],
            text=f"Masa: {planet['pl_masse']} M⊕<br>Radio: {planet['pl_rade']} R⊕<br>Período: {planet['pl_orbper']} días",
            hovertemplate="%{text}"
        ))
    fig.update_layout(
        title=f"Sistema planetario: {starName}",
        xaxis_title="Distancia (UA)",
        yaxis_title=""
    )
    fig.show()