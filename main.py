import os
import telebot
from flask import Flask, request
from telebot import types

TOKEN = 'YOUR TOKEN'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
text_messages = {
    'start':
        u'Приветствую тебя, {name}!\n'
        u'Я помогу тебе сделать онлайн заказ (это быстро и без очереди)🚀.\n\n'
        u'1. Выбери интересующий пакет (Ты можешь выбрать несколько✅)\n'
        u'2. Выбери время, когда захочешь назначить встречу⏰\n'
        u'3. Оплати заказ (это безопасно)⚔️\n',

    'help':
        u'Пока что я не знаю, чем тебе помочь, поэтому просто выпей кофе!'
}
@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Сделать заказ')
    bot.send_message(message.from_user.id, text_messages['start'].format(name=message.from_user.first_name),
                     reply_markup=markup)
@bot.message_handler(func=lambda message: True)
def choose_categories(message):
    cat_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cat_markup.row('Прайс-лист 💲', 'О компании 🏦')
    cat_markup.row('Акции 🎁', 'Контакты 📞')
    msg = bot.send_message(message.from_user.id, 'Что вас интересует?', reply_markup=cat_markup)
    bot.register_next_step_handler(msg, choose_drink)
@bot.message_handler(func=lambda message: True)
def choose_drink(message):
    drink_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == 'О компании 🏦':
        drink_markup.row('Основатель 🌟', 'Рабочая группа 🕴')
        drink_markup.row('Офис 🏋️‍️', 'Бригада 🏅')
    elif message.text == 'Прайс-лист 💲':
        drink_markup.row('Standard - M')
        drink_markup.row('Premium - L', 'Lite - S')
    elif message.text == 'Акции 🎁':
        drink_markup.row('All in')

    elif message.text == 'Контакты 📞':
        drink_markup.row('Телефон', 'Instagram', 'Адрес')
    drink_markup.row('Назад')

    msg = bot.send_message(message.from_user.id, 'Что вам угодно, господин(жа)', reply_markup=drink_markup)
    bot.register_next_step_handler(msg, choose_size)


def choose_size(message):
    size_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Назад':
        choose_categories(message)
        return
    else:
        if message.text == 'Основатель 🌟':
            bot.send_message(message.from_user.id, 'Jcyjdfntkm', reply_markup=size_markup)

        if message.text == 'Рабочая группа 🕴':
            bot.send_message(message.from_user.id, 'Все наши специалисты со стажем не менее 3-х лет', reply_markup=size_markup)

        if message.text == 'Standard - M':
            size_markup.row('View Examples')
            msg = bot.send_message(message.from_user.id, 'цена - 10000 за м^2.\n В цену входит:\n'
                                                   '- Чертеж\n'
                                                   '- Обработка...', reply_markup=size_markup)
        if message.text == 'Premium - L':
            msg = bot.send_message(message.from_user.id, 'цена - 15000 за м^2', reply_markup=size_markup)
            size_markup.row('View Examples')

        if message.text == 'Lite - S':
            msg = bot.send_message(message.from_user.id, 'цена - 6000 за м^2', reply_markup=size_markup)
            size_markup.row('View Examples')

        markup = types.InlineKeyboardMarkup()
        if message.text == 'Instagram':
            btn_my_site = types.InlineKeyboardButton(text='Наш сайт', url='https://www.instagram.com/zelux.kz/?hl=en')
            markup.add(btn_my_site)
            bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)

        if message.text == 'Телефон':
            bot.send_message(message.chat.id, "Номер телефона", reply_markup=size_markup)

        if message.text == 'Офис 🏋️‍️':
            bot.send_message(message.chat.id, "Адрес", reply_markup=size_markup)
        if message.text == 'Бригада 🏅':
            bot.send_message(message.chat.id, "У нас работае сразу n кол-во бригад, вся работа регулируются дежурным дизайнером",
                             reply_markup=size_markup)
        if message.text == 'All in':
            bot.send_message(message.chat.id, "Акция Планировка + визуализация + отделка",
                             reply_markup=size_markup)
        if message.text == 'Адрес':
            bot.send_message(message.chat.id, "Адрес",
                             reply_markup=size_markup)

# SERVER SIDE
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://adbotcode.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))