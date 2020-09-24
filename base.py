import numpy as np
import cv2

"""
video_capture = cv2.VideoCapture(0) - default system default webcam. Uzima kameru sa kompa.Moze se staviti i vise kamera ili eksterna kamera. 

"""
video_capture = cv2.VideoCapture(0)  #
def change_resolution(width, heigh):
    video_capture.set(3, width)
    video_capture.set(4, heigh)


change_resolution(640, 480)

while(True):
    # Capture frame-by-frame from a video
    ret, frame = video_capture.read()
    # Display the resulting frame
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ako hocemo gray frame
    # cv2.imshow('gray',gray)
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'): #za gasenje prozora
        break
# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()