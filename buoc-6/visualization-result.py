import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# muon chay phan code nay hay vao trong buoc 5 de chay

# Thiết lập phong cách cho biểu đồ
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (15, 5)

# Load dữ liệu với path mới
df = pd.read_csv('../public/amazon_final_processed.csv')

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