import cv2
import time
import numpy as np
LST = [0,1,2,3,2,1,3,0]
WIDTH = 3400
HEIGHT = 2200
def create_image(color):
    image = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    if color == 3:
        return image
    image[:,:,color] = 255
    return image
   
def show(): 
    for i in LST:
        cv2.imshow('image', create_image(i))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1)

show()