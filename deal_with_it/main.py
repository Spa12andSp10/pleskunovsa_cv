import cv2

image = cv2.imread("deal-with-it.png", cv2.IMREAD_UNCHANGED)

if image.shape[2] == 4:
    image_rgb = image[:, :, :3]
    image_alpha = image[:, :, 3]
else:
    raise ValueError("Error")

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")

while capture.isOpened():
    ret, frame = capture.read()

    key = chr(cv2.waitKey(1) & 0xFF)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3)

        if len(eyes) >= 2:
            (ex1, ey1, ew1, eh1) = eyes[0]
            (ex2, ey2, ew2, eh2) = eyes[1]

            xw = ex1 + ew1 // 2
            xw2 = ex2 + ew2 // 2
            yh = ey1 + eh1 // 2
            yh2 = ey2 + eh2 // 2

            center_x = (xw + xw2) // 2
            center_y = (yh + yh2) // 2

            eye_distance = abs(xw - xw2)
            if eye_distance < 10:
                continue

            glass_width = int(eye_distance * 2)
            glass_height = int(glass_width * image.shape[0] / image.shape[1])

            glass_x = center_x - glass_width // 2
            glass_y = center_y - glass_height // 2

            gx = max(0, glass_x)
            gy = max(0, glass_y)
            gx2 = min(roi_color.shape[1], gx + glass_width)
            gy2 = min(roi_color.shape[0], gy + glass_height)

            width = gx2 - gx
            height = gy2 - gy
            if width <= 0 or height <= 0:
                continue

            resized_glass = cv2.resize(image_rgb, (width, height))
            alpha = cv2.resize(image_alpha, (width, height))

            a = alpha / 255

            for i in range(0, 3):
                roi_color[gy:gy2, gx:gx2, i] = (a * resized_glass[:, :, i] +(1 - a) * roi_color[gy:gy2, gx:gx2, i])

    if key == "q":
        break
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()