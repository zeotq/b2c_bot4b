import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import user_data_save
import users_db
import keyboards
from manual_data_base_interaction import data_base


with open("token", "r") as f:
    TOKEN = f.readline()
    bot = Bot(TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

keyboard_main_menu = types.ReplyKeyboardMarkup(
    keyboard=keyboards.kb_main,
    resize_keyboard=True,
)
keyboard_admin = types.ReplyKeyboardMarkup(
    keyboard=keyboards.kb_admin,
    resize_keyboard=True,
)

class Form_order_reg(StatesGroup):
    adress = State()
    time = State()

help_info = "Помощь? Нет."
async def on_startup():
    print("Выполнен успешный запуск!", end = "\n\n\n")

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('<b>Добро пожаловать!</b>', parse_mode="HTML", reply_markup = keyboard_main_menu, allow_sending_without_reply=True)
    user_data_save.data_writer(dict(message.from_user))
    await message.delete()  

@dp.message_handler(commands=['menu'])
async def menu_command(message: types.Message):
    await message.reply(text = "/drone - для работы с дронами\n/help - получить помощь\n/close - закрыть меню", reply_markup = keyboard_main_menu, allow_sending_without_reply=True)
    await message.delete()

@dp.message_handler(commands=['zakaz'])
async def getstatus_command(message: types.Message):
    await message.answer('/place - оформить заказ\n/orders - ваши заказы\n/cancel - отменить заказ\n/close - закрыть меню', reply_markup = keyboard_dronedb, allow_sending_without_reply=True)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
   await message.reply(text=help_info)
   await message.delete()

class Form_Admin(StatesGroup):
    page_0 = State()
    page_2 = State()
    page_3 = State()

@dp.message_handler(commands=['admin'])
async def admin_page_0(message: types.Message):
    user = users_db.db_get_user_by_id(message.from_user.id)
    if user.isAdmin():
        await Form_Admin.page_0.set()
        await message.answer('<b>Открыта панель администратора</b>', parse_mode="HTML", reply_markup = keyboard_admin, allow_sending_without_reply=True)
    else:
        await message.reply(text="Недостаточно прав.")
        await message.delete()

@dp.message_handler(state=Form_Admin.page_0)
async def admin_page_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[0] = message.text
    await Form_Admin.next()
    await bot.send_message(message.from_user.id, text="Send ID",  reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form_Admin.page_2)
async def admin_page_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data[0] == "get_user_by_id":
            answer = users_db.db_get_user_by_id(message.text)
            data = answer.info()
            await bot.send_message(message.from_user.id, text=data)
            await state.finish()
        elif data[0] == "add_comment":
            await bot.send_message(message.from_user.id, text=users_db.db_get_user_by_id(message.text).getComments())
            data[1] = message.text
            await bot.send_message(message.from_user.id, text="Send comment:")
            await Form_Admin.next()
        elif data[0] == "set_trustfactor":
            data[1] = message.text
            await bot.send_message(message.from_user.id, text=users_db.db_get_user_by_id(data[1]).getTrustfactor())
            await bot.send_message(message.from_user.id, text="Send delta trust:")
            await Form_Admin.next()
        else:
            await bot.send_message(message.from_user.id, text="Wrong command")
            await state.finish()

@dp.message_handler(state=Form_Admin.page_3)
async def admin_page_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
         if data[0] == "add_comment":
            users_db.db_add_comment(data[1], message.text)
         else:
            users_db.db_set_trustfactor(data[1], int(message.text))
         await bot.send_message(message.from_user.id, text="Complete")
    await state.finish()

@dp.message_handler(state='*', commands=['close'])
async def close_menu_command(message: types.Message):
    msg = await message.reply(text='Открыть меню снова - /menu', reply_markup=types.ReplyKeyboardRemove())
    await message.delete()
    await asyncio.sleep(delay = 5)
    await msg.delete()

@dp.message_handler(commands=['id'])
async def get_id(message: types.Message):
    await bot.send_message(a:=message.from_user.id, text = a)

@dp.message_handler(commands=['place'])
async def palce_oreder(message: types.Message):
    await Form_order_reg.adress.set()
    await bot.send_message(message.from_user.id, text='Введите ваш адрес:',  reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['show_drone_db'])
async def show_drone_db(message: types.Message):
    await message.reply(text= f'{data_base(1)}')
    await message.delete()

@dp.message_handler(commands=['reset_drone_db'])
async def reset_drone_db(message: types.Message):
    msg = await message.reply(text= f'{data_base(2)}')
    await message.delete()
    await asyncio.sleep(delay = 2)
    await msg.delete()

@dp.message_handler(state=Form_order_reg.adress)
async def adress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text
    await bot.send_message(message.from_user.id, text='Введите время:')
    await Form_order_reg.next()

@dp.message_handler(state=Form_order_reg.time)
async def adress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await bot.send_message(message.from_user.id, text = f"Оформлен заказ на адрес: {data['adress']}, по номеру телефона {data['phone']}", reply_markup = keyboard_dronedb)
    #   В этом месте будет вызываться функция добавляющая заказ в базу данных. 
    await state.finish()

#   Любые некомандные сообщение в случае, когда state не обособлен будет отпраляться напрямую в личные сообщения модератора для анализа
@dp.message_handler()
async def backcall(message: types.Message):
    try:
        if message.from_user.id == 802558859:
            await message.answer(text = 'Admin_Profile')
        else:
            await message.answer(text = message.text.capitalize())
            await bot.send_message(802558859, f"{message.from_user.full_name} \ {message.from_user.id}: {message.text}")
    except:
        ...

#   Функция отправки сообщений пользователю непосредственно через userID
@dp.message_handler(state='*', commands=['send'])
async def send(message: types.Message):
    try:
        service_data = message.text.split(" ")
        format_message = message.text.replace(service_data[0]+" ", "").replace(service_data[1]+" ", "")
        await bot.send_message(service_data[1], f"{message.from_user.full_name} \ {message.from_user.id}: {format_message}")
    except:
        await message.answer(text = 'Ошибка отправки сообщения')

if __name__ == '__main__':
    executor.start_polling(dp)