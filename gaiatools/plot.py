from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
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
    results = results.dropna(subset=["ra", "dec", "pmra", "pmdec"])
    db = DBSCAN(eps=eps, min_samples=min_samples)
    features = results[["ra", "dec", "pmra", "pmdec"]]
    features_scaled = StandardScaler().fit_transform(features)
    db.fit(features_scaled)
    results["Cluster"] = db.labels_
    return results

def plot_clusters(results:DataFrame):
    c = results["Cluster"]
    noise = results[results["Cluster"] == -1]
    cluster = results[results["Cluster"] != -1]
    fig, ax = plt.subplots()
    ax.scatter(noise["ra"], noise["dec"], c="gray", s=5, alpha=0.3)
    ax.scatter(cluster["ra"], cluster["dec"], c=cluster["Cluster"], cmap="tab10")
    ax.set_xlabel("Right ascencion")
    ax.set_ylabel("Declination")
    ax.set_title("Clusters")
    plt.show()  