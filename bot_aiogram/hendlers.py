from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from .keyboard import mode, melody
from database import create_telem
import aiohttp
import aiosqlite
from .state import cleanings
from aiogram.fsm.context import FSMContext


router = Router()
IP_WIFI = "http://fghfgerwhj"

async def send_command_to_robot(action: str):
        full_url = f"{IP_WIFI}/command?action={action}" 
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(full_url, timeout=5) as response:
                    if response.status == 200:
                        print(f"Команда '{action}' успешно отправлена, ответ: {await response.text()}")
                        return True
                    else:
                        print(f"Ошибка HTTP {response.status} при отправке команды '{action}'")
                        return False
        except aiohttp.ClientConnectorError:
            print(f"Ошибка: Робот по адресу {IP_WIFI} недоступен. Проверь Wi-Fi и питание.")
            return False
        
@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Это бот для дистанционого управления роботом! \n\n <b>Комманды</b> \n\n /Температура \n /УборкаПредметов\n /ВоспроизвестиМелодий\n Настройки \n /Статус", parseMode = "HTML")

@router.message(Command("Температура"))
async def temperatur(message: Message):
    #передача температуры
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT temperatura, humidity FROM telem ORDER BY id DESC LIMIT 1") as cursor:
            row = await cursor.fetchone() 
        
        if row:
            temperatura, humidity = row 
            await message.answer(
                f"Температура {temperatura} \n"
                f"Влажность {humidity}"
            )
        else:
            await message.answer("Вы еще не измеряли температуру")

@router.message(Command("УборкаПредметов"))
async def yborka(message: Message):
    await message.answer("Выберите режим ", reply_markup=mode)

@router.message(Command("ВоспроизведениеМелодий"))
async def melody(message: Message):
    await message.answer("Выберите мелодию которую хотите воспроизвести ", reply_markup=melody)

@router.message(Command("Настройки"))
async def temperatur(message: Message):
    await message.answer("Настройки")
    await message.answer("Ваш Wi-Fi:")

@router.message(Command("Статус"))
async def temperatur(message: Message):
    await message.answer("Статус")
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT temp, hum, status FROM telem ORDER BY id DESC LIMIT 1") as cursor:

            row = await cursor.fetchone() 
            
            if row:
                statuses = row 
                
                await message.answer(f" Статус: {statuses}")
            else:
                await message.answer("Вы еще не запускади бота")


#Обработка клавиатур
@router.callback_query(F.data == "mode_time")
async def mode_times(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите нужно время только число (в минутах)")
    await state.set_state(cleanings.time)


@router.message(cleanings.time)
async def mode_time_receive(message: Message, state: FSMContext):
    text = message.text
    if not text or not text.isdigit():
        await message.answer("Пожалуйста, введите только число (минуты).")
        return

    minuts = int(text)
    time = minuts * 60 * 1000  

    await send_command_to_robot(f"cleaning_time_{minuts}") 

    await create_telem(time_cleaning=time)

    await message.answer(f"Время уборки установлено: {minuts} минут.")
    await state.clear()


@router.callback_query(F.data == "mode1")
async def mode_times(callback: CallbackQuery):
    min = await callback.answer("Если захотите остановить робота то напишите команду /stop и робот выключится")
    await send_command_to_robot("cleaning")

@router.callback_query(F.data == "harrypotter")
async def mode_times(callback: CallbackQuery):
    await callback.answer("Воспроизведение начнется через 5 сек")
    await send_command_to_robot("harrypotter")

@router.callback_query(F.data == "imperio")
async def mode_times(callback: CallbackQuery):
    await callback.answer("Воспроизведение начнется через 5 сек")
    await send_command_to_robot("imperio")

@router.callback_query(F.data == "game")
async def mode_times(callback: CallbackQuery):
    await callback.answer("Воспроизведение начнется через 5 сек")
    await send_command_to_robot("game")

@router.callback_query(F.data == "birthday")
async def mode_times(callback: CallbackQuery):
    await callback.answer("Воспроизведение начнется через 5 сек")
    await send_command_to_robot("birthday")

@router.callback_query(F.data == "christmas")
async def mode_times(callback: CallbackQuery):
    await callback.answer("Воспроизведение начнется через 5 сек")
    await send_command_to_robot("christmas")