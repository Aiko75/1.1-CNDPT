import json
import os


def merge_review_files():
    # Cấu hình đường dẫn
    input_folder = "tiki_reviews_data"
    output_file = "tong_hop_reviews.json"

    # Kiểm tra thư mục tồn tại
    if not os.path.exists(input_folder):
        print(f"❌ Lỗi: Không tìm thấy thư mục '{input_folder}'")
        return

    merged_data = []
    files = os.listdir(input_folder)

    # Chỉ lấy các file có đuôi .json
    json_files = [f for f in files if f.endswith(".json")]

    print(f"👉 Tìm thấy {len(json_files)} file trong thư mục. Đang tiến hành ghép...")

    count_success = 0
    total_reviews = 0

    for filename in json_files:
        file_path = os.path.join(input_folder, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)

                # Trích xuất ID sản phẩm từ tên file (ví dụ: review_276313958.json -> 276313958)
                # Hoặc lấy từ trong data nếu có
                product_id = filename.replace("review_", "").replace(".json", "")

                # Lấy danh sách review (nằm trong key 'data' của response API Tiki)
                reviews_list = content.get("data", [])

                if reviews_list:
                    # Tạo cấu trúc gọn gàng cho từng sản phẩm
                    product_entry = {
                        "product_id": product_id,
                        "total_reviews_fetched": len(reviews_list),
                        "reviews": reviews_list
                    }

                    merged_data.append(product_entry)

                    count_success += 1
                    total_reviews += len(reviews_list)

        except Exception as e:
            print(f"⚠️ Lỗi khi đọc file {filename}: {e}")

    # Lưu ra file tổng
    if merged_data:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)

        print("\n" + "=" * 40)
        print(f"✅ HOÀN TẤT!")
        print(f"📁 Đã gộp {count_success} file sản phẩm.")
        print(f"📝 Tổng cộng {total_reviews} đánh giá đã được lưu.")
        print(f"💾 File kết quả: {output_file}")
        print("=" * 40)
    else:
        print("❌ Không có dữ liệu nào được gộp.")


if __name__ == "__main__":
    merge_review_files()