import vk_api
import time
import random
import threading
import pymysql.cursors
import datetime
import json
from vk_api.longpoll import VkLongPoll, VkEventType

# Подключение VkAPI и longpoll
vk = vk_api.VkApi(token="161457ab7ac3880dcab5b0fa0bbf2292939385764483825201659877aacd4e553b8840514adda1025bbd6")
vk._auth_token()
longpoll = VkLongPoll(vk)

timeError = "Введите время в формате 'HH:MM'"
examError = "Проверьте корректность введённого названия предмета"
weekDayError = "Проверьте корректность введённого дня недели"

keyboard = {"one_time": False, "buttons": [
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "Расписание"
        },
        "color": "primary"
    },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Проверка ответов"
            },
            "color": "primary"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Поддержка"
            },
            "color": "primary"
        }]]}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

info = "Снизу появился список моих возможностей, нажми на любую из них чтобы узать подробнее о каждой"
schedule = "Используй это функцию чтобы добавить день для занятий" \
           "\n Напиши !schedule, а так же название предмета, день недели и время занятия" \
           "\n Пример: \n !schedule \n математика пятница 08:00 \n Или для удаления, используя DEL " \
           "\n Пример: \n !schedule DEL \n математика пятница 08:00"
check = "Используй эту функцию для проверки ответов" \
        "\n Напиши !check, а так же название предмета, номер теста и ответы на задания" \
        "\n Пример: \n !check \n математика 2019-07-25 \n 12 23 34 abc а1"
support = "Используй эту функцию чтобы сообщить о проблемах в моей работе или предложить что-то новое" \
          "\n Напиши !support и подробно опиши проблему в этом же сообщении"

exams = {"математика": "math", "математика база": "mathb", "русский язык": "rus", "английский язык": "en",
         "немецкий язык": "de", "французский язык": "fr", "испанский язык": "sp", "физика": "phys",
         "химия": "chem", "биология": "bio", "география": "geo", "обществознание": "soc",
         "литература": "lit", "информатика": "inf", "история": "hist", "math": "математика",
         "mathb": "математика база", "rus": "русский язык", "en": "английский язык",
         "de": "немецкий язык", "fr": "французский язык", "sp": "испанский язык", "phys": "физика",
         "chem": "химия", "bio": "биология", "geo": "география", "soc": "обществознание",
         "lit": "литература", "inf": "информатика", "hist": "история"}

weekDays = {"понедельник": "Monday", "вторник": "Tuesday", "среда": "Wednesday", "четверг": "Thursday",
            "пятница": "Friday", "суббота": "Saturday", "воскресенье": "Sunday"}


# Проверка строки времени
def checktime(strTime):
    try:
        datetime.datetime.strptime(strTime, '%H:%M')
    except ValueError:
        raise ValueError("Incorrect time format, should be HH:MM")


# Отпрака сообщений
def snd_msg(user_id, message):
    vk.method('messages.send', {'peer_id': user_id, 'message': message, 'random_id': random.randint(1, 2147483647)})

# Подключение mySQL
connection = pymysql.connect(host='localhost', user='root', password='gs651zv3mlt8@#GHCZ', db='ege_bot', charset='utf8mb4')
cursor = connection.cursor()
print("SUCCESSFULLY CONNECTED")

# Таблица юзеров
usersQuery = (""" 
              SELECT id, exam, weekDay, timeExam FROM users
              """)
cursor.execute(usersQuery)
resultsUsers = cursor.fetchall()

# Таблица тестов
testsQuery = ("""
              SELECT id, exam, numberTest FROM tests 
              """)
cursor.execute(testsQuery)
resultsTests = cursor.fetchall()

# Таблица ответов
answerQuery = (""" SELECT exam, numberTest, ans_1, ans_2,ans_3,ans_4,ans_5,ans_6,ans_7,ans_8,ans_9,
               ans_10,ans_11,ans_12,ans_13,ans_14,ans_15,ans_16,ans_17,ans_18, ans_19,ans_20,ans_21,ans_22,
               ans_23,ans_24,ans_25 FROM answers """)
cursor.execute(answerQuery)
resultsAnswer = cursor.fetchall()


# Второй поток
def secondThread():
    while True:
        now = datetime.datetime.now()
        nowDay = now.strftime("%A")
        nowDate = now.strftime("%Y-%m-%d")
        nowTime = now.strftime("%H:%M:%S")
        time.sleep(1)

        for resUsers in resultsUsers:
            if resUsers[2] == nowDay:
                if str(resUsers[3]) == nowTime:
                    print('time okk')
                    for resTests in resultsTests:
                        if resUsers[1] == resTests[1]:

                            print('name okk')
                            if str(resTests[2]) == nowDate:
                                print('date okk')
                                exam = exams[resUsers[1]]
                                msg_exam = "Сегодня " + exam + "\nВот вариант: "
                                test = resTests[0]
                                vk.method('messages.send', {'peer_id': resUsers[0], 'message': msg_exam,
                                                            'attachment': test,
                                                            'random_id': random.randint(1, 2147483647)})


# Maltreating
ans_msg = threading.Thread(target=secondThread, name="answer", args=())
ans_msg.start()

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text.lower() == "!info":
                vk.method("messages.send", {"peer_id": event.peer_id, "message": info, "random_id": 0,
                                            "keyboard": keyboard})
            elif event.text.lower() == "расписание":
                snd_msg(event.user_id, schedule)
            elif event.text.lower() == "проверка ответов":
                snd_msg(event.user_id, check)
            elif event.text.lower() == "поддержка":
                snd_msg(event.user_id, support)
            elif event.text.lower() == 'привет' \
                    or event.text.lower() == "здравствуй" \
                    or event.text.lower() == 'добрый день':
                snd_msg(event.user_id, "Привет!")
            elif event.text.lower() == 'пока' \
                    or event.text.lower() == 'до свидания':
                snd_msg(event.user_id, "Возвращайся скорее!")
            elif "!check" in event.text:
                event.text = event.text.split()
                for resAnswer in resultsAnswer:
                    if event.text[1].lower() in exams:
                        event.text[1] = exams[event.text[1]]
                        if resAnswer[1] == event.text[1]:
                            if resAnswer[2] == event.text[2]:
                                resAnswer = list(resAnswer)
                                del event.text[0:3]
                                del resAnswer[0:3]
                                wrongAnswer = []
                                wrongNumber = []
                                rightAnswer = []
                                for i in range(len(event.text)):
                                    if event.text[i] != resAnswer[i]:
                                        wrongAnswer.append(event.text[i])
                                        rightAnswer.append(str(resAnswer[i]))
                                        wrongNumber.append(str(i + 1))
                                if not wrongAnswer:
                                    snd_msg(event.user_id, "Молодец, у тебя нет ни одной ошибки!")
                                else:
                                    answerTest = 'У тебя ошибки в номерах: ' + ', '.join(wrongNumber) + '\n' + \
                                                 'Правильные ответы в этих номерах:  ' + ', '.join(rightAnswer)
                                    snd_msg(event.user_id, answerTest)
                            else:
                                snd_msg(event.user_id, "Проверьте корректность введённого номера варианта")
                    else:
                        snd_msg(event.user_id, "Проверьте корректность введённого названия пердмета")

            elif "!schedule" in event.text:
                event.text = event.text.split()
                id = event.user_id
                if event.text[1].lower() == "del":
                    try:
                        if event.text[2].lower() in exams:
                            exam = exams[event.text[2].lower()]
                            if event.text[3].lower() in weekDays:
                                weekDay = weekDays[event.text[3].lower()]
                                if checktime(event.text[4]) is None:
                                    timeExam = event.text[4]
                                    cursor.execute("""
                                                DELETE FROM users
                                                WHERE
                                                (id=%s AND exam=%s AND weekDay=%s AND timeExam=%s)""",
                                                   (id, exam, weekDay, timeExam))
                                    connection.commit()
                                    connection.close()
                                    connection = pymysql.connect(host='localhost', user='root', password='gs651zv3mlt8@#GHCZ',
                                                                 db='ege_bot', charset='utf8mb4')
                                    cursor = connection.cursor()
                                    print("SUCCESSFULLY CONNECTED")

                                    # Таблица юзеров
                                    usersQuery = (""" 
                                                  SELECT id, exam, weekDay, timeExam FROM users
                                                  """)
                                    cursor.execute(usersQuery)

                                    resultsUsers = cursor.fetchall()
                                    snd_msg(event.user_id, "Запись успешно удалена")
                                else:
                                    snd_msg(event.user_id, timeError)
                            else:
                                snd_msg(event.user_id, weekDayError)
                        else:
                            snd_msg(event.user_id, examError)
                    except:
                        snd_msg(event.user_id, "Извините, не удалось удалить запись"
                                               "\nПожалуйста повторите попытку позже")
                else:
                    try:
                        if event.text[1].lower() in exams:
                            exam = exams[event.text[1].lower()]
                            if event.text[2].lower() in weekDays:
                                weekDay = weekDays[event.text[2].lower()]
                                if checktime(event.text[3]) is None:
                                    timeExam = event.text[3]
                                    cursor.execute("""
                                                INSERT INTO users (id, exam, weekDay, timeExam)
                                                VALUES
                                                (%s, %s, %s, %s)""", (id, exam, weekDay, timeExam))
                                    connection.commit()
                                    connection.close()
                                    connection = pymysql.connect(host='localhost', user='root', password='gs651zv3mlt8@#GHCZ',
                                                                 db='ege_bot', charset='utf8mb4')
                                    cursor = connection.cursor()
                                    print("SUCCESSFULLY CONNECTED")

                                    # Таблица юзеров
                                    usersQuery = (""" 
                                                                                      SELECT id, exam, weekDay, timeExam FROM users
                                                                                      """)
                                    cursor.execute(usersQuery)

                                    resultsUsers = cursor.fetchall()
                                    snd_msg(event.user_id, "Запись успешно добавлена")
                                else:
                                    snd_msg(event.user_id, timeError)
                            else:
                                snd_msg(event.user_id, weekDayError)
                        else:
                            snd_msg(event.user_id, examError)
                    except:
                        snd_msg(event.user_id, "Извините, не удалось добавить запись "
                                               "\nПожалуйста повторите попытку позже")
            elif "!support" in event.text:
                snd_msg(292171486, event.text)
                snd_msg(event.user_id, 'Спасибо за ваше сообщение! \nЯ передам это своему создателю')
            else:
                snd_msg(event.user_id, 'К сожалению отвечать на это меня ещё не научили')
except Exception as E:
    time.sleep(1)
