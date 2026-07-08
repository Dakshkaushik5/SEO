import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SEO Analytics Dashboard", layout="wide")

st.title("🚀 SEO Semantic Analyzer & Content Gap Tool")
st.markdown("This tool uses Natural Language Processing (`Sentence-Transformers`) to cluster search intent and discover hidden competitor gaps.")

# Sidebar Configuration
st.sidebar.header("📁 Project Data Status")

# Check if data files exist
gsc_exists = os.path.exists("data/clustered_seo_data.csv")
gap_exists = os.path.exists("data/content_gaps.csv")

if gsc_exists:
    st.sidebar.success("✅ Clustered Data Found")
else:
    st.sidebar.error("❌ Run clustering.py first")

if gap_exists:
    st.sidebar.success("✅ Content Gap Analysis Found")
else:
    st.sidebar.error("❌ Run competitor_analyzer.py first")

# Main Content Tabs
tab1, tab2 = st.tabs(["📊 Keyword Intent Clusters", "🔍 Competitor Content Gaps"])

with tab1:
    st.header("Semantic Intent Clustering")
    if gsc_exists:
        df_cluster = pd.read_csv("data/clustered_seo_data.csv")
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Keywords", len(df_cluster))
        col2.metric("Identified Clusters", df_cluster['cluster_id'].nunique())
        col3.metric("Total Clicks", int(df_cluster['clicks'].sum()))
        
        # Select Cluster to view
        cluster_choice = st.selectbox("Filter by Intent Group:", sorted(df_cluster['cluster_id'].unique()))
        
        filtered_df = df_cluster[df_cluster['cluster_id'] == cluster_choice]
        st.dataframe(filtered_df[['query', 'clicks', 'impressions']], use_container_width=True)
        
        # Simple CTR Chart
        st.subheader("Performance Metric Breakdown")
        df_cluster['CTR (%)'] = (df_cluster['clicks'] / df_cluster['impressions']) * 100
        st.bar_chart(data=df_cluster, x='query', y='CTR (%)')
    else:
        st.info("Please run your backend clustering script to see metrics here.")

with tab2:
    st.header("Competitor Gap Strategy Map")
    if gap_exists:
        df_gaps = pd.read_csv("data/content_gaps.csv")
        
        # Exclude structural words for a cleaner dashboard display
        noise_words = ['contents', 'see also', 'references', 'further reading', 'navigation']
        df_gaps_clean = df_gaps[~df_gaps['Competitor Topic'].str.lower().isin(noise_words)]
        
        st.subheader("High Priority Content Recommendations")
        st.write("These structural topics were extracted from your competitor's site but have dangerously low semantic matching parameters against your keyword list:")
        
        st.dataframe(df_gaps_clean.sort_values(by="Similarity Score to Your Site"), use_container_width=True)
        
        # Add a download button for the content marketing team
        csv = df_gaps_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Content Gap Report as CSV",
            data=csv,
            file_name="seo_content_gaps.csv",
            mime="text/csv",
        )
    else:
        st.info("Please execute your competitor evaluation script to track keyword spaces.")