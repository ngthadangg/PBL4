import requests

def get_web_history():
    # Tạo danh sách lịch sử
    history = []

    # Lặp qua tất cả các trang web đã truy cập  edge://settings/profiles
    for url in requests.get("edge://history/all").json()["items"]:
        # Thêm trang web vào danh sách lịch sử
        history.append({
            "url": url["url"],
            "title": url["title"],
            "timestamp": url["lastVisitedDate"]
        })

    return history

# In lịch sử truy cập web
history = get_web_history()
for item in history:
    print(item["url"], item["title"], item["timestamp"])