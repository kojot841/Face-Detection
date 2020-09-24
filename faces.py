import numpy as np
import cv2
import pickle 

face_cascade = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_smile.xml')
glasses = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_eye_tree_eyeglasses.xml')
upper_body = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_upperbody.xml')
profile_face = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_profileface.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")  #ovo je nas training data

labels = {"person_name": 1} #ID svake osobe
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

def change_resolution(width, heigh):
    cap.set(3, width)
    cap.set(4, heigh)

change_resolution(640, 480)

while(True):
    ret, frame = cap.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #ako je veci skale factor, vise od 1 bude malo tacnije ali ne valja mnogo da bude vise od 1.5
													# isto vazi i za minNeighbors

    for (x, y, w, h) in faces:
    	roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end) #Region of Interest
    	roi_color = frame[y:y+h, x:x+w]  #koordinate visina i sirina

    	id_, conf = recognizer.predict(roi_gray)  #ovde radimo predictions
    	if conf>=1 and conf <= 80:
    		# print(5: #id_)
    		# print(labels[id_])
    		font = cv2.FONT_HERSHEY_TRIPLEX
    		person_name = labels[id_]
    		color = (255, 255, 255)
    		stroke = 1
    		cv2.putText(frame, person_name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

		#Recognize who this is? deep learning?
    	# img_item = "slika.png" #tu treba da bude random ime fajla, #cuva sliku (samo facu) kao png file
						#U ovaj deo moze da se ubaci da sacuva sliku i datum i bazu podataka tako da znamo kada je osoba dosla na posao
    					# recognize? deep learned model predict keras tensorflow pytorch scikit learn
    	# cv2.imwrite(img_item, roi_color)



    	color = (0,255,0) #BGR 0-255
    	stroke = 3
    	end_cord_x = x + w
    	end_cord_y = y + h
		# Crtamo trougao oko slike, definisimeo boju i stroke(debljinu linija trougla)
    	cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #pocetne kooordinate, visina i sirina trougla, kao i zavrsne koordinate
    	# eyes = eye_cascade.detectMultiScale(roi_gray)
    	prof_face = profile_face.detectMultiScale(roi_gray)
		# prof_face = profile_face.detectMultiScale(roi_gray)
    	for (ex,ey,ew,eh) in prof_face:
    		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


# Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
    	break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

def name(person_name):
	