import pprint
import vk_api
from config import *
import json
from datetime import datetime


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
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.wall.get(count=5, offset=1)
    if response['items']:
        cnt = 1
        for i in response['items']:
            print(f'===================== {cnt} =====================')
            cnt += 1
            print(i['text'] + ';')
            d = datetime.fromtimestamp(i["date"]).isoformat().split('T')
            print(f'date: {d[0]}, time: {d[1].split("Z")[0]}')


if __name__ == '__main__':
    main()
