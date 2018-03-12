#import argparse
import imutils
import cv2
import numpy as np
import csv

cap = cv2.VideoCapture('IMG_7530.MOV')
frames = np.array([[0,0,0,0,0,0]])

## Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
## Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    def find_contours(lower, upper, color):
        ## Threshold the HSV frame to get only blue colors
        mask = cv2.inRange(hsv, lower, upper)
        # and threshold it
        #mask = [mask_blue,mask_green,mask_red,mask_yellow]
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        ## find contours in the thresholded frame
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        ## loop over the contours
        for c in cnts:
            ## compute the center of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                '''
                ## draw the contour and center of the shape on the frame
                if color==1:
                    cv2.drawContours(frame, [c], -1, (255, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                elif color==2:
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                elif color==3:
                    cv2.drawContours(frame, [c], -1, (0, 0, 255), 2)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                elif color==4:
                    cv2.drawContours(frame, [c], -1, (0, 200, 200), 2)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                '''
                return np.array([[cX,cY]])
        return np.array([[0,0]])

    if ret == True:

        ## Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ## define range of blue color in HSV
        lower_blue = np.array([80,90,115])
        upper_blue = np.array([105,255,255])

        ## define range of green color in HSV
        lower_green = np.array([60,100,80])
        upper_green = np.array([80,255,255])

        ## define range of red colo5r in HSV
        lower_red = np.array([140,80,110])
        upper_red = np.array([190,255,255])
        '''
        ## define range of yellow color in HSV
        lower_yellow = np.array([0,50,80])
        upper_yellow = np.array([45,255,255])
        '''
        ## find contours in each color
        conts_blue = find_contours(lower_blue,upper_blue, 1)
        conts_green = find_contours(lower_green,upper_green, 2)
        conts_red = find_contours(lower_red,upper_red, 3)
        #conts_yellow = find_contours(lower_yellow,upper_yellow, 4)
        
        ## add contour centers into array
        conts = np.concatenate((conts_blue,conts_green,conts_red),axis=1)
        frames = np.concatenate((frames,conts),axis=0)
        '''
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        
        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
    ## break the loop
    else: 
        break

## when everything done, release the video capture object
cap.release()
 
## closes all the frames     
cv2.destroyAllWindows()

## write contour centers for each frame to a csv file
with open('centers.csv', 'wb') as csvfile:
    center_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for t in frames:
        center_writer.writerow(t)