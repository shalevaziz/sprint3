import cv2 
import numpy as np
from PIL import Image
import time


def get_color(image):
    img = Image.fromarray(image)
    if img is None:
        return (-1, -1, -1)
    colors = img.getcolors()
    if colors is None:
        return (-1, -1, -1)
    max_color = sorted(colors, key=lambda x: x[0], reverse=True)[0][1]
    return max_color


def has_changes(color_1, color_2, threshold=10):
    
    diff_sum = 0
    
    for i in range(3):
        diff_sum += abs(color_1[i] - color_2[i])
    
    return diff_sum > threshold
    
    

def decrypt(images):
    colors = [get_color(image) for image in images]
    relevant = []
    for i in range(len(colors) - 1):
        if has_changes(colors[i], colors[i + 1]):
            relevant += [colors[i]]
    
    relevant = [np.argmax(color) for color in relevant]
    
    return relevant


# show camera feed
def show_camera_feed():
    images = []
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)
    start = time.time()
    while time.time() - start < 10:
        ret, frame = cap.read()
        cropped_frame = frame[530:550, 950:970]
        images += [cropped_frame]
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('frame.jpg', frame)
            break
    cap.release()

    cv2.destroyAllWindows()
    
    return images
    
images = show_camera_feed()
dec = decrypt(images)
print(dec)