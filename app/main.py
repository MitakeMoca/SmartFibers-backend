from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.demo import demo

app = FastAPI()
app.include_router(demo, prefix="/demo", tags=['测试'])


origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"]
)


if __name__ == '__main__':
	uvicorn.run('main:app', port = 8084, reload = True)