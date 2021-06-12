import telebot
from telebot import types
from sql_api import StudentDB, check_db


bot = telebot.TeleBot('1845923104:AAFKJhZWXCm3xPZPF6Sp6ehl7U-pvyMLgBc')
data_base = None
user_id = ""


def create_data_base(message):
    keyboard = types.InlineKeyboardMarkup()
    key_empty_db = types.InlineKeyboardButton(text='Empty database', callback_data='empty_db')
    keyboard.add(key_empty_db)
    key_default_db = types.InlineKeyboardButton(text='Default database', callback_data='default_db')
    keyboard.add(key_default_db)
    question = 'Выберете какую базу данных вы хотите создать?' \
               ' Пустую или заполненную некоторыми значениями по умолчанию.'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in ("empty_db", "default_db"):
        if check_db(user_id + ".sqlite"):
            bot.send_message(call.message.chat.id, 'Ошибка! У вас уже создана база данных!\n')
            return
        global data_base
        try:
            if call.data == "empty_db":
                data_base = StudentDB(name=user_id + ".sqlite", template=call.data)
                bot.send_message(call.message.chat.id, 'Пустая база данных успешно создана!')
            elif call.data == "default_db":
                data_base = StudentDB(name=user_id + ".sqlite", template=call.data)
                bot.send_message(call.message.chat.id, 'База данных по умолчанию успешно создана!')
        except Exception as e:
            bot.send_message(call.message.chat.id, f'Ошибка при создании базы данных\n{e}')


def delete_data_base():
    pass


def show_data_base():
    global data_base
    if data_base is not None:
        data_base.show_db()


def clear_data_base():
    pass


def insert_new_entry():
    pass


def find_entry():
    pass


def delete_entry():
    pass


def update_entry():
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id, data_base
    if user_id == "":
        user_id = str(message.from_user.id)
        if check_db(user_id + ".sqlite"):
            data_base = StudentDB(user_id + ".sqlite")
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Привет! Я твой помощник в работе с базой данных студентов!\n"
                                               "Вот, что я умею:\n"
                                               "/help - помощь.\n"
                                               "/start - начать со мной общение.\n"
                                               "/create_data_base - создать базу данных.\n"
                                               "/delete_data_base - удалить базу данных.\n"
                                               "/show_data_base - показать базу данных.\n"
                                               "/clear_data_base - почистить базу данных.\n"
                                               "/insert_new_entry - добавить запись в базу данных.\n"
                                               "/update_entry - обновить запись в базе данных.\n"
                                               "/find_entry - поиск записи в базе данных.\n"
                                               "/delete_entry - удаление записи в базе данных.\n")
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Я обработчик базы данных студентов! Если хочешь узнать,"
                                               " что я умею, напиши /help!")
    elif message.text == "/create_data_base":
        create_data_base(message)
    elif message.text == "/delete_data_base":
        delete_data_base()
    elif message.text == "/show_data_base":
        show_data_base()
    elif message.text == "/clear_data_base":
        clear_data_base()
    elif message.text == "/insert_new_entry":
        insert_new_entry()
    elif message.text == "/update_entry":
        update_entry()
    elif message.text == "/find_entry":
        find_entry()
    elif message.text == "/delete_entry":
        delete_entry()
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
