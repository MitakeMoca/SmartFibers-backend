from fastapi import FastAPI
import uvicorn
from api.demo import demo

app = FastAPI()
app.include_router(demo, prefix="/demo", tags=['测试'])

if __name__ == '__main__':
	uvicorn.run('main:app', port = 8084, reload = True)