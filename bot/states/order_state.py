from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    service_type = State()    # Xizmat turi (Telegram bot yoki Veb-sayt)
    project_name = State()    # Loyiha nomi yoki g'oyasi
    description = State()     # Loyiha haqida batafsil tavsif
    budget = State()          # Taxminiy byudjet
    deadline = State()        # Bajarilish muddati
    contact = State()         # Aloqa ma'lumoti (telefon yoki username)
    confirmation = State()    # Buyurtmani tasdiqlash


class FeedbackState(StatesGroup):
    message = State()         # Adminga yuboriladigan xabar

