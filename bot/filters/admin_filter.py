from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from bot.config import ADMIN_IDS


class IsAdminFilter(Filter):
    """Foydalanuvchi admin ekanligini tekshiruvchi filtr"""
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user_id = event.from_user.id if event.from_user else 0
        return user_id in ADMIN_IDS
