import telebot
from telebot import types
from sql_api import StudentDB, check_db, print_tb


bot = telebot.TeleBot('1845923104:AAFKJhZWXCm3xPZPF6Sp6ehl7U-pvyMLgBc')
data_base = None
action = ""
table_to_clear = ""
insert_to = ""
user_id = ""
find_who = ""
delete_by = ""
delete_who = ""
update_who = ""
waiting_update_text = False
waiting_insert_text = False
waiting_find_text = False
waiting_delete_text = False


def create_keyboard(info: dict):
    keyboard = types.InlineKeyboardMarkup()
    for text, call_back in info.items():
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=call_back))
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global data_base, action, table_to_clear, waiting_insert_text, insert_to, find_who, waiting_find_text, \
        waiting_delete_text, delete_by, delete_who, update_who, waiting_update_text
    if call.data in ("empty_db", "default_db"):
        if check_db(user_id + ".sqlite"):
            bot.send_message(call.message.chat.id, 'Ошибка! У вас уже создана база данных!\n')
            return
        try:
            if call.data == "empty_db":
                data_base = StudentDB(name=user_id + ".sqlite", template=call.data)
                bot.send_message(call.message.chat.id, 'Пустая база данных успешно создана!')
            elif call.data == "default_db":
                data_base = StudentDB(name=user_id + ".sqlite", template=call.data)
                bot.send_message(call.message.chat.id, 'База данных по умолчанию успешно создана!')
        except Exception as e:
            bot.send_message(call.message.chat.id, f'Ошибка при создании базы данных\n{e}')
    elif call.data in ("yes", "no"):
        if data_base is not None and call.data == "yes":
            if action == "delete":
                try:
                    data_base.delete_data_base()
                    bot.send_message(call.message.chat.id, "База данных успешно удалена!")
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"Ошибка при удалении базы данных!\n{e}")
            elif action == "clear":
                try:
                    if table_to_clear == "students":
                        data_base.delete_student_table()  # CLEAR STUDENTS TABLE
                    if table_to_clear == "teacher":
                        pass  # CLEAR TEACHERS TABLE
                    if table_to_clear == "groups":
                        pass  # CLEAR GROUPS TABLE
                    if table_to_clear == 'all':
                        data_base.delete_all_tables()
                    bot.send_message(call.message.chat.id, "Очистка таблицы прошла успешно!")
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"Ошибка во время очистки таблицы({e}")
        elif call.data == "no":
            bot.send_message(call.message.chat.id, "База данных оставлена без изменений.")
        action = ""
        table_to_clear = ""
    elif call.data in ('students', 'teachers', 'groups', 'all'):
        table_to_clear = call.data
        question = 'Вы точно хотите очистить выбранную таблицу?'
        keyboard = create_keyboard({"Да": "yes",
                                    "Нет": "no"})
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data in ("student", "teacher", "group"):
        if call.data == "student":
            bot.send_message(call.message.chat.id, "Введите данные в следующем формате"
                                                   " (name, course, group_name, teacher_name)")
        elif call.data == "teacher":
            bot.send_message(call.message.chat.id, "Введите данные в следующем формате"
                                                   " (name, subject)")
        elif call.data == "group":
            bot.send_message(call.message.chat.id, "Введите данные в следующем формате"
                                                   " (group_name)")
        waiting_insert_text = True
        insert_to = call.data
    elif call.data in ("target_student", "target_teacher"):
        if call.data == "target_student":
            bot.send_message(call.message.chat.id, "Пока что я умею искать студентов только по имени группы!"
                                                   " Пожалуйста, введи имя группы")
        if call.data == "target_teacher":
            bot.send_message(call.message.chat.id, "Пока что я умею искать учителей только по предметам!"
                                                   " Пожалуйста, введи название предмета")
        find_who = call.data
        waiting_find_text = True
    elif call.data in ("delete_student", "delete_teacher", "delete_group"):
        delete_who = call.data
        if call.data == "delete_student":
            keyboard = create_keyboard({"По id": "by_id",
                                        "По имени": 'by_name'})
            question = "Как будем удалять?"
            bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data in ("by_id", "by_name"):
        if call.data == "by_id":
            bot.send_message(call.message.chat.id, "Введи id!")
        elif call.data == "by_name":
            bot.send_message(call.message.chat.id, "Введи имя!")
        waiting_delete_text = True
        delete_by = call.data
    elif call.data in ("update_student", "update_teacher"):
        if call.data == "update_student":
            bot.send_message(call.message.chat.id, "Пока что я умею менять только имя!). Введи id студента и новое имя "
                                                   "в формате (id name)")
        elif call.data == "update_teacher":
            bot.send_message(call.message.chat.id, "Пока что я умею менять только предмет!). "
                                                   "Введи название id учителя и название нового предмета в формате"
                                                   "(id name)")
        waiting_update_text = True
        update_who = call.data


def create_data_base(message):
    keyboard = create_keyboard({"Empty database": "empty_db",
                                "Default database": "default_db"})
    question = 'Выберете какую базу данных вы хотите создать?' \
               ' Пустую или заполненную некоторыми значениями по умолчанию.'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def delete_data_base(message):
    global action
    action = "delete"
    question = 'Вы точно хотите удалить базу данных?'
    keyboard = create_keyboard({"Да": "yes",
                                "Нет": "no"})
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def show_data_base(message):
    global data_base
    try:
        if data_base is not None:
            bot.send_message(message.chat.id, data_base.show_db())
        else:
            bot.send_message(message.chat.id, "Вышей базы данных не существует. Прежде чем посмотреть, создайте её!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка. Вышей базы данных не существует."
                                          f" Прежде чем посмотреть, создайте её!{e}")


def clear_data_base(message):
    global action
    action = "clear"
    keyboard_clear = create_keyboard({"Студенты": "students",
                                      "Учителя": "teachers",
                                      "Группы": "groups",
                                      "Все": "all"})
    question = 'Какую таблицу вы хотите почистить?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard_clear)


def insert_new_entry(message):
    keyboard = create_keyboard({"Студента": "student",
                                "Учителя": "teacher",
                                "Группу": "group"})
    question = "Кого будем добавлять в базу данных?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# студенты - по имени группы, учителей по предметам
def find_entry(message):
    keyboard = create_keyboard({"Студента": "target_student",
                                "Учителя": "target_teacher"})
    question = "Кого будем искать?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# студенты - по имени и по айди
def delete_entry(message):
    keyboard = create_keyboard({"Студента": "delete_student",
                                "Учителя": "delete_teacher",
                                "Группу": "delete_group"})
    question = "Кого будем удалять? Пока что я умею удалять только студента!"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# студентам имя, учителям предмат
def update_entry(message):
    keyboard = create_keyboard({"Студента": "update_student",
                                "Учителя": "update_teacher"})
    question = "Кого будем обновлять?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id, data_base, waiting_insert_text, insert_to, waiting_find_text, find_who, waiting_delete_text, \
        delete_by, delete_who, waiting_update_text, update_who
    if waiting_insert_text:
        waiting_insert_text = False
        try:
            params = message.text.split(" ")
            if insert_to == "student":
                params[1] = int(params[1])
                data_base.insert_student(params)  # STUDENT INSERT
            elif insert_to == "teacher":
                data_base.insert_teacher(params)  # TEACHER INSERT
            elif insert_to == "group":
                data_base.insert_group(params)   # GROUP INSERT
            bot.send_message(message.from_user.id, "Запись успешно добавлена!")
        except Exception as e:
            bot.send_message(message.from_user.id, f"Неправильный формат данных или ошибка вставки({e}")
        insert_to = ""
        return
    if waiting_find_text:
        waiting_find_text = False
        try:
            params = message.text.split(" ")
            result = ""
            if find_who == "target_student":
                result = data_base.find_students_by_group_name(params[0])  # FIND STUDENT
            if find_who == "target_teacher":
                result = data_base.find_teachers_by_subject(params[0])  # FIND TEACHER
            bot.send_message(message.from_user.id, "Вот, что я нешёл:\n" + print_tb(result))
        except Exception as e:
            bot.send_message(message.from_user.id, f"Неправильный формат данных или ошибка поиска({e}")
        find_who = ""
        return
    if waiting_delete_text:
        waiting_delete_text = False
        try:
            params = message.text.split(" ")
            if delete_who == "delete_student":
                # DELETE STUDENT
                if delete_by == "by_id":
                    data_base.delete_student(student_id=int(params[0]))  # DELETE STUDENT BY ID
                elif delete_by == "by_name":
                    data_base.delete_student(student_name=params[0])  # DELETE STUDENT BY NAME
            bot.send_message(message.from_user.id, "Запись успешно удалена!")
        except Exception as e:
            bot.send_message(message.from_user.id, f"Неправильный формат данных или ошибка во время удаления({e}")
        delete_by = ""
        delete_who = ""
        return
    if waiting_update_text:
        waiting_update_text = False
        try:
            params = message.text.split(" ")
            if update_who == "update_student":
                data_base.update_student_name(params)  # UPDATE STUDENT
            elif update_who == "update_teacher":
                data_base.update_teacher_subject(params)  # UPDATE TEACHER
            bot.send_message(message.from_user.id, "Запись успешно обновлена!")
        except Exception as e:
            bot.send_message(message.from_user.id, f"Неправильный формат данных или ошибка во время обновления({e}")
        update_who = ""
        return

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
        delete_data_base(message)
    elif message.text == "/show_data_base":
        show_data_base(message)
    elif message.text == "/clear_data_base":
        clear_data_base(message)
    elif message.text == "/insert_new_entry":
        insert_new_entry(message)
    elif message.text == "/update_entry":
        update_entry(message)
    elif message.text == "/find_entry":
        find_entry(message)
    elif message.text == "/delete_entry":
        delete_entry(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
