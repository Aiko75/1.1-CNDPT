import pandas as pd

df = pd.read_csv("amazon.csv", encoding="utf-8")

price_cols = ["discounted_price", "actual_price"]

for col in price_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace("â‚¹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

for col in price_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df[price_cols].head())
print(df[price_cols].dtypes)

df.info()
df.drop_duplicates(inplace=True)
df.isna().sum()

df.to_csv("amazon_cleaned.csv", index=False)
