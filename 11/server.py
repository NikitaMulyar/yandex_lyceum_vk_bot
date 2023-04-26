import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import requests
import os


API_GEO = '40d1649f-0493-4b70-98ba-98533de7710b'
URL_GEOCODER = 'http://geocode-maps.yandex.ru/1.x/'
URL_MAPS = 'http://static-maps.yandex.ru/1.x/'


def get_coords(address):
    geocoder_params = {
        "apikey": API_GEO,
        "geocode": address,
        "format": "json"}

    try:
       json_response = requests.get(URL_GEOCODER, params=geocoder_params).json()
    except Exception:
        return -1

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_lattitude), float(toponym_longitude)


def get_map(a, map_):
    map_params = {
        "ll": ",".join([str(a[1]), str(a[0])]),
        "l": map_,
        "z": 14
    }

    try:
        image = requests.get(URL_MAPS, params=map_params).content
    except Exception:
        return -1

    return image


KBRD = VkKeyboard()
KBRD.add_button('Спутник', VkKeyboardColor.PRIMARY)
KBRD.add_button('Гибрид', VkKeyboardColor.POSITIVE)
KBRD.add_button('Схема', VkKeyboardColor.SECONDARY)
KBRD.one_time = True
KBRD = KBRD.get_keyboard()
USERS_DATA = {}

PLACE_REQUEST = 1
TYPE_REQUEST = 2

def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.Fydit1KvA5aYDYg9dnCVzogGy-3NqlKRdXsPKb7bZUPhVH2su7AoK2RmpJK1N7tjar619_srnS9h3iQhZF5HlRkoeabrmpH-t7tfiDSzpD3bRXw9kuwyjaYkW6j58_J6j4dmwoMIvfX2t4ZZkI-e6H3MEb5KjcgjBmEiv-EgZeNAfvymquNPK8rYH4jEW8fvHKn4MvRokl5IKs3gkldlnQ'
    )

    longpoll = VkBotLongPoll(vk_session, group_id='220148670')

    vk = vk_session.get_api()
    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                id = event.obj.message['from_id']
                if id not in USERS_DATA:
                    USERS_DATA[id] = {'place': '', 'state': PLACE_REQUEST, 'type': '',
                                      'coords': None}
                    vk.messages.send(user_id=id,
                                     message=f"Привет! Напиши адрес/название местности, а я пришлю тебе ее карту!",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=VkKeyboard().get_empty_keyboard())
                    continue
                if USERS_DATA[id]['state'] == PLACE_REQUEST:
                    USERS_DATA[id]['place'] = event.obj.message['text']
                    try:
                        r = get_coords(USERS_DATA[id]['place'])
                        if r == -1:
                            raise Exception
                    except Exception as e:
                        print(e)
                        vk.messages.send(user_id=id,
                                         message=f"Неверный адрес.",
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=VkKeyboard().get_empty_keyboard())
                        continue
                    USERS_DATA[id]['coords'] = r
                    USERS_DATA[id]['state'] = TYPE_REQUEST
                    vk.messages.send(user_id=id,
                                     message=f"Теперь выбери тип карты!",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=KBRD)
                elif USERS_DATA[id]['state'] == TYPE_REQUEST:
                    if event.obj.message['text'] not in ['Спутник', 'Гибрид', 'Схема']:
                        vk.messages.send(user_id=id,
                                         message=f"Выбери тип карты.",
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=KBRD)
                        continue
                    tmp = {'Спутник': 'sat', 'Схема': 'map', 'Гибрид': 'sat,skl'}
                    USERS_DATA[id]['type'] = event.obj.message['text']
                    USERS_DATA[id]['state'] = PLACE_REQUEST
                    try:
                        image = get_map(USERS_DATA[id]['coords'], tmp[USERS_DATA[id]['type']])
                        if image == -1:
                            raise Exception
                    except Exception:
                        vk.messages.send(user_id=id,
                                         message=f"Не получилось построить карту.",
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=VkKeyboard().get_empty_keyboard())
                        return
                    data = vk.photos.getMessagesUploadServer()
                    with open('photo.png', mode='wb') as f:
                        f.write(image)
                    path = os.path.abspath('./photo.png')
                    res = requests.post(data['upload_url'].replace('\\', ''), files={'photo': (path, open(path, mode='rb'))}).json()
                    res = vk.photos.saveMessagesPhoto(photo=res['photo'], server=res['server'],
                                                      hash=res['hash'])[-1]
                    vk.messages.send(user_id=id,
                                     message=f"Это {USERS_DATA[id]['place']}. Что вы еще хотите увидеть?",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=VkKeyboard().get_empty_keyboard(),
                                     attachment=f'photo{res["owner_id"]}_{res["id"]}')

if __name__ == '__main__':
    main()

"""
continue
            try:
                txt = event.obj.message['text'].split('-')
                d = datetime(year=int(txt[0]), month=int(txt[1]), day=int(txt[2])).weekday()
                DAYS = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'}
                s = f"День недели для {event.obj.message['text']}: {DAYS[d]}"
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=s,
                                 random_id=random.randint(0, 2 ** 64))
            except Exception:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Неверно указана дата.",
                                 random_id=random.randint(0, 2 ** 64))
"""
