import numpy as np
import cv2
widthImg = 700
heightImg = 1000
x=0

imgDisplayAnskey = np.zeros([heightImg, widthImg, 3], dtype=np.uint8)
imgDisplayAnskey.fill(255)
cv2.putText(imgDisplayAnskey, "", (250, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.line(imgDisplayAnskey, (250, 50), (450, 50), (255, 0, 0), 5)
cv2.imshow('',imgDisplayAnskey)
cv2.waitKey(100000)