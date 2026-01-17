import pandas as pd
import re
import os
from underthesea import word_tokenize

# --- CẤU HÌNH ---
INPUT_FILE = '../buoc-2/bao_cao_tiki.xlsx'
OUTPUT_FILE = 'tiki_cleaned_final.xlsx'


def xu_ly_review_tiki():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Lỗi: Không tìm thấy file '{INPUT_FILE}'")
        return

    print(">>> 1. Đang đọc dữ liệu...")
    df = pd.read_excel(INPUT_FILE)

    # Gộp Title và Content để xử lý một thể
    df['full_text'] = df['title'].fillna('') + " " + df['content'].fillna('')

    # Lọc bỏ dòng trống
    df = df[df['full_text'].str.strip() != ""]

    print(">>> 2. Đang tiền xử lý văn bản theo yêu cầu...")

    def clean_text_custom(text):
        if not isinstance(text, str):
            return ""

        # 1. Chuyển thành chữ thường
        text = text.lower()

        # 2. Xử lý URL (Xóa link http...)
        text = re.sub(r'http\S+|www\S+', ' ', text)

        # 3. Xử lý Ký tự lặp (Spam)
        # Tìm ký tự lặp lại từ 3 lần trở lên -> Rút gọn còn 1 lần
        # VD: "tốtttttt" -> "tốt", "đẹppppp" -> "đẹp"
        # Logic: \1 là ký tự tìm thấy, {2,} là lặp thêm 2 lần nữa (tổng >= 3)
        text = re.sub(r'([a-zÀ-ỹ])\1{2,}', r'\1', text)

        # 4. Xử lý Ký tự lạ + Icon + Lỗi dính dấu câu
        # Thay thế TẤT CẢ ký tự không phải chữ cái (icon, *, !, ,, .) bằng DẤU CÁCH
        # Việc này đồng thời tách các từ bị dính (VD: "đẹp,giao" -> "đẹp giao")
        text = re.sub(r"[^a-zA-ZÀ-ỹ\s]", " ", text)

        # 5. Xử lý khoảng trắng thừa (do bước 4 tạo ra)
        # VD: "hàng    tốt" -> "hàng tốt"
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    # Áp dụng hàm clean
    df["clean_text"] = df["full_text"].apply(clean_text_custom)

    print(">>> 3. Đang tách từ tiếng Việt (Underthesea)...")
    try:
        df["tokens"] = df["clean_text"].apply(lambda x: word_tokenize(x, format="text"))
    except Exception as e:
        print(f"⚠️ Lỗi tách từ (có thể bỏ qua nếu không cần thiết): {e}")

    # --- KIỂM TRA KẾT QUẢ ---
    print("\n=== TEST THỬ 5 DÒNG ===")
    sample_data = [
        "Hàng tốtttttt quá shop ơi ❤️❤️❤️",
        "Giao hàng nhanhhhhh,đóng gói kĩ",
        "Sản phẩm 5 sao ***** nhé !!!",
        "hàng đẹp,giao nhanh",
        "chat luong!!!!!"
    ]

    for line in sample_data:
        cleaned = clean_text_custom(line)
        print(f"Gốc: {line}")
        print(f"Sửa: {cleaned}")
        print("-" * 20)

    # Lưu kết quả
    df[['product_id', 'review_id', 'rating', 'clean_text', 'tokens']].to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ Đã lưu file sạch vào: {OUTPUT_FILE}")


if __name__ == "__main__":
    xu_ly_review_tiki()