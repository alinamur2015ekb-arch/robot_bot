import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot_aiogram.hendlers import router as hendlers_router
from database import init_telem

load_dotenv()
TOKEN = os.getenv("token")

dp = Dispatcher()
dp.include_routers(hendlers_router)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get('PORT', '8000'))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"Health server on port {port}")
    server.serve_forever()


async def pinger():
    while True:
        await asyncio.sleep(60)
    
async def main():
    bot = Bot(TOKEN)
    await init_telem()
    
    Thread(target=run_health_server, daemon=True).start()
    
    asyncio.create_task(pinger())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
