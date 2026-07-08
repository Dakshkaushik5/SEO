import pandas as pd
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_competitor():
    print("Loading your clustered data...")
    df_your_site = pd.read_csv('data/clustered_seo_data.csv')
    
    # 1. Scrape Competitor Content
    # Using a Wikipedia page as a safe example, but this could be a competitor's blog post!
    url = "https://en.wikipedia.org/wiki/Pandas_(software)"
    print(f"Scraping competitor page: {url}...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all headings (H2 and H3) as competitor topics
    competitor_headings = [h.get_text().strip() for h in soup.find_all(['h2', 'h3'])]
    # Filter out empty or short navigation text
    competitor_headings = [h for h in competitor_headings if len(h) > 5 and "Navigation" not in h]
    
    print(f"Found {len(competitor_headings)} topics on competitor site.")

    # 2. Vectorize Competitor Topics
    print("Embedding competitor topics...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    comp_embeddings = model.encode(competitor_headings)
    your_embeddings = model.encode(df_your_site['query'].tolist())

    # 3. Calculate Similarity (The Content Gap)
    print("Analyzing gaps...")
    gaps = []
    
    for i, comp_topic in enumerate(competitor_headings):
        # Calculate cosine similarity between this competitor topic and ALL of your keywords
        similarity_scores = cosine_similarity([comp_embeddings[i]], your_embeddings)[0]
        max_similarity = max(similarity_scores)
        
        # If the highest similarity to any of your keywords is low (e.g., < 0.45), it's a content gap!
        if max_similarity < 0.45:
            gaps.append({
                'Competitor Topic': comp_topic,
                'Similarity Score to Your Site': round(float(max_similarity), 2)
            })

    # 4. Display Results
    df_gaps = pd.DataFrame(gaps)
    print("\n==== CONTENT GAP DISCOVERED ====")
    print("Your competitor is talking about these topics, but your site has NO matching keywords:")
    print(df_gaps.to_string(index=False))
    
    df_gaps.to_csv('data/content_gaps.csv', index=False)
    print("\nGap analysis saved to data/content_gaps.csv")

if __name__ == "__main__":
    analyze_competitor()
    