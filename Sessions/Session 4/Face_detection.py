import cv2

faceCascade = cv2.CascadeClassifier("/home/cristina/Desktop/AC Labs/AC-Labs-Ethergate-2019/Sessions/Session 4/haarcascade_frontalface_default.xml")

video_capture = cv2.VideoCapture(0)


while True:
    
    ret, frame = video_capture.read()

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

    if cv2.waitKey(1) == 27: # ESC
        break  


video_capture.release()
cv2.destroyAllWindows()
