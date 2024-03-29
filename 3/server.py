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


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)



def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    upload_photo(vk)


if __name__ == '__main__':
    main()
