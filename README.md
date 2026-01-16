II. Đề cương chi tiết (Nội dung cho file .docx)
1. Giới thiệu bài toán & ý nghĩa thực tiễn
Bài toán: Phân tích hành vi và phản hồi của người dùng đối với các sản phẩm trên nền tảng thương mại điện tử Amazon.
Ý nghĩa: Giúp doanh nghiệp hiểu được mong muốn của khách hàng, nhận diện các vấn đề về chất lượng sản phẩm thông qua review và tối ưu hóa chiến lược giảm giá.
2. Mô tả nguồn dữ liệu & phương pháp thu thập
Nguồn: Bộ dữ liệu "Amazon Sales Dataset" từ Kaggle (1,465 bản ghi).
Phương pháp: Tải dữ liệu tự động thông qua API kagglehub và quản lý bằng thư viện Pandas.
3. Tiền xử lý dữ liệu
Làm sạch: Xóa bỏ các ký tự đặc biệt trong cột giá (₹, â‚¹), xử lý giá trị thiếu (NaN) và loại bỏ trùng lặp.
Chuẩn hóa văn bản: Chuyển về chữ thường, loại bỏ Emoji, HTML tags, và sử dụng lemmatization để đưa từ về gốc (ví dụ: "charging" -> "charge").

4. Phân tích dữ liệu mô tả (EDA)
Thống kê: Điểm Rating trung bình đạt 4.09/5, cho thấy mức độ hài lòng của khách hàng rất cao.
Xu hướng: Các sản phẩm thuộc danh mục Phụ kiện điện tử (Cáp, Sạc) chiếm số lượng áp đảo.
Tương quan: Mức giảm giá sâu không phải lúc nào cũng mang lại Rating cao tuyệt đối, người dùng quan tâm nhiều hơn đến công năng sử dụng.
5. Áp dụng khai thác dữ liệu
Sentiment Analysis: Sử dụng thuật toán VADER xác định được 1,421 phản hồi tích cực, chỉ có 34 phản hồi tiêu cực.
Clustering (K-Means): Phân dữ liệu thành 3 nhóm lớn. Nhóm lớn nhất (Cluster 2) tập trung vào các thiết bị ngoại vi và cáp kết nối.
Topic Modeling (LDA): Trích xuất được 5 chủ đề chính bao gồm: Đồ gia dụng, Văn phòng phẩm, Thiết bị sạc nhanh, Cáp USB và Trải nghiệm người dùng chung.
6. Kết quả & nhận xét
Kết quả: Hệ thống đã tự động phân loại được khối lượng lớn văn bản review sang các dạng nhãn định lượng.
Nhận xét: Khách hàng trên Amazon cực kỳ ưu ái các sản phẩm sạc nhanh và cáp kết nối. Các review tiêu cực (34 bản ghi) cần được lọc riêng để xử lý các vấn đề về lỗi kỹ thuật sản phẩm.
7. Kết luận và hướng phát triển
Kết luận: Machine Learning giúp tự động hóa quá trình giám sát chất lượng sản phẩm từ phản hồi khách hàng.
Hướng phát triển: Áp dụng các mô hình học sâu (Deep Learning) như BERT để phân tích cảm xúc chính xác hơn hoặc xây dựng hệ thống gợi ý sản phẩm (Recommendation System) dựa trên các Cluster đã tìm được.

Phân tích code đề tài khai thác và phân tích xu hướng đánh giá sản phẩm từ dữ liệu thương mại điện tử.
Do thầy cho phép sử dụng dataset công khai, ở đây ta sẽ sử dụng dataset từ trên kaggle.
Bước 1 sẽ là thu thập dataset từ trên kaggle

import kagglehub

path = kagglehub.dataset_download("karkavelrajaj/amazon-sales-dataset")

print("Path to dataset files:", path)

Dòng code trên sẽ tiến hành tải dataset trên kaggle mà ta đã chọn, sau đó sẽ in ra path dẫn đến dataset mà ta đã tải về.
Bước 2 sẽ là lưu trữ và tiền xử lý đơn giản dataset

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

Ở trong bước này, ta sẽ gọi lên dataset mà ta đã tải về, sau đó, tiến hành tiền xử lý đơn giản như tiến hành loại bỏ các kí đặc biệt trong cột discounted_price và cột actual_price.
Sau khi loại bỏ kí hiệu đặc biệt khỏi 2 cột trên, code tiến hành lọc và bỏ các duplicates có trong dataset.
Cuối cùng,code tạo ra dataset mới gọi là amazon_cleaned.csv

Ở bước thứ 3, ta tiến hành thực hiện tiền xử lý dữ liệu có trong dataset.

import pandas as pd
import numpy as np
import re
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

df = pd.read_csv('amazon_cleaned.csv')
print(f"Loaded data. Shape: {df.shape}")

if 'discount_percentage' in df.columns:
    df['discount_percentage'] = (
        df['discount_percentage']
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
    )
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

if 'rating_count' in df.columns:
    df['rating_count'] = (
        df['rating_count']
        .astype(str)
        .str.replace(',', '', regex=False)
    )
    # Fill missing values with 0 before converting
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)

if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)

print("Additional numerical columns cleaned.")

if 'category' in df.columns:
    # Split by pipe '|'
    cat_split = df['category'].str.split('|', expand=True)

    if cat_split.shape[1] > 0: df['main_category'] = cat_split[0]
    if cat_split.shape[1] > 1: df['sub_category_1'] = cat_split[1]
    if cat_split.shape[1] > 2: df['sub_category_2'] = cat_split[2]

    print("Categories split successfully.")

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True) # CHANGED: Download wordnet for lemmatization
nltk.download('omw-1.4', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() # CHANGED: Initialize Lemmatizer

def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = emoji.replace_emoji(text, replace='')

    text = text.lower()

    text = re.sub(r'<.*?>', '', text)

    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()

    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    return " ".join(cleaned_words)

text_cols = ['review_content', 'review_title', 'about_product']

print("Starting NLP processing (this may take a moment)...")
for col in text_cols:
    if col in df.columns:
        # Create new columns prefixed with 'clean_'
        df[f'clean_{col}'] = df[col].apply(clean_text)

output_file = 'amazon_final_processed.csv'
output_file_json = 'amazon_final_processed.json'
df.to_csv(output_file, index=False)
df.to_json(output_file_json, orient='records')

print(f"Done! Final processed file saved to: {output_file}")
print(f"Final Columns: {df.columns.tolist()}")

Ở trong code trên, sau khi ta gọi dataset ta có được sau bước hai lên, ta tiến hành xử lý dữ liệu để phục vụ cho các bước sau.
Code loại bỏ kí tự "%" và biến giá trị trong cột discounted_percentage thành float, cũng như biến giá trị cột rating_count thành int.
Sau đó, code tiến hành xử lý các dòng có giá trị lỗi là "|".
Sau khi hoàn thành, code tiến hành tách các cột category ra thành các cột nhỏ hơn để phục vụ cho việc phân tích dữ liệu sau này.
Một khi hoàn thành, code sẽ tiến hành tiền xử lý text có trong dataset. 
Ở đây, ta cần có thư viện nltk, xong từ thư viện nltk, ta import stopwords và WordNetLemmatizer
Code tiến hành gọi stopwords và WordNetLemmatizer lên, sau đó, code tiến hành loại bỏ emoji nếu có trong cột review-content và review_title.
Code ngoài ra còn đưa tất các text về lowercase, loại bỏ html nếu có và loại bỏ kí tự đặc biệt nếu có  và đưa text về 1 dạng thống nhất để cho xử lý dữ liệu sau nay, ví dụ như "charging" thành "charge".
Sau khi xử lý xong, code áp dụng text đã qua xử lý vào các cột.
Cuối cùng code tạo file dataset mới tên amazon_final_processed.csv, in ra thông báo hoàn thành và tên file .csv chứa dataset đã tiền xử lý.

