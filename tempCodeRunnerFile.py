import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Variables
width , height = int(1280) , int(720)
folderPath = "Presentation"

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#Get the list of images
pathImages = sorted(os.listdir(folderPath),key=len)


#Variables
imgNum = 0
hs ,ws = int(120*1),int(213*1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = -1
annotationStart = False
#Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

 
while True:
    # Importing Images
    success, img = cap.read()
    img = cv2.flip(img,1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNum])
    imgCurrent = cv2.imread(pathFullImage)
    hands , img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0, 255, 0),5)
 
    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx , cy = hand['center']
        lmlist = hand['lmList']

        #constraint values for easier drawing
        
        indexFinger =lmlist[8][0],lmlist[8][1]


        if cy <= gestureThreshold: #if hand is at the height of the face

            #gesture 1 - left
            if fingers == [1,0,0,0,0]:
                print("left")
                annotationStart = False
                if imgNum >0:
                    buttonPressed = True
                    imgNum -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    
            #gesture 2 - right
            if fingers == [0,0,0,0,1]:
                print("right")
                annotationStart = False
                if imgNum < len(pathImages)-1:
                    buttonPressed = True
                    imgNum +=1
                    annotations = [[]]
                    annotationNumber = -1
                     
        #gesture 3 - show pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED) 

        #gesture 4 - draw pointer
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber +=1
                annotations.append([])
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)                 
        else:
            annotationStart = False

        #gesture 5 - Erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop()
                annotationNumber -= 1
                buttonPressed = True
        #gesture 6 - quite
        # if fingers == [1, 1, 1, 1, 1]:
        #     break
            
    if buttonPressed is True:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)

    #adding webcam on the slides
    imageSmall = cv2.resize(img,(ws , hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imageSmall



    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break