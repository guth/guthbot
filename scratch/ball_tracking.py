from collections import deque
from imutils.video import VideoStream
import numpy
import argparse
import cv2
import imutils
import time

# Sample video path:
# --video C:\Users\guthr\Desktop\git\guthbot\videos\TestVideo.mp4
MINIMUM_RADIUS = 10

# construct the argument parse and parse the arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-v", "--video", help="path to the (optional) video file")
argument_parser.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(argument_parser.parse_args())

# Define the lower and upper boundaries of the "green" ball
# in the HSV color space.
green_lower = (29, 86, 6)
green_upper = (64, 255, 255)

# Initialize the list of tracked points.
points = deque(maxlen=args["buffer"])

if not args.get("video", False):
    # If a video path was not supplied, grab the reference to the webcam.
    video_stream = VideoStream(src=0).start()
else:
    # Otherwise, grab a reference to the video file.
    video_stream = cv2.VideoCapture(args["video"])

# Allow the camera or video file to warm up.
time.sleep(3.0)  # Sleep for 3 seconds

while True:
    # Grab the current frame
    frame = video_stream.read()

    # Handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # If we are viewing a video and we did not grab a frame,
    # then we've reached the end of the video and we're done.
    if frame is None:
        break

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small blobs
    # left in the mask
    mask = cv2.inRange(hsv, green_lower, green_upper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Find the contours in the mask and initialize the current
    # (x, y) center of the ball
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Only proceed if at least one contour was found.
    center = None
    if len(contours) > 0:
        # Find the largest contour in the mask, then use it to
        # compute the minimum enclosing circle and centroid.
        c = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius meets a minimum size
        if radius > MINIMUM_RADIUS:
            # Draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Update the points list
    points.appendleft(center)

    # Loop over the set of tracked points
    for i in range(1, len(points)):
        # If either of the tracked points are None, ignore them
        if points[i - 1] is None or points[i] is None:
            continue

        # Compute the thickness of the line and draw the connecting line
        thickness = int(numpy.sqrt(args["buffer"] / (i + 1)) * 2.5)
        cv2.line(frame, points[i - 1], points[i], (0, 0, 255), thickness)

    # Show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

if not args.get("video", False):
    # If we are not using a video file, stop the camera video stream
    video_stream.stop()
else:
    # Otherwise, release the camera
    video_stream.release()

# Close all windows
cv2.destroyAllWindows()

print("Hello, world!")

