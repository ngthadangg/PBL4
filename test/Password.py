import crypt

def get_passwords():
    # Truy cập vào dữ liệu mật khẩu
    with open("/etc/passwd", "r") as f:
        for line in f:
            username, _, _, _, password = line.split(":")

            # Giải mã mật khẩu
            password = crypt.crypt(password, "$6$salt")

            # Lưu trữ mật khẩu
            with open("D:\\Semeter 5\\PBL4\\PBL\\passwords.txt", "a") as f:
                f.write(username + ":" + password + "\n")


# Chạy hàm get_passwords()
get_passwords()