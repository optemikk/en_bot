from aiogram.types import InputFile, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, InputMedia, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import types

from random import choice

from loader import dp, bot, database
from forms import *

from texts import *
from config import *


async def check_subs(msg):
    # user_channel_status = await bot.get_chat_member(chat_id=-1001572670607, user_id=msg)
    # if user_channel_status['status'] == 'left':
    #     await bot.send_message(chat_id=msg,
    #                            text='⚠️ <b>Вы не подписались канал!</b>\n\n<i>Для начала работы бота, подпишитесь на канал!</i>',
    #                            reply_markup=InlineKeyboardMarkup().add(
    #                                InlineKeyboardButton(text='Канал', url='https://t.me/ohmyenglishhh'),
    #                                InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')),
    #                            parse_mode=types.ParseMode.HTML)
    #     return False
    # else:
    #     return True
    return True


async def prepare_msg(question):
    reply_markup = InlineKeyboardMarkup()
    if question == 'q21':
        text = 'Вы прошли тест!'
        reply_markup.add(InlineKeyboardButton(text='Узнать результаты', callback_data='results'))
    else:
        for k, i in enumerate(qst[question][0]):
            reply_markup.add(InlineKeyboardButton(text=i[:-1],
                                                  callback_data=f'{question}{i[-1]}'))
        text = qst[question][1]
    return {'markup': reply_markup, 'text': text}


# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    user_id = msg.from_user.id
    response = await check_subs(msg=msg.from_user.id)
    print(response)
    if response:
        if len(database.select_value(table='users', keys='rowid, *', where=f"user_id = {user_id}")) == 0:
            database.add_value(table='users', values=f'{user_id}, 0')
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_markup.add(InlineKeyboardButton(text='Начать прохождение'))
        await msg.answer(text=start_text, parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)
        database.update_value(table='stats', key='clicks = clicks + 1', where='rowid = 1')
        database.update_value(table='stats', key='clicks_day = clicks_day + 1', where='rowid = 1')
        database.update_value(table='stats', key='clicks_week = clicks_week + 1', where='rowid = 1')
        database.update_value(table='stats', key='clicks_month = clicks_month + 1', where='rowid = 1')
        # data['clicks'] += 1
        # data['clicks_day'] += 1
        # data['clicks_week'] += 1
        # data['clicks_month'] += 1
        # write_json(file_path='stats.json', data=data)


@dp.message_handler(commands=["mailing"])
async def mail_users(msg: types.Message):
    if str(msg.from_user.id) in admins:
        await Form.message.set()
        await msg.reply("✏️Отправьте мне сообщение, которое вы хотите использовать в глобальной рассылке!")


@dp.message_handler(commands=["stats"])
async def mail_users(msg: types.Message):

    clicks_all = database.select_value(table='stats', keys='*', where=f'rowid = 1')[0]
    clicks = clicks_all[0]
    clicks_day = clicks_all[1]
    clicks_week = clicks_all[2]
    days = clicks_all[3]
    users = len(database.select_value(table='users', keys='*', where=''))
    active_users = clicks_all[4]
    banned_users = clicks_all[5]

    if str(msg.from_user.id) in admins:
        await msg.reply(f"<b>Статистика по боту:</b>\n\n"
                        f"<i>Всего переходов:</i> <b>{clicks}</b>\n"
                        f"<i>Переходов сегодня:</i> <b>{clicks_day}</b>\n"
                        f"<i>Переходов за неделю:</i> <b>{clicks_week}</b>\n"
                        f"<i>Переходов за месяц:</i> <b>{clicks_week}</b>\n\n"
                        f"<i>Дней работы бота:</i> <b>{days}</b>\n\n"
                        f"<i>Всего пользователей:</i> <b>{users}</b>\n"
                        f"<i>Активных пользователей:</i> <b>{active_users}</b>\n"
                        f"<i>Мёртвых пользователей:</i> <b>{banned_users}</b>\n", parse_mode=types.ParseMode.HTML)
    print(msg.chat.id)
    print(msg.from_user.id)


# обработчик текстовых сообщений
@dp.message_handler(content_types=['text'])
async def message_handler(msg: types.Message):
    user_id = msg.from_user.id
    if msg.text == 'Начать прохождение':
        database.update_value(table='users', key='count = 0', where=f'user_id = {user_id}')
        # users[str(msg.from_user.id)]['count'] = 0
        returns = await prepare_msg(question='q01')
        await msg.answer(text=test_text, parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(text=returns['text'], parse_mode=types.ParseMode.HTML, reply_markup=returns['markup'])

# обработчик инлайн кнопок
@dp.callback_query_handler()
async def query_handler(query: CallbackQuery):
    user_id = query.from_user.id
    global mail_button
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text='Канал', url='https://t.me/ohmyenglishhh'))
    if query.data == 'results':
        # level = int(users[str(query.from_user.id)]["count"])
        level = database.select_value(table='users', keys='count', where=f'user_id = {user_id}')[0][0]
        if 0 <= level <= 4:
            text = 'А1\n<i>Начальный уровень владения языком.</i>'
        elif 5 <= level <= 8:
            text = 'A2\n<i>Уровень владения языком чуть выше начального.</i>'
        elif 9 <= level <= 12:
            text = 'B1\n<i>Средний уровень владения языком.</i>'
        elif 13 <= level <= 16:
            text = 'B2\n<i>Уровень владения языком выше среднего.</i>'
        elif 17 <= level <= 18:
            text = 'C1\n<i>Продвинутый уровень владения языком.</i>'
        else:
            text = 'С2\n<i>Профессиональный уровень владения языком.</i>'
        await query.message.delete()
        await bot.send_message(chat_id=query.from_user.id,
                               text=f'📚 Ваш результат: <b>{level} из 20</b>'
                                    f'\n\n🧠 Уровень знания языка - <b>{text}</b>', parse_mode=types.ParseMode.HTML)
        await bot.send_message(chat_id=query.from_user.id,
                               text='📈 <b>Для ежедневной тренировки знания языка советую вам подписаться на мой канал!</b>',
                               reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)

    elif query.data == 'check_sub':
        response = await check_subs(msg=query.from_user.id)
        if response:
            if len(database.select_value(table='users', keys='rowid, *', where=f"user_id = {user_id}")) == 0:
                database.add_value(table='users', values=f'{user_id}, 0')
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_markup.add(InlineKeyboardButton(text='Начать прохождение'))
            await bot.send_message(chat_id=query.from_user.id, text=start_text, parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)
            await query.message.delete()

    elif query.data == 'send_mailing':
        users = [i[0] for i in database.select_value(table='users', keys='*')]
        print(users)
        active_users = 0
        banned_users = 0
        if mail_button == '':
            mail_button = InlineKeyboardMarkup()
        for i in users:
            print(i)
            try:
                if mail_type == 'text':
                    await bot.send_message(text=mail_text, chat_id=int(i), reply_markup=mail_button, parse_mode='HTML')
                elif mail_type == 'photo':
                    await bot.send_photo(caption=mail_text, photo=mail_photo, chat_id=int(i), reply_markup=mail_button,
                                         parse_mode='HTML')
                active_users += 1
            except Exception as exc:
                print(exc)
                banned_users += 1
                pass
        await bot.send_message(chat_id=query.from_user.id, text= f'Сообщения разосланы пользователям {active_users}!')
        database.update_value(table='stats', key=f'active_users = {active_users}', where='rowid = 1')
        database.update_value(table='stats', key=f'banned_users = {banned_users}', where='rowid = 1')

        await query.message.delete()


    elif query.data == 'cancel_mailing':
        await query.message.edit_text(text='Рассылка отменена!')


    elif query.data == 'add_button':
        await Form.button.set()
        await bot.send_message(chat_id=query.from_user.id, text= f'Введите текст кнопки и ссылку через пробел:\n\nПример: "привет @username"')


    elif query.data[0] == 'q':
        print('query-data', query.data)
        question = f'q{int(query.data[1:3]) + 1}' if int(query.data[1:3]) >= 9 else f'q0{int(query.data[1:3]) + 1}'
        print('question', question)
        returns = await prepare_msg(question=question)
        print('returns', returns)
        if query.data[-1] == 'f':
            text = f'{choice(false_answers)}' \
                   f'\n✅ Правильный ответ - {qst[query.data[:3]][2]}' \
                   f'\n\n{returns["text"]}'
        else:
            text = f'{choice(true_answers)}' \
                   f'\n\n{returns["text"]}'
            database.update_value(table='users', key='count = count + 1', where=f'user_id = {user_id}')
        await query.message.edit_text(text=text, parse_mode=types.ParseMode.HTML, reply_markup=returns['markup'])
    # elif int(query.data[0]) < 19:
    #     print(query.data)
    #     returns = await prepare_msg(question=f'q{int(query.data[:2]) + 1}' if int(query.data[:2]) >= 9 else f'q0{int(query.data[:2]) + 1}')
    #     print(returns)
    #     if query.data[-1] == 'f':
    #         text = f'{choice(false_answers)}' \
    #                f'\n✅ Правильный ответ - {query.data.split("-")[1]}' \
    #                f'\n\n{returns["text"]}'
    #     else:
    #         text = f'{choice(true_answers)}' \
    #                f'\n\n{returns["text"]}'
    #         users[str(query.from_user.id)]['count'] += 1
    #         write_json(file_path='data.json', data=users)
    #
    #     await query.message.edit_text(text=text, parse_mode=types.ParseMode.HTML, reply_markup=returns['markup'])
        # await bot.send_message(chat_id=query.from_user.id, text=text, parse_mode=types.ParseMode.HTML, reply_markup=returns['markup'])


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(msg: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    await state.finish()
    await bot.send_message(chat_id=msg.from_user.id, text='Отменено успешно!')


@dp.message_handler(state=Form.message, content_types=['photo', 'text'])
async def process_mailing(message: types.Message, state: FSMContext):
    global mail_text, reply_message, mail_photo, mail_type, mail_button
    """Process user name"""

    reply_markup = InlineKeyboardMarkup()
    reply_markup.row(*[InlineKeyboardButton(text='Отправить', callback_data='send_mailing'),
                                                InlineKeyboardButton(text='Отменить', callback_data='cancel_mailing')])
    reply_markup.row(*[InlineKeyboardButton(text='Добавить кнопку', callback_data='add_button')])


    await state.finish()
    await message.reply(f"Ваше сообщение для рассылки:")
    msg_type = message.content_type
    if msg_type == 'text':
        mail_type = message.content_type
        mail_text = message.text
        reply_message = await bot.send_message(message.from_user.id, message.text, reply_markup=reply_markup, parse_mode='HTML')
    elif msg_type == 'photo':
        mail_type = message.content_type
        document_id = message.photo[0].file_id
        info = await bot.get_file(document_id)
        mail_photo = info.file_id
        mail_text = message.caption
        reply_message = await bot.send_photo(chat_id=message.from_user.id, caption=message.caption, photo=mail_photo, reply_markup=reply_markup, parse_mode='HTML')


@dp.message_handler(state=Form.button, content_types=['text'])
async def button(message: types.Message, state: FSMContext):
    global mail_text, reply_message, mail_photo, mail_type, mail_button

    reply_markup = InlineKeyboardMarkup()
    reply_markup.row(*[InlineKeyboardButton(text='Отправить', callback_data='send_mailing'),
                       InlineKeyboardButton(text='Отменить', callback_data='cancel_mailing')])
    reply_markup.row(*[InlineKeyboardButton(text='Добавить кнопку', callback_data='add_button')])

    await state.finish()
    await message.reply(f"Ваше сообщение для рассылки:", reply_markup=reply_markup)

    button_text = ' '.join(message.text.split()[:-1])
    url = message.text.split()[-1]
    if url[0] == '@':
        url = 'https://t.me/' + url[1:]
    mail_button = InlineKeyboardMarkup()
    mail_button.add(InlineKeyboardButton(text=button_text, url=url))

    print(button_text)
    print(url)
    print(mail_button)

    msg_type = message.content_type
    if msg_type == 'text':
        reply_message = await bot.send_message(message.from_user.id, mail_text, reply_markup=mail_button,
                                               parse_mode='HTML')
    elif msg_type == 'photo':
        reply_message = await bot.send_photo(chat_id=message.from_user.id, caption=mail_text, photo=mail_photo,
                                             reply_markup=mail_button, parse_mode='HTML')
