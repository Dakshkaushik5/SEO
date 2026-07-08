import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def run_seo_clustering():
    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv('data/gsc_data.csv')
    
    # Clean queries
    df['query'] = df['query'].str.strip().str.lower()
    queries = df['query'].tolist()

    # 2. Vectorize Queries (Semantic Embedding)
    print("Converting text queries to semantic vectors (Embeddings)...")
    # This downloads a lightweight sentence transformer from HuggingFace
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(queries)

    # 3. Cluster with K-Means
    # We will look for 4 distinct topical groups (e.g., Python Basics, ML, Pandas, Web Dev)
    print("Clustering keywords...")
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(embeddings)

    # 4. View and Save Results
    print("\n--- Clustering Results ---")
    for cluster in range(num_clusters):
        print(f"\nGroup {cluster}:")
        keywords_in_cluster = df[df['cluster_id'] == cluster]['query'].tolist()
        print(", ".join(keywords_in_cluster))

    # Save to a new file
    df.to_csv('data/clustered_seo_data.csv', index=False)
    print("\nResults saved to data/clustered_seo_data.csv")

if __name__ == "__main__":
    run_seo_clustering()