import re

text = "https://facebook"
print("text = " + text)
# Thay thế toàn bộ các chuỗi bắt đầu bằng "https://" thành một chuỗi rỗng, kể cả chuỗi có độ dài bất kỳ
text = re.sub(r"https://\S+", "", text)

print("newtest: "+ text)
