import cv2
import os
import numpy as np
from PIL import Image #pill je python image library
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # direktorijum gde se fajl nalazi,
image_dir = os.path.join(BASE_DIR, "images") #direktorijum gde su slike, images folder

face_cascade = cv2.CascadeClassifier('OpenCV_folder/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()  #Koristio sam LBPHF Recognizier ali moze se koristit i bilo koji

current_id = 0
label_ids = {}
y_labels = [] #sadrzi sve labels
x_train = []  #lista sadrzi brojeve piksela

for root, dirs, files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"): #trazi sve jpg i png fajlove
			path = os.path.join(root, file)
			label = os.path.basename(root).replace(" ", "-").lower() #uzima naziv foldera, zato im dajem naziv po imenu, ako ima space onda dodajemo crtu
			#print(label, path)
			if not label in label_ids: #dodajemo ID svakom label-u i dodajemo ga u dictionary
				label_ids[label] = current_id
				current_id += 1
			id_ = label_ids[label]
			#print(label_ids)
			#y_labels.append(label) # some number
			#x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
			pil_image = Image.open(path).convert("L") # grayscale L znaci da je pretvorimo u grayscale, ovom komandom otvaramo sliku
			size = (550, 550)
			final_image = pil_image.resize(size, Image.ANTIALIAS) # da resize odradimo kako bi tacniji model bio. Mada ovo ne mora ako su slike koje imamo dobre rezolucije, sve slike koje imamo bi trebalo da su iste ili slicne velicine
			image_array = np.array(final_image, "uint8") #uzima sliku i pretvara je u numpy array. Uzima svaki piksel sa slike i pretvara ga u niz
			# na ovome zelimo da treniramo nas model.

			# print(image_array)
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

			for (x,y,w,h) in faces:
				roi = image_array[y:y+h, x:x+w] #region of interest
				x_train.append(roi)
				y_labels.append(id_)


# print(y_labels)
# print(x_train)
#USe pickle to save lavbel ids to that we can use it in faces.py
with open("pickles/face-labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels)) #dodaju se 2 parametra: Image arrrays i labels array koji smo konvertovali u numpy array
recognizer.save("recognizers/face-trainner.yml")