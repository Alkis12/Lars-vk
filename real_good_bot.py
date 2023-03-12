import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from role_play_option import role
from ready_function import *
import random
import json

chit = False
GROUP_ID = 201055044
TOKEN = 'd035b43482561f2e51bd4db71c6bd75efb21435118dc0695b9e467a8f1a8ba5eef53595cc8eca4650e85e'
name = 'ларс'
with open("keys.json", "r", encoding='utf8') as re:
    keys = json.load(re)

players = []


def show_married(event, vk):
    s = 'Список браков:' + '\n'
    li = []
    for chel1 in braki:
        response = vk.users.get(user_ids=chel1)
        first_name1 = response[0]['first_name']
        second_name1 = response[0]['last_name']
        for chel2, id, x in braki[chel1]:
            if x == 1:
                if {chel1, chel2} not in li:
                    li.append({chel1, chel2})
                else:
                    break
                response = vk.users.get(user_ids=chel2)
                first_name2 = response[0]['first_name']
                second_name2 = response[0]['last_name']
                s += f'@id{chel1}({first_name1} {second_name1}) и @id{chel2}({first_name2} {second_name2})' + '\n'
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=s,
        random_id=random.randint(0, 2 ** 64))


def main():
    f = True
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            t = event.obj.message['text']
            antismoke(event, vk, t)
            if t.lower() == name:
                print_help(vk, event, t)
            elif t and t.split()[0].lower() == name:
                t = ' '.join(t.split()[1:])
                if keys['key'] == t.lower():
                    send_keys(event, vk, vip)
                elif keys["key_on"] == t.lower():
                    f = True
                elif keys["key_off"] == t.lower():
                    f = False
                elif keys['key_show_vip'] == t.lower():
                    show_vip(event, vk, vip)
                elif keys['key_in_vip'] == t.lower():
                    in_vip(event, vk, vip)
                elif keys['key_from_vip'] == t.lower():
                    from_vip(event, vk, vip)
                elif keys['key_show_married'] == t.lower():
                    show_married(event, vk)
                elif keys['key_married'] == t.lower():
                    married(event, vk)
                elif keys['key_married_yes'] == t.lower().split()[0]:
                    married1(event, vk, t.lower().split()[1])
                elif keys['key_married_no'] == t.lower().split()[0]:
                    married2(event, vk, t.lower().split()[1])
                elif keys['key_call'] in t.lower():
                    call(event, vk)
                elif keys['key_mirror'] in t.lower():
                    mirror(event, vk, t)
                elif keys['key_know_id'] in t.lower():
                    know_id(event, vk)
                else:
                    continue
            elif f:
                role(event, vk, t)


if __name__ == '__main__':
    main()
