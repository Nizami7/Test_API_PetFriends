import pytest
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при невалидном email и
            в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_key_for_empty_email_pass(password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при пустом email"""
    status, result = pf.get_api_key(email='', passwd=password)

    assert status == 403


def test_get_api_key_for_not_valid_email_and_password(
        email=invalid_email,
        password=invalid_password
):
    """ Проверяем, что запрос api ключа с неверным email пользователя
        возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


@pytest.mark.xfail
def test_add_new_pet_with_invalid_age(name='Мышкин', animal_type='драчун',
                                      age='-4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с neкорректными данными"""


    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)


    auth_key = pf.get_api_key(valid_email, valid_password)[1]


    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


    assert status == 422
    assert result['name'] == name


def test_successful_add_foto_of_pet(
        pet_id='',
        pet_photo_path='images/cat1.jpg'):
    """Проверяем успешность запроса на добавление фото питомца по его id"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo_path)


    assert status == 200
    assert result['pet_photo']


def test_add_new_pet_with_empty_name(
        name=' ',
        animal_type='Драчун',
        age='13',
        pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с пустым полем name выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    assert status == 200
    assert 'name' in result


def test_add_new_pet_with_incorrect_age(
        name='Мышкин',
        animal_type='драчун',
        age='1000000',
        pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с некорректным параметром возраст питомца = 1000000
        выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    assert status == 200
    assert result['name'] == name
    assert result['age'] == age


def test_rejection_update_self_pet_info_without_name(
        name='',
        animal_type='драчун',
        age=3
):
    """ Проверяем невозможность очистить имя питомца
        путём передачи пустого поля name """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key,
        pet_id,
        name,
        animal_type,
        age
    )

    # Проверяем что статус ответа = 200 и имя питомца не стало пустым
    assert status == 200
    assert result['name']


def test_update_pet_info_with_invalid_photo(
        pet_photo='tests/images/cat0.txt'
):
    """ Проверяем, что запрос на добавление фото фармата txt выполнится с кодом ошибки 500"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(
        auth_key,
        pet_id,
        pet_photo
    )
    print(result)
    assert status == 500


def test_rejection_update_self_pet_info_without_animal_type(
        name='Мышкин',
        animal_type='',
        age=13
):
    """ Проверяем невозможность очистить типа питомца путём
        передачи пустого поля animal_type """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key,
        pet_id,
        name,
        animal_type,
        age
    )
    # Проверяем что статус ответа = 200 и тип питомца не пустой
    assert status == 200
    assert result['animal_type']


def test_add_new_pet_with_valid_data_without_foto(
        name='Тростиночка',
        animal_type='Котетский',
        age='1'):
    """ Проверяем, что запрос на добавление нового питомца
        без фото с указанными параметрами выполняется успешно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key,
        name,
        animal_type,
        age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
