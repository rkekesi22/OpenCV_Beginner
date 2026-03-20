from subprocess import check_output

import cv2
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    # difference between two picture
    diff = cv2.absdiff(frame1, frame2)

    # show all
    #cv2.imshow('frame1 (elozo)', frame1)
    #cv2.imshow('frame2 (kovetkezo)', frame2)
    #cv2.imshow('diff', diff)

    # gray
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    #hsv
    #cv2.imshow('hsv diff', hsv)
    #hsv = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)

    #only the red parts are white
    #lower = (0,120, 70)
    #upper = (10, 255, 255)

    #mask = cv2.inRange(hsv, lower, upper)
    #cv2.imshow('mask', mask)

    #zajszűrés
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #cv2.imshow('gray diff', gray)
    #cv2.imshow('blur', blur)

    # threshold
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    #cv2.imshow('thresh', thresh)

    # dilate
    dilated = cv2.dilate(thresh, None, iterations=3)
    #cv2.imshow('dilated', dilated)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    is_movement = False

    for contour in contours:
        #zaj kiszűrés
        if cv2.contourArea(contour) < 2000:
            continue

        #Movement --> Save
        is_movement = True

        #Téglalap számítás
        x,y,w,h = cv2.boundingRect(contour)

        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(frame1, "Movement!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if is_movement:
            filename = f"movement_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame1)

    cv2.imshow("Kamera", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()


    # exit ESC
    if cv2.waitKey(10) == 27:
        break

#cap.release()
#cv2.destroyAllWindows()