import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import psycopg2


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
    # age = datetime.datetime.now() - int(response[0]['bdate'])
    user_info = [response[0]['id'], response[0]['first_name'], response[0]['last_name'],
                 response[0]['sex'], response[0]['city']['title']]
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
    vk = vk_api.VkApi(token=USER_TOKEN)
    response = vk.method('photos.get',
                        {'owner_id': owner_id,
                        'album_id': 'profile',
                        'count': 10,
                        'extended': 1,
                        'photo_sizes': 1})
    user_photo = []
    # for i in range(response['count']):
    print(response)
    # print([response['items'][0]['likes']['count'],
    #              'photo' + str(response['items'][0]['owner_id']) + '_' + str(response['items'][0]['id']), str(response['items'][0]['sizes']['url'])])
    print(response['items'][0]['sizes'][-1]['url'])





if __name__ == '__main__':
    search_users('1', '18', '36', 'Тула')
    get_photo(1)