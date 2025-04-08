from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from ultralytics import YOLO
import io
import asyncio
from pathlib import Path

demo = APIRouter()

BASE_DIR = Path(__file__).parent.parent
model_path = BASE_DIR / "train-YOLO8m_300_1280_flipud_1" / "weights" / "best.pt"
print(model_path)

# 加载模型
model = YOLO(str(model_path))


@demo.post("/predict")
async def handle_image(file: UploadFile = File(...)):
    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        None,  # 使用默认线程池
        lambda: model(image)  # 直接调用模型进行预测
    )

    # 提取结果并绘制检测框
    result = results[0]
    plotted_img_array = result.plot()  # 获取带标注的numpy数组（BGR格式）

    # 将BGR转换为RGB并生成Pillow图像
    plotted_img = Image.fromarray(plotted_img_array[..., ::-1])  # BGR转RGB

    # 将图像保存到内存字节流
    img_io = io.BytesIO()
    plotted_img.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")