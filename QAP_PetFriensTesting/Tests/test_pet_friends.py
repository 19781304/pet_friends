import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_invalid_credentials(email='invalid_email', password='invalid_password'):
    """ Проверяем что запрос api ключа с неверными данными возвращает статус не 200 """
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_add_pet_with_invalid_image_format(name='Геннадий', animal_type='крокодил', age='3', pet_photo=r'C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Миша1'):
    """ Проверяем что происходит при добавлении питомца с некорректным форматом изображения """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert 'name' not in result


def test_add_pet_with_missing_fields(name='Вася', animal_type='', age='',pet_photo=r'C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Гена.jpg'):
    """ Проверяем что происходит при добавлении питомца с пропущенными обязательными полями """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    assert status != 200
    assert 'pets'not in result

def test_add_pet_with_excessive_age(name='12345', animal_type='12345', age='1', pet_photo=r'C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Гена.jpg'):
    """ Проверяем что происходит при добавлении питомца с вводом цыфр в обязательные поля вместо букв """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert 'pets'not in result


def test_get_pet_info_with_invalid_pet_id():
    """ Проверяем что происходит при запросе информации о питомце с неверным ID """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    invalid_pet_id = '12345invalid'
    status, result = pf.get_pet_info(auth_key, invalid_pet_id)
    assert status != 200
    assert 'pets'not in result

def test_update_pet_info_with_invalid_data():
    """ Проверяем что происходит при обновлении данных питомца с некорректными данными """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], '', '', -1)
        assert status != 200
        assert 'pets' not in result

def test_filter_pets_by_my_pets():
    """Проверяем, что фильтр 'my_pets' возвращает только своих питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')

    assert status == 200
    assert 'pets' in result, "Ответ не содержит ключ 'pets'"


    assert all('id' in pet for pet in result['pets']), "В данных о питомцах отсутствует 'id'"


def test_add_new_pet_with_valid_data(name='Геннадий', animal_type='крокодил',
                                     age='4', pet_photo= r'C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Гена.jpg'):
    """Проверю что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pets'] == new_pets




def test_update_pet_info_when_no_pets():
    """ Проверяю что происходит при попытке обновить информацию о питомце, когда питомцы отсутствуют """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        try:
            pf.update_pet_info(auth_key, 'nonexistent_pet_id', 'NewName', 'NewType', 5)
        except Exception as e:
            assert str(e) == "There is no my pets"


def test_delete_my_pet():
    """Проверяю, что питомец успешно удаляется"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')

    assert status == 200
    assert 'pets' in result, "Ответ не содержит ключ 'Кусь'"

    if len(result['pets']) == 0:
        pytest.skip("У пользователя нет питомцев для удаления")

    pet_id = result['pets'][0]['id']

    status = pf.delete_pet(auth_key, pet_id)


def test_update_pet_info():
    """Проверяю, что можно изменить данные питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')


    assert status == 200
    assert isinstance(result, dict), "Ответ не является JSON"
    assert 'pets' in result, "Ответ не содержит ключ 'pets'"

    if not result['pets']:
        pytest.skip("У пользователя нет питомцев для обновления")
    pet_id = result['pets'][0]['id']
    print("Старые данные питомца: {result['pets'][0]}")
    new_name = "Гена"
    new_animal_type = "Крокодил"
    new_age = 5
    new_photo=r'C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Клуша.jpg'
    status, updated_pet = pf.update_pet_info(auth_key, pet_id, new_name, new_animal_type, new_age,new_photo)

    assert status == 200
    assert isinstance(updated_pet, dict), "Ответ API не JSON: {updated_pet}"

    assert updated_pet.get('name') == new_name, "Имя питомца не обновилось"
    assert updated_pet.get('animal_type') == new_animal_type, "Тип питомца не обновился"
    assert updated_pet.get('age') == new_age, "Возраст питомца не обновился"






