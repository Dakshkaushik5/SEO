import streamlit as st
import pandas as pd
import os
import subprocess  # Allows python to run our backend scripts if missing

st.set_page_config(page_title="AI SEO Analytics Dashboard", layout="wide")

st.title("🚀 AI-Powered SEO Semantic Analyzer & Content Gap Tool")
st.markdown("This tool uses Natural Language Processing (`Sentence-Transformers`) to cluster search intent and discover hidden competitor gaps.")

# Ensure data directory exists on the cloud server
if not os.path.exists("data"):
    os.makedirs("data")

# --- AUTO PIPELINE RUNNER ---
# If files don't exist, run the scripts automatically on deployment
if not os.path.exists("data/gsc_data.csv"):
    with st.spinner("Generating base SEO data..."):
        subprocess.run(["python", "generate_data.py"])

if not os.path.exists("data/clustered_seo_data.csv"):
    with st.spinner("Running NLP Clustering Pipeline (Downloading model, this may take a minute)..."):
        subprocess.run(["python", "src/clustering.py"])

if not os.path.exists("data/content_gaps.csv"):
    with st.spinner("Running Competitor Gap Analysis Web Scraper..."):
        subprocess.run(["python", "src/competitor_analyzer.py"])
# ----------------------------

# Sidebar Configuration
st.sidebar.header("📁 Project Data Status")
gsc_exists = os.path.exists("data/clustered_seo_data.csv")
gap_exists = os.path.exists("data/content_gaps.csv")

if gsc_exists and gap_exists:
    st.sidebar.success("✅ All Pipelines Active & Loaded")
else:
    st.sidebar.warning("⚠️ Initializing Data Pipelines...")

# Main Content Tabs
tab1, tab2 = st.tabs(["📊 Keyword Intent Clusters", "🔍 Competitor Content Gaps"])

with tab1:
    st.header("Semantic Intent Clustering")
    if os.path.exists("data/clustered_seo_data.csv"):
        df_cluster = pd.read_csv("data/clustered_seo_data.csv")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Keywords", len(df_cluster))
        col2.metric("Identified Clusters", df_cluster['cluster_id'].nunique())
        col3.metric("Total Clicks", int(df_cluster['clicks'].sum()))
        
        cluster_choice = st.selectbox("Filter by Intent Group:", sorted(df_cluster['cluster_id'].unique()))
        filtered_df = df_cluster[df_cluster['cluster_id'] == cluster_choice]
        st.dataframe(filtered_df[['query', 'clicks', 'impressions']], use_container_width=True)
        
        st.subheader("Performance Metric Breakdown")
        df_cluster['CTR (%)'] = (df_cluster['clicks'] / df_cluster['impressions']) * 100
        st.bar_chart(data=df_cluster, x='query', y='CTR (%)')

with tab2:
    st.header("Competitor Gap Strategy Map")
    if os.path.exists("data/content_gaps.csv"):
        df_gaps = pd.read_csv("data/content_gaps.csv")
        
        noise_words = ['contents', 'see also', 'references', 'further reading', 'navigation']
        df_gaps_clean = df_gaps[~df_gaps['Competitor Topic'].str.lower().isin(noise_words)]
        
        st.subheader("High Priority Content Recommendations")
        st.dataframe(df_gaps_clean.sort_values(by="Similarity Score to Your Site"), use_container_width=True)
        
        csv = df_gaps_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Content Gap Report as CSV",
            data=csv,
            file_name="seo_content_gaps.csv",
            mime="text/csv",
        )
        