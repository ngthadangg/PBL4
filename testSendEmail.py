import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    # Thông tin của người gửi
    from_email = 'dangnghialap2003@gmail.com'
    password = 'vqnc fovp woff pkbj'  # Nên sử dụng ứng dụng cụ thể để tránh sử dụng mật khẩu chính

    # Tạo đối tượng MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))

    # Thiết lập kết nối SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Đăng nhập vào email của bạn
    server.login(from_email, password)

    # Gửi email
    server.sendmail(from_email, to_email, msg.as_string())

    # Đóng kết nối
    server.quit()

# Sử dụng hàm để gửi email
to_email = 'nhathoang261203@gmail.com'
subject = 'Chào anh hoàng'
body = 'ChàO anh hoàng em là  thanh Đăng'

send_email(to_email, subject, body)
