import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =============================================================================
# 1. LOAD DATA
# =============================================================================
# Adjust filename if necessary for your local environment
filename = 'tiki_cleaned_final.xlsx - Sheet1.csv'

try:
    df = pd.read_excel('tiki_cleaned_final.xlsx')
    print("--- Data Loaded Successfully ---")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    exit()

# Handle missing text
if 'clean_text' in df.columns:
    df['clean_text'] = df['clean_text'].astype(str).fillna('')

# Set plot style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# =============================================================================
# 2. RULE-BASED EMOTIONAL ANALYSIS (Pandas Only)
# =============================================================================
print("\n--- Starting Dictionary-Based Emotional Analysis ---")

# Define Vietnamese Sentiment Dictionary (Tu dien cam xuc)
# Since we cannot use external ML libs, we define keywords manually.
positive_keywords = [
    'tốt', 'hay', 'tuyệt', 'đẹp', 'hài lòng', 'thích', 'nhanh', 'ok', 'ổn',
    'xuất sắc', 'chất lượng', 'xịn', 'rẻ', 'kỹ', 'cẩn thận', 'tận tình', 'love'
]

negative_keywords = [
    'tệ', 'kém', 'xấu', 'chán', 'thất vọng', 'lâu', 'đắt', 'hỏng', 'rách',
    'cũ', 'bẩn', 'nhầm', 'lừa', 'không', 'đừng', 'phí'
]


def calculate_sentiment_pandas(text):
    text = text.lower()
    # Count occurrences of positive words
    pos_score = sum(text.count(word) for word in positive_keywords)
    # Count occurrences of negative words
    neg_score = sum(text.count(word) for word in negative_keywords)

    # Determine label
    if pos_score > neg_score:
        return 'Positive'
    elif neg_score > pos_score:
        return 'Negative'
    else:
        return 'Neutral'


# Apply the function using Pandas
df['emotion_label'] = df['clean_text'].apply(calculate_sentiment_pandas)

print("Emotion classification completed.")
print(df['emotion_label'].value_counts())

# =============================================================================
# 3. VISUALIZATION
# =============================================================================

# --- Chart 1: Emotion Distribution (Phân bố cảm xúc) ---
plt.figure(figsize=(8, 6))
sns.countplot(x='emotion_label', data=df, palette='coolwarm',
              order=['Negative', 'Neutral', 'Positive'])
plt.title('Distribution of Emotions (Dictionary-Based)', fontsize=15)
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.show()

# --- Chart 2: Emotion vs Rating (Quan hệ Cảm xúc - Điểm đánh giá) ---
if 'rating' in df.columns:
    plt.figure(figsize=(10, 6))

    # Boxplot shows the range of ratings for each emotion
    sns.boxplot(x='emotion_label', y='rating', data=df, palette='Set2',
                order=['Negative', 'Neutral', 'Positive'])

    plt.title('Relationship between Emotion and Rating', fontsize=15)
    plt.xlabel('Emotion')
    plt.ylabel('Rating (Stars)')
    plt.show()

# =============================================================================
# 4. SAVE RESULTS
# =============================================================================
# Save result to check accuracy
df.to_csv('tiki_emotion_pandas_only.csv', index=False, encoding='utf-8-sig')
print("\nAnalysis saved to 'tiki_emotion_pandas_only.csv'")