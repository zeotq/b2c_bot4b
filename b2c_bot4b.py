﻿import asyncio
from random import choice
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import user_data_save
import users_db
import keyboards
from taxiuser import taxiuser

with open("token.txt", "r") as f:
    TOKEN = f.readline()
    bot = Bot(TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

class GlobalState(StatesGroup):
    main_menu = State()
class TaxiState(StatesGroup):
    service_reg = State()
    service_reg_main = State()
    service_reg_name = State()
    service_main = State()
class Form_Admin(StatesGroup):
    page_0 = State()
    page_2 = State()
    page_3 = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('<b>Добро пожаловать!</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_main_menu)
    user_data_save.data_writer(dict(message.from_user))
    await message.delete()
    await GlobalState.first()

@dp.message_handler(commands=['menu'], state = "*")
async def menu_command(message: types.Message):
    await message.answer('<b>Главное меню</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_main_menu)
    await message.delete()
    await GlobalState.first()

@dp.message_handler(commands=['help'], state = "*")
async def help_command(message: types.Message):
   await message.answer(text="/menu - открыть меню,\n/close - закрыть")
   await message.delete()

@dp.message_handler(commands=['id'], state = "*")
async def get_id(message: types.Message):
    await bot.send_message(a:=message.from_user.id, text = a)

@dp.message_handler(commands=['admin'], state = "*")
async def admin_page_0(message: types.Message):
    user = users_db.db_get_user_by_id(message.from_user.id)
    if user.isAdmin():
        await Form_Admin.page_0.set()
        await message.answer('<b>Открыта панель администратора</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_admin)
    else:
        await message.answer(text="Недостаточно прав.")
        await message.delete()

@dp.message_handler(commands=['exit', 'close'], state='*')
async def close_menu_command(message: types.Message):
    await message.answer(text='Главное меню', reply_markup = keyboards.keyboard_main_menu)
    await message.delete()
    await GlobalState.first()

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

@dp.message_handler(state=TaxiState.service_reg_main, content_types=types.ContentType.CONTACT)
async def taxi_reg_main(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
         user = data[message.from_user.id]
         user.update(phone_number=message.contact.phone_number)
         print(user.get_user_data())
         data[message.from_user.id] = user
         print(data[message.from_user.id].get_user_data())

@dp.message_handler(state=TaxiState.service_reg_main)
async def taxi_reg_main(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = data[message.from_user.id]
        print(user.get_user_data())
        if user.isFull():
            print("chtck_0")
            print(user.get_user_data())
            await message.answer(f'<b>Вы можете продожить или изменить данные</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_reg_finish)
        if message.text == "Имя":
            await TaxiState.service_reg_name.set()
            await message.answer("Введите имя:", reply_markup = types.ReplyKeyboardRemove())
        elif message.text == "Далее":
            print(user.get_user_data())
            if user.isFull():
                user.write_user()
                await message.answer(f'<b>Успешно!</b>\nИмя: {user.name}\nНомер телефона: {user.phone_number}', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_0)
                await state.finish()
                await TaxiState.service_main.set()
            else: pass
        print(data[message.from_user.id].get_user_data())

@dp.message_handler(state=TaxiState.service_reg)
async def taxi_reg_0(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Регистрация":
            user = taxiuser(message.from_user.id)
            data[message.from_user.id] = user
            if user.isFull():
                await message.answer(f'<b>Ваш аккаунт найден!</b>\nИмя: {user.name}\nНомер телефона: {user.phone_number}', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_reg_finish)
            else:
                await message.answer(f'<b>Укажите актуальные номер телефона и имя</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_reg)
            await TaxiState.service_reg_main.set()
            print(data[message.from_user.id].get_user_data())

@dp.message_handler(state=TaxiState.service_reg_name)
async def taxi_reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = data[message.from_user.id]
        user.update(name = message.text)
        data[message.from_user.id] = user
        await message.answer(f'Имя пользователя <b>{user.name}</b> сохранено', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_reg)
        await TaxiState.service_reg_main.set()
        print(data[message.from_user.id].get_user_data())

@dp.message_handler(state="*")
async def silkway(message: types.Message):
    text = message.text
    if text == "Заказ такси 🚖":
        await TaxiState.service_reg.set()
        await message.answer('<b>Сервис такси:</b>', parse_mode="HTML", reply_markup = keyboards.keyboard_taxi_0, allow_sending_without_reply=True)
    elif text == "Доставка еды 🥂":
        await TaxiState.service_reg.set()
    elif text == "Информация о проекте":
        pass
    elif text == "Закрыть":
        await message.answer(text='Открыть снова - /menu', reply_markup = types.ReplyKeyboardRemove())
        await message.delete()
        await asyncio.sleep(delay = 5)
    else:
        data = [
        "Я тебя не понял", "Команда не распознана", "Проверьте корректность сообщения", "Нет"
        ]
        await message.answer(text = choice(data))

if __name__ == '__main__':
    executor.start_polling(dp)