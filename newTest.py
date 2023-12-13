import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_advertisement_email(to_email):
    # Thông tin người gửi
    from_email = 'dangnghialap2003@gmail.com'
    password = 'vqnc fovp woff pkbj'  # Sử dụng mật khẩu ứng dụng nếu cần thiết

    # Tạo đối tượng MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Khám phá sản phẩm mới từ Apple'

    # Nội dung email
    body = """
    Chào bạn,

    Apple vừa ra mắt sản phẩm mới và bạn không muốn bỏ lỡ cơ hội!

    Hãy truy cập trang web của chúng tôi để biết thêm chi tiết: https://www.apple.com

    Trân trọng,
    Đội ngũ Apple
    """

    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Thiết lập kết nối SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Đăng nhập vào email của bạn
        server.login(from_email, password)

        # Gửi email
        server.sendmail(from_email, to_email, msg.as_string())

        print("Email đã được gửi thành công!")

    except Exception as e:
        print("Có lỗi xảy ra khi gửi email:", str(e))

    finally:
        # Đóng kết nối
        server.quit()

# Gọi hàm để gửi email quảng cáo
to_email = '102210310@sv1.dut.udn.vn'
send_advertisement_email(to_email)
