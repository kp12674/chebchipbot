import random
from datetime import datetime
import time
import asyncio
import aiosqlite
import string
import sqlite3
from decimal import *
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton

path = "data/database_file/DB.sqlite"



async def register_user(user_id, user_name, first_name):
	async with aiosqlite.connect(path) as db:

		await db.execute("INSERT INTO users"
						 "(user_id, user_name, first_name)"
						 "VALUES (?, ?, ?)",
						 [user_id, user_name, first_name])

		await db.commit()

async def get_user(user_id):
	async with aiosqlite.connect(path) as db:

		profile = await db.execute(f"SELECT * FROM users WHERE user_id = ?", (user_id,))

		return await profile.fetchone()

async def get_alluser():
	async with aiosqlite.connect(path) as db:

		profile = await db.execute(f"SELECT * FROM users")
		profile = await profile.fetchall()

		list = []
		for i in profile:
			list.append(i[0])

		return list

async def checkalllist():
	async with aiosqlite.connect(path) as db:

		data = await db.execute(f"SELECT * FROM Alllist")
		data = await data.fetchall()

		if len(data) == 0:
			return 0
		else:
			text = ""
			for i in data:
				text += f"{i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]}\n"
			return text

async def delrepk(rep):
	async with aiosqlite.connect(path) as db:

		await db.execute("DELETE FROM Alllist WHERE num = ?", (rep,))

		await db.commit()

async def getrep(rep):
	async with aiosqlite.connect(path) as db:

		data = await db.execute("SELECT * FROM Alllist WHERE num = ?", (rep,))

		return await data.fetchone()

async def getalllistrep():
	async with aiosqlite.connect(path) as db:

		data = await db.execute(f"SELECT * FROM Alllist")
		data = await data.fetchall()

		return data

async def getthisrepontheday(rep):
	async with aiosqlite.connect(path) as db:

		data = await db.execute(f"SELECT * FROM Alllist WHERE num = {rep}")
		data = await data.fetchone()

		return data

async def getalllistrepsthisday(day):
	async with aiosqlite.connect(path) as db:

		data = await db.execute(f"SELECT * FROM Alllist WHERE date = {day}")
		data = await data.fetchall()

		return data

async def editthisintherep(rep, thiss, text):
	async with aiosqlite.connect(path) as db:

		this = thiss.split("-")[0]
		index = int(thiss.split("-")[1]) - 1
		tables = ['date', 'time', 'type', 'wtime', 'number', 'price']

		await db.execute(f"UPDATE Alllist SET {tables[index]} = ? WHERE {tables[index]} = ? AND num = ?", (text, this, rep,))

		await db.commit()

async def addrepinlist(day, date, type, wtime, number, price):
	async with aiosqlite.connect(path) as db:

		await db.execute(f"INSERT INTO Alllist (date, time, type, wtime, number, price) VALUES (?, ?, ?, ?, ?, ?)", [day, date, type, wtime, number, price])

		await db.commit()







async def create_tables():
	async with aiosqlite.connect(path) as db:
		await db.execute("CREATE TABLE IF NOT EXISTS Alllist("
						 "num INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, type TEXT, wtime TEXT, number INT, price INT)")

		await db.execute("CREATE TABLE IF NOT EXISTS users("
						 "user_id INTEGER, user_name TEXT, first_name TEXT)")

		await db.commit()

