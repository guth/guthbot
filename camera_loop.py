# This code runs in the GoPiGo Jupyter notebook.

from ipywidgets import widgets, Layout
import easygopigo3 as easy
from time import sleep

import cv2
import numpy as np
from IPython.display import Image, display
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera

my_gpg3 = easy.EasyGoPiGo3()

darkgrey = '#888888'
items_layout = Layout(flex='1 1 auto',
                      width='auto')  # override the default width of the button to 'auto' to let the button grow

box_layout = Layout(display='flex',
                    flex_flow='column',
                    align_items='stretch',
                    border='solid',
                    width='30%')

def on_forward_clicked(b):
    my_gpg3.forward()

def on_backward_clicked(b):
    my_gpg3.backward()

def on_stop_clicked(b):
    my_gpg3.stop()

def on_left_clicked(b):
    my_gpg3.left()

def on_right_clicked(b):
    my_gpg3.right()


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))


def on_stop_loop_clicked(b):
    mode = "STOP"

def on_start_loop_clicked(b):
    print("Start loop clicked")
    mode = "CAMERA"

    while True:
        if mode == "CAMERA":

            rawCapture.truncate(0)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array

                # TODO: Better image preprocessing. Some of this helped, sometimes.
                # norm_img = np.zeros((image.shape[0], image.shape[1]))
                # image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
                # image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
                # image = cv2.GaussianBlur(image, (1, 1), 0)

                frame_text = pytesseract.image_to_string(image)

                if frame_text is not None and len(frame_text) > 0:
                    frame_text = frame_text.lower()
                    print(f'Frame text: {frame_text}')

                    if "hello" in frame_text or "drive" in frame_text:
                        mode = "DRIVE"
                    elif "right" in frame_text:
                        mode = "RIGHT"
                    elif "left" in frame_text:
                        mode = "LEFT"
                    elif "stop" in frame_text:
                        mode = "STOP"

                    if mode != "CAMERA":
                        break

                # print("camera image:")
                # _, image = cv2.imencode('.jpeg', image)
                # display(Image(data=image))

                rawCapture.truncate(0)
        elif mode == "DRIVE":
            my_gpg3.forward()
            sleep(1)
            my_gpg3.stop()
            mode = "CAMERA"
        elif mode == "RIGHT":
            my_gpg3.right()
            sleep(1)
            my_gpg3.stop()
            mode = "CAMERA"
        elif mode == "LEFT":
            my_gpg3.left()
            sleep(1)
            my_gpg3.stop()
            mode = "CAMERA"
        else:  # mode == "STOP"
            my_gpg3.stop()
            camera.stop_preview()
            camera.close()


buttons = []
descriptions = ["Go Forward", "Left", "STOP", "Right", "Go Backward", "Start Loop", "STOP Loop"]
callbacks = [on_forward_clicked, on_left_clicked, on_stop_clicked, on_right_clicked, on_backward_clicked,
             on_start_loop_clicked, on_stop_loop_clicked]
for i in range(7):
    buttons.append(widgets.Button(description=descriptions[i], layout=items_layout))
    buttons[i].style.button_color = darkgrey
    buttons[i].on_click(callbacks[i])

buttons[2].style.button_color = 'red'  # stop button
buttons[6].style.button_color = 'red'  # stop loop button

mid_row = widgets.HBox([buttons[1], buttons[2], buttons[3]])
display(widgets.VBox([buttons[0], mid_row, buttons[4], buttons[5], buttons[6]], layout=box_layout))