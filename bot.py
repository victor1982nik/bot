import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import json

with open("data.json", "r") as file:
    data = json.load(file)

def update_data():
    with open("data.json", "w") as file:
        json.dump(data,file, indent=4, ensure_ascii=False)

bot = telebot.TeleBot("token")

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

menu_keyboard.add(KeyboardButton("Поступление денег"))
menu_keyboard.add(KeyboardButton("Расход денег"))
menu_keyboard.add(KeyboardButton("Посмотреть отчет"))

@bot.message_handler(commands=['start'])
def start(message: Message):
    if str(message.chat.id) not in data.keys():
        data[str(message.chat.id)] = []
        update_data()
    sent_message = bot.send_message(message.chat.id, 'Сделайте выбор:', reply_markup=menu_keyboard)
    bot.register_next_step_handler(sent_message, button_parse)

def button_parse(message: Message):
    if message.text == 'Поступление денег':
        sent_message = bot.send_message(message.chat.id, 'Введите сумму поступления и комментарий через пробел: ')
        bot.register_next_step_handler(sent_message, handler_income)
    elif message.text == 'Поступление денег':
        sent_message = bot.send_message(message.chat.id, 'Введите сумму расхода и комментарий через пробел: ')
        bot.register_next_step_handler(sent_message, handler_outcome)
    elif message.text == 'Посмотреть отчет':
        full_count_income = 0
        full_count_outcome = 0

        for operation in data[str(message.chat.id)]:
            if operation['status'] == 'plus':
                full_count_income += operation['count']
            else:
                full_count_outcome += operation['count']

        message_text = f'Всего израсходовано: {full_count_outcome} грн\nВсего получено: {full_count_income} грн \n\n'
                
        for operation in data[str(message.chat.id)]:
            if operation['status'] == 'plus':
                message_text += f'+ {operation['count']} | {operation['comment']}\n'
            else:
                message_text += f'- {operation['count']} | {operation['comment']}\n'
        bot.send_message(message.chat.id, message_text)
        start(message)

def handler_income(message:Message):
    count = message.text.split(' ',1)[0]
    comment = message.text.split(' ',1)[1]
    data[str(message.chat.id)].append(
        {
            'count': int(count),
            'comment': comment,
            'status': 'plus'
        }
    )
    bot.send_message(message.chat.id, 'Поступление добавлено')
    update_data()
    start(message)

def handler_outcome(message:Message):
    count = message.text.split(' ',1)[0]
    comment = message.text.split(' ',1)[1]
    data[str(message.chat.id)].append(
        {
            'count': int(count),
            'comment': comment,
            'status': 'minus'
        }
    )
    bot.send_message(message.chat.id, 'Расход добавлен')
    update_data()
    start(message)

bot.infinity_polling()