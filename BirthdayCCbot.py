import telebot
import datetime
from telebot.types import BotCommand
import schedule
import time 
import threading

# Токен, который ты получил от BotFather
TOKEN = "7866073916:AAE9XLKVNWSv79cHkw0RP4aKTmwi-nARBjQ"

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для перевода названий месяцев из родительного падежа в именительный
month_nominative = {
    "января": "Январь", "февраля": "Февраль", "марта": "Март", "апреля": "Апрель",
    "мая": "Май", "июня": "Июнь", "июля": "Июль", "августа": "Август",
    "сентября": "Сентябрь", "октября": "Октябрь", "ноября": "Ноябрь", "декабря": "Декабрь"
}

# Словарь для перевода названий месяцев из именительного падежа в родительный
month_genitive = {
    "январь": "января", "февраль": "февраля", "март": "марта", "апрель": "апреля",
    "май": "мая", "июнь": "июня", "июль": "июля", "август": "августа",
    "сентябрь": "сентября", "октябрь": "октября", "ноябрь": "ноября", "декабрь": "декабря"
}

# Словарь для перевода английских названий месяцев на русский (именительный падеж)
month_english_to_russian = {
    "january": "январь", "february": "февраль", "march": "март", "april": "апрель",
    "may": "май", "june": "июнь", "july": "июль", "august": "август",
    "september": "сентябрь", "october": "октябрь", "november": "ноябрь", "december": "декабрь"
}

# Данные о днях рождения сотрудников (измененные)
birthdays = {
    "Волкова Александра": "2024-01-08",
    "Артемьева Анна": "2024-01-11",
    "Минченко Софья": "2024-02-07",
    "Пегова Алина": "2024-02-07",
    "Храмов Владислав": "2024-03-05",
    "Киселев Петр": "2024-03-08",
    "Юнусова Алина": "2024-03-28",
    "Фондиков Никита": "2024-04-01",
    "Семчук Валерия": "2024-04-04",
    "Галкин Никита": "2024-04-13",
    "Бильданов Ян": "2024-05-15",
    "Павлов Максим": "2024-05-28",
    "Эебердыева Майя Мурадовна": "2024-05-29",
    "Пугачева Ирина Алексеевна": "2024-06-13",
    "Кравченко Полина": "2024-06-23",
    "Неведомская Александра": "2024-07-01",
    "Фролова Соня": "2024-07-01",
    "Комиссарова Екатерина": "2024-07-13",
    "Кулик Елена": "2024-07-22",
    "Юдина Евгения": "2024-07-23",
    "Рахимов Тимур": "2024-07-28",
    "Туркиа Александр": "2024-07-28",
    "Ложкомоев Никита": "2024-08-16",
    "Третьякова Светлана": "2024-09-06",
    "Никоненко Анастасия": "2024-09-09",
    "Катькина Яна": "2024-09-14",
    "Карташов Владислав": "2024-10-10",
    "Джангаров Артем": "2024-10-11",
    "Суринова Полина": "2024-10-14",
    "Мхитарян Аксель": "2024-10-20",
    "Щеренко Арина": "2024-10-26",
    "Ларина Виктория": "2024-11-15",
    "Лазырин Михаил Сергеевич": "2024-11-19",
    "Садикова Екатерина": "2024-11-27",
    "Хныкова Диана": "2024-12-10",
    "Пассер Дарья": "2024-12-15",
    "Гриб Екатерина": "2024-12-27"
}

# Словарь для хранения состояния пользователя (для отслеживания, какую информацию он должен ввести)
user_state = {}

# Множество для хранения всех подписчиков
subscribers = set()

# Команда для показа даты день рождения конкретного сотрудника
@bot.message_handler(commands=['birthday_info'])
def birthday_info(message):
    user_id = message.from_user.id
    user_state[user_id] = 'waiting_for_name'  # Устанавливаем состояние ожидания имени
    bot.reply_to(message, "Пожалуйста, введите Фамилия Имя (Например, Иванов Иван) участника для получения информации о дне рождения:")

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'waiting_for_name')
def process_birthday_info(message):
    user_id = message.from_user.id
    name = message.text.strip()

    # Словарь для перевода номеров месяцев в родительный падеж
    month_names_russian = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля",
        8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    if name in birthdays:
        # Преобразуем строку с датой в объект даты
        birthday_date = datetime.datetime.strptime(birthdays[name], "%Y-%m-%d").date()
        # Извлекаем день и месяц
        day = birthday_date.day
        month = month_names_russian[birthday_date.month]
        # Формируем строку ответа
        formatted_date = f"{day} {month}"
        bot.reply_to(message, f"{name.title()} родился(лась) {formatted_date}.")
    else:
        bot.reply_to(message, f"Информация о дне рождения для '{name.title()}' не найдена.")

    user_state[user_id] = None  # Сбрасываем состояние пользователя

# Команда для показа дней рождений в указанном месяце
@bot.message_handler(commands=['birthdays_in_month'])
def birthdays_in_month(message):
    user_id = message.from_user.id
    user_state[user_id] = 'waiting_for_month'  # Устанавливаем состояние ожидания месяца
    bot.reply_to(message, "Пожалуйста, введите название месяца для получения списка дней рождений:")

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'waiting_for_month')
def process_birthdays_in_month(message):
    user_id = message.from_user.id
    month = message.text.strip().lower()

    # Словарь для перевода названий месяцев из именительного падежа в числовой формат
    month_names_to_number = {
        "январь": "01", "февраль": "02", "март": "03", "апрель": "04",
        "май": "05", "июнь": "06", "июль": "07", "август": "08",
        "сентябрь": "09", "октябрь": "10", "ноябрь": "11", "декабрь": "12"
    }

    # Словарь для перевода названий месяцев в родительный падеж (для даты рождения)
    month_genitive = {
        "январь": "января", "февраль": "февраля", "март": "марта", "апрель": "апреля",
        "май": "мая", "июнь": "июня", "июль": "июля", "август": "августа",
        "сентябрь": "сентября", "октябрь": "октября", "ноябрь": "ноября", "декабрь": "декабря"
    }

    # Словарь для перевода названий месяцев в предложный падеж (для заголовка)
    month_prepositional = {
        "январь": "январе", "февраль": "феврале", "март": "марте", "апрель": "апреле",
        "май": "мае", "июнь": "июне", "июль": "июле", "август": "августе",
        "сентябрь": "сентябре", "октябрь": "октябре", "ноябрь": "ноябре", "декабрь": "декабре"
    }

    month_number = month_names_to_number.get(month, None)

    if month_number is None:
        bot.reply_to(message, f"Месяц '{month}' не распознан. Пожалуйста, введите корректное название месяца.")
        return

    birthdays_in_month = []

    for name, birthday_str in birthdays.items():
        birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d").date()
        if birthday.strftime('%m') == month_number:
            day = birthday.day
            # Используем родительный падеж для даты рождения
            month_russian = month_genitive[month]
            formatted_date = f"{day} {month_russian}"
            birthdays_in_month.append(f"{name}: {formatted_date}")

    if birthdays_in_month:
        # Используем предложный падеж для заголовка
        response = f"Дни рождения в {month_prepositional[month]}:\n" + "\n".join(birthdays_in_month)
    else:
        response = f"Нет дней рождения в {month_prepositional[month]}."

    bot.reply_to(message, response)
    user_state[user_id] = None  # Сбрасываем состояние пользователя

# Команда для показа ближайших дней рождений
@bot.message_handler(commands=['check_birthdays'])
def check_birthdays(message):
    today = datetime.datetime.now().date()
    upcoming_birthdays = []
    for name, birthday_str in birthdays.items():
        birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d").date()
        birthday_this_year = birthday.replace(year=today.year)
        delta_days = (birthday_this_year - today).days
        if 0 <= delta_days <= 7:
            day = birthday_this_year.day
            month_russian = month_genitive[birthday_this_year.month]
            formatted_date = f"{day} {month_russian}"
            upcoming_birthdays.append(f"{name}: {formatted_date}")
    
    if upcoming_birthdays:
        response = "Ближайшие дни рождения:\n" + "\n".join(upcoming_birthdays)
    else:
        response = "На этой неделе нет дней рождения."
    
    bot.reply_to(message, response)

# Устанавливаем доступные команды и их описание
def set_bot_commands():
    commands = [
        BotCommand("/start", "Начать работу с ботом"),
        BotCommand("/check_birthdays", "Узнать ближайшие дни рождения на неделю"),
        BotCommand("/help", "Я могу помочь вам отслеживать дни рождения участников. Вот список доступных команд:"),
        BotCommand("/birthday_info", "Узнать дату рождения участника, например: /birthday_info Иванов Иван"),
        BotCommand("/birthdays_in_month", "Узнать дни рождения участников в конкретном месяце, например: /birthdays_in_month октябрь")
    ]
    bot.set_my_commands(commands)

# Вызываем установку команд при старте бота
set_bot_commands()

# Команда /start для добавления пользователя в список подписчиков
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    subscribers.add(user_id)  # Добавляем пользователя в список
    welcome_text = (
        "Привет! Я BirthdayCCbot. Я буду уведомлять о днях рождения участников Case Club RUDN!\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом и получить список всех команд.\n"
        "/help - Я могу помочь вам отслеживать дни рождения участников. Вот список доступных команд:\n"
        "/check_birthdays - Узнать, у кого из участников день рождения в ближайшие 7 дней.\n"
        "/birthday_info Фамилия Имя - Узнать дату рождения конкретного участника.\n"
        "/birthdays_in_month название месяца - Показать дни рождения участников в указанном месяце."
    )
    bot.reply_to(message, welcome_text)

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я могу помочь вам отслеживать дни рождения участников. Вот список доступных команд:\n"
        "/start - Начать работу с ботом.\n"
        "/check_birthdays - Узнать ближайшие дни рождения участников.\n"
        "/birthday_info Фамилия Имя - Узнать дату рождения конкретного участника.\n"
        "/birthdays_in_month название месяца - Узнать дни рождения в указанном месяце."
    )
    bot.reply_to(message, help_text)

# Кому будет осуществляться рассылка
subscribers = set()  # Здесь будут храниться все подписчики

# Добавляем всех пользователей в список подписчиков
@bot.message_handler(func=lambda message: True)
def track_users(message):
    user_id = message.from_user.id
    subscribers.add(user_id)
    print(f"Добавлен новый подписчик с user_id: {user_id}")

# Словарь для перевода номеров месяцев в родительный падеж
month_names_russian = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля",
    8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

month_number_to_name = {
    1: "январь", 2: "февраль", 3: "март", 4: "апрель", 5: "май", 6: "июнь",
    7: "июль", 8: "август", 9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
}

# Функция для автоматической проверки дней рождений
def check_birthdays_auto():
    today = datetime.date.today()  # Текущая дата
    print(f"Сегодня: {today}")  # Выводим текущую дату

    for name, birthday_str in birthdays.items():
        birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d").date()
        birthday_this_year = birthday.replace(year=today.year)
        days_until_birthday = (birthday_this_year - today).days

        # Выводим информацию о расчете разницы в днях для каждого участника
        print(f"До дня рождения {name} осталось: {days_until_birthday} дней")

        # Преобразуем числовое значение месяца в строку
        month_name = month_number_to_name[birthday_this_year.month]

        # Теперь используем строковое значение месяца для доступа к month_genitive
        month_russian = month_genitive[month_name]

        # Уведомление за 1 день до дня рождения
        if days_until_birthday == 1:
            day = birthday_this_year.day
            formatted_date = f"{day} {month_russian}"

            # Отправляем уведомление каждому подписчику
            for user_id in subscribers:
                bot.send_message(user_id, f"Завтра свой день рождения празднует {name}! ({formatted_date})")

        # Уведомление в сам день рождения
        elif days_until_birthday == 0:
            for user_id in subscribers:
                bot.send_message(user_id, f"Сегодня свой день рождения празднует {name}! Поздравляем с днем рождения!")

# Настройка расписания с помощью библиотеки schedule
schedule.every().day.at("09:00").do(check_birthdays_auto)

# Основной цикл для работы с schedule
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Запуск отдельного потока для работы schedule
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

# Запуск бота
bot.polling()
