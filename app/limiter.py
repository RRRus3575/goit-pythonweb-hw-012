from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware


limiter = Limiter(key_func=get_remote_address)


def exempt_health_checks(request: Request):
    return request.url.path == "/health"

limiter._request_filters.append(exempt_health_checks)


def rate_limit_exceeded_handler(request: Request, exc):
    error_message = "Too many requests"

    if isinstance(exc, RateLimitExceeded):
        error_message = exc.error_message
    
    else:
        error_message = str(exc)
    
    return JSONResponse(
        status_code=429,
        content={"error": f"Rate limit exceeded: {error_message}"}
    )

limiter.handler = rate_limit_exceeded_handler


def add_rate_limit_middleware(app):
    app.state.limiter = limiter  
    app.add_middleware(SlowAPIMiddleware)
