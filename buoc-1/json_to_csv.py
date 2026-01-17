import json
import csv
import os


def convert_reviews_json_to_csv():
    # Cấu hình tên file
    input_file = "tong_hop_reviews.json"
    output_file = "tiki_reviews_final.csv"

    # Kiểm tra file đầu vào
    if not os.path.exists(input_file):
        print(f"❌ Lỗi: Không tìm thấy file '{input_file}'")
        return

    print(">>> Đang đọc file JSON...")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi đọc JSON: {e}")
        return

    # Mở file CSV để ghi
    # newline='' là bắt buộc trên Windows để không bị dòng trống xen kẽ
    with open(output_file, mode="w", encoding="utf-8-sig", newline="") as csv_file:
        # Định nghĩa các cột bạn muốn lấy
        fieldnames = [
            "product_id",  # ID sản phẩm
            "review_id",  # ID đánh giá
            "rating",  # Số sao (1-5)
            "title",  # Tiêu đề đánh giá
            "content",  # Nội dung chi tiết
            "customer_name",  # Tên khách hàng
            "thank_count",  # Số lượt cảm thấy hữu ích
            "created_at",  # Ngày tạo
            "images_count"  # Số lượng ảnh đính kèm (nếu cần)
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Ghi dòng tiêu đề (Header)
        writer.writeheader()

        total_rows = 0

        print(">>> Đang chuyển đổi dữ liệu...")

        # Duyệt qua từng sản phẩm trong file tổng hợp
        for product in data:
            p_id = product.get("product_id", "")
            reviews_list = product.get("reviews", [])

            # Duyệt qua từng review của sản phẩm đó
            for review in reviews_list:
                # Trích xuất thông tin người dùng an toàn
                created_by = review.get("created_by", {})
                full_name = created_by.get("full_name") if created_by else "Ẩn danh"

                # Tạo dòng dữ liệu
                row = {
                    "product_id": p_id,
                    "review_id": review.get("id"),
                    "rating": review.get("rating"),
                    "title": review.get("title", ""),
                    "content": review.get("content", ""),
                    "customer_name": full_name,
                    "thank_count": review.get("thank_count", 0),
                    "created_at": review.get("created_at"),  # Timestamp hoặc string tùy API
                    "images_count": len(review.get("images", []))
                }

                # Ghi dòng vào file CSV
                writer.writerow(row)
                total_rows += 1

    print("\n" + "=" * 40)
    print(f"✅ HOÀN TẤT! Đã xuất ra file: {output_file}")
    print(f"📝 Tổng số dòng dữ liệu: {total_rows}")
    print("=" * 40)


if __name__ == "__main__":
    convert_reviews_json_to_csv()