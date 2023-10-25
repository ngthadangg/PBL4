import psutil

def get_app_history():
    # Lay danh sach cac tien trinh
    processes = psutil.process_iter()
    
    for process in processes:
        # print(process.name())
        #Lay ten cua tien trinh
        name = process.as_dict()["name"]
        
        #lay thoi gian bat ddau cua tien trinh
        start_time = process.create_time()
        
        #Them vao danh sach lich su tien trinh
        history.append(
            {
                "name": name,
                "start_time": start_time
            }
        )
#tao danh sach lich su tien trinh
history = []

#lay lich su cac ung dung
get_app_history()        
    
for app in history:
    print(app["name"] , app["start_time"])
    