from components.object_detector import ObjectDetector

detector_settings = {
    "weights": "nets/256x192-yolo-tiny-3l_final.weights",
    "cfg": "nets/256x192-yolo-tiny-3l.cfg",
    "width": 256,
    "height": 192,
    "min_confidence": 0.5,
    "threshold": 0.4
}

detector = ObjectDetector(detector_settings)

while True:
    detector.detect()
