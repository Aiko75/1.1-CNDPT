import requests
import json
import time
import random
import os


def fetch_tiki_reviews(product_id, spid, seller_id, page=1):
    """
    Hàm lấy đánh giá sản phẩm Tiki
    """
    base_url = "https://tiki.vn/api/v2/reviews"

    # Đã sửa limit thành 10 theo yêu cầu
    params = {
        "limit": "10",
        "include": "comments,contribute_info,attribute_vote_summary",
        "sort": "score|desc,id|desc,stars|all",
        "page": str(page),
        "spid": str(spid),
        "product_id": str(product_id),
        "seller_id": str(seller_id)
    }

    # Headers giả lập trình duyệt
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://tiki.vn/product-p{product_id}.html",  # Referer động
        "Origin": "https://tiki.vn",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ❌ Lỗi HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Lỗi kết nối: {e}")
        return None


def main():
    input_file = "tiki_top_choice.json"
    output_folder = "tiki_reviews_data"

    # 1. Kiểm tra file đầu vào
    if not os.path.exists(input_file):
        print(f"Lỗi: Không tìm thấy file '{input_file}'. Hãy chạy bước lấy danh sách sản phẩm trước.")
        return

    # 2. Tạo thư mục chứa kết quả nếu chưa có
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Đã tạo thư mục '{output_folder}' để lưu review.")

    # 3. Đọc dữ liệu
    print(">>> Đang đọc danh sách sản phẩm...")
    with open(input_file, "r", encoding="utf-8") as f:
        data_source = json.load(f)

    # Lấy danh sách items (dựa trên cấu trúc file json bạn cung cấp)
    items = data_source.get("items", [])

    # Chỉ lấy 100 sản phẩm đầu tiên (hoặc ít hơn nếu danh sách ko đủ 100)
    limit_products = 150
    items_process = items[:limit_products]

    print(f">>> Tìm thấy {len(items)} sản phẩm. Sẽ xử lý {len(items_process)} sản phẩm đầu tiên.\n")

    # 4. Vòng lặp xử lý
    for index, item in enumerate(items_process, 1):
        # Trích xuất thông tin từ JSON
        p_id = item.get("id")
        spid = item.get("seller_product_id")
        sell_id = item.get("seller_id")
        name = item.get("name", "Sản phẩm không tên")

        if not p_id:
            continue

        print(f"[{index}/{len(items_process)}] Đang lấy review cho: {name[:40]}...")
        print(f"   -> ID: {p_id} | SPID: {spid}")

        # Gọi hàm fetch
        review_data = fetch_tiki_reviews(p_id, spid, sell_id)

        if review_data:
            # Lưu file riêng cho từng sản phẩm
            filename = f"{output_folder}/review_{p_id}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(review_data, f, ensure_ascii=False, indent=4)

            # Thống kê nhanh
            count = len(review_data.get('data', []))
            print(f"   ✅ Đã lưu {count} review vào '{filename}'")
        else:
            print("   ⚠️ Không lấy được dữ liệu.")

        # --- QUAN TRỌNG: Nghỉ ngẫu nhiên từ 1 đến 3 giây để tránh bị block ---
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)

    print("\n>>> HOÀN THÀNH TOÀN BỘ QUÁ TRÌNH!")


if __name__ == "__main__":
    main()