import vk_api
from settings import GROUP_TOKEN, USER_TOKEN
from random import randrange
from vk_api.longpoll import VkLongPoll
import json
import datetime


# получает информацию о пользователе
def get_info(user_id):
    user_id = user_id
    vk = vk_api.VkApi(token=GROUP_TOKEN)
    response = vk.method('users.get', {'user_ids': user_id, 'fields': 'city, sex, bdate'})
    user_info = [response[0]['id'], response[0]['first_name'], response[0]['last_name'],
                 response[0]['sex'], response[0]['city']['title'], f'https://vk.com/id{response[0]["id"]}']
    return user_info


# Ищет людей по критериям
def search_users(sex, age_from, age_to, city):
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk = vk_api.VkApi(token=USER_TOKEN)
    response = vk.method('users.search',
                         {'sort': 1,
                          'sex': sex,
                          'status': 1,
                          'age_from': age_from,
                          'age_to': age_to,
                          'has_photo': 1,
                          'count': 25,
                          'online': 1,
                          'hometown': city
                          })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
    return all_persons


# Ищет фото людей
def get_photo(owner_id):
    try:
        vk = vk_api.VkApi(token=USER_TOKEN)
        response = vk.method('photos.get',
                             {'owner_id': owner_id,
                              'album_id': 'profile',
                              'count': 10,
                              'extended': 1,
                              'photo_sizes': 1})
        users_photos = []
        for i in range(len(response['items'])):
            users_photos.append(
                [response['items'][i]['likes']['count'],
                 response['items'][i]['sizes'][-1]['url']])
        return users_photos
    except(vk_api.exceptions.ApiError, TypeError):
        pass


# Сортирует фото по лайкам
def sort_photo(photo_list):
    try:
        sort_list = sorted(photo_list, key=lambda x: int(x[0]), reverse=True)
        return sort_list[:3]
    except(vk_api.exceptions.ApiError, TypeError):
        return ['нет фото']

def get_long_poll(token):
    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)
    return longpoll

def write_msg(user_id, message):
    vk_api.VkApi(token=GROUP_TOKEN).method('messages.send',
                                           {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

# создает файл json по результатам поиска
def create_json(lst):
    today = datetime.date.today()
    today_str = f'{today.day}.{today.month}.{today.year}'
    result = {}
    result_list = []
    for num, info in enumerate(lst):
        result['data'] = today_str
        result['first_name'] = info[0]
        result['second_name'] = info[1]
        result['link'] = info[2]
        result['id'] = info[3]
        result_list.append(result.copy())
    with open("result.json", "a", encoding='UTF-8') as write_file:
        json.dump(result_list, write_file, ensure_ascii=False)
    print('Информация с результатами поиска успешно записана в json файл.')


if __name__ == '__main__':
    print(get_info(552707168))
