import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import imghdr  # Thư viện này sẽ xác định loại ảnh

def send_email_with_image(to_email):
    # Thông tin người gửi
    from_email = 'dangnghialap2003@gmail.com'
    password = 'vqnc fovp woff pkbj'  # Sử dụng mật khẩu ứng dụng nếu cần thiết

    # Tạo đối tượng MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Email với hình ảnh'

    # Nội dung email (HTML)
    body = """
    <p>Chào bạn,</p>
    <p>Đây là một email với hình ảnh:</p>
    <p><img src="cid:image1" alt="Hình ảnh"></p>
    <p>Trân trọng,</p>
    <p>Đội ngũ của bạn</p>
    """

    # Thêm nội dung email
    msg.attach(MIMEText(body, 'html'))

    # Chèn hình ảnh
    image_path = 'D:\Semeter 5\PBL4\PBL\image\screenshot-20231119-003442.png'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        image_type = imghdr.what(image_path)
        image_name = 'image.jpg'
        image = MIMEImage(image_data, image_type)
        image.add_header('Content-ID', '<image1>')
        image.add_header('Content-Disposition', 'inline', filename=image_name)
        msg.attach(image)

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

# Gọi hàm để gửi email với hình ảnh
to_email = '102210310@sv1.dut.udn.vn'
send_email_with_image(to_email)
