import cv2

# Open camera
cap = cv2.VideoCapture(0)

# Check if camera opened
if not cap.isOpened():
    print("Camera not found!")
    exit()

# Variables for drawing
drawing = False
ix, iy = -1, -1

# Drawing canvas
canvas = None


# Mouse callback function
def draw(event, x, y, flags, param):
    global ix, iy, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(
                canvas,
                (ix, iy),
                (x, y),
                (0, 0, 255),
                5
            )
            ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(
            canvas,
            (ix, iy),
            (x, y),
            (0, 0, 255),
            5
        )


# Create window
cv2.namedWindow("Camera Drawing")
cv2.setMouseCallback("Camera Drawing", draw)


while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not found!")
        break

    # Flip camera like a mirror
    frame = cv2.flip(frame, 1)

    # Create canvas after getting camera frame
    if canvas is None:
        canvas = frame.copy()

    # Show drawing on camera
    output = cv2.addWeighted(frame, 1, canvas, 1, 0)

    cv2.imshow("Camera Drawing", output)

    key = cv2.waitKey(1) & 0xFF

    # Press C to clear drawing
    if key == ord('c'):
        canvas = frame.copy()

    # Press S to save drawing
    elif key == ord('s'):
        cv2.imwrite("my_drawing.jpg", output)
        print("Drawing saved!")

    # Press Q or ESC to quit
    elif key == ord('q') or key == 27:
        break


# Release camera
cap.release()
cv2.destroyAllWindows()