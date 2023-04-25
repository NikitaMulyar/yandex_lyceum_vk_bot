import datetime
import json
import random
from datetime import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

LOGIN = '79775446373'
PASSWORD = 'antirockwho'


def auth_handler():
    with open('codes.json', mode='r') as file:
        res = json.loads(file.read())
    key = res[0]
    res.pop(0)
    with open('codes.json', mode='w') as file:
        json.dump(res, file)
    remember_device = True

    return key, remember_device


def get_wall(vk: vk_api.vk_api.VkApiMethod):
    response = vk.wall.get(count=5, offset=1)
    if response['items']:
        cnt = 1
        for i in response['items']:
            print(f'===================== {cnt} =====================')
            cnt += 1
            print(i['text'] + ';')
            d = datetime.fromtimestamp(i["date"]).isoformat().split('T')
            print(f'date: {d[0]}, time: {d[1].split("Z")[0]}')


def get_friends(vk: vk_api.vk_api.VkApiMethod):
    response = vk.friends.get(fields="bdate, city")
    res = []
    if response['items']:
        for i in response['items']:
            res.append((i['last_name'], i['first_name'], i.get('bdate', 'None')))
    cnt = 1
    for i in sorted(res, key=lambda a: a[0]):
        print(f'{cnt}. {i[0]} {i[1]}. День рождения: {i[2]}')
        cnt += 1


def upload_photo(vk: vk_api.vk_api.VkApiMethod):
    up = vk_api.VkUpload(vk)
    up.photo(photos=[f'static/img/{i}.jpeg' for i in range(1, 4)], album_id=291455597,
             group_id=220062557)


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.qFQUTPgIWJRg2W0jbLzqG5V1fgX8XFijNr9e50mvsds1CGgkRjlWUY7tNtvfAFrDgcn29_BBeYsM5Jd3SdjiB9tZ1Beo3LpDfoDdrRMqUmFlqjWJl_VKJmWI19HCfumO_m-jofnyIfpzKngJ8tQysVPbgNIOxd2cOZ2RHMmMyN2ujK3N4U6wkmjb4IH-JGFTFlBKahSRBOiz7oIXnHbxhg'
    )

    longpoll = VkBotLongPoll(vk_session, group_id='220062557')

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
