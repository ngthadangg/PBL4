import threading
import datetime
from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
})
ref = db.reference('history')

# Biến toàn cục để theo dõi thời gian đã trôi qua và kiểm soát việc kết thúc chương trình

def update_firebase():

    try:
        # Lấy thời gian hiện tại
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_hour = now.hour

        # Tạo hoặc cập nhật nút ngày trong Firebase
        date_ref = ref.child(current_date)

        # Tạo hoặc cập nhật nút giờ trong Firebase
        hour_ref = date_ref.child(str(current_hour))

        # Đọc giá trị hiện tại từ Firebase
        current_minutes = hour_ref.child("total_minutes").get() or 0

        # Cộng thêm 1 vào giá trị hiện tại
        current_minutes += 1

        # Cập nhật giá trị mới lên Firebase
        hour_ref.update({"total_minutes": current_minutes})

        # Lặp lại hàm sau mỗi phút
        threading.Timer(60, update_firebase).start()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Bắt đầu tính thời gian từ khi chương trình được khởi chạy
    update_firebase()

    try:
        # Chương trình của bạn ở đây...

        # Ví dụ: để chương trình chạy 5 phút trước khi kết thúc
        threading.Timer(300, lambda: setattr(running, False)).start()

        # Để chương trình không kết thúc ngay lập tức
        input("Nhấn Enter để kết thúc chương trình...")
    except Exception as e:
        print(f"Error: {e}")

