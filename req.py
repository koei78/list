import requests

url = "http://localhost:5000/upload"

# フォームデータ
data = {
    "shop_name": "テスト店舗",
    "address": "東京都千代田区1-1",
    "phone":"08074469081",
    "next_call_date":"2025/07/08",
    "next_call_time":"17:00",
    "time":"平日9:00～18:00",
    "day":"土日祝",
    "top_name":"伊藤健太",
    "summary":"テスト店舗の概要",
    "homepage_url":""
}
# ファイルデータ
files = {
    "file": open("test.csv", "rb")
}

# POST送信
response = requests.post(url, data=data, files=files)

# 結果表示
print("Status Code:", response.status_code)
print("Response Text:", response.text)