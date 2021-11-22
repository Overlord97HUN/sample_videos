import cv2
import numpy as np
import glob
import time

########Find Chessboard Corners - objPoints and imgPoints ##############################################

chessboardSize = (7,5) # Hányszor hányas a kalibrációs papír (nem a mezők, hanem metszéspontok száma!!!)
frameSize = (640,480) # A képek felbontása

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001) #???

objp = np.zeros((chessboardSize[0]*chessboardSize[1],3),np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

objPoints = [] #3D pontok a valós térben
imgPoints = [] #2D pontok a képtérben

images = glob.glob('sample_images_checkerboard/*.jpg') # listába gyűjti a mappán belüli .jpg - fileokat

for image in images :
    print(image)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    cv2.imshow('img',img)
#    cv2.waitKey(0)

    ret, corners = cv2.findChessboardCorners(gray, chessboardSize,None)
    #print(corners)
    if ret == True:
        objPoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgPoints.append(corners)

        #nézzük meg mit találtunk a képeken:

        cv2.drawChessboardCorners(img,chessboardSize,corners2,ret)
        cv2.imshow('chessboard',img)
        cv2.waitKey(0)

cv2.destroyAllWindows()

######## Camera Calibration based on the sample images ############################################

ret, cameraMatrix,dist,rvecs, tvecs = cv2.calibrateCamera(objPoints,imgPoints,frameSize, None,None)

print('Camera Calibrated: ',ret)
print('\nCamera Matrix: \n: ',cameraMatrix)
print('\nDistortion Parameters:\n',dist)
print('\nRotation Vectors: \n',rvecs)
print('\nTranslation Vectors:\n',tvecs)

######## Undistortion #############################################################################

img = cv2.imread('sample_images_checkerboard/10.jpg')
h,w = img.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix,dist,(w,h),1,(w,h))

dst = cv2.undistort(img,cameraMatrix,dist, None,newCameraMatrix)

x,y,w,h = roi
dst = dst[y:y+h,x:x+w]
cv2.imwrite('undistorted/result1.jpg',dst)

##fejlszetés: a camera mátrixot elmenteni egy külső file-ba majd azt
##behívni a project python file-ba
