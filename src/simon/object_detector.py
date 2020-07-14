import cv2 # for object detection
from gpiozero import CPUTemperature # for getting CPU temp
import time # for timeouts
import numpy as np
import pigpio



# constants
CAM_ID = 0
LABELS = [
    "elephant",
    "tiger",
    "star",
    "cat",
    "frog"
]
CONFIG_PATH = "256x192-yolo-tiny-3l.cfg"
WEIGHTS_PATH = "256x192-yolo-tiny-3l_final.weights"
BUFFER_SIZE = 1
NETWORK_WIDTH = 256
NETWORK_HEIGHT = 192
MAX_CPU_TEMP = 70 # celsius
MIN_CONFIDENCE = 0.4
THRESHOLD = 0.4

# @pre pigpio demon must be running (sudo pigpiod)
# Hardware PWM available for GPIO 12, 13, 18, 19 (BCM scheme)
PWM_FREQUENCY = 50000

def initialize_pins(pi):
    for i in [14, 8, 15, 7]:
        pi.set_mode(i, pigpio.OUTPUT)

def drive(running_time, pi, power):
    PWM_DUTY_CYCLE = int(round(50 * power, 0))

    try:
        duty = PWM_DUTY_CYCLE * 10000 # Max: 1M
        for i in [18, 12]:
            pi.hardware_PWM(i, PWM_FREQUENCY, duty)
        running = True
    except:
        print('Hardware PWM not available on GPIO ')
        pi.stop()

    if running:
        time.sleep(running_time)
        for i in [18, 12]:
            pi.write(i, 0)
        pi.stop()

def brake():
    pi = pigpio.pi()
    initialize_pins(pi)

    for i in [14, 15, 7, 8]:
        pi.write(i, 1)
    
    drive(0.5, pi, 1)



def drive_straight(running_time, direction, power):
    pi = pigpio.pi()
    initialize_pins(pi)

    if direction == "forward":
        hi_low = [0, 1]
    elif direction == "reverse":
        hi_low = [1, 0]

    for i in [14, 8]:
        pi.write(i, hi_low[0])

    for i in [15, 7]:
        pi.write(i, hi_low[-1])

    drive(running_time, pi, power)
    brake()

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
def detect():
    start = time.time()

    # <3 for the cpu
    while cpu.temperature > MAX_CPU_TEMP:
        print(f"{cpu.temperature} is too hot! cooling down...")
        time.sleep(0.1)
    
    # print('get a frame from the camera')
    (grabbed, frame) = video_stream.read()

    # end of the stream
    if not grabbed:
        print('stream endend')

    (W, H) = (None, None)

    # if the frame dimensions are empty, grab them
    if W is None or H is None:
       # print('get the frame dimensions')
        (H, W) = frame.shape[:2]

    # rotate the frame because of the camera mount
    if frame is not None:
       # print('rotating frame')
        frame = cv2.rotate(frame, cv2.ROTATE_180)

    # let the network process the frame 
    # print('let the network process the frame')                      
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

        return idxs.flatten()

    print(f"took {time.time() - start} seconds")

    return None
    

drive_straight(2,"forward",0.8)

result = detect()

while result == None:
    drive_straight(2,"forward",0.8)
    result = detect()

while True:
    drive_straight(1, "forward", 0.2)
    drive_straight(1, "reverse", 0.2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('exited')
        break

# destroy video stream
print('cleaning up')
video_stream.release()