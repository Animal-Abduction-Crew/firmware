import cv2 # for object detection
from gpiozero import CPUTemperature # for getting CPU temp
import time # for timeouts
import numpy as np

# constants
CAM_ID = 0
LABELS = [
    "elephant",
    "tiger",
    "star",
    "cat",
    "frog"
]
CONFIG_PATH = "config.cfg"
WEIGHTS_PATH = "yolo.weights"
BUFFER_SIZE = 1
NETWORK_WIDTH = 192
NETWORK_HEIGHT = 128
MAX_CPU_TEMP = 70 # celsius
MIN_CONFIDENCE = 0.5
THRESHOLD = 0.4

def init_network(CONFIG_PATH, WEIGHTS_PATH):
    print('loading network')
    return cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)

net = init_network(CONFIG_PATH, WEIGHTS_PATH)

layer_names = net.getLayerNames()
layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def init_video_stream(cam_id, buffer_size, width, height):
    print('init video stream')
    video_stream = cv2.VideoCapture(cam_id)
    video_stream.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
    video_stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    video_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return video_stream

video_stream = init_video_stream(CAM_ID, BUFFER_SIZE, NETWORK_WIDTH, NETWORK_HEIGHT)

# init cpu temp momitor
print('init cpu monitor')
cpu = CPUTemperature()

# loop over the frames
print('start looping over frames')
while True:
    
    # <3 for the cpu
    while cpu.temperature > MAX_CPU_TEMP:
        print(f"{cpu.temperature} is too hot! cooling down...")
        time.sleep(0.1)
    
    print('get a frame from the camera')
    (grabbed, frame) = video_stream.read()

    # end of the stream
    if not grabbed:
        print('stream endend')
        break

    (W, H) = (None, None)

    # if the frame dimensions are empty, grab them
    if W is None or H is None:
        print('get the frame dimensions')
        (H, W) = frame.shape[:2]

    # let the network process the frame 
    print('let the network process the frame')                      
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (NETWORK_WIDTH, NETWORK_HEIGHT), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(layer_names)
    
    # initialize our lists of detected bounding boxes, confidences,
    # and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layer_outputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability)
            # of the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > MIN_CONFIDENCE:
                # scale the bounding box coordinates back relative to
                # the size of the image, keeping in mind that YOLO
                # actually returns the center (x, y)-coordinates of
                # the bounding box followed by the boxes' width and
                # height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top
                # and and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates,
                # confidences, and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping
    # bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, THRESHOLD)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # get the name and confidence
            name = LABELS[classIDs[i]]
            confidence = confidences[i]

            print(f"Found {name} with confidence {confidence} x: {x}, y: {y}, w: {w}, h: {h}")           
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('exited')
        break

# destroy video stream
print('cleaning up')
video_stream.release()