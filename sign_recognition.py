import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    #HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #red color range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    #contours
    contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    is_movement = False

    for contour in contours:
        if cv2.contourArea(contour) > 1000:

            is_movement = True

            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            last_save = 0

            if is_movement and time.time() - last_save > 10:
                filename = f"redSign_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                last_save = time.time()

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()