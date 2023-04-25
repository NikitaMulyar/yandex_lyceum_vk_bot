import datetime
import random
from datetime import datetime
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def was_user(id_):
    with open('users.json', mode='r') as f:
        file = json.loads(f.read())
    if str(id_) not in file:
        file.append(str(id_))
    else:
        return True
    with open('users.json', mode='w') as f:
        json.dump(list(file), f)
    return False


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.AfOwv-pjPeT8BqfUhPghWO-itxGhX1I0ZuV4-ILvw4u6cZvqxZdZQuHCwkI_6MIodq2EeXRGQqqsPZHYk98J1KNPfLBvLPHxj--jAqK8ft30XcQURyXMnvy-kAm5cH9_hdYRhtbS3y9EVOQZ69afOjlsuqW6sD3zfDKJpxYfasop1K9Vr3OSRWT2OpEJe6YrtK139_yGU0cYp9KqtjvgCg'
    )

    longpoll = VkBotLongPoll(vk_session, group_id='220126026')

    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not was_user(event.obj.message['from_id']):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет! Присылай мне даты в формате YYYY-MM-DD, а я скажу, какой это день недели!",
                                 random_id=random.randint(0, 2 ** 64))
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


if __name__ == '__main__':
    main()
