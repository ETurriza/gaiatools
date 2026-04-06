from sklearn.cluster import HDBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from pandas import DataFrame
import plotly.graph_objects as go
import numpy as np

def plot_sky(results: DataFrame):
    results = results.copy()
    results = results.dropna(subset=["parallax"])
    results = results[results["parallax"] > 0.1]
    results["color"] = results["phot_bp_mean_mag"] - results["phot_rp_mean_mag"]
    results["distance"] = 1000 / results["parallax"]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=results["ra"],
        y=results["dec"],
        z=results["distance"],  
        mode='markers',
        marker=dict(
            size=2,
            color=results["color"],
            colorscale="RdBu_r",
            opacity=0.8
        ),
        hovertemplate="RA: %{x:.4f}<br>Dec: %{y:.4f}<br>Distancia: %{z:.1f} pc<br>Radio: %{text}"
    ))
    
    fig.update_layout(
        title="Stellar Map 3D",
        scene=dict(
            xaxis_title="Right Ascension",
            yaxis_title="Declination",
            zaxis_title="Distance (parsecs)"
        )
    )
    fig.show()

def plot_hr(results:DataFrame):
    results = _compute_absolute_magnitude(results)
    results["Color"] = results["phot_bp_mean_mag"] - results["phot_rp_mean_mag"]
    c = results["Color"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=c, 
                             y= results["M_G"], 
                             mode='markers', 
                             marker=dict(
                            color=c,
                             colorscale='RdBu_r'),
                             text=results["source_id"].astype(str) + "<br>M_G: " + results["M_G"].round(2).astype(str) + "<br>Distancia: " + results["distance"].round(1).astype(str) + " pc",
                             hovertemplate= "%{text}"
                             ))
    fig.update_layout(yaxis=dict(autorange="reversed"), title='Hertzprung-Russel Diagram', xaxis_title='BP - RP (Color Index)', yaxis_title='Absolute Magnitud (M_G)')
    fig.show()


def hdbscan(results:DataFrame, min_cluster_size=15):
    results = results.dropna(subset=["ra", "dec", "pmra", "pmdec"])
    hdb = HDBSCAN(min_cluster_size=min_cluster_size)
    features = results[["ra", "dec", "pmra", "pmdec"]]
    features_scaled = StandardScaler().fit_transform(features)
    hdb.fit(features_scaled)
    results["Cluster"] = hdb.labels_
    return results

def plot_clusters(results: DataFrame):
    noise = results[results["Cluster"] == -1]
    cluster = results[results["Cluster"] != -1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=noise["ra"], y=noise["dec"],
        mode='markers',
        marker=dict(color="gray", size=3, opacity=0.3),
        name="Noise"
    ))
    
    fig.add_trace(go.Scatter(
        x=cluster["ra"], y=cluster["dec"],
        mode='markers',
        marker=dict(color=cluster["Cluster"], colorscale="turbo", size=4),
        text="Cluster: " + cluster["Cluster"].astype(str),
        hovertemplate="%{text}<br>RA: %{x:.4f}<br>Dec: %{y:.4f}",
        name="Clusters"
    ))
    
    fig.update_layout(
        title="Stellar Clusters",
        xaxis_title="Right Ascension",
        yaxis_title="Declination"
    )
    fig.show() 

def _compute_absolute_magnitude(results:DataFrame) ->DataFrame: 
    newResults = results.dropna(subset=["parallax", "parallax_over_error", "phot_g_mean_mag"])
    newResults = newResults[(newResults["parallax"] > 0) & (newResults["parallax_over_error"] > 5)]
    newResults["distance"] = 1000/newResults["parallax"]
    newResults["M_G"] = newResults["phot_g_mean_mag"] + 5 - 5 * np.log10(newResults["distance"])
    return newResults
