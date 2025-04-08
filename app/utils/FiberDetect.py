from ultralytics import YOLO

class FiberDetect:
    def __init__(self):
        self.model = YOLO('../train/train-YOLO8m_300_1280_flipud_1/weights/best.pt')
