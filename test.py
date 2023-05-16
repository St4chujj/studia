from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data\haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)
print('Shape of Faces matrix --> ', FACES.shape)
print('Shape of Faces matrix --> ', LABELS.shape)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)



while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        #cropowanie zdjecia do formatu RGB
        crop_img=frame[y:y+h, x:x+w, :]
        #robienie do wektorów
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)
        #output=knn.predict(resized_img)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255))
        #tworzenie obramówki
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
    cv2.imshow("FRAME", frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()

