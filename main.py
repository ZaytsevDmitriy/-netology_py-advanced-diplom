import re

from vk_api.longpoll import VkEventType

from database import reg_user, chek_user, chek_user_black_list, add_user_black_list, add_user_profile, add_photo
from vk_function import search_users, get_photo, sort_photo, get_info, get_long_poll, write_msg, create_json
from settings import GROUP_TOKEN




def chek_pattern(patern, string_):  # проверяет строку на соответствие патерну
    result = re.match(patern, string_)
    if result is not None:
        return True


def get_search_params(string_):  # формирует список параметров
    params_list = string_.split(' ')
    if params_list[0] == 'женщина' or 'девушка':
        params_list[0] = '1'
    elif params_list[0] == 'мужчина' or 'парень':
        params_list[0] = '2'
    else:
        params_list[0] = '0'
    if int(params_list[1][:2]) < 18:
        write_msg(event.user_id, "Минимальный возраст 18 лет")
    elif int(params_list[1][3:]) > 100:
        write_msg(event.user_id, "Максимальный возраст 100 лет")
    else:
        return params_list




if __name__ == '__main__':

    for event in  get_long_poll(GROUP_TOKEN).listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id} хочешь найти пару?\n"
                                             f"Да или Нет")
                elif request == "да":
                    user_ = chek_user(event.user_id)
                    if user_ is None:
                        reg_user(event.user_id)  # Добавляет пользователя в БД
                    write_msg(event.user_id, f"Для поиска партнера необходимо больше узнать о твоих предпочтениях. \n"
                                             f"Напиши пол, возраст и город партнера.\n"
                                             f"Например  женщина 18-30 Москва\n")
                elif chek_pattern(r'[а-я]{7}\s\d{2}-\d{2}\s[а-я]+', request) is True:  # выводит анкеты
                    params = get_search_params(request)
                    people = search_users(params[0], params[1][:2], params[1][3:], params[2])
                    create_json(people)
                    for i in people:
                        id_ = int(i[-1])
                        user_black_list = chek_user_black_list(id_)
                        if user_black_list is None:
                            photo_list = get_photo(id_)
                            sort_list = sort_photo(photo_list)
                            write_msg(event.user_id, f"{str(i[0])} {i[1]} {i[2]}")
                            for photo in sort_list:
                                write_msg(event.user_id, f"{str(photo[1])}")
                    write_msg(event.user_id, f"Для того чтобы добавить анкету в черный список набери ЧС и ID\n"
                                             f"Например - ЧС 1\n"
                                             f"Для того чтобы добавить анкету в избранное набери ДИ и ID\n"
                                             f"Например - ДИ 1\n"
                              )
                elif chek_pattern(r'[ч][с]\s*\d+', request) is True:  # Добавляет в ЧС
                    id_ = request.split(' ')[1]
                    list_ = get_info(id_)
                    add_user_black_list(list_)
                    write_msg(event.user_id, f"{list_[1:3]} в ЧС")
                elif chek_pattern(r'[д][и]\s*\d+', request) is True:  # Добавляет в избранное
                    id_ = request.split(' ')[1]
                    list_ = get_info(id_)
                    add_user_profile(list_)
                    add_photo(id_)
                    write_msg(event.user_id, f"{list_[1:3]} в избранном")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
