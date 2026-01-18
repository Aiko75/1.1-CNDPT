import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# 1. LOAD DỮ LIỆU
# =============================================================================
# Sử dụng đúng tên file hiện có trong môi trường (định dạng CSV)
filename = 'tiki_cleaned_final.xlsx - Sheet1.csv'

try:
    df = pd.read_excel('tiki_cleaned_final.xlsx')
    print("--- Đã tải dữ liệu thành công ---")
    print(df.info())
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{filename}'.")
    exit()

# Cấu hình giao diện biểu đồ
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# =============================================================================
# 2. PHÂN TÍCH ĐƠN BIẾN (UNIVARIATE ANALYSIS)
# =============================================================================

# --- A. Phân bố Rating ---
if 'rating' in df.columns:
    plt.figure()
    # Sử dụng countplot của seaborn để đếm và vẽ biểu đồ cột cho cột 'rating'
    ax = sns.countplot(x='rating', data=df, palette='viridis')
    plt.title('Phân bố điểm đánh giá (Rating)', fontsize=15)
    plt.xlabel('Điểm (Sao)')
    plt.ylabel('Số lượng')
    plt.show()

# --- B. Phân tích độ dài bình luận (Word Count) ---
if 'clean_text' in df.columns:
    # Sử dụng Pandas để tách chuỗi và đếm số phần tử (số từ)
    df['word_count'] = df['clean_text'].astype(str).str.split().str.len()

    plt.figure()
    # Vẽ biểu đồ phân phối độ dài comment
    sns.histplot(df['word_count'], bins=50, kde=True, color='skyblue')
    plt.title('Phân bố độ dài bình luận (Số từ)', fontsize=15)
    plt.xlabel('Số từ')
    plt.ylabel('Tần suất')
    plt.show()

# =============================================================================
# 3. PHÂN TÍCH ĐA BIẾN (BIVARIATE ANALYSIS)
# =============================================================================

# --- Quan hệ giữa Rating và Độ dài bình luận ---
if 'rating' in df.columns and 'word_count' in df.columns:
    plt.figure()
    sns.boxplot(x='rating', y='word_count', data=df, palette='Set2')
    plt.title('Mối quan hệ giữa Rating và Độ dài bình luận', fontsize=15)
    plt.xlabel('Rating')
    plt.ylabel('Số từ')
    plt.show()

# =============================================================================
# 4. TÌM TỪ KHÓA PHỔ BIẾN (Chỉ dùng Pandas)
# =============================================================================

if 'clean_text' in df.columns:
    # Kỹ thuật:
    # 1. str.split(): Tách từng dòng text thành list các từ
    # 2. explode(): Biến mỗi phần tử trong list thành một dòng dữ liệu riêng biệt (trải phẳng dữ liệu)
    # 3. value_counts(): Đếm tần suất xuất hiện của từng từ
    top_words = df['clean_text'].astype(str).str.split().explode().value_counts().head(20)

    # Chuyển kết quả Series sang DataFrame để vẽ
    df_top_words = top_words.reset_index()
    df_top_words.columns = ['Word', 'Frequency']

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Frequency', y='Word', data=df_top_words, palette='magma')
    plt.title('Top 20 từ xuất hiện nhiều nhất', fontsize=15)
    plt.xlabel('Số lần xuất hiện')
    plt.ylabel('Từ')
    plt.show()

print("\n--- Hoàn tất phân tích ---")