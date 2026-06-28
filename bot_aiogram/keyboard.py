from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


mode = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="По времени", callback_data="mode_time")],
        [InlineKeyboardButton(text="По ручной остановке", callback_data="mode1")]
    ]
)

melody = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Harry Potter", callback_data="harrypotter")],
        [InlineKeyboardButton(text="Имперский марш", callback_data="imperio")],
        [InlineKeyboardButton(text="Игра Пристолов", callback_data="game")],
        [InlineKeyboardButton(text="Happy birthday", callback_data="birthday")],
        [InlineKeyboardButton(text="Merry christmas", callback_data="christmas")]
    ]
)