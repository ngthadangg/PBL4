from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
})
ref = db.reference('history')

def get_hourly_data(date):
    hourly_data = [0] * 24  # Khởi tạo mảng với 24 giờ, giá trị ban đầu là 0

    date_ref = ref.child(date)

    # Lặp qua từng giờ trong ngày
    for hour in range(24):
        hour_str = str(hour)
        hour_ref = date_ref.child(hour_str)

        # Lấy giá trị total_minutes từ Firebase hoặc mặc định là 0 nếu không có dữ liệu
        total_minutes = hour_ref.child("total_minutes").get() or 0

        # Lưu giá trị vào mảng theo giờ
        hourly_data[hour] = total_minutes

    return hourly_data

if __name__ == "__main__":
    # Thay thế "2023-01-01" bằng ngày bạn quan tâm
    target_date = "2023-12-06"
    
    result = get_hourly_data(target_date)
    
    # In ra mảng chứa tổng số phút hoạt động của chương trình cho từng giờ
    print(result)
