'''import cv2

video = cv2.VideoCapture(0)
address = "http://192.168.1.104:8080/video"
video.open(address)

while True:
    success, img = video.read()
    cv2.imshow("Webcam",img)

'''