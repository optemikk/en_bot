import asyncio

from texts import *
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, InputMedia, ReplyKeyboardMarkup, KeyboardButton

from random import choice
from jsonwriter import *

from datetime import datetime

API_KEY = '6524572114:AAG4WfvdNkswheVRkIjg4ir0BWLc-MLgvKs'
# API_KEY = '6056114434:AAELexyjt28rMSLaR8Me2BGZMDXwHkrZnHI'
storage = MemoryStorage()
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=storage)
users = {}
admins = ['972383332']



class Form(StatesGroup):
    message = State()


async def update_stats():
    data = read_json(file_path='stats.json')
    time = datetime.now().strftime('%H:%M')
    print(time)
    if time == '00:00':
        data['day'] += 1
        data['clicks_day'] = 0
        if data['day'] % 7 == 0:
            data['clicks_week'] = 0
        elif data['day'] % 30 == 0:
            data['clicks_week'] = 0
    write_json(file_path='stats.json', data=data)
    await asyncio.sleep(60)


# подготовка сообщения (текста, кнопок)
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



# проверка подписки на канал
# (chat_id в bot.get_chat_member - айди самого канала. как получить его - отдельная история :) )
async def check_subs(msg):
    user_channel_status = await bot.get_chat_member(chat_id=-1001572670607, user_id=msg)
    if user_channel_status['status'] == 'left':
        await bot.send_message(chat_id=msg,
                               text='⚠️ <b>Вы не подписались канал!</b>\n\n<i>Для начала работы бота, подпишитесь на канал!</i>',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(text='Канал', url='https://t.me/ohmyenglishhh'),
                                   InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')),
                               parse_mode=types.ParseMode.HTML)
        return False
    else:
        return True


# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    data = read_json(file_path='stats.json')
    users = read_json(file_path='data.json')
    response = await check_subs(msg=msg.from_user.id)
    print(response)
    if response:
        if msg.from_user.id not in users:
            users[str(msg.from_user.id)] = {'count': 0}
            write_json(file_path='data.json', data=users)
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_markup.add(InlineKeyboardButton(text='Начать прохождение'))
        await msg.answer(text=start_text, parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)
        data['clicks'] += 1
        data['clicks_day'] += 1
        data['clicks_week'] += 1
        data['clicks_month'] += 1
        write_json(file_path='stats.json', data=data)


@dp.message_handler(commands=["mailing"])
async def mail_users(msg: types.Message):
    data = read_json('data.json')
    if str(msg.from_user.id) in admins:
        await Form.message.set()
        await msg.reply("✏️Отправьте мне сообщение, которое вы хотите использовать в глобальной рассылке!")


@dp.message_handler(commands=["stats"])
async def mail_users(msg: types.Message):
    data = read_json('stats.json')
    users = read_json('data.json')
    if str(msg.from_user.id) in admins:
        await msg.reply(f"<b>Статистика по боту:</b>\n\n"
                        f"<i>Всего переходов:</i> <b>{data['clicks']}</b>\n"
                        f"<i>Переходов сегодня:</i> <b>{data['clicks_day']}</b>\n"
                        f"<i>Переходов за неделю:</i> <b>{data['clicks_week']}</b>\n"
                        f"<i>Переходов за месяц:</i> <b>{data['clicks_month']}</b>\n\n"
                        f"<i>Дней работы бота:</i> <b>{data['day']}</b>\n\n"
                        f"<i>Всего пользователей:</i> <b>{len(users)}</b>\n"
                        f"<i>Активных пользователей:</i> <b>{data['active_users']}</b>\n"
                        f"<i>Мёртвых пользователей:</i> <b>{data['banned_users']}</b>\n", parse_mode=types.ParseMode.HTML)
    print(msg.chat.id)
    print(msg.from_user.id)


# обработчик текстовых сообщений
@dp.message_handler(content_types=['text'])
async def message_handler(msg: types.Message):
    users = read_json(file_path='data.json')
    if msg.text == 'Начать прохождение':
        users[str(msg.from_user.id)]['count'] = 0
        returns = await prepare_msg(question='q01')
        await msg.answer(text=test_text, parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(text=returns['text'], parse_mode=types.ParseMode.HTML, reply_markup=returns['markup'])

# обработчик инлайн кнопок
@dp.callback_query_handler()
async def query_handler(query: CallbackQuery):
    users = read_json(file_path='data.json')
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text='Канал', url='https://t.me/ohmyenglishhh'))
    if query.data == 'results':
        level = int(users[str(query.from_user.id)]["count"])
        if 0 < level < 5:
            text = 'A1\n<i>Начальный уровень владения языком. Стоит начать изучать язык усерднее.</i>'
        elif 5 < level < 10:
            text = 'A2\n<i>Уровень владения языком чуть ниже среднего. Хороший результат, но стоит продолжить его изучать.</i>'
        elif 10 < level < 15:
            text = 'B1\n<i>Средний уровень владения языком. Отличный результат! Практика языка вам не помешает!</i>'
        else:
            text = 'B2\n<i>Уровень владения языком выше среднего. Отличный результат! Практика языка вам не помешает!</i>'
        await query.message.delete()
        await bot.send_message(chat_id=query.from_user.id,
                               text=f'📚 Ваш результат: <b>{users[str(query.from_user.id)]["count"]} из 20</b>'
                                    f'\n\n🧠 Уровень знания языка - <b>{text}</b>', parse_mode=types.ParseMode.HTML)
        await bot.send_message(chat_id=query.from_user.id,
                               text='📈 <b>Для ежедневной тренировки знания языка советую вам подписаться на мой канал!</b>',
                               reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)

    elif query.data == 'check_sub':
        response = await check_subs(msg=query.from_user.id)
        if response:
            if query.from_user.id not in users:
                users[str(query.from_user.id)] = {'count': 0}
                write_json(file_path='data.json', data=users)
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_markup.add(InlineKeyboardButton(text='Начать прохождение'))
            await bot.send_message(chat_id=query.from_user.id, text=start_text, parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)
            await query.message.delete()

    elif query.data == 'send_mailing':
        users = read_json('data.json')
        data = read_json('stats.json')
        c = 0
        b = 0
        for i in users:
            try:
                if mail_type == 'text':
                    await bot.send_message(text=mail_text, chat_id=int(i))
                elif mail_type == 'photo':
                    await bot.send_photo(caption=mail_text, photo=mail_photo, chat_id=int(i))
                c += 1
            except:
                b += 1
                pass
        await bot.send_message(chat_id=query.from_user.id, text= f'Сообщения разосланы пользователям {c}!')
        data['active_users'] = c
        data['banned_users'] = b
        write_json(file_path='stats.json', data=data)


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
            users[str(query.from_user.id)]['count'] += 1
            write_json(file_path='data.json', data=users)
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
    users = read_json('users.json')
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await bot.send_message(chat_id=msg.from_user.id, text='Отменено успешно!')


@dp.message_handler(state=Form.message, content_types=['photo', 'text'])
async def process_mailing(message: types.Message, state: FSMContext):
    global mail_text, reply_message, mail_photo, mail_type
    """Process user name"""

    reply_markup = InlineKeyboardMarkup().row(*[InlineKeyboardButton(text='Отправить', callback_data='send_mailing'), InlineKeyboardButton(text='Отменить', callback_data='cancel_mailing')])

    await state.finish()
    await message.reply(f"Ваше сообщение для рассылки:")
    msg_type = message.content_type
    if msg_type == 'text':
        mail_type = message.content_type
        mail_text = message.text
        reply_message = await bot.send_message(message.from_user.id, message.text, reply_markup=reply_markup)
    elif msg_type == 'photo':
        mail_type = message.content_type
        document_id = message.photo[0].file_id
        info = await bot.get_file(document_id)
        mail_photo = info.file_id
        mail_text = message.caption
        reply_message = await bot.send_photo(chat_id=message.from_user.id, caption=message.caption, photo=mail_photo, reply_markup=reply_markup)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_stats())
    executor.start_polling(dp)