import pandas as pd
import numpy as np
import re
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ---------------------------------------------------------
# 1. LOAD THE DATA (Output from your previous code)
# ---------------------------------------------------------
df = pd.read_csv('amazon_cleaned.csv')
print(f"Loaded data. Shape: {df.shape}")

# ---------------------------------------------------------
# 2. CLEANING NUMERICAL COLUMNS (That were skipped previously)
# ---------------------------------------------------------

# A. Discount Percentage: Remove '%' and convert to float
if 'discount_percentage' in df.columns:
    df['discount_percentage'] = (
        df['discount_percentage']
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
    )
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

# B. Rating Count: Remove ',' and convert to int
# Example: "24,269" -> 24269
if 'rating_count' in df.columns:
    df['rating_count'] = (
        df['rating_count']
        .astype(str)
        .str.replace(',', '', regex=False)
    )
    # Fill missing values with 0 before converting
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)

# C. Rating: Fix the specific data error where value is "|"
# This matches non-numeric characters and turns them into NaN
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)

print("Additional numerical columns cleaned.")

# ---------------------------------------------------------
# 3. CATEGORY SPLITTING
# ---------------------------------------------------------
# The 'category' column looks like: "Computers|Accessories|Cables"
# We split this into separate columns for better analysis.
if 'category' in df.columns:
    # Split by pipe '|'
    cat_split = df['category'].str.split('|', expand=True)

    # Take the first 3 levels (adjust if you need more)
    if cat_split.shape[1] > 0: df['main_category'] = cat_split[0]
    if cat_split.shape[1] > 1: df['sub_category_1'] = cat_split[1]
    if cat_split.shape[1] > 2: df['sub_category_2'] = cat_split[2]

    print("Categories split successfully.")

# ---------------------------------------------------------
# 4. TEXT PRE-PROCESSING (NLP)
# ---------------------------------------------------------
# Prepares 'review_content' and 'review_title' for AI/Sentiment Analysis

# Download necessary NLTK data (run once)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True) # CHANGED: Download wordnet for lemmatization
nltk.download('omw-1.4', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() # CHANGED: Initialize Lemmatizer

def clean_text(text):
    if not isinstance(text, str):
        return ""

    # 1. Remove Emojis
    text = emoji.replace_emoji(text, replace='')

    # 2. Lowercase
    text = text.lower()

    # 3. Remove HTML tags (<br>, etc.)
    text = re.sub(r'<.*?>', '', text)

    # 4. Remove special characters (punctuation, numbers)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 5. Tokenization, Stopword Removal & Lemmatization
    words = text.split()

    # CHANGED: Use lemmatize() instead of stem().
    # This keeps "cable" as "cable" and "cables" as "cable", rather than "cabl".
    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    return " ".join(cleaned_words)

# Apply to text columns
text_cols = ['review_content', 'review_title', 'about_product']

print("Starting NLP processing (this may take a moment)...")
for col in text_cols:
    if col in df.columns:
        # Create new columns prefixed with 'clean_'
        df[f'clean_{col}'] = df[col].apply(clean_text)

# ---------------------------------------------------------
# 5. SAVE FINAL RESULT
# ---------------------------------------------------------
output_file = 'amazon_final_processed.csv'
output_file_json = 'amazon_final_processed.json'
df.to_csv(output_file, index=False)
df.to_json(output_file_json, orient='records')

print(f"Done! Final processed file saved to: {output_file}")
print(f"Final Columns: {df.columns.tolist()}")