import cv2
import numpy as np
import time

sample_time = 10

cap = cv2.VideoCapture('sample_videos/checkerboard.avi')


frames = []

def image_processing (img):
    monochrome = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return monochrome

j = 0
font = cv2.FONT_HERSHEY_SIMPLEX
org = (20,50)
fontScale = 1
color = (255,0,0)
thickness = 2

while(cap.isOpened()):
    ret,frame = cap.read()
    if ret == True:
        j += 1
        image = image_processing(frame)
        cv2.putText(image,str(j),org,font,fontScale,color,thickness,cv2.LINE_AA)
        cv2.imshow('chechkerboard',image)
        frames.append(image)
        #time.sleep(0.2)
    if cv2.waitKey(1) == ord('q'):
        break

print(len(frames))
i = 0
for img in frames:
    i += 1
    if i <= 350 and i%sample_time == 0:
        cv2.imwrite('sample_images_checkerboard/'+str(i)+'.jpg',img)
print(frames[150].shape)


cap.release()
cv2.destroyAllWindows()
