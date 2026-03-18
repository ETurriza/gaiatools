from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from pandas import DataFrame

def plot_sky(results:DataFrame):
    fig, ax = plt.subplots()
    ax.scatter(results["ra"], results["dec"], s= 1/results["phot_g_mean_mag"])
    ax.set_xlabel("Right ascencion")
    ax.set_ylabel("Declination")
    ax.set_title("Stellar map")
    plt.show()

def plot_hr(results:DataFrame):
    results = results.copy()
    results["Color"] = results["phot_bp_mean_mag"] - results["phot_rp_mean_mag"]
    c = results["Color"]
    fig, ax = plt.subplots()
    ax.scatter(x=c, y=results["phot_g_mean_mag"], c = c, cmap='coolwarm')
    ax.invert_yaxis()
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Brightness")
    ax.set_title("Hertzsprung-Russell diagram")
    plt.show()

def dbscan(results:DataFrame, eps = 0.3, min_samples=15):
    results = results.copy()
    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(results[["ra", "dec", "pmra", "pmdec"]]) 
    results["Cluster"] = db.labels_
    return results

def plot_clusters(results:DataFrame):
    c = results["Cluster"]
    fig, ax = plt.subplots()
    ax.scatter(results["ra"], results["dec"], c=c, cmap='coolwarm')
    ax.set_xlabel("Right ascencion")
    ax.set_ylabel("Declination")
    ax.set_title("Clusters")
    plt.show()