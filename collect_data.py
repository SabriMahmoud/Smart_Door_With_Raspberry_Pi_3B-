import cv2

name = 'Amine' 

cam = cv2.VideoCapture(2)

cv2.namedWindow("press space to capture a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to capture a photo", 1000, 1000)
print("Press Echape to end the process")
img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture")
        break
    cv2.imshow("press space to capture a photo", frame)
    

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
