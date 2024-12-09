import cv2
import numpy as np

# Create a blank image with zeros
image = np.zeros((512, 512, 3), np.uint8)

# Draw a green line
cv2.line(image, (0, 0), (511, 511), (0, 255, 0), 5)

# Draw a red rectangle
cv2.rectangle(image, (384, 0), (510, 128), (0, 0, 255), 3)

# Draw a blue circle
cv2.circle(image, (447, 63), 63, (255, 0, 0), -1)

# Display the image
cv2.imshow('Image', image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()




