from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)

def exempt_health_checks(request: Request):
    """Исключаем системные проверки из лимитирования запросов"""
    return request.url.path == "/health"

limiter.request_filter(exempt_health_checks)

def add_rate_limit_middleware(app):
    app.add_middleware(SlowAPIMiddleware)
