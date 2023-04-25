import vk_api
import json
from datetime import datetime


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


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)

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
