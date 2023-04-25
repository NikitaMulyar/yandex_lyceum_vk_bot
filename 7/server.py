import vk_api

LOGIN = '79775446373'
PASSWORD = 'antirockwho'


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
    response = vk.photos.get(album_id=202082471, group_id=29166271)
    if response['items']:
        cnt = 1
        for i in response['items']:
            print(f"{cnt}.")
            d = i['sizes'][-1]
            print(f"Height: {d['height']}, Width: {d['width']}\nURL: {d['url']}")
            print()
            cnt += 1


if __name__ == '__main__':
    main()
