import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_csv('amazon_cleaned.csv')

# Function to clean currency strings (removes '₹' and ',')
def clean_currency(x):
    if isinstance(x, str):
        x = x.replace('₹', '').replace(',', '').strip()
    return x

# Function to clean percentage strings (removes '%')
def clean_percent(x):
    if isinstance(x, str):
        x = x.replace('%', '').strip()
    return x

# Apply cleaning to Price columns
df['discounted_price'] = df['discounted_price'].apply(clean_currency).astype(float)
df['actual_price'] = df['actual_price'].apply(clean_currency).astype(float)

# Apply cleaning to Discount Percentage
df['discount_percentage'] = df['discount_percentage'].apply(clean_percent).astype(float)

# Fix 'rating_count' (remove commas)
# We use fillna(0) just in case there are missing counts
df['rating_count'] = df['rating_count'].str.replace(',', '').fillna(0).astype(int)

# --- CRITICAL FIX FOR RATING COLUMN ---
# This dataset often contains a specific error where one rating is "|".
# We use 'coerce' to turn that error into NaN, then fill it.
df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)

print("Data Types after cleaning:")
print(df.dtypes)

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download stopwords (run this once)
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove HTML tags (if any) and special characters/numbers
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 3. Tokenize (split into words)
    words = text.split()

    # 4. Remove Stopwords and Stemming
    cleaned_words = [stemmer.stem(word) for word in words if word not in stop_words]

    return " ".join(cleaned_words)


# Apply to review_content
df['cleaned_review'] = df['review_content'].apply(preprocess_text)

print(df[['review_content', 'cleaned_review']].head())

# Split the category string by the pipe symbol '|'
# This creates new columns: Main Category, Sub Category 1, etc.
category_split = df['category'].str.split('|', expand=True)

# Rename the first few columns (depending on how deep the hierarchy goes)
df['main_category'] = category_split[0]
df['sub_category_1'] = category_split[1]
df['sub_category_2'] = category_split[2]

# Drop the original messy category column if you want
# df.drop(columns=['category'], inplace=True)

print(df[['main_category', 'sub_category_1']].head())

# Check for duplicates based on product_id
duplicates = df.duplicated(subset=['product_id']).sum()
print(f"Duplicates found: {duplicates}")

# Remove them
df = df.drop_duplicates(subset=['product_id'])