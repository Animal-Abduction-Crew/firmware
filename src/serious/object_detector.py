import cv2 # for object detection
from gpiozero import CPUTemperature # for getting CPU temp
import time # for timeouts
import numpy as np
import pigpio
import queue
import threading

class ObjectDetector:

    MAX_CPU_TEMP = 70
    LABELS = [
        "elephant",
        "tiger",
        "star",
        "cat",
        "frog"
    ]

    def __init__(self, settings):

        self.NETWORK_HEIGHT = settings["height"]
        self.NETWORK_WIDTH = settings["width"]
        self.CONFIG_PATH = settings["cfg"]
        self.WEIGHTS_PATH = settings["weights"]
        self.MIN_CONFIDENCE = settings["min_confidence"]
        self.THRESHOLD = settings["threshold"]

        self.buffer = queue.Queue()

        print('loading network')
        self.net = cv2.dnn.readNetFromDarknet(self.CONFIG_PATH, self.WEIGHTS_PATH)
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        print('init video stream')
        self.stream = cv2.VideoCapture(0) # cam id is 0
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.NETWORK_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.NETWORK_HEIGHT)

        print('init frame graber')
        frame_graber_thread = threading.Thread(target=self._frame_reader)
        frame_graber_thread.daemon = True
        frame_graber_thread.start()

        print('init cpu monitor')
        self.cpu = CPUTemperature()

    def _protect_cpu(self):
        while self.cpu.temperature > self.MAX_CPU_TEMP:
            print(f"{cpu.temperature} is too hot! cooling down...")
            time.sleep(0.1)

    def _frame_reader(self):
        while True:
            ret, frame = self.stream.read()
            if not ret:
                break
            if not self.buffer.empty():
                try:
                    self.buffer.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.buffer.put(frame)

    def detect(self):
        start = time.time()

        # <3 for the cpu
        self._protect_cpu()
        
        # print('get a frame from the camera')
        frame = self.buffer.get()

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
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (self.NETWORK_WIDTH, self.NETWORK_HEIGHT), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.layer_names)
        
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
                if confidence > self.MIN_CONFIDENCE:
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
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.MIN_CONFIDENCE, self.THRESHOLD)

        # print(f"took {time.time() - start} seconds")

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping

            detections = []

            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # get the name and confidence
                name = self.LABELS[classIDs[i]]
                confidence = confidences[i]

                print(f"Found {name} with confidence {confidence} x: {x}, y: {y}, w: {w}, h: {h}")

                detections.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "name": name,
                    "confidence": confidence
                })

            return detections

        return None
