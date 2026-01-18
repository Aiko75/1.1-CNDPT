import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# =============================================================================
# 1. LOAD DATA (FIXED)
# =============================================================================
# The error happened because the file is actually a CSV in this environment.
filename = 'tiki_cleaned_final.xlsx - Sheet1.csv'

try:
    df = pd.read_excel('tiki_cleaned_final.xlsx')
    print("--- Data Loaded Successfully ---")
    print(f"Total Rows: {len(df)}")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found. Please check the directory.")
    # Stop execution if file is missing
    exit()

# Handle missing values in text columns
if 'clean_text' in df.columns:
    df['clean_text'] = df['clean_text'].astype(str).fillna('')

# Set global plot style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n--- 2. Starting EDA ---")

# A. Univariate Analysis: Rating Distribution
if 'rating' in df.columns:
    plt.figure()
    sns.countplot(x='rating', data=df, palette='viridis')
    plt.title('Distribution of Ratings')
    plt.show()

# B. Univariate Analysis: Word Count
df['word_count'] = df['clean_text'].apply(lambda x: len(x.split()))
plt.figure()
sns.histplot(df['word_count'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Review Length (Word Count)')
plt.show()

# C. Bivariate Analysis: Rating vs Word Count
if 'rating' in df.columns:
    plt.figure()
    sns.boxplot(x='rating', y='word_count', data=df, palette='Set2')
    plt.title('Word Count by Rating')
    plt.show()

# D. Common Words
top_words = df['clean_text'].str.split().explode().value_counts().head(20)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_words.values, y=top_words.index, palette='magma')
plt.title('Top 20 Most Frequent Words')
plt.show()

# =============================================================================
# 3. DATA MINING (TF-IDF & K-MEANS)
# =============================================================================
print("\n--- 3. Starting Data Mining ---")

# A. TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['clean_text'])
print(f"TF-IDF Matrix Shape: {X.shape}")

# B. K-Means Clustering
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X)
df['cluster'] = kmeans.labels_

# Show top terms per cluster
print("Top terms per cluster:")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
for i in range(k):
    print(f"Cluster {i}: ", end='')
    for ind in order_centroids[i, :10]:
        print(f'{terms[ind]} ', end='')
    print()

# =============================================================================
# 4. EMOTIONAL ANALYSIS (SENTIMENT)
# =============================================================================
print("\n--- 4. Starting Emotional Analysis ---")

analyzer = SentimentIntensityAnalyzer()

# A. Calculate Score
df["sentiment_score"] = df["clean_text"].apply(
    lambda x: analyzer.polarity_scores(x)["compound"]
)

# B. Classify Emotion
def classify_emotion(score):
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

df['emotion_label'] = df['sentiment_score'].apply(classify_emotion)

# C. Visualization: Emotion Distribution
plt.figure()
sns.countplot(x='emotion_label', data=df, palette='coolwarm',
              order=['Negative', 'Neutral', 'Positive'])
plt.title('Distribution of Emotions')
plt.show()

# D. Visualization: Emotion vs Rating
if 'rating' in df.columns:
    plt.figure()
    sns.boxplot(x='emotion_label', y='rating', data=df, palette='Set2',
                order=['Negative', 'Neutral', 'Positive'])
    plt.title('Relationship between Emotion and Rating')
    plt.show()

# Save final result
output_file = 'tiki_final_analysis_complete.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nAll steps completed. Final data saved to '{output_file}'")