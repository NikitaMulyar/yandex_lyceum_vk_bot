import json
import random
import wikipedia
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


def main():
    wikipedia.set_lang('ru')
    vk_session = vk_api.VkApi(
        token='vk1.a.xFPfVeRVBmaXpfz7ogTMnZncMn2G44aWRwc_z8sFmUcustdWChwwMccytf0XuxEF0MEdGU4troGgBhnu71OGKh5-nngybRJenksZs87N0cuWWmrbbVb3oZRXdHdWCTRuVkiUc89obSiM4nSYVX_jS_2nAXIHoWia5PH6ZhMR_F_D_-x-wl5mdCZ4Moyh2pW05qNQCG7eniTbO4IC7G3uBQ'
    )

    longpoll = VkBotLongPoll(vk_session, group_id='220118907')

    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            txt = event.obj.message['text'].lower()
            if not txt.startswith('?'):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет! Я вики-бот - найду все! Присылай запросы (? <запрос>), а я поищу об этом в Википедии!",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                try:
                    prompt = "?".join(txt.split('?')[1:]).strip()
                    res = wikipedia.summary(prompt)
                except Exception:
                    res = 'По вашему запросу ничего не найдено.'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=res,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
