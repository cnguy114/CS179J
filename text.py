import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

print (frame)

cv2.imwrite(r'./179jGit/temp.jpg',frame)
