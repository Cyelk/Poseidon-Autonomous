import cv2
import numpy as np

def find_intersections(lines):
    """Find intersections between detected lines."""
    intersections = []
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines):
            if i >= j:  # Avoid duplicate pairs
                continue
            rho1, theta1 = line1[0]
            rho2, theta2 = line2[0]

            # Convert polar coordinates to line equations
            A = np.array([
                [np.cos(theta1), np.sin(theta1)],
                [np.cos(theta2), np.sin(theta2)]
            ])
            b = np.array([[rho1], [rho2]])

            # Solve for intersection point (x, y)
            try:
                point = np.linalg.solve(A, b)  # Solve Ax = b
                x, y = point.flatten()
                intersections.append((int(x), int(y)))  # Save integer coordinates
            except np.linalg.LinAlgError:
                pass  # Skip if lines are parallel
    return intersections

# Step 1: Load the CARLA image
image = cv2.imread("C:\\Users\\anast\\Documents\\opencvApp\\114773.png")
resized = cv2.resize(image, (640, 640))  # Ensure the image is 640x640

# Step 2: Apply color filtering to isolate road lane markings
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
lower_white = np.array([0, 0, 200])  # Define range for white (lane markings)
upper_white = np.array([255, 50, 255])
mask = cv2.inRange(hsv, lower_white, upper_white)  # Create mask for white colors
filtered = cv2.bitwise_and(resized, resized, mask=mask)

# Step 3: Detect edges on the filtered image
edges = cv2.Canny(mask, 50, 150)

# Step 4: Detect lines using Hough Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 120)  # Adjust threshold (120)

# Step 5: Draw lines on the original image
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green lines

# Step 6: Find and draw intersections
if lines is not None:
    intersections = find_intersections(lines)
    for x, y in intersections:
        if 0 <= x < 640 and 0 <= y < 640:  # Ensure intersections are within image bounds
            cv2.circle(resized, (x, y), 5, (0, 0, 255), -1)  # Red circles

# Step 7: Display the results
cv2.imshow("Original Image with Lines and Intersections", resized)
cv2.imshow("Filtered Image", filtered)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()




