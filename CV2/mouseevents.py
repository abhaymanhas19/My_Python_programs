import numpy as np
import cv2 as cv

# def draw_circle(event,x,y,flags,param):
#     if event == cv.EVENT_LBUTTONDBLCLK:
#         cv.circle(img,(x,y),50,(255,190,0),-1)
 

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
 
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
 
    if event == cv.EVENT_LBUTTONDOWN: # : As soon as the user presses (clicks) the left mouse button anywhere over the window.
        print("yes")
        drawing = True
        ix,iy = x,y
 

    elif event == cv.EVENT_MOUSEMOVE: # Any time the mouse moves inside the window (regardless of whether a button is down).
        print("No")
        if drawing == True:
            if mode == True:
                cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv.circle(img,(x,y),5,(0,0,255),-1)
 
    elif event == cv.EVENT_LBUTTONUP: # As soon as the user releases the left mouse button.
        print("af")
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv.circle(img,(x,y),5,(0,0,255),-1)



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
