from selenium import webdriver

def get_web_history():
    # Khởi chạy trình duyệt Chrome
    driver = webdriver.Chrome()

    # Duyệt đến trang web chrome://history/
    driver.get("edge://history/all")

    # Thu thập dữ liệu truy cập web
    history = []
    for item in driver.find_elements_by_class_name("history-entry"):
        url = item.find_element_by_tag_name("a").get_attribute("href")
        title = item.find_element_by_class_name("history-title").text
        timestamp = item.find_element_by_class_name("history-timestamp").text

        history.append({
            "url": url,
            "title": title,
            "timestamp": timestamp
        })

    # Đóng trình duyệt Chrome
    driver.quit()

    return history

# In lịch sử truy cập web
history = get_web_history()
for item in history:
    print(item["url"], item["title"], item["timestamp"])