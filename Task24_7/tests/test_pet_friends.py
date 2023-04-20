from api import PetFriends
from settings import *
import os

pf = PetFriends()

# Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key
def test_get_api_key_for_valid_user(email=my_email, password=my_password):

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

# Проверяем, что запрос всех питомцев возвращает не пустой список.
def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(my_email, my_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Проверяем, что можно добавить питомца с корректными данными
def test_add_new_pet_with_valid_data(name='Барсик', animal_type='кот',
                                     age='2', pet_photo='images/Bars.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(my_email, my_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

# Проверяем возможность удаления питомца
def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барс", "кот", "1", "images/Bars.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

# Проверяем возможность обновления информации о питомце
def test_successful_update_self_pet_info(name='Барсетка', animal_type='кошка', age=2):

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


#    10 добавленных тестов
# Проверяем, что можно добавить питомца с данными без фотографии
def test_add_new_pet_without_photo(name='Бар', animal_type='кот', age='4'):

    _, auth_key = pf.get_api_key(my_email, my_password)

    status, result = pf.add_new_pet_wh_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# Проверяем что можно добавить фотографию питомца в существующую запись
def test_add_pet_photo(pet_photo='images/cat1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break


    if pet_id == "":
        _, result = pf.add_new_pet_wh_photo(auth_key, name='Бар', animal_type='кот', age='4')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ""

# Проверяем, что запрос питомцев со значением параметра filter = 'my_pets' возвращает не пустой список
def test_get_list_pets_with_valid_key(filter='my_pets'):

    _, auth_key = pf.get_api_key(my_email, my_password)

    pf.add_new_pet_wh_photo(auth_key, name='Барсук', animal_type='зверь', age='5')

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Проверяем что запрос API-ключа возвращает статус 403 при некорректных или "пустых" email и
# password, а в результате содержится сообщение об ошибке
def test_get_api_key_negative():

    status, result = pf.get_api_key(my_email, my_password_neg)

    assert status == 403
    assert 'Запрещенный' in result

    status, result = pf.get_api_key(my_email_neg, my_password)

    assert status == 403
    assert 'Запрещенный' in result

    status, result = pf.get_api_key(my_email, my_password_null)

    assert status == 403
    assert 'Запрещенный' in result

    status, result = pf.get_api_key(my_email_null, my_password)

    assert status == 403
    assert 'Запрещенный' in result

# Проверяем, что запрос питомцев с некорректным значением параметра filter выдаёт статус ошибки 500,
# а также - некорректным или "пустым" значением параметра auth_key выдаёт статус ошибки 403
def test_get_list_pets_negative():

    _, auth_key = pf.get_api_key(my_email, my_password)
    filter = 'pet'
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'Некорректное значение фильтра' in result

    auth_key['key'] = str(auth_key.values()) + 'a'
    filter = ''
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Запрещенный' in result

    auth_key['key'] = ''
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Запрещенный' in result

# Проверяем возможность удаления питомца с некорректным или "пустым" auth_key, "пустым" pet_id
def test_delete_pet_negative():

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барсик", "кот", "2", "images/Bars.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    my_list_id = [my_pets['pets'][i]['id'] for i in range(len(my_pets['pets']))]
    pet_id = my_pets['pets'][0]['id']

    auth_key['key'] = str(auth_key.values()) + 'a'

    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 403
    assert pet_id in my_list_id

    auth_key['key'] = ''

    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 403
    assert pet_id in my_list_id

    _, auth_key = pf.get_api_key(my_email, my_password)

    pet_id = ''

    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 404
    assert 'Не найден' in result

# Проверяем возможность обновления информации о питомце с некорректным (тип-строка) значением параметра age
def test_update_pet_negative(name='Брас', animal_type='кот'):

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барсик", "кот", "2", "images/Bars.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    age = 'год'

    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    if status == 200:
        raise Exception("Параметр 'age' типа 'string' не должен корректно обрабатываться сервером")
    else:
        assert status == 400

# Проверка возможности добавления изображения в формате bmp
def test_add_pet_photo_negative_bmp():

    pet_photo = 'images/Barsir.bmp'

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break

    if pet_id == "":
        _, result = pf.add_new_pet_wh_photo(auth_key, name='Барс', animal_type='кот', age='2')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    if status == 200:
        raise Exception("Сервисом должны поддерживаться файлы только форматов jpg, jpeg, png")
    else:
        assert status == 400
        assert result['pet_photo'] == ""

# Проверка возможности добавления файла в формате txt вместо допускаемых в форматах jpg, jpeg, png
def test_add_pet_photo_negative_txt():

    pet_photo = 'images/Фото.txt'

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break

    if pet_id == "":
        _, result = pf.add_new_pet_wh_photo(auth_key, name='Барс', animal_type='кот', age='2')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    if status == 200:
        raise Exception("Сервисом должны поддерживаться файлы только форматов jpg, jpeg, png")
    else:
        assert status == 500

# Проверяем возможность использования в имени питомца более 255 символов (500 символов)
def test_add_new_pet_without_photo_negative(animal_type='кот', age='2'):

    _, auth_key = pf.get_api_key(my_email, my_password)

    name = '''
            БарсuZsGlJjYxOYdPTJebhuJgGgWuaYBpUbxEtxKEhGtXiuBkyCIufWQqTAbaXlAQzaZOEvvxRgGaMKTFLduRaouihOuXjxHqPXq
            bjzkjPSCYbtFaqiDBnzNcJymvCsPTAEWlFBofUqdhmSpOihjBumquPfqWXkmEUSvsXGQAVBwZZsSXsXQYnYPrCbCGoZRoJIBOgSRJp
            ePQWGBlPCnrIlkOdYobRLcXFgbwxRmwySAvfHLiBVyhIudSNenbvyjzZxraJzMKupefOTeKoNiIiAfiEKIejvoABMdFYcUWsibgfmc
            sDnExHGpozUFTetzoCTSdTGckvgJicwngwV7EKIoBeGuYLCouOGOSZWMSPpPFCVSagjiXZIayxvZVWkdomVwMjxvOxpCotcTxAsVdQ
            STEujFqccMxVtWQayFdFDrDOrWMsRLymSNYgVyCLuIPMlcxhzFVFhMgpRwhHYfjQVWsLpaOpkhEnkflRtqkZQgFeOeLm21
            '''

    status, _ = pf.add_new_pet_wh_photo(auth_key, name, animal_type, age)

    if status == 200:
        raise Exception("Сервисом не должны поддерживаться строки более 255 символов")
    else:
        assert status == 400
