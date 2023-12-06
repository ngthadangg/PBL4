import requests
from bs4 import BeautifulSoup

def get_title_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.text.strip()
            else:
                return "Không có tiêu đề"
        else:
            return "Không thể truy cập trang web"
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Ví dụ sử dụng
url = "https://www.facebook.com/"
title = get_title_from_url(url)
print(f"Tiêu đề của {url}: {title}")
