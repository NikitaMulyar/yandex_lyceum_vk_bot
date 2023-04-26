import vk_api
import json
from flask import Flask, render_template, redirect, request, abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

LOGIN = '79775446373'
PASSWORD = 'antirockwho'


AUTH = 0
vk = vk_api.VkApi().get_api()


def auth():
    global AUTH, vk
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    try:
        vk_session.auth()
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    except vk_api.AuthError as error_msg:
        abort(401)
        return
    vk = vk_session.get_api()
    AUTH = 1


@app.route('/vk_stat/<int:id>', methods=['GET', 'POST'])
def vk_stat(id):
    # if not AUTH:
    #     auth()
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login=login, password=password, captcha_handler=captcha_handler)
    try:
        vk_session.auth()
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    except vk_api.AuthError as error_msg:
        abort(401)
        return ''
    vk = vk_session.get_api()
    ids = [220146832, 220126026, 220125061, 220118907, 220062557]
    try:
        response = vk.stats.get(group_id=id, stats_groups='reach', timestamp_from=1681145509)
    except vk_api.exceptions.ApiError as e:
        print(e.error)
        print(e)
        if e.error['error_code'] == 13:
            abort(504)
        if e.error['error_code'] == 100:
            abort(404)
        if e.error['error_code'] == 15:
            abort(403)  # forbidden
    except Exception as e:
        print(e)
        abort(500)
    res = {'activity': {}, 'ages': {}, 'cities': {}, 'countries': {}}
    for i in response:
        try:
            for k, v in i['activity'].items():
                if k not in res['activity']:
                    res['activity'][k] = v
                else:
                    res['activity'][k] += v
        except Exception:
            pass
        try:
            for val in i['reach']['age']:
                if val['value'] not in res['ages']:
                    res['ages'][val['value']] = val['count']
                else:
                    res['ages'][val['value']] += val['count']
        except Exception:
            pass
        try:
            for val in i['reach']['cities']:
                if val['name'] not in res['cities']:
                    res['cities'][val['name']] = val['count']
                else:
                    res['cities'][val['name']] += val['count']
        except Exception:
            pass
        try:
            for val in i['reach']['countries']:
                if val['name'] not in res['countries']:
                    res['countries'][val['name']] = val['count']
                else:
                    res['countries'][val['name']] += val['count']
        except Exception:
            pass

    return render_template('main.html', data=res)


@app.route('/', methods=['GET', 'POST'])
def main():
    return '<h1>Vk.com Statistics</h1>'


def auth_handler():
    with open('codes.json', mode='r') as file:
        res = json.loads(file.read())
    key = res[0]
    res.pop(0)
    with open('codes.json', mode='w') as file:
        json.dump(res, file)
    remember_device = True

    return key, remember_device


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


if __name__ == '__main__':
    app.run(port=8080)
