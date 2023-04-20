import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    # Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
    # JSON с уникальным ключом пользователя, найденного по указанным email и паролем
    def get_api_key(self, email: str, passwd: str) -> json:

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
    # со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
    # либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
    # собственных питомцев
    def get_list_of_pets(self, auth_key: json, filter_set: str = "") -> json:

        headers = {'auth_key': auth_key['key']}
        filter_set = {'filter': filter_set}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter_set)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
    # запроса на сервер и результат в формате JSON с данными добавленного питомца
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    # Метод отправляет на сервер запрос на удаление питомца по-указанному ID и возвращает
    # статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
    def delete_pet(self, auth_key: json, pet_id: str) -> json:

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
    # возвращает статус запроса и result в формате JSON с обновлёнными данными питомца
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Метод отправляет на сервер данные о добавляемом питомце без его фотографии и возвращает статус
    # запроса на сервер и результат в формате JSON с данными добавленного питомца
    def add_new_pet_wh_photo(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    # Метод отправляет на сервер файл с фотографией питомца и возвращает статус
    # запроса на сервер и результат в формате JSON с данными добавленного файла
    def add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:

        files = {'pet_photo': open(pet_photo, 'rb')}
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=files)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result