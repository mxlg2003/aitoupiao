from fastapi import FastAPI, Request, Response, HTTPException
from db.session import SessionLocal
from core import router, config
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from public.logger import logger


__author__ = '吾延'
app = FastAPI(docs_url="/vote_docs", redoc_url='/vote_redoc')
app.include_router(router.api_router, prefix='/api')

# 对静态文件放行
app.mount("/media", StaticFiles(directory="media"), name="media")


# 设置允许跨域
app.add_middleware(CORSMiddleware, allow_origins=config.ALLOW_ORIGINS, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


# 自定义http异常
@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse({'code': exc.status_code, 'message': exc.detail})


# 自定义请求体验证错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.debug(exc.errors())
    return JSONResponse({'code': 404, 'message': exc.errors()})


@app.middleware('http')
async def session_middleware(request: Request, call_text):
    response = Response('请求页面不存在...',  status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_text(request)
    except Exception as e:
        logger.debug(e)
    finally:
        request.state.db.close()
    return response

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8088)
