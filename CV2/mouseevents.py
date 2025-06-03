import numpy as np
import cv2 as cv

def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img,(x,y),50,(255,190,0),-1)
 


img= np.zeros(shape=(512,512,3),dtype=np.uint8)
cv.namedWindow("Random Picture",cv.WINDOW_NORMAL)
# cv.resizeWindow("Random Picture")
cv.setMouseCallback("Random Picture",draw_circle)


while True:
    cv.imshow("Random Picture",img)
    number = cv.waitKey(100)
    if number & 0xFF == 27: # ESC
        break
   
    if cv.getWindowProperty("Random Picture", cv.WND_PROP_VISIBLE) < 1:
        break

cv.destroyAllWindows()
