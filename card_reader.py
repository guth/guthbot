# https://builtin.com/data-science/python-ocr
# https://pypi.org/project/pytesseract/

from imutils.video import VideoStream
from PIL import Image
import cv2
import pytesseract
import numpy as np
import time

# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def camera_loop():
    video_stream = VideoStream(src=0).start()

    # Allow the camera or video file to warm up.
    time.sleep(3.0)  # Sleep for 3 seconds

    while True:
        # Grab the current frame
        frame = video_stream.read()

        if frame is None:
            print("Frame is None!")
            break

        norm_img = np.zeros((frame.shape[0], frame.shape[1]))
        frame = cv2.normalize(frame, norm_img, 0, 255, cv2.NORM_MINMAX)
        frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1]
        frame = cv2.GaussianBlur(frame, (1, 1), 0)

        # Try to find text
        frame_text = pytesseract.image_to_string(frame)
        print(f"Frame text: {frame_text}")

        # Show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # If the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

        pass


if __name__ == '__main__':
    # filename1 = "images/1_python-ocr.jpg"
    # image1 = np.array(Image.open(filename1))
    # text1 = pytesseract.image_to_string(image1)
    # print("text 1: " + text1)
    #
    # filename2 = "images/2_python-ocr.jpg"
    # image2 = np.array(Image.open(filename2))
    # text2 = pytesseract.image_to_string(image2)
    # print("text 2: " + text2)

    camera_loop()
