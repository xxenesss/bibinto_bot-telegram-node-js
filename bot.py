from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import sqlite3
import config

bot = Bot(token="токен")

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserInformation(StatesGroup):
    us_name = State()
    us_insta = State()
    us_city = State()
    us_gender = State()
    liked_id = State()
    ocenka_wait = State()
    ocenka_wait_city = State()
    ocenka_wait_gender = State()
    city_wait = State()
    gender_wait = State()
    photo_wait = State()
    change_name = State()
    change_inst = State()
    change_city = State()
    change_gender = State()
    change_photo = State()
    old = State()
    tgname = State()
    comment_city = State()
    comment_gender = State()
    comment_anyway = State()
    change_old = State()


class dbinfo(StatesGroup):
    userid = State()
    username = State()
    report = State()
    senduserid = State()
    sendusermsg = State()


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, user_name: str, user_instagram: str, user_city: str, user_gender: str, user_old: str, user_tgname: str):
    cursor.execute('INSERT INTO register (user_id, user_name, user_instagram, user_city, user_gender, user_old, user_tgname) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, user_instagram, user_city, user_gender, user_old, user_tgname))
    conn.commit()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    joinedFile = open("userstats.txt", "r")
    joinedUsers = set()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("userstats.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)
    try:
        select_sql = f"SELECT user_name FROM register WHERE user_id = {message.from_user.id}"
        cursor.execute(select_sql)
        result = cursor.fetchall()
        for data2 in result:
            name = data2[0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="Смотреть анкеты людей 👁")
        button2 = types.KeyboardButton(text='Моя анкета 👤')
        button3 = types.KeyboardButton(text='Репорт 🆘')
        keyboard.add(button1, button2, button3)
        await message.answer(f'🍃 {name}, Ты находишься в главном меню, выбери действие по кнопке ниже.',
                             reply_markup=keyboard)
    except:
        await message.answer(
            f'Привет, {message.from_user.first_name}. Я -  {config.bot_name}.\nЧто я делаю?\nЯ помогаю людям познакомиться, найти новых друзей, отношения.')
        await message.answer(
            'Сейчас тебе нужно заполнить анкету для того, что-бы ты смог(ла) оценивать других людей, а другие смогли оценивать тебя 😜')
        await message.answer('Все данные ниже будут видны другим людям! Приступим...')
        await message.answer('Как тебя зовут?')
        await UserInformation.us_name.set()


@dp.message_handler(state=UserInformation.us_name)
async def get_name(message: types.Message, state: FSMContext):
    s = message.text
    f = (s.count('.'))
    if f > 0:
        await message.answer('Обнаружена ссылка.')
    else:
        await state.update_data(us_name=message.text)
        keyboard_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="Мужской")
        button2 = types.KeyboardButton(text="Женский")
        keyboard_gender.add(button1, button2)
        await message.answer("Отлично, теперь выбери свой пол.", reply_markup=keyboard_gender)
        await UserInformation.us_gender.set()


@dp.message_handler(state=UserInformation.us_gender)
async def get_name(message: types.Message, state: FSMContext):
    if message.text == 'Мужской' or message.text == 'Женский':
        await state.update_data(us_gender=message.text)
        await message.answer("Напиши свой Instagram", reply_markup=types.ReplyKeyboardRemove())
        await UserInformation.us_insta.set()
    else:
        await message.answer("Упс, ошибка 🥺\n Выбери пол по кнопкам ниже!")


@dp.message_handler(state=UserInformation.us_insta)
async def get_insta(message: types.Message, state: FSMContext):
    s = message.text
    f = (s.count('.'))
    if f > 0:
        await message.answer('Обнаружена ссылка.')
    else:
        await state.update_data(us_insta=message.text)
        await message.answer("Теперь укажи свой город")
        await UserInformation.us_city.set()


@dp.message_handler(state=UserInformation.us_city)
async def get_old(message: types.Message, state: FSMContext):
    s = message.text
    f = (s.count('.'))
    if f > 0:
        await message.answer('Обнаружена ссылка.')
    else:
        await state.update_data(us_city=message.text)
        await message.answer('Сколько тебе лет?')
        await UserInformation.old.set()


@dp.message_handler(state=UserInformation.old)
async def get_city(message: types.Message, state: FSMContext):
    try:
        s = int(message.text)
        await state.update_data(old=message.text)
        await message.answer('Последний шаг! Отправь свою фотографию.')
        await UserInformation.photo_wait.set()
    except:
        await message.answer('Введите цифру!')


@dp.message_handler(state=UserInformation.photo_wait, content_types=['photo'])
async def get_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(f'photos\\{message.from_user.id}.jpeg')
    data = await state.get_data()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Смотреть анкеты людей 👁")
    button2 = types.KeyboardButton(text='Моя анкета 👤')
    button3 = types.KeyboardButton(text='Репорт 🆘')
    keyboard.add(button1, button2, button3)
    us_name = data['us_name']
    us_gender = data['us_gender']
    us_instagram = data['us_insta']
    us_city = data['us_city']
    old = data['old']
    db_table_val(user_id=message.from_user.id, user_name=us_name, user_instagram=us_instagram, user_city=us_city,
                 user_gender=us_gender, user_old=old, user_tgname=message.from_user.username)
    await message.answer(
        'Анкета сохранена. Теперь ты можешь оценивать других людей 🥰\nКогда тебя будут оценивать другие люди, тебе будут приходить их анкеты.\n Рекомендую отключить от меня уведомления 😇',
        reply_markup=keyboard)
    await state.finish()


@dp.message_handler(content_types=['text'], text='Анкеты')
async def db_conn(message: types.Message):
    if message.from_user.id == config.develop_id:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        d = sum(1 for line in open('userstats.txt'))
        await message.answer(f'Успешное подключение к DataBaseSqlie3\nАнкет в базе: {d}')
        await message.answer("Введите ID пользователя")
        await dbinfo.userid.set()


@dp.message_handler(state=dbinfo.userid)
async def db_search_info_id(message: types.Message, state: FSMContext):
    await state.update_data(userid=message.text)
    select_sql = (f"SELECT user_id FROM register WHERE user_id = {message.text}")
    cursor.execute(select_sql)
    result = cursor.fetchall()
    if cursor.fetchone() is None:
        await message.answer(f'[Error DB] ID Invalid.')
    elif cursor.fetchone() is {user_id}:
        select_sql = f"SELECT user_name, user_instagram, user_city, sr_ocenka, kolvo_ocenok, user_gender, user_old, user_tgname FROM register WHERE user_id = {message.text}"
        cursor.execute(select_sql)
        result = cursor.fetchall()
        for data in result:
            name = data[0]
            insta = data[1]
            city = data[2]
            ocenka = data[3]
            kolvo = data[4]
            gender = data[5]
            old = data[6]
            tgname = data[7]
            await bot.send_photo(message.chat.id, types.InputFile(f'./photos/{message.text}.jpeg'),
                                 caption=f"Вот инфа о (@{tgname}) [{tgname}](tg://user?id={message.text}):\n\n👤 Имя: " + str(
                                     name) + "\n🥑 Возраст: " + str(old) + "\n👬 Пол: " + str(
                                     gender) + "\n💫 Inst: " + str(insta) + "\n🌎 Город: " + str(
                                     city) + "\n\n📈 Средняя оценка: " + str(ocenka) + " ⭐", parse_mode='Markdown')
            await state.finish()


@dp.message_handler(content_types=['text'], text='Репорт 🆘')
async def report_send(message: types.Message):
    await message.answer(
        "Опишите полную суть жалобы, старайтесь писать ясно и кратко.\n\nЕсли Вы хотите пожаловаться на анкету, введите ID Анкеты.")
    await dbinfo.report.set()


@dp.message_handler(state=dbinfo.report)
async def db_search_info_id(message: types.Message, state: FSMContext):
    await state.update_data(report=message.text)
    select_sql = f"SELECT user_name, user_instagram, user_city, sr_ocenka, kolvo_ocenok, user_gender, user_old, user_tgname FROM register WHERE user_id = {message.from_user.id}"
    cursor.execute(select_sql)
    result = cursor.fetchall()
    for data in result:
        name = data[0]
        insta = data[1]
        city = data[2]
        ocenka = data[3]
        kolvo = data[4]
        gender = data[5]
        old = data[6]
        tgname = data[7]
    await bot.send_message(config.admin_chat,
                           f"Новый репорт от [{tgname}](tg://user?id={message.from_user.id}):\nTelegram ID Автора: {message.from_user.id}\n\nСообщение: {message.text}",
                           parse_mode='Markdown')
    await message.answer('Ваша жалоба отправлена. Примерное время ожидания: 1 час')
    await dbinfo.next()


@dp.message_handler(content_types=['text'])
async def message(message: types.Message):
    if message.text == '/dev':
        if message.from_user.id == config.develop_id:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(text="Статистика")
            button2 = types.KeyboardButton(text='Анкеты')
            keyboard.add(button1, button2)
            await message.answer(f'Привет, мой повелитель! Что пожелаешь на этот раз?', reply_markup=keyboard)
    if message.text == "Статистика":
        if message.from_user.id == config.develop_id:
            d = sum(1 for line in open('userstats.txt'))
            await message.answer(
                f'Пользователей: *{d}* \nСообщений бота: в разработке\nВсего сообщений: в разработке\nОценили "n" раз\n\nРазработчик: [максимУсы](tg://user?id={config.develop_id})',
                parse_mode='Markdown')
    if message.text == 'Моя анкета 👤':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="Назад 🔙")
        button2 = types.KeyboardButton(text="Сменить данные анкеты ⚙️")
        keyboard.add(button1, button2)
        select_sql = f"SELECT user_name, user_instagram, user_city, sr_ocenka, kolvo_ocenok, user_gender, user_old FROM register WHERE user_id = {message.from_user.id}"
        cursor.execute(select_sql)
        result = cursor.fetchall()
        for data in result:
            name = data[0]
            insta = data[1]
            city = data[2]
            ocenka = data[3]
            kolvo = data[4]
            gender = data[5]
            old = data[6]
        if message.from_user.id == message.from_user.id:
            try:
                sr_ocenka1 = int(ocenka) / int(kolvo)
                sr_ocenka2 = round(sr_ocenka1, 1)
            except:
                sr_ocenka2 = 0
            await bot.send_photo(message.from_user.id, types.InputFile(f'./photos/{message.from_user.id}.jpeg'),
                                 caption="☀️ Твоя анкета:\n\n👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(
                                     old) + "\n👬 Пол: " + str(gender) + "\n💫 Inst: " + str(
                                     insta) + "\n🌎 Город: " + str(city) + "\n\n📈 Средняя оценка: " + str(
                                     sr_ocenka2) + "⭐", reply_markup=keyboard)
    elif message.text == 'Назад 🔙':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="Смотреть анкеты людей 👁")
        button2 = types.KeyboardButton(text='Моя анкета 👤')
        button3 = types.KeyboardButton(text='Репорт 🆘')
        keyboard.add(button1, button2, button3)
        await message.answer('🍃 Ты находишься в главном меню, выбери действие по кнопке ниже.', reply_markup=keyboard)
    elif message.text == 'Смотреть анкеты людей 👁':
        await message.answer('👁 ‍Режим просмотра анкет', reply_markup=types.ReplyKeyboardRemove())
        inlinekeyboard = types.InlineKeyboardMarkup()
        inlinekeyboard.add(types.InlineKeyboardButton(text="Оценивать людей другого города 🌎", callback_data="gorod"))
        inlinekeyboard.add(types.InlineKeyboardButton(text="Оценивать людей другого пола 👄", callback_data="gender"))
        inlinekeyboard.add(types.InlineKeyboardButton(text="Мне всё равно, погнали оценивать всех 😌", callback_data="gonext_anyway"))
        await message.answer('Кого будем оценивать?', reply_markup=inlinekeyboard)
    elif message.text == 'Сменить данные анкеты ⚙️':
        inlinekeyboard2 = types.InlineKeyboardMarkup()
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Имя", callback_data="change_name"))
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Инстаграм", callback_data="change_inst"))
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Город", callback_data="change_city"))
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Пол", callback_data="change_gender"))
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Возраст", callback_data="change_old"))
        inlinekeyboard2.add(types.InlineKeyboardButton(text="Фото", callback_data="change_photo"))
        await message.answer('Выберите, что желаете сменить в своей анкете.', reply_markup=inlinekeyboard2)

@dp.callback_query_handler(text="gorod")
async def send(call: types.CallbackQuery):
    await call.message.answer('Напиши город для поиска')
    await call.answer()
    await UserInformation.city_wait.set()

@dp.callback_query_handler(text="gender")
async def send(call: types.CallbackQuery):
    keyboard_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Мужской")
    button2 = types.KeyboardButton(text="Женский")
    keyboard_gender.add(button1, button2)
    await call.message.answer('Выбери пол для поиска', reply_markup=keyboard_gender)
    await call.answer()
    await UserInformation.gender_wait.set()

@dp.message_handler(state=UserInformation.city_wait)
async def get_name(message: types.Message, state: FSMContext):
    global city1
    await state.update_data(city_wait=message.text)
    data_city = await state.get_data()
    city1 = data_city['city_wait']
    select_sql = f"SELECT user_id, user_name, user_instagram, user_city, user_gender, user_old FROM register WHERE user_city = '{city1}' ORDER BY RANDOM() LIMIT 1"
    cursor.execute(select_sql)
    result = cursor.fetchall()
    for data in result:
        user_id = data[0]
        name = data[1]
        insta = data[2]
        city = data[3]
        gender = data[4]
        old = data[5]
        await state.update_data(liked_id=user_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="1")
        button2 = types.KeyboardButton(text='2')
        button3 = types.KeyboardButton(text='3')
        button4 = types.KeyboardButton(text='4')
        button5 = types.KeyboardButton(text='5')
        button6 = types.KeyboardButton(text='6')
        button7 = types.KeyboardButton(text='7')
        button8 = types.KeyboardButton(text='8')
        button9 = types.KeyboardButton(text='9')
        button10 = types.KeyboardButton(text='10')
        keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
        await bot.send_photo(message.from_user.id, types.InputFile(f'./photos/{user_id}.jpeg'),
                             caption=f"👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(old) + "\n👬 Пол " + str(
                                 gender) + "\n💫 Inst: " + str(insta) + "\n🌎 Город: " + str(
                                 city) + "\n\nОцени от 1 до 10.", reply_markup=keyboard)
        await UserInformation.ocenka_wait_city.set()

    @dp.message_handler(state=UserInformation.ocenka_wait_city)
    async def get_name(message: types.Message, state: FSMContext):
        global liked_id
        try:
            s = int(message.text)
            if 0 < s < 11:
                data = await state.get_data()
                liked_id = data['liked_id']
                select_sql = f"SELECT user_name, user_instagram, user_city, user_gender FROM register WHERE user_id = {message.from_user.id}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data2 in result:
                    name = data2[0]
                    insta = data2[1]
                    city = data2[2]
                await bot.send_photo(data['liked_id'], types.InputFile(f'./photos/{message.from_user.id}.jpeg'),
                                     caption=f"🤙🏻 Новая оценка от [{message.from_user.username}](tg://user?id=({message.from_user.id}):\n💫 Inst: {insta}\n🌎 Город: {city}\n⭐ Оценка: {message.text}",
                                     parse_mode='Markdown')
                inlinekeyboard = types.InlineKeyboardMarkup()
                inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_city"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="Добавить комментарий", callback_data="comment_city"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
                select_sql = f"SELECT sr_ocenka, kolvo_ocenok FROM register WHERE user_id = {data['liked_id']}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data3 in result:
                    ocenka1 = data3[0]
                    kolvo1 = data3[1]
                ocenka2 = int(ocenka1) + int(message.text)
                kolvo2 = int(kolvo1) + 1
                sql_update_query = f"Update register set sr_ocenka = {ocenka2}, kolvo_ocenok = {kolvo2} where user_id = {data['liked_id']}"
                cursor.execute(sql_update_query)
                conn.commit()
                await message.answer(f'Ваша оценка: {message.text} ⭐\n\nВыберите дальнейшее действие.',
                                     reply_markup=inlinekeyboard)
                await state.finish()
            else:
                await message.answer('Оценка принимается от 1 до 10!')
        except:
            await message.answer('Принимается только число!')

        @dp.callback_query_handler(text="gonext_city")
        async def send(call: types.CallbackQuery, state: FSMContext):
            select_sql1 = f"SELECT user_id, user_name, user_instagram, user_city, user_old, user_gender FROM register WHERE user_city = '{city1}' ORDER BY RANDOM() LIMIT 1"
            cursor.execute(select_sql1)
            result = cursor.fetchall()
            for data in result:
                user_id = data[0]
                name = data[1]
                insta = data[2]
                city = data[3]
                old = data[4]
                gender = data[5]
            await state.update_data(liked_id=user_id)
            await call.message.answer_photo(types.InputFile(f'./photos/{user_id}.jpeg'),
                                            caption="👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(
                                                old) + "\n👬 Пол " + str(gender) + "\n💫 Inst: " + str(
                                                insta) + "\n🌎 Город: " + str(city) + "\n\nОцени от 1 до 10.")
            await call.answer()
            await UserInformation.ocenka_wait_city.set()
        @dp.callback_query_handler(text="comment_city")
        async def send(call: types.CallbackQuery):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Напишите комментарий')
            await UserInformation.comment_city.set()
            await call.answer()
            @dp.message_handler(state=UserInformation.comment_city)
            async def comment(message: types.Message, state: FSMContext):
                await bot.send_message(liked_id,
                                       f"🤙🏻 Новое сообщение от {message.from_user.username}\n\n{message.text}")
                inlinekeyboard = types.InlineKeyboardMarkup()
                inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_city"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
                await message.answer('Сообщение успешно отправлено!', reply_markup=inlinekeyboard)
                await state.finish()

@dp.message_handler(state=UserInformation.gender_wait)
async def get_name(message: types.Message, state: FSMContext):
    if message.text == 'Мужской' or message.text == 'Женский':
        global gender1
        await state.update_data(gender_wait=message.text)
        data_gender = await state.get_data()
        gender1 = data_gender['gender_wait']
        select_sql = f"SELECT user_id, user_name, user_instagram, user_city, user_old, user_gender FROM register WHERE user_gender = '{gender1}' ORDER BY RANDOM() LIMIT 1"
        cursor.execute(select_sql)
        result = cursor.fetchall()
        for data in result:
            user_id = data[0]
            name = data[1]
            insta = data[2]
            city = data[3]
            old = data[4]
            gender = data[5]
            await state.update_data(liked_id=user_id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(text="1")
            button2 = types.KeyboardButton(text='2')
            button3 = types.KeyboardButton(text='3')
            button4 = types.KeyboardButton(text='4')
            button5 = types.KeyboardButton(text='5')
            button6 = types.KeyboardButton(text='6')
            button7 = types.KeyboardButton(text='7')
            button8 = types.KeyboardButton(text='8')
            button9 = types.KeyboardButton(text='9')
            button10 = types.KeyboardButton(text='10')
            keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
            await bot.send_photo(message.from_user.id, types.InputFile(f'./photos/{user_id}.jpeg'),
                                 caption="👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(old) + "\n👬 Пол " + str(
                                     gender) + "\n💫 Inst: " + str(insta) + "\n🌎 Город: " + str(
                                     city) + "\n\nОцени от 1 до 10.", reply_markup=keyboard)
            await UserInformation.ocenka_wait_gender.set()
    else:
        await message.answer('Пожалуйста, укажите нормальный пол.')

    @dp.message_handler(state=UserInformation.ocenka_wait_gender)
    async def get_name(message: types.Message, state: FSMContext):
        global liked_id
        try:
            s = int(message.text)
            if 0 < s < 11:
                data = await state.get_data()
                liked_id = data['liked_id']
                select_sql = f"SELECT user_name, user_instagram, user_city, user_gender FROM register WHERE user_id = {message.from_user.id}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data2 in result:
                    name = data2[0]
                    insta = data2[1]
                    city = data2[2]
                await bot.send_photo(data['liked_id'], types.InputFile(f'./photos/{message.from_user.id}.jpeg'),
                                     caption=f"🤙🏻 Новая оценка от [{message.from_user.username}](tg://user?id=({message.from_user.id}):\n💫 Inst: {insta}\n🌎 Город: {city}\n⭐ Оценка: {message.text}",
                                     parse_mode='Markdown')
                inlinekeyboard = types.InlineKeyboardMarkup()
                inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_gender"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="Добавить комментарий", callback_data="comment_gender"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
                select_sql = f"SELECT sr_ocenka, kolvo_ocenok FROM register WHERE user_id = {data['liked_id']}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data3 in result:
                    ocenka1 = data3[0]
                    kolvo1 = data3[1]
                ocenka2 = int(ocenka1) + int(message.text)
                kolvo2 = int(kolvo1) + 1
                sql_update_query = f"Update register set sr_ocenka = {ocenka2}, kolvo_ocenok = {kolvo2} where user_id = {data['liked_id']}"
                cursor.execute(sql_update_query)
                conn.commit()
                await message.answer(f'Ваша оценка: {message.text}⭐\n\nВыберите дальнейшее действие.',
                                     reply_markup=inlinekeyboard)
                await state.finish()
            else:
                await message.answer('Только число от 1 до 10')
        except:
            await message.answer('Принимается только число')
        @dp.callback_query_handler(text="gonext_gender")
        async def send(call: types.CallbackQuery, state: FSMContext):
            select_sql1 = f"SELECT user_id, user_name, user_instagram, user_city, user_old, user_gender FROM register WHERE user_gender = '{gender1}' ORDER BY RANDOM() LIMIT 1"
            cursor.execute(select_sql1)
            result = cursor.fetchall()
            for data in result:
                user_id = data[0]
                name = data[1]
                insta = data[2]
                city = data[3]
                old = data[4]
                gender = data[5]
            await state.update_data(liked_id=user_id)
            await call.message.answer_photo(types.InputFile(f'./photos/{user_id}.jpeg'),
                                            caption=f"👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(
                                                old) + "\n👬 Пол " + str(gender) + "\n💫 Inst: " + str(
                                                insta) + "\n🌎 Город: " + str(city) + "\n\nОцени от 1 до 10.")
            await call.answer()
            await UserInformation.ocenka_wait_gender.set()
        @dp.callback_query_handler(text="comment_gender")
        async def send(call: types.CallbackQuery):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Напишите комментарий')
            await UserInformation.comment_gender.set()
            await call.answer()
            @dp.message_handler(state=UserInformation.comment_gender)
            async def comment(message: types.Message, state: FSMContext):
                await bot.send_message(liked_id,
                                       f"🤙🏻 Новое сообщение от {message.from_user.username}\n\n{message.text}")
                inlinekeyboard = types.InlineKeyboardMarkup()
                inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_gender"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
                await message.answer('Сообщение успешно отправлено!', reply_markup=inlinekeyboard)
                await state.finish()


@dp.callback_query_handler(text="gonext_anyway")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    select_sql = f"SELECT user_id, user_name, user_instagram, user_city, user_old, user_gender FROM register WHERE user_id != {call.from_user.id}  ORDER BY RANDOM() LIMIT 1"
    cursor.execute(select_sql)
    result = cursor.fetchall()
    for data in result:
        user_id = data[0]
        name = data[1]
        insta = data[2]
        city = data[3]
        old = data[4]
        gender = data[5]
        await state.update_data(liked_id=int(user_id))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="1")
        button2 = types.KeyboardButton(text='2')
        button3 = types.KeyboardButton(text='3')
        button4 = types.KeyboardButton(text='4')
        button5 = types.KeyboardButton(text='5')
        button6 = types.KeyboardButton(text='6')
        button7 = types.KeyboardButton(text='7')
        button8 = types.KeyboardButton(text='8')
        button9 = types.KeyboardButton(text='9')
        button10 = types.KeyboardButton(text='10')
        keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
        await bot.send_photo(call.from_user.id, types.InputFile(f'./photos/{user_id}.jpeg'),
                             caption="👤 Имя: " + str(name) + "\n🥑 Возраст: " + str(old) + "\n👬 Пол " + str(
                                 gender) + "\n💫 Inst: " + str(insta) + "\n🌎 Город: " + str(
                                 city) + "\n\nОцени от 1 до 10.", reply_markup=keyboard)
        await call.answer()
        await UserInformation.ocenka_wait.set()

    @dp.message_handler(state=UserInformation.ocenka_wait)
    async def get_name(message: types.Message, state: FSMContext):
        global liked_id
        try:
            s = int(message.text)
            if 0 < s < 11:
                data = await state.get_data()
                liked_id = data['liked_id']
                select_sql = f"SELECT user_name, user_instagram, user_city, user_gender FROM register WHERE user_id = {message.from_user.id}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data2 in result:
                    name = data2[0]
                    insta = data2[1]
                    city = data2[2]
                await bot.send_photo(data['liked_id'], types.InputFile(f'./photos/{message.from_user.id}.jpeg'),
                                     caption=f"🤙🏻 Новая оценка от [{message.from_user.username}](tg://user?id=({message.from_user.id}):\n💫 Inst: {insta}\n🌎 Город: {city}\n⭐ Оценка: {message.text}",
                                     parse_mode='Markdown')
                select_sql = f"SELECT sr_ocenka, kolvo_ocenok FROM register WHERE user_id = {data['liked_id']}"
                cursor.execute(select_sql)
                result = cursor.fetchall()
                for data3 in result:
                    ocenka1 = data3[0]
                    kolvo1 = data3[1]
                ocenka2 = int(ocenka1) + int(message.text)
                kolvo2 = int(kolvo1) + 1
                sql_update_query = f"Update register set sr_ocenka = {ocenka2}, kolvo_ocenok = {kolvo2} where user_id = {data['liked_id']}"
                cursor.execute(sql_update_query)
                conn.commit()
                inlinekeyboard = types.InlineKeyboardMarkup()
                inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_anyway"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="Добавить комментарий", callback_data="comment_anyway"))
                inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
                await message.answer(f'Ваша оценка: {message.text} ⭐\n\nВыберите дальнейшее действие.',
                                     reply_markup=inlinekeyboard)
                await state.finish()
            else:
                await message.answer('Только число от 1 до 10')
        except:
            await message.answer("Принимается только число!")

    @dp.callback_query_handler(text="comment_anyway")
    async def send(call: types.CallbackQuery):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Напишите комментарий')
        await UserInformation.comment_anyway.set()
        await call.answer()
        @dp.message_handler(state=UserInformation.comment_anyway)
        async def comment(message: types.Message, state: FSMContext):
            await bot.send_message(liked_id, f"🤙🏻 Новое сообщение от {message.from_user.username}\n\n{message.text}")
            inlinekeyboard = types.InlineKeyboardMarkup()
            inlinekeyboard.add(types.InlineKeyboardButton(text="Следующая анкета ➡", callback_data="gonext_anyway"))
            inlinekeyboard.add(types.InlineKeyboardButton(text="❌ Выйти из оценки ❌", callback_data="back"))
            await message.answer('Сообщение успешно отправлено!', reply_markup=inlinekeyboard)
            await state.finish()

@dp.callback_query_handler(text="back")
async def send(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Смотреть анкеты людей 👁")
    button2 = types.KeyboardButton(text='Моя анкета 👤')
    button3 = types.KeyboardButton(text='Репорт 🆘')
    keyboard.add(button1, button2, button3)
    await call.message.answer('🍃 Ты находишься в главном меню, выбери действие по кнопке ниже.',
                              reply_markup=keyboard)
    await call.answer()

@dp.callback_query_handler(text="change_name")
async def send(call: types.CallbackQuery):
    await call.message.answer('Как тебя зовут?')
    await call.answer()
    await UserInformation.change_name.set()

    @dp.message_handler(state=UserInformation.change_name)
    async def change_name(message: types.Message, state: FSMContext):
        s = message.text
        f = (s.count('.'))
        if f == 0:
            await state.update_data(change_name=message.text)
            data = await state.get_data()
            new_name = str(data['change_name'])
            sql_update_query = f"Update register set user_name = '{new_name}' where user_id = {message.from_user.id}"
            cursor.execute(sql_update_query)
            conn.commit()
            await message.answer('Новое имя установлено!')
            await state.finish()
        else:
            await message.answer('Обнаружена ссылка!')


@dp.callback_query_handler(text="change_inst")
async def send(call: types.CallbackQuery):
    await call.message.answer('Напиши свой Instagram')
    await call.answer()
    await UserInformation.change_inst.set()

    @dp.message_handler(state=UserInformation.change_inst)
    async def change_name(message: types.Message, state: FSMContext):
        s = message.text
        f = (s.count('.'))
        if f == 0:
            await state.update_data(change_inst=message.text)
            data = await state.get_data()
            new_inst = str(data['change_inst'])
            sql_update_query = f"Update register set user_instagram = '{new_inst}' where user_id = {message.from_user.id}"
            cursor.execute(sql_update_query)
            conn.commit()
            await message.answer('Новый Instagram установлен')
            await state.finish()
        else:
            await message.answer('Обнаружена ссылка!')


@dp.callback_query_handler(text="change_city")
async def send(call: types.CallbackQuery):
    await call.message.answer('Где ты живешь?')
    await call.answer()
    await UserInformation.change_city.set()

    @dp.message_handler(state=UserInformation.change_city)
    async def change_name(message: types.Message, state: FSMContext):
        s = message.text
        f = (s.count('.'))
        if f == 0:
            await state.update_data(change_city=message.text)
            data = await state.get_data()
            new_city = str(data['change_city'])
            sql_update_query = f"Update register set user_city = '{new_city}' where user_id = {message.from_user.id}"
            cursor.execute(sql_update_query)
            conn.commit()
            await message.answer('Новый город установлен')
            await state.finish()
        else:
            await message.answer('Обнаружена ссылка!')


@dp.callback_query_handler(text="change_gender")
async def send(call: types.CallbackQuery):
    keyboard_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Мужской")
    button2 = types.KeyboardButton(text="Женский")
    keyboard_gender.add(button1, button2)
    await call.message.answer('Выберите пол для смены', reply_markup=keyboard_gender)
    await call.answer()
    await UserInformation.change_gender.set()

    @dp.message_handler(state=UserInformation.change_gender)
    async def change_name(message: types.Message, state: FSMContext):
        if message.text == 'Мужской' or message.text == 'Женский':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(text="Смотреть анкеты людей 👁")
            button2 = types.KeyboardButton(text='Моя анкета 👤')
            button3 = types.KeyboardButton(text='Репорт 🆘')
            keyboard.add(button1, button2, button3)
            await state.update_data(change_gender=message.text)
            data = await state.get_data()
            new_gender = str(data['change_gender'])
            sql_update_query = f"Update register set user_gender = '{new_gender}' where user_id = {message.from_user.id}"
            cursor.execute(sql_update_query)
            conn.commit()
            await message.answer('Новый пол учатновлен.', reply_markup=keyboard)
            await state.finish()
        else:
            await message.answer("Упс, ошибка 🥺\n Выбери пол по кнопкам ниже!")


@dp.callback_query_handler(text="change_old")
async def send(call: types.CallbackQuery):
    await call.message.answer('Сколько тебе лет?')
    await call.answer()
    await UserInformation.change_old.set()

    @dp.message_handler(state=UserInformation.change_old)
    async def change_name(message: types.Message, state: FSMContext):
        await state.update_data(change_old=message.text)
        try:
            data = await state.get_data()
            new_old = int(data['change_old'])
            sql_update_query = f"Update register set user_old = '{new_old}' where user_id = {message.from_user.id}"
            cursor.execute(sql_update_query)
            conn.commit()
            await message.answer('Новый возраст установлен')
            await state.finish()
        except:
            await message.answer('Вы ввели неккоректный возраст!')

@dp.callback_query_handler(text="change_photo")
async def send(call: types.CallbackQuery):
    await call.message.answer('Пришли мне свою фотографию')
    await call.answer()
    await UserInformation.change_photo.set()

    @dp.message_handler(state=UserInformation.change_photo, content_types=['photo'])
    async def change_name(message: types.Message, state: FSMContext):
        await message.photo[-1].download(f'photos\\{message.from_user.id}.jpeg')
        await message.answer('Фото обновлено!')
        await state.finish()


#@dp.message_handler(content_types=['text'], text='🏆 ТОП')
#async def rating(message: types.Message):
 #   select_sql(f"SELECT user_id, user_name, kolvo_ocenok FROM register order by kolvo_ocenok desc")
  #  cursor.execute(select_sql)
   # result = cursor.fetchall()
    #one = emo.emojize(':one:', use_aliases=True)
    #two = emo.emojize(':two:', use_aliases=True)
    #three = emo.emojize(':three:', use_aliases=True)
    #four = emo.emojize(':four:', use_aliases=True)
    #five = emo.emojize(':five:', use_aliases=True)
    #six = emo.emojize(':six:', use_aliases=True)
    #seven = emo.emojize(':seven:', use_aliases=True)
    #eight = emo.emojize(':eight:', use_aliases=True)
    #nine = emo.emojize(':nine:', use_aliases=True)
    #ten = emo.emojize(':ten:', use_aliases=True)
    #zero = emo.emojize(':zero:', use_aliases=True)
    #em = {0: zero, 1: one, 2: two, 3: three, 4: four, 5: five, 6: six, 7: seven, 8: eight, 9: nine, 10: ten}
    #message_lines = []
    #for index, item in enumerate(result, 1):
        #message_lines.append(f"{em.get(index)} [{item[1]}](tg://user?id={item[0]}): {item[2]} топа")
        #am = message_lines[:10]
        #mes = '\n'.join(am)
        #await message.answer(f'ТОП по оценкам\n{mes}', parse_mode='Markdown')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
