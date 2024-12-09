def rectangles_intersect(rect1, rect2):
    # Rectangles defined as [x1, y1, x2, y2] (top-left and bottom-right corners)
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2

    # Check if rectangles overlap
    if x1 > x4 or x3 > x2 or y1 > y4 or y3 > y2:
        return False  # No intersection
    return True  # Intersection exists

rect1 = [0, 0, 3, 3]
rect2 = [2, 2, 5, 5]

if rectangles_intersect(rect1, rect2):
    print("Rectangles intersect.")
else:
    print("Rectangles do not intersect.")
