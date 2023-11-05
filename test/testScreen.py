import imutils
import pyautogui
import cv2
from datetime import datetime

now = datetime.now()
nameScreen = "D:\\screenshot"+ now.strftime("%H%M%S") +".png"

# Another Type
pyautogui.screenshot(nameScreen)
# we can then load our screenshot from disk in OpenCV format
image = cv2.imread(nameScreen)

# Hiển thị ảnh
cv2.imshow("hacker.com", imutils.resize(image))
cv2.waitKey(0) #wait for keyboard press