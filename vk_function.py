import psycopg2
import vk_api
from vk_api.longpoll import VkLongPoll

with open('vk_group_token.txt', 'r') as file_objekt:
    GROP_TOKEN = file_objekt.read().strip()
with open('vktoken.txt', 'r') as file_objekt:
    USER_TOKEN = file_objekt.read().strip()

vk = vk_api.VkApi(token=GROP_TOKEN)
longpoll = VkLongPoll(vk)

conn = psycopg2.connect(dbname='vkinder', user='vkinder',
                        password='netology', host='localhost')
cursor = conn.cursor()


# получает информацию о пользователе
def get_info(user_id):
    user_id = user_id
    vk = vk_api.VkApi(token=GROP_TOKEN)
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


if __name__ == '__main__':
    print(get_info(552707168))
