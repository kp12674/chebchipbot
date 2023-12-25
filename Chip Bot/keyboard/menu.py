from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configuration import config

from data.csdb import *

async def MainKey():
    keyboard = InlineKeyboardMarkup(row_width = 2)
    alllist = InlineKeyboardButton(text="👀  Все записи", callback_data="alllist")
    addrep = InlineKeyboardButton(text="📥  Добавить", callback_data="addrep")
    editrep = InlineKeyboardButton(text="🛠  Изменить запись", callback_data="editrep")
    delrep = InlineKeyboardButton(text="❌  Удалить запись", callback_data="delrep")
    keyboard.add(alllist)
    keyboard.add(addrep)
    keyboard.add(editrep, delrep)

    return keyboard

async def MenuAlllist(page: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 7, )
    listallrep = await getalllistrep()
    dates = []
    for i in listallrep:
        dates.append(int(i[1]))
    sorted(dates)
    keyboard.add(*[InlineKeyboardButton(f"{i}",callback_data=f"selectonthisdayreps|{i}") for i in set(dates)])

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="BackKeyMain")
    keyboard.add(Back)

    return keyboard

async def getlistallrepsday(page: int=0, day: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 3)
    listallrep = await getalllistrepsthisday(day)
    if page == 0:
        x = 0
        for rep in listallrep:
            x += 1
            if x <= 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectthisdayrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) > 7:
            keyboard.add(InlineKeyboardButton(text=f"Next >",
                                          callback_data=f"thisdayreplistnext|{page + 7}|{rep[1]}"))
        else:
            pass
    else:
        x = 0
        for rep in listallrep:
            x += 1
            if x > page and x <= page + 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectthisdayrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) <= page + 7:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"thisdayreplistback|{page - 7}|{rep[1]}"))
        else:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"thisdayreplistback|{page - 7}|{rep[1]}"),
                         InlineKeyboardButton(text=f"Next >", callback_data=f"thisdayreplistnext|{page + 7}|{rep[1]}"))

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="alllist")
    keyboard.add(Back)

    return keyboard

# async def MenuAlllist():
#     keyboard = InlineKeyboardMarkup(row_width = 2)
#     addrep = InlineKeyboardButton(text="📥  Добавить", callback_data="addrep")
#     editrep = InlineKeyboardButton(text="🛠  Изменить запись", callback_data="editrep")
#     delrep = InlineKeyboardButton(text="❌  Удалить запись", callback_data="delrep")
#     Back = InlineKeyboardButton(text="🔙  Вернуться", callback_data="BackKeyMain")
#     keyboard.add(addrep)
#     keyboard.add(editrep, delrep)
#     keyboard.add(Back)
#
#     return keyboard

async def BackKeyM():
    keyboard = InlineKeyboardMarkup(row_width = 2)
    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="BackKeyMain")

    keyboard.add(Back)

    return keyboard

async def BacDkKeyM():
    keyboard = InlineKeyboardMarkup(row_width = 2)
    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="alllist")

    keyboard.add(Back)

    return keyboard

async def BackKeyMD(y):
    keyboard = InlineKeyboardMarkup(row_width = 2)
    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data=f"BackKeyDMain|{y}")

    keyboard.add(Back)

    return keyboard

async def MenudelAlllistrep(page: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 7, )
    listallrep = await getalllistrep()
    dates = []
    for i in listallrep:
        dates.append(int(i[1]))
    sorted(dates)
    keyboard.add(*[InlineKeyboardButton(f"{i}",callback_data=f"selectdelthisdayreps|{i}") for i in set(dates)])

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="BackKeyMain")
    keyboard.add(Back)

    return keyboard
async def delllistallrep(page: int=0, day: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 3)
    listallrep = await getalllistrepsthisday(day)
    if page == 0:
        x = 0
        for rep in listallrep:
            x += 1
            if x <= 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectdelrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) > 7:
            keyboard.add(InlineKeyboardButton(text=f"Next >",
                                          callback_data=f"delreplistnext|{page + 7}|{rep[1]}"))
        else:
            pass
    else:
        x = 0
        for rep in listallrep:
            x += 1
            if x > page and x <= page + 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectdelrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) <= page + 7:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"delreplistback|{page - 7}|{rep[1]}"))
        else:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"delreplistback|{page - 7}|{rep[1]}"),
                         InlineKeyboardButton(text=f"Next >", callback_data=f"delreplistnext|{page + 7}|{rep[1]}"))

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="delrep")
    keyboard.add(Back)

    return keyboard

async def MenueditAlllistrep(page: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 7, )
    listallrep = await getalllistrep()
    dates = []
    for i in listallrep:
        dates.append(int(i[1]))
    sorted(dates)
    keyboard.add(*[InlineKeyboardButton(f"{i}",callback_data=f"selecteditthisdayreps|{i}") for i in set(dates)])

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="BackKeyMain")
    keyboard.add(Back)

    return keyboard
async def editlistallrep(page: int=0, day: int=0):
    keyboard = InlineKeyboardMarkup(row_width = 3)
    listallrep = await getalllistrepsthisday(day)
    if page == 0:
        x = 0
        for rep in listallrep:
            x += 1
            if x <= 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectededitrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) > 7:
            keyboard.add(InlineKeyboardButton(text=f"Next >",
                                          callback_data=f"editreplistnext|{page + 7}|{rep[1]}"))
        else:
            pass
    else:
        x = 0
        for rep in listallrep:
            x += 1
            if x > page and x <= page + 7:
                keyboard.add(InlineKeyboardButton(text=f"Время: {rep[2]} Работа: {rep[3]} Стоимость: {rep[6]} Номер: {rep[5]}", callback_data=f"selectededitrep|{rep[0]}"))
            else:
                pass
        if len(listallrep) <= page + 7:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"editreplistback|{page - 7}|{rep[1]}"))
        else:
            keyboard.add(InlineKeyboardButton(text=f"< Back", callback_data=f"editreplistback|{page - 7}|{rep[1]}"),
                         InlineKeyboardButton(text=f"Next >", callback_data=f"editreplistnext|{page + 7}|{rep[1]}"))

    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="editrep")
    keyboard.add(Back)

    return keyboard

async def listeditselectrep(rep):
    keyboard = InlineKeyboardMarkup(row_width = 2)
    data = await getrep(rep)
    x = -1
    for i in data:
        x += 1
        if x == 1:
            pass
        else:
            keyboard.add(InlineKeyboardButton(text=f"{i}", callback_data=f"editthisselectrep|{rep}|{i}-{x}"))
    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="editrep")

    keyboard.add(Back)

    return keyboard

async def selectdayrepadd():
    keyboard = InlineKeyboardMarkup(row_width = 6)
    keyboard.add(*[InlineKeyboardButton(f"{i}",callback_data=f"selectdayrepaddthis|{i}") for i in range(1, 32)])
    Back = InlineKeyboardButton(text="🔙 Вернуться", callback_data="BackKeyMain")

    keyboard.add(Back)

    return keyboard

