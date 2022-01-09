import pytest

from vk_function import get_info, search_users, get_photo, sort_photo


class TestVkinder:

    def setup_class(self):
        print('method setup_class')

    def setup(self):
        print('method setup')

    def teardown(self):
        print('method teardown')

    # Проверка получения информации о пользователе
    @pytest.mark.parametrize('user_id, result', [
        ('1', [1, 'Павел', 'Дуров', 2, 'Санкт-Петербург', 'https://vk.com/id1'])])
    def test_get_info(self, user_id, result):
        assert get_info(user_id) == result

    # Проверка поиска анкет
    @pytest.mark.parametrize('sex, age_from, age_to, city, result', [
        ('1', '18', '21', 'Москва', True)])
    def test_search_users(self, sex, age_from, age_to, city, result):
        assert bool(search_users(sex, age_from, age_to, city)) == result

    # Тест поиска фотографий
    @pytest.mark.parametrize('user_id, result', [('1', True)])
    def test_get_photo(self, user_id, result):
        assert bool(get_photo(user_id)) == result

    # Тест сортировки по количеству лайков
    @pytest.mark.parametrize('list_photos, result',
                             [(['1', '3', '2'],
                               ['3', '2', '1'])])
    def test_sort_photo(self, list_photos, result):
        assert sort_photo(list_photos) == result
