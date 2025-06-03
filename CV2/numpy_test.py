import numpy as np

# array = np.array([[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]])

# random arry creation
# array = np.zeros(shape=(1,2))

# print(help(np.zeros))
# print("array:",array)
# print(array[0][0])
# print(array[0][0,2])

# # array information 
# print("len of arrray:",len(array))
# print("dimension of array:",array.ndim)
# print("shape of array:",array.shape)



##################################################################################################################
# creating img and do alternation on image 
import cv2 as cv
import numpy as np

img = np.full(shape=(512,512,3),fill_value=150,dtype=np.uint8)
# cv.line(img,(0,0),(511,511),(255,0,0),10)

cv.rectangle(img=img,pt1=(150,150),pt2=(200,300),color=(0,255,0),thickness=3)

font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img=img,text='OpenCV',org=(10,500), fontFace=font, fontScale=6,color=(255,255,0),thickness=7)

cv.circle(img=img,center=(447,63), radius=50, color=(0,0,255),thickness= -1)
cv.imshow("Custom Image",img)
cv.waitKey(4000)
cv.destroyAllWindows()

