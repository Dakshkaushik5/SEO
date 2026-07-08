import pandas as pd

# Mock Google Search Console data (Keywords a python learning site might rank for)
mock_data = {
    'query': [
        'how to learn python', 'python tutorials for beginners', 'best python course',
        'machine learning with python', 'how to build a random forest in python', 'scikit-learn tutorial',
        'what is pandas in python', 'how to merge dataframes in pandas', 'python data cleaning guide',
        'django web development', 'how to make a website with python', 'flask vs django tutorial'
    ],
    'clicks': [120, 95, 80, 45, 30, 25, 110, 85, 40, 60, 50, 35],
    'impressions': [2000, 1500, 1100, 900, 600, 500, 1800, 1400, 700, 1000, 950, 800]
}

df = pd.DataFrame(mock_data)
df.to_csv('data/gsc_data.csv', index=False)
print("Mock SEO data successfully created inside the data/ folder!")