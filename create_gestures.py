import cv2
import numpy as np
import os

image_x, image_y = 50, 50

cap = cv2.VideoCapture(0)
fbag = cv2.createBackgroundSubtractorMOG2()

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def main(g_id):
    total_pics = 1200
    cap = cv2.VideoCapture(0)
    x, y, w, h = 300, 50, 350, 350

    create_folder("C:\\Users\\SONY\\Desktop\\gestures_final\\" + str(g_id))
    pic_no = 0
    flag_start_capturing = False
    frames = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        ret, img = cap.read()
    
        cv2.rectangle(img, (300,300), (100,100), (0,255,0),0)
        crop_img = img[100:300, 100:300] 
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)


        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)


        _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        cv2.imshow('Thresholded', thresh1)

        (version, _, _) = cv2.__version__.split('.')

        if version == '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                   cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version == '4':
            contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                   cv2.CHAIN_APPROX_NONE)


        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 10000 and frames > 50:
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                pic_no += 1
                save_img = thresh1[y1:y1 + h1, x1:x1 + w1]
                if w1 > h1:
                    save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                elif h1 > w1:
                    save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                save_img = cv2.resize(save_img, (image_x, image_y))
                cv2.putText(frame, "Capturing...", (30, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (127, 255, 255))
                cv2.imwrite("C:\\Users\\SONY\\Desktop\\gestures_final\\" + str(g_id) + "/" + str(pic_no) + ".jpg", save_img)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, str(pic_no), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 127, 255))
        cv2.imshow("Capturing gesture", frame)
        cv2.imshow("thresh1", thresh1)
        keypress = cv2.waitKey(1)
        if keypress == ord('c'):
            if flag_start_capturing == False:
                flag_start_capturing = True
            else:
                flag_start_capturing = False
                frames = 0
        if flag_start_capturing == True:
            frames += 1
        if pic_no == total_pics:
            break


g_id = input("Enter gesture number: ")
main(g_id)

print("hi")
