import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import os

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    photo_path = r"C:\Users\nataz\PycharmProjects\QAP_PetFriensTesting\Tests\pet_photo\Гена.jpg"

    if os.path.exists(photo_path):
        print("✅ Файл найден!")
    else:
        print("❌ Файл не найден! Проверьте путь.")

    def get_api_key(self, email, password):
        """ Получаю API ключ для пользователя """
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url + 'api/key', headers=headers)
        return res.status_code, self._get_json_response(res)

    def get_list_of_pets(self, auth_key, filter=''):
        """ Получаю список питомцев с указанным фильтром """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
           result = res.json()
        except json.decoder.JSONDecodeError:
           result = res.text
        return status, result

    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        url = self.base_url + 'api/pets'
        headers = {'auth_key': auth_key['key']}

        files = {'pet_photo': open(pet_photo, 'rb')}
        data = {"name": name, "animal_type": animal_type, "age": age}

        response = requests.post(url, headers=headers, data=data, files=files)

        try:
            result = response.json()  
        except ValueError:
            result = response.text  

        return response.status_code, result

    def get_pet_info(self, auth_key, pet_id):
        """Получаю информацию о питомце по его ID"""
        headers = {'auth_key': auth_key['key']}
        res = requests.get(self.base_url + 'api/pets/{pet_id}', headers=headers)
        return res.status_code, self._get_json_response(res)

    def delete_pet(self, auth_key, pet_id):
        """ Удаляю питомца по его ID """
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/{pet_id}', headers=headers)
        return res.status_code, self._get_json_response(res)

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age, photo=None):
        """обнавляю информацию о питомце"""

        url = 'https://{self.base_url}api/pets/'
        headers = {'auth_key': auth_key['key']}
        data = {"name": name, "animal_type": animal_type, "age": age}
        files = {'pet_photo': open(photo, 'rb')} if photo else None
        response = requests.put(url, headers=headers, data=data, files=files)
        if files:
            files['pet_photo'].close()

        return response.status_code, response.json()

    def _get_json_response(self, res):
        """ Обработка JSON-ответов API """
        try:
            return res.json()
        except json.decoder.JSONDecodeError:
            return res.text


