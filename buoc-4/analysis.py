import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. CẤU HÌNH GIAO DIỆN ĐỒ THỊ
# ---------------------------------------------------------
# Thiết lập style cho Seaborn để đồ thị trông chuyên nghiệp hơn
sns.set_theme(style="whitegrid")
# Hỗ trợ hiển thị tiếng Việt hoặc ký tự đặc biệt nếu có
plt.rcParams['figure.figsize'] = (12, 6)

# ---------------------------------------------------------
# 2. LOAD DỮ LIỆU
# ---------------------------------------------------------
# Đọc file CSV đã được làm sạch từ bước trước
df = pd.read_csv('../public/amazon_final_processed.csv')

# ---------------------------------------------------------
# 3. PHÂN TÍCH TỔNG QUAN (DESCRIPTIVE STATISTICS)
# ---------------------------------------------------------
print("--- Thống kê mô tả các cột số ---")
print(df.describe()) # Xem mean, min, max của rating, discount...

# ---------------------------------------------------------
# 4. TRỰC QUAN HÓA (VISUALIZATION)
# ---------------------------------------------------------

# Đồ thị 1: Top 10 danh mục sản phẩm phổ biến nhất
plt.figure(figsize=(12, 6))
# Đếm số lượng sản phẩm theo từng main_category
top_categories = df['main_category'].value_counts().nlargest(10)
sns.barplot(x=top_categories.values, y=top_categories.index, palette='viridis')
plt.title('Top 10 Danh mục sản phẩm phổ biến nhất trên Amazon')
plt.xlabel('Số lượng sản phẩm')
plt.ylabel('Danh mục chính')
plt.show()

# Đồ thị 2: Phân phối điểm đánh giá (Rating Distribution)
plt.figure(figsize=(10, 6))
# Sử dụng histplot để xem mật độ điểm số từ 0 đến 5
sns.histplot(df['rating'], bins=20, kde=True, color='skyblue')
plt.title('Phân phối điểm đánh giá của người dùng (Rating)')
plt.xlabel('Điểm đánh giá')
plt.ylabel('Tần suất')
plt.show()

# Đồ thị 3: Mối quan hệ giữa % Giảm giá và Điểm đánh giá
plt.figure(figsize=(10, 6))
# Kiểm tra xem giảm giá sâu có giúp tăng điểm rating không
sns.scatterplot(data=df, x='discount_percentage', y='rating', alpha=0.5, color='orange')
plt.title('Mối quan hệ giữa % Giảm giá và Điểm đánh giá')
plt.xlabel('% Giảm giá')
plt.ylabel('Rating')
plt.show()

# ---------------------------------------------------------
# 5. TỔNG HỢP DỮ LIỆU (AGGREGATION)
# ---------------------------------------------------------
# Tính điểm rating trung bình cho mỗi danh mục chính
category_rating = df.groupby('main_category')['rating'].mean().sort_values(ascending=False)
print("\n--- Rating trung bình theo từng danh mục ---")
print(category_rating)