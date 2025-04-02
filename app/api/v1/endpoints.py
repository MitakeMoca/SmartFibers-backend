from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO

router = APIRouter()

# Load YOLOv8 model (you can change 'yolov8n.pt' to other model sizes)
model = YOLO("yolov8n.pt")

async def process_image(image_bytes: bytes):
    """Process image with YOLOv8 and return annotated image"""
    # Convert bytes to numpy array
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Run object detection
    results = model(image)

    # Get annotated image
    annotated_image = results[0].plot()

    # Convert back to bytes
    _, encoded_image = cv2.imencode(".jpg", annotated_image)
    return BytesIO(encoded_image.tobytes())

@router.post("/detect/")
async def handle_image(file: UploadFile = File(...)):
    """Handle image upload and return detection results"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image file
        image_bytes = await file.read()

        # Process image
        processed_image = await process_image(image_bytes)

        # Return processed image
        return StreamingResponse(processed_image, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
