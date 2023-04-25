import datetime
import json
import random
from datetime import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

LOGIN = '79775446373'
PASSWORD = 'antirockwho'


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    with open('codes.json', mode='r') as file:
        res = json.loads(file.read())
    key = res[0]
    res.pop(0)
    with open('codes.json', mode='w') as file:
        json.dump(res, file)
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.SB6IBIttAopz-GizAevbns_Zwo4mFtiVdBtjCwhTHaPJpZdwRI9X35uFpp6Dz7pB8LmywuMCDeUmulKYw9V-oFsPLNBXliCDW1uNHDGMuOokWXA1Aw7BEVxhM6EY1I_c9nU9G-7LdmB8_RpmEAIj2UzxuDNt3HWlcjyKI8dbxaVVVywZKq8JWKPxgrTko6FJ64sJ4I9XOsopjEabkoWk_Q'
    )

    longpoll = VkBotLongPoll(vk_session, group_id='220125061')

    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            txt = event.obj.message['text'].lower()
            id = event.obj.message['from_id']
            user_get = vk.users.get(user_ids=id, fields='city')[0]
            einlad = "А ты знал, что можно узнать " \
                     "информацию а сегодняшнем дне? " \
                     "Используй слова 'время', 'число', " \
                     "'дата', 'день' в своем сообщении!"
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Привет, {user_get['first_name']}! " +
                                     f"Как поживает {user_get['city']['title']}?" if
                             user_get.get(
                                 'city') is not None else "",
                             random_id=random.randint(0, 2 ** 64))
            login, password = LOGIN, PASSWORD
            vk_session2 = vk_api.VkApi(
                login, password,
                # функция для обработки двухфакторной аутентификации
                auth_handler=auth_handler
            )

            try:
                vk_session2.auth(token_only=True)
            except vk_api.AuthError as error_msg:
                print(error_msg)
                return
            vk2 = vk_session2.get_api()
            response = vk2.photos.get(album_id=292939865, group_id=220125061)
            if response['items']:
                img = random.choice(response['items'])
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 attachment=f'photo{img["owner_id"]}_{img["id"]}',
                                 random_id=random.randint(0, 2 ** 64),
                                 message="Куку!")
            if 'день' not in txt and 'время' not in txt and 'число' not in txt and 'дата' not in txt:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=einlad,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                tm = datetime.now()
                DAYS = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'}
                s = f"Дата: {tm.day}.{tm.month}.{tm.year}, время (МСК): {tm.hour}:{tm.minute}\nДень недели: {DAYS[tm.weekday()]}"
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=s,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
