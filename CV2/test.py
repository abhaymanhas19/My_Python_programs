import cv2 as cv

# # Read img
# try:
#     img = cv.imread("email.png")
#     cv.imshow("window",img)

#     # wait key is the function that takes the time in milliseconds to show the image for specific time period.
#     cv.waitKey(10000)
#     # cv.destroyAllWindows()
# except Exception as e:
#     print("Failed with error:",str(e))


##############################################################
## working with videos



def capture_video():
    fourcc  = cv.VideoWriter_fourcc(*'mp4v') #  H.264, H.265, and VP9 most common video codec 
    output = cv.VideoWriter("output.mp4",fourcc,20.0,(640,480))

    codecs = [
        ('mp4v', 'output.mp4'),
        ('XVID', 'output.avi'),
        ('MJPG', 'output.avi')
    ]

    capture = cv.VideoCapture(0)
    while capture.isOpened():

        result , frame = capture.read()

        if not result:
            print("freame didn't capture//.")
            break

        output.write(frame) 
        cv.imshow("Recording",frame)

        # wait for a keyboard key presss for a millisecond 
        if cv.waitKey(1) == ord('q')  or cv.getWindowProperty('Recording', cv.WND_PROP_VISIBLE) < 1 :
            break


    capture.release()
    output.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
