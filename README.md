# 🚀 SEO Semantic Analyzer & Content Gap Tool

An advanced NLP data science project that automates search intent mapping and competitor content gap analysis using semantic embeddings.

## 📈 Business Problem
Traditional SEO keyword research relies on exact text matching, grouping words like "python tutorial" and "python course" manually. This process doesn't scale and misses the deeper human *intent* behind search queries. Furthermore, identifying content gaps against competitors requires hours of manual page-by-page auditing.

This tool solves these issues by:
1. Transforming raw search queries into semantic vector spaces to cluster keywords by intent automatically.
2. Scraping competitor landing pages and using Cosine Similarity to surface critical topical gaps.

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.x
* **NLP & Modeling:** `Sentence-Transformers` (`all-MiniLM-L6-v2`), `scikit-learn` (K-Means Clustering)
* **Web Scraping:** `BeautifulSoup4`, `requests`
* **Data Manipulation:** `pandas`, `NumPy`
* **UI/Dashboard:** `Streamlit`

## ⚙️ How It Works

1. **Semantic Vector Embeddings:** Text queries are converted into 384-dimensional dense vectors using a pre-trained Transformer model. This ensures terms like "how to learn python" and "python guide for beginners" map together based on meaning rather than string matching.
2. **Unsupervised Clustering:** A K-Means algorithm groups queries into distinct tactical clusters representing specific search silos.
3. **Causal Gap Detection:** Competitor HTML headers are scraped, vectorized, and mathematically compared against internal topics via Cosine Similarity matrix calculations. Low-scoring overlaps flag direct structural content gaps.

## 🚀 Local Deployment

To run this project locally, clone the repository and follow these steps:

1. **Set up a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: .\env\Scripts\Activate.ps1