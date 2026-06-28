import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio
from bot_aiogram.hendlers import router as hendlers_router
from database import init_telem

load_dotenv()
TOKEN = os.getenv("token")

dp = Dispatcher()
dp.include_routers(
    hendlers_router #роутер
)

async def main():
    bot = Bot(TOKEN)
    await init_telem()
    await dp.start_polling(bot) 
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")
