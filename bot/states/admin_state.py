from aiogram.fsm.state import State, StatesGroup


class BroadcastState(StatesGroup):
    message = State()         # Tarqatiladigan xabar
    confirmation = State()    # Yuborishni tasdiqlash


class AddPortfolioState(StatesGroup):
    title = State()           # Loyiha nomi
    category = State()        # Toifasi (bot / website)
    description = State()     # Loyiha haqida tavsif
    link = State()            # Havolasi (link)
    photo = State()           # Rasmi (ixtiyoriy)


class AdminReplyState(StatesGroup):
    target_user_id = State()  # Qaysi foydalanuvchiga
    message = State()         # Javob xabari

