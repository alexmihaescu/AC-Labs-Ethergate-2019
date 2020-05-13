import cv2
import imutils
import os 

faceCascade = cv2.CascadeClassifier("/home/cristina/Desktop/AC Labs/AC-Labs-Ethergate-2019/Sessions/Session 4/haarcascade_frontalface_default.xml")
output = "/home/cristina/Desktop/AC Labs/AC-Labs-Ethergate-2019/Sessions/Session 5/dataset"

video_capture = cv2.VideoCapture(0)

total = 0
while True:
    
    ret, frame = video_capture.read()
    orig = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 6, 
        minSize= (40,40)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(frame , (x,y), (x+w,y+h), (0,255,0),2)

    
    cv2.imshow('Face Detection', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        p = os.path.sep.join([output, "{}.png".format(str(total).zfill(3))])
        cv2.imwrite(p,orig)
        total +=1
    elif key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
