# clustering_analysis.py
from androguard.core.bytecodes.apk import APK
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import pandas as pd

samples_folder = "samples"

def extract_permissions():
    apk_data = []
    for file in os.listdir(samples_folder):
        if file.endswith(".apk"):
            apk = APK(os.path.join(samples_folder, file))
            apk_data.append({
                "file": file,
                "permissions": apk.get_permissions()
            })
    return apk_data

def run_clustering(apk_data, n_clusters=3):
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform([a["permissions"] for a in apk_data])

    # Dimensionality reduction for visualization
    X_reduced = PCA(n_components=2).fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    df = pd.DataFrame({
        "File": [a["file"] for a in apk_data],
        "Cluster": labels
    })

    plt.figure(figsize=(8,6))
    plt.scatter(X_reduced[:,0], X_reduced[:,1], c=labels, cmap="viridis", s=60)
    for i, f in enumerate(df["File"]):
        plt.text(X_reduced[i,0]+0.01, X_reduced[i,1]+0.01, f[:10], fontsize=8)
    plt.title("APK Permission Pattern Clusters")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.tight_layout()
    plt.savefig("output/clusters.png")
    plt.close()
    print("✅ Clustering complete. Plot saved at output/clusters.png")

    return df, labels

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    apk_data = extract_permissions()
    df, labels = run_clustering(apk_data)
    df.to_csv("output/cluster_results.csv", index=False)
