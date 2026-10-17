from .start import router as start_router
from .sections import router as sections_router
from .order import router as order_router
from .admin import router as admin_router
from .calculator import router as calculator_router

__all__ = [
    "start_router",
    "sections_router",
    "order_router",
    "admin_router",
    "calculator_router",
]
