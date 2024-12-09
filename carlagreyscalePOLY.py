import cv2
import numpy as np
import os

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

def draw_tangents(image, curve_points):
    """Fit a curve to the road and draw tangents."""
    # Fit a polynomial to the curve points
    curve_points = np.array(curve_points)
    x = curve_points[:, 0]
    y = curve_points[:, 1]
    poly_coeffs = np.polyfit(x, y, 2)  # Fit a quadratic curve (2nd-degree polynomial)
    poly = np.poly1d(poly_coeffs)

    # Draw the curve on the image
    for i in range(min(x), max(x)):
        y_curve = int(poly(i))
        if 0 <= y_curve < image.shape[0]:
            image[y_curve, i] = [255, 0, 255]  # Magenta curve

    # Compute tangents at the midpoints and endpoints
    tangent_points = [x[0], x[len(x) // 2], x[-1]]
    for xi in tangent_points:
        yi = poly(xi)
        dydx = np.polyder(poly)(xi)  # First derivative gives the tangent slope

        # Tangent direction: (dx, dy) for a small dx
        dx = 50
        dy = int(dydx * dx)

        # Tangent line endpoints
        pt1 = (int(xi), int(yi))
        pt2 = (int(xi + dx), int(yi + dy))
        pt3 = (int(xi - dx), int(yi - dy))

        cv2.line(image, pt1, pt2, (0, 255, 255), 2)  # Yellow tangent line
        cv2.line(image, pt1, pt3, (0, 255, 255), 2)

# Step 1: Load the CARLA image
image_path = r"C:\Users\anast\Documents\opencvApp\118015.png"  # Update this path with the correct file
if not os.path.exists(image_path):
    print(f"Error: The file {image_path} does not exist. Please check the path.")
    exit()

image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not load image from {image_path}. Please check the file format.")
    exit()

resized = cv2.resize(image, (640, 640))  # Ensure the image is 640x640

# Step 2: Convert the image to grayscale
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Step 3: Detect edges
edges = cv2.Canny(gray, 50, 150)

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

# Step 6: Detect contours to approximate the road curve
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    if len(contour) > 10:  # Ignore small contours
        curve_points = contour.squeeze().tolist()
        draw_tangents(resized, curve_points)

# Step 7: Define the output directory
output_dir = r"C:\Users\anast\Documents\opencvApp\output"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Step 8: Save the processed images using the image number
image_number = os.path.splitext(os.path.basename(image_path))[0]  # Extract the image number
output_image_path = os.path.join(output_dir, f"curves_and_tangents_{image_number}.png")
output_edges_path = os.path.join(output_dir, f"edges_{image_number}.png")

cv2.imwrite(output_image_path, resized)  # Save the image with curves and tangents
cv2.imwrite(output_edges_path, edges)  # Save the edge-detected image

# Step 9: Display the results
cv2.imshow("Curves and Tangents", resized)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
