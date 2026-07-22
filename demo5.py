import cv2 as cv

import mediapipe as mp
import numpy as np
import math


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands =  mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) 

box_x = 100
box_y = 100
box_size = 100

L1 = 0
L2 = 0
is_activate = False

cap = cv.VideoCapture(0)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

while True:
    ret,image = cap.read()

    image = cv.flip(image,1)
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            # print(hand_landmarks.landmark[8].x)
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[4]
            indexX,indexY = int(index.x*width),int(index.y*height)
            middleX,middleY = int(middle.x*width),int(middle.y*height)

            # 3 手指捏和距离计算
            dis = math.hypot((indexX-middleX),(indexY-middleY))
            # print(dis)
            cv.circle(image,(indexX,indexY),20,(0,0,200),2)
            # 4 手指捏合才走
            if dis<30:
                # 1 判断手指在方框上
                if ((indexX>box_x) and (indexX<box_x+box_size)) and ((indexY>box_y) and (indexY<box_y+box_size)):
                    # print("在")
                    if is_activate==False:
                        is_activate  = True
                        L1 = abs(indexX-box_x)
                        L2 = abs(indexY-box_y)
                else:
                    # print("不在")
                    pass
            # 5 不捏和不走
            else:
                is_activate = False
            # 2 手指带着方框走
            if is_activate:
                box_x = indexX-L1
                box_y = indexY-L2
    # 6 盒子透明
    overlay = image.copy()
    cv.rectangle(image,(box_x,box_y),(box_x+box_size,box_y+box_size),(0,200,0),-1)
    image = cv.addWeighted(overlay,0.5,image,0.5,0)
    cv.imshow("win1",cv.flip(image,1))


    code = cv.waitKey(1) & 0xFF

    if code ==27 or code ==113:
        break

cap.release()
cv.destroyAllWindows()