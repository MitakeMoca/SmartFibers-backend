from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from utils.ResultGenerator import ResultGenerator
from PIL import Image
import io

demo = APIRouter()


@demo.post("/handle")
async def handle_image(file: UploadFile = File(...)):
    # 读取上传的图片文件
    img_bytes = await file.read()

    # 使用 Pillow 打开图片
    image = Image.open(io.BytesIO(img_bytes))

    # 转换图片为灰度图
    grayscale_image = image.convert("L")

    # 保存灰度图到内存
    img_io = io.BytesIO()
    grayscale_image.save(img_io, format="PNG")
    img_io.seek(0)

    # 返回灰度图作为响应
    return StreamingResponse(img_io, media_type="image/png")
