# Tiki Reviews Scraping & Analysis Pipeline 🛒📊

Dự án này là một quy trình tự động hóa (Pipeline) hoàn chỉnh để thu thập, quản lý và tiền xử lý dữ liệu đánh giá sản phẩm từ Tiki.vn. Hệ thống bao gồm 3 giai đoạn chính: Cào dữ liệu (Scraping), Quản lý & Thống kê (Management), và Tiền xử lý văn bản (Preprocessing).

## 📦 Yêu cầu cài đặt (Prerequisites)

Trước khi chạy, hãy đảm bảo bạn đã cài đặt Python và các thư viện cần thiết:

```bash
pip install requests pandas openpyxl underthesea matplotlib

```

---

## 🚀 QUY TRÌNH THỰC HIỆN

### GIAI ĐOẠN 1: Thu thập dữ liệu (Data Collection)

Giai đoạn này chịu trách nhiệm lấy dữ liệu thô từ API của Tiki và chuyển đổi sang định dạng bảng (CSV).

#### 1. Lấy danh sách sản phẩm (`fetch_tiki_api.py`)

* **Chức năng:** Kết nối đến API `widgets/top_choise` của Tiki để lấy danh sách các sản phẩm đang bán chạy/nổi bật.
* **Kỹ thuật:** Sử dụng Fake Headers (User-Agent, Referer) để giả lập trình duyệt, vượt qua cơ chế chặn bot cơ bản.
* **Output:** File `tiki_top_choice.json` chứa thông tin cơ bản (ID, Seller ID, SKU) của các sản phẩm.

#### 2. Cào đánh giá chi tiết (`fetch_tiki_reviews.py`)

* **Chức năng:** Đọc danh sách sản phẩm từ file JSON ở bước trên. Gửi request đến API Reviews của Tiki để lấy comment cho từng sản phẩm.
* **Kỹ thuật:**
* Tự động tạo thư mục `tiki_reviews_data`.
* Sử dụng cơ chế **Random Sleep (1-3 giây)** giữa các lần gọi để tránh bị khóa IP.
* Lưu trữ review của mỗi sản phẩm thành một file JSON riêng biệt để đảm bảo an toàn dữ liệu.


* **Output:** Thư mục `tiki_reviews_data/` chứa hàng loạt file `review_{id}.json`.

#### 3. Gộp dữ liệu (`tong_hop_reviews.py`)

* **Chức năng:** Quét toàn bộ thư mục `tiki_reviews_data`, đọc tất cả các file JSON lẻ và gộp chúng thành một danh sách duy nhất.
* **Kỹ thuật:** Trích xuất chỉ các trường cần thiết, loại bỏ metadata thừa.
* **Output:** File `tong_hop_reviews.json`.

#### 4. Chuyển đổi sang CSV (`json_to_csv.py`)

* **Chức năng:** Làm phẳng (Flatten) cấu trúc JSON lồng nhau. Mỗi review sẽ trở thành một dòng trong file CSV.
* **Kỹ thuật:** Sử dụng encoding `utf-8-sig` để file CSV hiển thị đúng Tiếng Việt khi mở bằng Excel.
* **Output:** File `tiki_reviews_final.csv`.

---

### GIAI ĐOẠN 2: Quản lý & Thống kê sơ bộ (Data Management)

#### 5. Kiểm tra và báo cáo (`saving-and-manage.py`)

* **Chức năng:** Sử dụng thư viện **Pandas** để đọc file CSV và thực hiện các bước làm sạch cơ bản cũng như thống kê.
* **Các thao tác chính:**
* Chuyển đổi Timestamp (`created_at`) sang định dạng ngày tháng (`datetime`).
* Loại bỏ các đánh giá trùng lặp (Duplicate removal).
* Tính điểm đánh giá trung bình (Average Rating) cho từng sản phẩm.
* Thống kê phân bố số sao (1 sao vs 5 sao).
* Lọc ra các review tiêu cực (1-2 sao) để kiểm tra.


* **Output:** File `bao_cao_tiki.xlsx` (Định dạng Excel dễ đọc).

---

### GIAI ĐOẠN 3: Tiền xử lý dữ liệu (Data Preprocessing)

#### 6. Làm sạch văn bản chuyên sâu (`preprocessing-data.py`)

* **Chức năng:** Chuẩn bị dữ liệu văn bản sạch để phục vụ cho các bài toán AI/Machine Learning (như Phân tích cảm xúc).
* **Các kỹ thuật xử lý NLP (Natural Language Processing):**
* **Gộp văn bản:** Kết hợp `Tiêu đề` và `Nội dung` để có ngữ cảnh đầy đủ.
* **Regex Cleaning:**
* Chuyển về chữ thường.
* Xóa URL, Link rác.
* **Chống Spam ký tự:** Rút gọn các từ bị kéo dài (VD: "tốtttttt" -> "tốt", "đẹppppp" -> "đẹp").
* **Xử lý ký tự lạ:** Thay thế icon, emoji, dấu câu sai quy cách bằng khoảng trắng (VD: "đẹp,giao" -> "đẹp giao").


* **Tách từ (Tokenization):** Sử dụng thư viện `underthesea` để tách từ tiếng Việt (VD: "giao hàng" -> "giao_hàng").


* **Output:** File `tiki_cleaned_final.xlsx` (Chứa cột `tokens` và `clean_text` đã sẵn sàng train model).

---

## ⚠️ Lưu ý quan trọng

1. **Rate Limiting:** Trong file `fetch_tiki_reviews.py`, code đã set thời gian nghỉ ngẫu nhiên (`time.sleep`). Không nên xóa dòng này để tránh bị Tiki chặn IP.
2. **Đường dẫn file:** Kiểm tra kỹ đường dẫn file (input/output path) trong các file code nếu bạn thay đổi cấu trúc thư mục.
3. **Thư viện Underthesea:** Lần đầu chạy `preprocessing-data.py`, thư viện có thể cần tải model ngôn ngữ về, hãy đảm bảo có kết nối mạng.