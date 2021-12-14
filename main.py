from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from database import reg_user, chek_user
from vk_function import search_users

with open('vk_group_token.txt', 'r') as file_objekt:
    GROP_TOKEN = file_objekt.read().strip()
token = GROP_TOKEN


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id} хочешь найти себе пару?\n"
                                         f"Для начала поиска напиши СТАРТ")
            elif request == "старт":
                user_ = chek_user(event.user_id)
                if user_ == None:
                    reg_user(event.user_id)  # Добавляет пользователя в БД
                write_msg(event.user_id, f"Для поиска партнера необходимо больше узнать о твоих предпочтениях. \n"
                          f"Сначала напиши пол партнера женщина  или мужчина")
            elif request == "женщина":
                sex = 1
                write_msg(event.user_id, f"Укажи минимальный возраст")
            elif request == "мужчина":
                sex = 2
                write_msg(event.user_id, f"Укажи минимальный возраст")
            elif int(request) < 18:
                write_msg(event.user_id, f"Минимальный возраст 18 лет")
            elif int(request) >= 18:
                age_from = int(request)
                write_msg(event.user_id, f"Укажи максимальный возраст партнера")
            elif 18 <= int(request) < 100:
                age_to = int(request)
                write_msg(event.user_id, f"Укажи город")
            elif request != None:
                city = request
                people = search_users(sex, age_from, age_to, city)
                write_msg(event.user_id, f"{people}")
            elif not 18 <= int(request) < 100:
                write_msg(event.user_id, f"Укажи возраст в интервале от 18 до 100 лет :)")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")