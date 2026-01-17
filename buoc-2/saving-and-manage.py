import pandas as pd
import matplotlib.pyplot as plt


def quan_ly_du_lieu_tiki():
    file_path = '../buoc-1/tiki_reviews_final.csv'

    print(">>> 1. Đang đọc dữ liệu từ CSV...")
    try:
        # Đọc file CSV
        df = pd.read_csv(file_path)
        print(f"✅ Đã tải thành công {len(df)} dòng dữ liệu.")
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file csv. Hãy chạy bước 1 trước.")
        return

    # --- KIỂM TRA DỮ LIỆU ---
    print("\n>>> 2. Thông tin tổng quan:")
    print(df.info())  # Xem kiểu dữ liệu và số lượng non-null

    print("\n>>> 5 dòng đầu tiên:")
    print(df.head())

    # --- LÀM SẠCH & CHUYỂN ĐỔI ---
    print("\n>>> 3. Xử lý dữ liệu...")

    # a. Chuyển đổi 'created_at' từ timestamp (số giây) sang dạng ngày tháng đọc được
    # Tiki thường trả về Unix Timestamp (số nguyên)
    if 'created_at' in df.columns:
        df['ngay_danh_gia'] = pd.to_datetime(df['created_at'], unit='s')
        # Xóa cột cũ nếu không cần
        # df.drop(columns=['created_at'], inplace=True)
        print("   -> Đã chuyển đổi cột 'created_at' sang 'ngay_danh_gia'")

    # b. Loại bỏ các dòng trùng lặp (nếu có)
    initial_count = len(df)
    df.drop_duplicates(subset=['review_id'], inplace=True)
    final_count = len(df)
    if initial_count > final_count:
        print(f"   -> Đã loại bỏ {initial_count - final_count} review trùng lặp.")

    # --- PHÂN TÍCH CƠ BẢN ---
    print("\n>>> 4. Thống kê cơ bản:")

    # a. Tính điểm đánh giá trung bình theo từng sản phẩm
    # Group by 'product_id' và tính mean của cột 'rating'
    avg_rating = df.groupby('product_id')['rating'].mean().reset_index()
    avg_rating.rename(columns={'rating': 'diem_trung_binh'}, inplace=True)

    # Làm tròn 2 chữ số thập phân
    avg_rating['diem_trung_binh'] = avg_rating['diem_trung_binh'].round(2)

    print("\n[BẢNG ĐIỂM TRUNG BÌNH THEO SẢN PHẨM]")
    print(avg_rating)

    # b. Đếm số lượng đánh giá theo số sao (1 sao -> 5 sao)
    star_counts = df['rating'].value_counts().sort_index()
    print("\n[PHÂN BỐ SỐ SAO TOÀN BỘ DATA]")
    print(star_counts)

    # c. Lọc ra các review tiêu cực (1-2 sao) để đọc thử
    negative_reviews = df[df['rating'] <= 2]
    print(f"\n[REVIEW TIÊU CỰC] Tìm thấy {len(negative_reviews)} đánh giá 1-2 sao.")
    if not negative_reviews.empty:
        print("Ví dụ 1 review tiêu cực:")
        sample = negative_reviews.iloc[0]
        print(f"   - Khách: {sample['customer_name']}")
        print(f"   - Nội dung: {sample['content']}")

    # --- XUẤT FILE EXCEL (Optional) ---
    # Xuất ra Excel để gửi báo cáo sẽ đẹp hơn CSV
    output_excel = 'bao_cao_tiki.xlsx'
    df.to_excel(output_excel, index=False)
    print(f"\n✅ Đã lưu file đã xử lý ra Excel: {output_excel}")


if __name__ == "__main__":
    quan_ly_du_lieu_tiki()