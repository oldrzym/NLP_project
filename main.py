from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json

from app.schemas import MaskRequestModel
from app.masking import apply_masking

from pullenti.Sdk import Sdk
Sdk.initialize_all()

app = FastAPI(title="Сервис маскирования данных")

class EscapeBackslashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get('Content-Type') == 'application/json':
            body = await request.body()
            try:
                # Пытаемся исправить неправильное экранирование перед декодированием JSON
                data = body.decode("utf-8").replace("\\", "\\\\")
                # Переписываем тело запроса исправленными данными
                request._body = data.encode("utf-8")
            except json.JSONDecodeError:
                return JSONResponse(status_code=400, content={"detail": "Invalid JSON format"})
        response = await call_next(request)
        return response

# Добавляем Middleware в приложение
app.add_middleware(EscapeBackslashMiddleware)

@app.post("/mask/", response_model=MaskRequestModel)
async def mask(request_model: MaskRequestModel):
    """
    Асинхронная функция для обработки HTTP POST запросов для маскирования данных.

    Args:
        request_model (MaskRequestModel): Модель данных запроса, содержащая текст для маскирования.

    Returns:
        JSONResponse: Ответ сервера с маскированными данными и статусом 200 в случае успеха.
    
    Raises:
        HTTPException: Исключение с кодом 500 и описанием ошибки, если произошла ошибка в процессе маскирования.
    """
    try:
        masked_data = apply_masking(request_model.text)
        return JSONResponse(content={"masked_data": masked_data}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
