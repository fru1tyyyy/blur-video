import numpy as np
import cv2

vid = cv2.VideoCapture("video/traffic.mp4")
talking = cv2.VideoCapture("video/talking.mp4")
wm1 = cv2.imread("img/watermark1.png", cv2.IMREAD_UNCHANGED)
wm2 = cv2.imread("img/watermark2.png", cv2.IMREAD_UNCHANGED)
wm1 = cv2.resize(wm1, (1280, 720))
wm2 = cv2.resize(wm2, (1280, 720))
talking_active = True
out = cv2.VideoWriter("traffic.avi",
                      cv2.VideoWriter_fourcc(*"MJPG"),
                      30.0,
                      (1280, 720))

total_no_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)

vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
brightness_sum = 0
frame_check = 30
for i in range(frame_check):
    ret, temp_frame = vid.read()
    if not ret:
        break
    gray_temp = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2GRAY)
    brightness_sum += np.mean(gray_temp)

avg_brightness = brightness_sum / frame_check
print("Average brightness:", avg_brightness)
is_night = avg_brightness < 100
vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

face_cascade = cv2.CascadeClassifier("face_detector.xml")

for frame_count in range(0, int(total_no_frames)):
    success, frame = vid.read()
    if not success:
        break

    if is_night:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v + 50, 0, 255)
        final_hsv = cv2.merge((h, s, v))
        frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(face, (51, 51), 30)
        frame[y:y+h, x:x+w] = blur
        
    if talking_active:
        ret_talking, talking_frame = talking.read()
        if ret_talking:
            talking_frame = cv2.resize(talking_frame, (320, 180))
            frame[0:180, 0:320] = talking_frame
        else:
            talking_active = False
    
    current_wm = wm1 if talking_active else wm2
    frame = cv2.addWeighted(frame, 1.0, current_wm, 0.3, 0)
    
    out.write(frame)

vid.release()
talking.release()

end = cv2.VideoCapture("video/endscreen.mp4")

while True:
    ret_end, end_frame = end.read()
    if not ret_end:
        break
    
    end_frame = cv2.resize(end_frame, (1280, 720))
    out.write(end_frame)

end.release()
out.release()
cv2.destroyAllWindows()
print("Done")