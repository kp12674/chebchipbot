# -*- coding: utf-8 -*-
import aiogram, re, traceback, random, json, datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
# Local imports
from configuration import config
from filters import IsPrivate
from keyboard import menu, admin
from data.csdb import *
from states.main_states import *

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(IsPrivate(), commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    user = await get_user(message.from_user.id)
    if user is None:
        await register_user(message.from_id, message.from_user.username, message.from_user.first_name)
        await message.answer_photo(photo=open('photo/Main.jpg', 'rb'), caption=f"⠀\n<b>👋  Привет, {message.from_user.first_name}</b>\n⠀", reply_markup=await menu.MainKey())
    else:
        await message.answer_photo(photo=open('photo/Main.jpg', 'rb'), caption=f"⠀\n<b>👋  Привет, {message.from_user.first_name}</b>\n⠀", reply_markup=await menu.MainKey())
    

@dp.callback_query_handler(text="BackKeyMain", state="*")
async def BackKeyMain(call: CallbackQuery, state: FSMContext):
    await state.finish()
    message = call.message
    await message.edit_caption(caption=f"⠀\n<b>👋  Привет, {message.chat.first_name}</b>\n⠀", reply_markup=await menu.MainKey())
    

@dp.callback_query_handler(lambda call: call.data.startswith("BackKeyDMain"), state="*")
async def BackKeyDMain(call: CallbackQuery, state: FSMContext):
    message = call.message
    y = int(call.data.split("BackKeyDMain|")[1])
    await message.delete()
    for i in range(1, y+1):
        await bot.delete_message(message.chat.id, message.message_id-i)
    await message.answer_photo(photo=open('photo/Main.jpg', 'rb'), caption=f"⠀\n<b>👋  Привет, {message.chat.first_name}</b>\n⠀", reply_markup=await menu.MainKey())
    

@dp.callback_query_handler(text="alllist", state="*")
async def listrep(call: CallbackQuery, state: FSMContext):
    await state.finish()
    message = call.message
    check = await checkalllist()
    if check == 0:
        await call.answer(f"У вас нет записей  ❌")
    else:
        await message.edit_caption(caption=f"⠀\n<b>🗓  Выберите день ↷</b>\n⠀",
                                   reply_markup=await menu.MenuAlllist())
    

@dp.callback_query_handler(lambda call: call.data.startswith("selectonthisdayreps"), state="*")
async def selectonthisdayreps(call: CallbackQuery, state: FSMContext):
    message = call.message
    day = call.data.split("selectonthisdayreps|")[1]
    listallrep = await getalllistrepsthisday(day)
    text = "<b>🗓 Записи на этот день ↷</b>\n\n"
    for data in listallrep:
        text += f"Время: {data[1]} число {data[2]}\nРабота: {data[3]}\nСтоимость: {data[6]}\nНомер: <code>{data[5]}</code>\nВремя работы: {data[4]}\n\n"
    if len(text) > 1024:
        await message.delete()
        y = 0
        for x in range(0, len(text), 4096):
            y += 1
            await message.answer(text="<b>" + text[x:x + 4096] + "</b>")
        await message.answer("Back", reply_markup=await menu.BackKeyMD(y))
    else:
        await message.edit_caption(caption=text, reply_markup=await menu.BacDkKeyM())
    

@dp.callback_query_handler(lambda call: call.data.startswith("thisdayreplistnext"), state="*")
async def thisdayreplistnext(call: CallbackQuery, state: FSMContext):
    message = call.message
    text = call.data.split("thisdayreplistnext|")[1]
    page = text.split("|")[0]
    day = text.split("|")[1]
    await message.edit_caption(caption=f"<b>🗓 Записи на этот день ↷</b>", reply_markup=await menu.getlistallrepsday(page=int(page), day=int(day)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("thisdayreplistback"), state="*")
async def thisdayreplistback(call: CallbackQuery, state: FSMContext):
    message = call.message
    text = call.data.split("thisdayreplistback|")[1]
    page = text.split("|")[0]
    day = text.split("|")[1]
    await message.edit_caption(caption=f"<b>🗓 Записи на этот день ↷</b>", reply_markup=await menu.getlistallrepsday(page=int(page), day=int(day)))
    

# @dp.callback_query_handler(lambda call: call.data.startswith("selectthisdayrep"), state="*")
# async def selectthisdayrep(call: CallbackQuery, state: FSMContext):
#     message = call.message
#     rep = call.data.split("selectthisdayrep|")[1]
#     data = await getthisrepontheday(rep)
#     await message.edit_caption(caption=f"⠀\n<b>Время: {data[1]} число {data[2]}\nРабота: {data[3]}\nСтоимость: {data[6]}\nНомер: <code>{data[5]}</code>\nВремя работы: {data[4]}</b>\n⠀", reply_markup=await menu.getlistallrepsday(day=int(data[1])))







@dp.callback_query_handler(text="delrep", state="*")
async def delrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    check = await checkalllist()
    if check == 0:
        await call.answer(f"У вас нет записей  ❌")
    else:
        await message.edit_caption(caption=f"<b>⚙️ Удаление записи ↷</b>",
                               reply_markup=await menu.MenudelAlllistrep())
    

@dp.callback_query_handler(lambda call: call.data.startswith("selectdelthisdayreps"), state="*")
async def selectdelthisdayreps(call: CallbackQuery, state: FSMContext):
    message = call.message
    day = call.data.split("selectdelthisdayreps|")[1]
    await message.edit_caption(caption='<b>⚙️ Выберите запись ↷</b>', reply_markup=await menu.delllistallrep(day=day))
    

@dp.callback_query_handler(lambda call: call.data.startswith("delreplistnext"), state="*")
async def delreplistnext(call: CallbackQuery, state: FSMContext):
    message = call.message
    page = call.data.split("delreplistnext|")[1]
    day = page.split("|")[1]
    await message.edit_caption(caption=f"<b>⚙️ Удаление записи ↷</b>", reply_markup=await menu.delllistallrep(page=int(page), day=int(day)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("delreplistback"), state="*")
async def delreplistback(call: CallbackQuery, state: FSMContext):
    message = call.message
    page = call.data.split("delreplistback|")[1]
    day = page.split("|")[1]
    await message.edit_caption(caption=f"<b>⚙️ Удаление записи ↷</b>", reply_markup=await menu.delllistallrep(page=int(page), day=int(day)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("selectdelrep"), state="*")
async def selectdelrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    await state.finish()
    rep = call.data.split("selectdelrep|")[1]
    await delrepk(rep)
    await call.answer(f"Запись удалена  ❌")
    await message.edit_caption(caption=f"⠀\n<b>👋  Привет, {message.from_user.first_name}</b>\n⠀", reply_markup=await menu.MainKey())
    








@dp.callback_query_handler(text="editrep", state="*")
async def editrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    check = await checkalllist()
    if check == 0:
        await call.answer(f"У вас нет записей  ❌")
    else:
        await message.edit_caption(caption=f"<b>⚙️ Изменение записей ↷</b>",
                               reply_markup=await menu.MenueditAlllistrep())
    

@dp.callback_query_handler(lambda call: call.data.startswith("selecteditthisdayreps"), state="*")
async def selecteditthisdayreps(call: CallbackQuery, state: FSMContext):
    message = call.message
    day = call.data.split("selecteditthisdayreps|")[1]
    await message.edit_caption(caption='<b>⚙️ Выберите запись ↷</b>', reply_markup=await menu.editlistallrep(day=day))
    

@dp.callback_query_handler(lambda call: call.data.startswith("editreplistnext"), state="*")
async def editreplistnext(call: CallbackQuery, state: FSMContext):
    message = call.message
    page = call.data.split("editreplistnext|")[1]
    day = page.split("|")[1]
    await message.edit_caption(caption=f"<b>⚙️ Изменение записей ↷</b>", reply_markup=await menu.editlistallrep(int(page), day=int(day)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("editreplistback"), state="*")
async def editreplistback(call: CallbackQuery, state: FSMContext):
    message = call.message
    page = call.data.split("editreplistback|")[1]
    day = page.split("|")[1]
    await message.edit_caption(caption=f"<b>⚙️ Изменение записей ↷</b>", reply_markup=await menu.editlistallrep(int(page), day=int(day)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("selectededitrep"), state="*")
async def selecteditrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    rep = call.data.split("selectededitrep|")[1]
    await message.edit_caption(caption=f"<b>⚙️ Выберите что хотите изменить ↷</b>", reply_markup=await menu.listeditselectrep(int(rep)))
    

@dp.callback_query_handler(lambda call: call.data.startswith("editthisselectrep"), state="*")
async def editthisselectrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    data = call.data.split("editthisselectrep|")[1]
    rep = data.split("|")[0]
    this = data.split("|")[1]
    await state.update_data(rep=rep)
    await state.update_data(this=this)
    await editthisselectrepstate.answer.set()
    await message.edit_caption(caption=f"<b>⚙️ Введите на что хотите изменить ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=editthisselectrepstate.answer)
async def editthisselectrep(message: types.Message, state: FSMContext):
    text = message.text
    rep = (await state.get_data())['rep']
    this = (await state.get_data())['this']
    await editthisintherep(rep, this, text)
    await message.answer_photo(photo=open('photo/Main.jpg', 'rb'), caption=f"<b>✅ Успешно изменено</b>", reply_markup=await menu.BackKeyM())
    await state.finish()
    

@dp.callback_query_handler(text="addrep", state="*")
async def addrep(call: CallbackQuery, state: FSMContext):
    message = call.message
    await message.edit_caption(caption=f"<b>📝 Выберите день записи ↷</b>", reply_markup=await menu.selectdayrepadd())
    

@dp.callback_query_handler(lambda call: call.data.startswith("selectdayrepaddthis"), state="*")
async def selectdayrepaddthis(call: CallbackQuery, state: FSMContext):
    message = call.message
    day = call.data.split("selectdayrepaddthis|")[1]
    await state.update_data(day=day)
    await addrepstates.date.set()
    await message.edit_caption(caption=f"<b>📝 Напишите время записи ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=addrepstates.date)
async def addrepstate(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(date=text)
    await addrepstates.next()
    await message.answer(f"<b>📝 Напишите тип работы ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=addrepstates.types)
async def addrepstate(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(type=text)
    await addrepstates.next()
    await message.answer(f"<b>📝 Напишите длительность работы ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=addrepstates.wtime)
async def addrepstate(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(wtime=text)
    await addrepstates.next()
    await message.answer(f"<b>📝 Напишите номер клиента ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=addrepstates.number)
async def addrepstate(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(number=text)
    await addrepstates.next()
    await message.answer(f"<b>📝 Напишите прайс работы ↷</b>", reply_markup=await menu.BackKeyM())
    

@dp.message_handler(IsPrivate(), state=addrepstates.price)
async def addrepstate(message: types.Message, state: FSMContext):
    date = (await state.get_data())['date']
    day = (await state.get_data())['day']
    type = (await state.get_data())['type']
    wtime = (await state.get_data())['wtime']
    number = (await state.get_data())['number']
    price = message.text
    await addrepinlist(day, date, type, wtime, number, price)
    await message.answer_photo(photo=open('photo/Main.jpg', 'rb'), caption=f"<b>✅ Запись успешно добавлена</b>", reply_markup=await menu.BackKeyM())
    list = await get_alluser()
    list.remove(message.chat.id)
    for i in list:
        await bot.send_message(chat_id=i, text=f"<b>✅ Добавлена запись\n\nВремя: {day} число {date}\nРабота: {type}\nСтоимость: {price}\nНомер: <code>{number}</code>\nВремя работы: {wtime}</b>")
    await state.finish()
    














async def on_startup(dp):
    await create_tables()

if __name__ == "__main__":
    print("Bot by Pled")
    executor.start_polling(dp, on_startup=on_startup)