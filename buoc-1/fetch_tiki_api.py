import requests
import json


def fetch_tiki_api():
    # URL bạn cung cấp
    url = "https://api.tiki.vn/raiden/v3/widgets/top_choise"

    # Các tham số trong URL (Query Parameters)
    params = {
        "version": "2",
        "_v": "2",
        "clear": "1",
        "trackity_id": "37244d7a-da13-3f20-83e3-0fa1b7507f13",
        "_rf": "rotate_by_ctr"
    }

    # --- QUAN TRỌNG NHẤT: BỘ HEADERS GIẢ LẬP TRÌNH DUYỆT ---
    # Tiki kiểm tra rất kỹ phần này
    headers = {
        # Giả làm trình duyệt Chrome trên Windows
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        # Đánh lừa Tiki là request này đến từ trang chủ Tiki
        "Referer": "https://tiki.vn/",
        "Origin": "https://tiki.vn",

        # Các header phụ trợ để giống thật hơn
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    print(f">>> Đang gửi request đến Tiki...")

    try:
        # Gửi request GET
        response = requests.get(url, headers=headers, params=params, timeout=10)

        # Kiểm tra trạng thái
        print(f">>> Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # --- LƯU RA FILE JSON ---
            filename = "tiki_top_choice.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"✅ Thành công! Đã lưu dữ liệu vào '{filename}'")

            # In thử thống kê ngắn gọn
            items = data.get("data", [])
            print(f"-> Số lượng sản phẩm lấy được: {len(items)}")
            if items:
                first_item = items[0]
                print(f"-> Ví dụ sản phẩm đầu: {first_item.get('name')} - Giá: {first_item.get('price')}")

        elif response.status_code == 502:
            print("❌ Vẫn bị lỗi 502 Bad Gateway.")
            print("Nguyên nhân: Tiki phát hiện thư viện 'requests' của Python (TLS Fingerprint).")
            print("Giải pháp: Cần dùng thư viện 'curl_cffi' (Xem hướng dẫn bên dưới).")

        else:
            print(f"❌ Lỗi khác: {response.text}")

    except Exception as e:
        print(f"Lỗi kết nối: {e}")


if __name__ == "__main__":
    fetch_tiki_api()