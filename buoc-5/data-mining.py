# Cài đặt thư viện: !pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import seaborn as sns
import matplotlib.pyplot as plt

# Load dữ liệu với path mới
df = pd.read_csv('../public/amazon_final_processed.csv')

# Khởi tạo bộ phân tích
analyzer = SentimentIntensityAnalyzer()

# Áp dụng phân tích cảm xúc lên cột clean_review_content
# Compound score: > 0.05 (Tích cực), < -0.05 (Tiêu cực), còn lại là Trung tính
df["sentiment_score"] = df["clean_review_content"].apply(
    lambda x: analyzer.polarity_scores(str(x))["compound"]
)

# Phân loại nhãn cảm xúc
def label_sentiment(score):
    if score >= 0.05: return "Positive"
    elif score <= -0.05: return "Negative"
    else: return "Neutral"

df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

print("--- Kết quả phân tích cảm xúc ---")
print(df["sentiment_label"].value_counts())

# 1. Chuyển đổi văn bản thành vector số bằng TF-IDF
# Giới hạn 1000 đặc trưng quan trọng nhất
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X = vectorizer.fit_transform(df["clean_review_content"].fillna(""))

# 2. Áp dụng KMeans để chia làm 3 cụm (ví dụ: Chất lượng, Giá cả, Giao hàng)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

print("\n--- Số lượng bản ghi trong mỗi cụm ---")
print(df["cluster"].value_counts())

# Sử dụng ma trận X từ bước TF-IDF ở trên
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

# Hàm hiển thị các từ khóa của từng chủ đề
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

print("\n--- Các chủ đề chính được tìm thấy ---")
display_topics(lda, vectorizer.get_feature_names_out(), 10)

# Tạo layout 1 hàng 3 cột để so sánh
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. BIỂU ĐỒ PHÂN BỐ CỤM (Clustering Distribution)
# Dựa trên Log: Cluster 2 chiếm ưu thế với 1053 bản ghi
sns.countplot(x="cluster", data=df, ax=axes[0], palette="magma")
axes[0].set_title("Phân bố các cụm sản phẩm (K-Means)", fontsize=14)
axes[0].set_xlabel("Cụm (Cluster)")
axes[0].set_ylabel("Số lượng sản phẩm")

# 2. BIỂU ĐỒ CẢM XÚC (Sentiment Analysis)
# Dựa trên Log: Positive (1421), Negative (34), Neutral (10)
sns.countplot(x="sentiment_label", data=df, ax=axes[1], order=["Positive", "Neutral", "Negative"], palette="viridis")
axes[1].set_title("Tỷ lệ cảm xúc người dùng (VADER)", fontsize=14)
axes[1].set_xlabel("Trạng thái cảm xúc")
axes[1].set_ylabel("Số lượng Review")

# 3. BIỂU ĐỒ MỐI QUAN HỆ GIỮA CỤM VÀ RATING
# Kiểm tra xem các cụm khác nhau có mức điểm đánh giá khác nhau không
sns.boxplot(x="cluster", y="rating", data=df, ax=axes[2], palette="Set2")
axes[2].set_title("Phân bổ điểm Rating theo từng Cụm", fontsize=14)
axes[2].set_xlabel("Cụm")
axes[2].set_ylabel("Điểm Rating")

plt.tight_layout()
plt.show()