import numpy as np
import cv2 as cv



def nothing(x):
    pass

img = np.zeros(shape=(512,512,3),dtype=np.uint8)
window_name = "ColorChoosen"
cv.namedWindow(window_name,cv.WINDOW_NORMAL)

cv.createTrackbar("R",window_name,0,255,nothing)
cv.createTrackbar("G",window_name,0,255,nothing)
cv.createTrackbar("B",window_name,0,255,nothing)

switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch,window_name,0,1,nothing)

while(1):
    cv.imshow(window_name,img)
    key = cv.waitKey(1) & 0xff
    if key ==  27:
        break

    # get current positions of four trackbars
    r = cv.getTrackbarPos('R', window_name)
    g = cv.getTrackbarPos('G',window_name)
    b = cv.getTrackbarPos('B',window_name)
    s = cv.getTrackbarPos(switch,window_name)
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
 
cv.destroyAllWindows()


