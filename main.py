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
    asyncio.create_task(pinger())
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):
        pass

def run_health_server():
    port_str = os.environ.get('PORT', '8000')
    try:
        port = int(port_str)
    except ValueError:
        print(f"Ошибка: PORT='{port_str}' не является числом. Используем порт 8000 по умолчанию.")
        port = 8000
    
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"HTTP Health Server запущен на порту {port}")
    httpd.serve_forever()

async def pinger():
    """Пингует сам себя, чтобы Render не «усыплял» сервис"""
    await asyncio.sleep(15) 
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                url = os.environ.get('RENDER_EXTERNAL_URL')
                if not url:
                    print("Предупреждение: не задана переменная RENDER_EXTERNAL_URL. Пинги могут не работать.")
                    url = f"http://localhost:{os.environ.get('PORT', '8000')}"
                
                async with session.get(url, timeout=10) as response:
                    print(f"Пинг выполнен! Статус: {response.status}")
            except Exception as e:
                print(f"Ошибка пинга: {e}")
            await asyncio.sleep(600)  

def handle_sigterm(signum, frame):
    print("Получен сигнал завершения (SIGTERM). Остановка...")
    sys.exit(0)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
        signal.signal(signal.SIGTERM, handle_sigterm)
        threading.Thread(target=run_health_server, daemon=True).start()
        time.sleep(2) 
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")
