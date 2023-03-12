import json
import random

with open("vip.json", "r", encoding='utf8') as re:
    vip = json.load(re)
with open("braki.json", "r", encoding='utf8') as re:
    braki = json.load(re)


def print_help(vk, event, t):
    mess_old = '''ЭТО НЕАКТУАЛЬНО ЛОЛ Я ЕГО МЕНЯЮ ВСЕ ВРЕМЯ
    На данный момент я могу делать следующее:
                                !{key_help} - вывод справочного меню
                                !{key_call}id********* - вызов пользователя
                                !{key_in_vip}id********* - ТОЛЬКО ДЛЯ ВИП. Добавить в ВИП пользователя
                                !{key_no_vip}id********* - ТОЛЬКО ДЛЯ ВИП. Удалить из ВИП пользователя
                                !{key_show_vip} - вывести список всех пользователей, находящихся в ВИП
                                !{key} - ТОЛЬКО ДЛЯ ВИП. Получить команды для активации и деактивации бота
                                ДЛЯ ВИП! Вы можете поставить !! перед своим сообщением и бот его повторит с акцентом на Ваш статус''',
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message='*звук молчания*',
        random_id=random.randint(0, 2 ** 64))


def show_vip(event, vk, vip):
    s = 'Эти люди состоят в ВИП классе!!!\n'
    for i in sorted(vip):
        response = vk.users.get(user_ids=i)
        first_name = response[0]['first_name']
        second_name = response[0]['last_name']
        s += f'@id{i}({first_name} {second_name})\n'
    s = s[:-1]
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=s,
        random_id=random.randint(0, 2 ** 64))


def in_vip(event, vk, vip):
    if 'reply_message' in event.obj.message:
        if event.obj.message['from_id'] in vip:
            i = event.obj.message['reply_message']['from_id']
            vip.append(i)
            with open("vip.json", "w") as wr:
                json.dump(vip, wr)
            response = vk.users.get(user_ids=i)
            first_name = response[0]['first_name']
            second_name = response[0]['last_name']
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message=f'Пользователь переведен в статус ВИП: @id{i}({first_name} {second_name})',
                random_id=random.randint(0, 2 ** 64))
        else:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message=f'Вы не состоите в ВИП и у Вас нет права на данную операцию',
                random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='Чел ты токсик, надо ответом на соо эту команду юзать',
            random_id=random.randint(0, 2 ** 64))


def from_vip(event, vk, vip):
    if 'reply_message' in event.obj.message:
        if event.obj.message['from_id'] in vip:
            i = event.obj.message['reply_message']['from_id']
            if i in vip:
                vip.remove(i)
                with open("vip.json", "w") as wr:
                    json.dump(vip, wr)
                response = vk.users.get(user_ids=i)
                first_name = response[0]['first_name']
                second_name = response[0]['last_name']
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=f'Пользователь удален из ВИП: @id{i}({first_name} {second_name})',
                    random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=f'Этот пользователь не состоит в ВИП',
                    random_id=random.randint(0, 2 ** 64))
        else:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message=f'Вы не состоите в ВИП и у Вас нет права на данную операцию',
                random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='Чел ты токсик, надо ответом на соо эту команду юзать',
            random_id=random.randint(0, 2 ** 64))


def call(event, vk):
    if 'reply_message' in event.obj.message:
        i = event.obj.message['reply_message']['from_id']
        response = vk.users.get(user_ids=i)
        first_name = response[0]['first_name']
        second_name = response[0]['last_name']
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=f'Вас вызвали: @id{i}({first_name} {second_name})',
            random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='Чел ты токсик, надо ответом на соо эту команду юзать',
            random_id=random.randint(0, 2 ** 64))


def send_keys(event, vk, vip):
    with open("keys.json", "r", encoding='utf8') as re:
        keys = json.load(re)
    if event.obj.message['from_id'] in vip:
        vk.messages.send(
            user_id=event.obj.message['from_id'],
            message=f'Включение бота: {keys["key_on"]}\nВыключение бота: {keys["key_off"]}',
            random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=f'Вы не состоите в ВИП и у Вас нет права на данный запрос',
            random_id=random.randint(0, 2 ** 64))


def mirror(event, vk, t):
    text = t[8:][::-1]
    if text:
        text = text.split('(')
        tt = []
        for i in text:
            tt.append(i.replace(')', '('))
        text = ')'.join(tt)
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=text,
            random_id=random.randint(0, 2 ** 64))


def know_id(event, vk):
    if 'reply_message' in event.obj.message:
        id = event.obj.message['reply_message']['from_id']
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=f'Ну вот тебе id: {id}',
            random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='Чел ты токсик, надо ответом на соо эту команду юзать',
            random_id=random.randint(0, 2 ** 64))


def antismoke(event, vk, t):
    if event.obj.message['attachments'] and event.obj.message['attachments'][0]['type'] == 'sticker':
        if event.obj.message['attachments'][0]['sticker']['sticker_id'] in [51120, 20836]:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message='КУРЕНИЕ ЗДОРОВЬЮ ВРЕДИТ, ХВАТИТ УЖЕ',
                random_id=random.randint(0, 2 ** 64))
    if '🚬' in t:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='фу курятина ой то есть курение',
            random_id=random.randint(0, 2 ** 64))


def pacefic(event, vk, t):
    if t == t.upper():
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message="тише тише поспокойнее",
            random_id=random.randint(0, 2 ** 64))


def married(event, vk):
    if 'reply_message' in event.obj.message:
        chel1 = event.obj.message['from_id']
        chel2 = event.obj.message['reply_message']['from_id']
        if chel2 < 0:
            return
        if str(chel1) in braki:
            braks = braki[str(chel1)]
            for i in braks:
                if i[0] == str(chel2) and i[2] == 1:
                    vk.messages.send(
                        peer_id=event.obj.message['peer_id'],
                        message="Хехе я против повторных браков ой",
                        random_id=random.randint(0, 2 ** 64))
                    return
        response = vk.users.get(user_ids=chel1)
        first_name1 = response[0]['first_name']
        second_name1 = response[0]['last_name']
        response = vk.users.get(user_ids=chel2)
        first_name2 = response[0]['first_name']
        second_name2 = response[0]['last_name']
        id = random.randint(0, 2 ** 64)
        s1 = f'@id{chel2}({first_name2} {second_name2}), согласны ли Вы вступить в брак с {first_name1} {second_name1}?'
        s2 = f'Напишите "Ларс да/нет {id}" для подверждения (или отказа)\nЦИФРЫ ПОСЛЕ да или нет ПИСАТЬ ОБЯЗАТЕЛЬНО'
        chel1 = str(chel1)
        chel2 = str(chel2)
        if chel1 in braki:
            braki[chel1].append([chel2, id, 2])
        else:
            braki[chel1] = [[chel2, id, 2]]
        if chel2 in braki:
            braki[chel2].append([chel1, id, 3])
        else:
            braki[chel2] = [[chel1, id, 3]]
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=s1 + '\n' + s2,
            random_id=random.randint(0, 2 ** 64))
        with open("braki.json", "w") as wr:
            json.dump(braki, wr)
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message='надо ответом на соо эту команду юзать...',
            random_id=random.randint(0, 2 ** 64))


def married1(event, vk, id):
    id = int(id)
    chel1 = event.obj.message['from_id']
    if str(chel1) not in braki:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message="У Вас нет действующих предложений вступить в брак...",
            random_id=random.randint(0, 2 ** 64))
        return
    braks = braki[str(chel1)]
    for ii, i in enumerate(braks):
        if i[1] == id and i[2] == 3:
            chel2 = int(i[0])
            break
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=f"Нет предложений вступить в брак с таким id ({id})",
            random_id=random.randint(0, 2 ** 64))
        return
    braki[str(chel1)][ii] = [str(chel2), id, 1]
    braks = braki[str(chel2)]
    for ii, i in enumerate(braks):
        if i[1] == id and i[2] == 2:
            break
    braki[str(chel2)][ii] = [str(chel1), id, 1]

    response = vk.users.get(user_ids=chel1)
    first_name1 = response[0]['first_name']
    second_name1 = response[0]['last_name']
    response = vk.users.get(user_ids=chel2)
    first_name2 = response[0]['first_name']
    second_name2 = response[0]['last_name']
    s1 = f'@id{chel1}({first_name1} {second_name1}) и @id{chel2}({first_name2} {second_name2}) обвенчались!'
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=s1,
        random_id=random.randint(0, 2 ** 64))
    with open("braki.json", "w") as wr:
        json.dump(braki, wr)


def married2(event, vk, id):
    id = int(id)
    chel1 = event.obj.message['from_id']
    if str(chel1) not in braki:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message="У Вас итак нет действующих предложений вступить в брак...",
            random_id=random.randint(0, 2 ** 64))
        return
    braks = braki[str(chel1)]
    for ii, i in enumerate(braks):
        if i[1] == id and i[2] == 3:
            chel2 = int(i[0])
            break
    else:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            message=f"Нет предложений вступить в брак с таким id ({id})",
            random_id=random.randint(0, 2 ** 64))
        return
    del braki[str(chel1)][ii]
    braks = braki[str(chel2)]
    for ii, i in enumerate(braks):
        if i[1] == id and i[2] == 2:
            break
    del braki[str(chel2)][ii]
    response = vk.users.get(user_ids=chel1)
    first_name1 = response[0]['first_name']
    second_name1 = response[0]['last_name']
    response = vk.users.get(user_ids=chel2)
    first_name2 = response[0]['first_name']
    second_name2 = response[0]['last_name']
    s1 = f'@id{chel2}({first_name2} {second_name2}), хаха @id{chel1}({first_name1} {second_name1}) не хочет с тобой в брак'
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=s1,
        random_id=random.randint(0, 2 ** 64))
    with open("braki.json", "w") as wr:
        json.dump(braki, wr)
