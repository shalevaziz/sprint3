
import cv2



if __name__ == '__main__':
    
    image = cv2.imread('frame.jpg')
    
    # crop the image in the middle: 20 by 20 pixels
    
    
    # Convert the image to grayscale
    gray = image[:, :, 2]
    
    # threshold the image
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    
    # show the thresholded image
    cv2.imshow('Thresholded Image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    # find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw the contours
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    
    # display the image
    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    