from turtledemo.lindenmayer import replace

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import sqlite3
import random


bot = Bot(token='5508239066:AAE5GtUnIi4VLfA0a3ud0EhuGo4eGkpx1NQ')
dp = Dispatcher(bot)
db = sqlite3.connect('base.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    balance BIGINT NOT NULL DEFAULT 5000
)""")
db.commit()






@dp.message_handler(commands=("start"))
async def echo(msg: types.message):
    id_user = msg.from_user.id
    db = sqlite3.connect('base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (id_user,))
    db.commit()
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(user_id) VALUES(?)", (id_user,))
        db.commit()



@dp.message_handler(commands=("profile"))
async def profile(msg: types.message):
    id_user = msg.from_user.id
    db = sqlite3.connect('base.db')
    cur = db.cursor()
    username = msg.from_user.username
    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (id_user,))
    db.commit()
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(user_id) VALUES(?)", (id_user,))
        balance = cur.execute("SELECT balance FROM users WHERE user_id =?", (id_user,)).fetchone()[0]
        lol = int(balance)
        await msg.answer(f"Привет {username}!"
                         f"Твой баланс: {lol}")
    else:
        balance = cur.execute("SELECT balance FROM users WHERE user_id =?", (id_user,)).fetchone()[0]
        lol = int(balance)
        await msg.answer(f"Привет {username}!"
                   f"Твой баланс: {lol}")
    db.commit()



@dp.message_handler(commands=("casino"))
async def casino(msg: types.message):
    id_user = msg.from_user.id
    try:
        db = sqlite3.connect('base.db')
        cur = db.cursor()
        username = msg.from_user.username
        bet = int(msg.text[8:])
        lol = round(random.uniform(0, 2), 2)
        sot = bet * lol
        print(sot)
        print(bet)
        cur.execute("SELECT user_id FROM users WHERE user_id = ?", (id_user,))
        db.commit()

        if cur.fetchone() is None:
            cur.execute("INSERT INTO users(user_id) VALUES(?)", (id_user,))
            balance = int(cur.execute("SELECT balance FROM users WHERE user_id =?", (id_user,)).fetchone()[0])
            kkkkk = int(balance)
            if balance < bet:
                await msg.answer("Недостаточно средств!")
            else:
                if lol < 1.0:
                    kkkkk = int(balance)
                    await msg.answer(f"Вы проиграли!\n"
                                    f"коф = {lol}")
                    cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (sot, id_user,))
                else:
                    await msg.answer(f"Вы win!\n"
                                 f"коф = {lol}\n"
                                     f"Ваш баланс: {kkkkk}")
                    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (sot, id_user,))
                db.commit()
        else:
            balance = cur.execute("SELECT balance FROM users WHERE user_id =?", (id_user,)).fetchone()[0]
            if balance < bet:
                await msg.answer("Недостаточно средств!")
            else:
                if lol < 1.0:
                    await msg.answer(f"Вы проиграли!\n"
                                 f"коф = {lol}")
                    cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (sot, id_user,))
                    print(balance)
                else:
                    await msg.answer(f"Вы win!\n"
                                 f"коф = {lol}")
                    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (sot, id_user,))
                    print(balance)
                db.commit()
        db.commit()
    except Exception as err:
        print(err)
        await msg.answer("После казино надо ввести ставку!!!!!")




executor.start_polling(dp)