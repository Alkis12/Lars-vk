import random
import json
import pymorphy2
import requests

with open("keys.json", "r", encoding='utf8') as re:
    keys = json.load(re)
with open("vip.json", "r", encoding='utf8') as re:
    vip = json.load(re)
this = ''
last = ''
chit = True
mil = ['Божечки-кошечки', 'Святые мандаринки', 'Ааа', "Ох"]
with open("list.json", "r", encoding='utf8') as re:
    do = json.load(re)
with open("lisolo.json", "r", encoding='utf8') as re:
    solo = json.load(re)
milan_pad = {'datv': 'Милане', 'accs': 'Милану', 'ablt': 'Миланой', 'gent': 'Миланы'}
alex_pad = {'datv': 'Алекандре', 'accs': 'Александру', 'ablt': 'Александрой', 'gent': 'Александры'}


def dazai_pashal(event, vk):
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        attachment='audio466260834_456239111',
        random_id=random.randint(0, 2 ** 64))


def random_phrase1(gender):
    s = f'{random.choice(mil)}, '
    s += f'это {random.choice(["очень", "таак", "так"])} {random.choice(["мило", "трогательно", "неожиданно"])}, что '
    if gender == "masc":
        word = "попытался"
    else:
        word = "попыталась"
    s += f'ты {random.choice(["пытаешься", "хочешь", word])} применить действие '
    s += f'{random.choice(["к боту", "ко мне"])}{random.choice(["💜💜💜", "🖤", "❤❤❤"])}'
    return s


def random_phrase2():
    s = f'Но мы {random.choice(["всего лишь", "только лишь", "лишь"])} {random.choice(["машины", "роботы", "боты"])}'
    s += f'{random.choice(["💔", "😔", "🤧"])}'
    return s


def dodo(event, vk, dop, verb):
    f = False
    dop += do[verb][1]
    if verb == 'кусь':
        verb = 'сделать'
        dop = ' кусь' + dop
    if verb == 'суицид':
        verb = 'совершить'
        if random.randint(1, 10) == 1:
            dop = ' двойное самоубийство' + dop
        else:
            dop = ' суицид' + dop
    form = do[verb][0]
    morph = pymorphy2.MorphAnalyzer()
    response = vk.users.get(user_ids=this)
    first_name = response[0]['first_name']
    gender = morph.parse(first_name)[0].tag.gender
    if 'reply_message' in event.obj.message:
        i = event.obj.message['reply_message']['from_id']
    else:
        i = last
    if i < 0:
        if verb == 'совершить' and (dop == ' суицид с' or dop == ' двойное самоубийство с'):
            response = vk.users.get(user_ids=this)
            second_name = response[0]['first_name']
            second_name = morph.parse(second_name)[0].inflect({'ablt'}).word
            second_name = '@id' + str(this) + '(' + second_name.title() + ')'
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message=f'Ларс совершает самоубийство вместе с {second_name}',
                random_id=random.randint(0, 2 ** 64))
        elif verb not in ("уебать", 'украсть', 'сжечь', 'стукнуть', 'врезать', 'избить', 'убить', 'закопать', "забрать", "сломать", "отшить", "унизить"):
            if verb == 'обнять':
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message='Обнимает в ответ 💜',
                    random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=random_phrase1(gender),
                    random_id=random.randint(0, 2 ** 64))
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=random_phrase2(),
                    random_id=random.randint(0, 2 ** 64))
        else:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message='Слушай ну это даже жестоко... Я то не могу ответить тебе по достоинству...',
                random_id=random.randint(0, 2 ** 64))
        return
    if do[verb][2]:
        form2 = set(do[verb][2])
    else:
        if gender is None:
            gender = 'masc'
        form2 = {"past", gender}
    response = vk.users.get(user_ids=i)
    second_name = response[0]['first_name']
    global chit
    if verb in ("уебать", 'украсть', 'стукнуть', 'врезать', 'убить', 'закопать', "забрать", "сломать", "отшить", "унизить") and first_name != 'Алексей' and second_name == 'Алексей' and chit:
        i = this
        f = True
    response = vk.users.get(user_ids=i)
    vs = verb
    verb = morph.parse(verb)[0].inflect(form2).word + dop
    if 'кусь за жопу' in verb and first_name != 'Жанель':
        return
    second_name = response[0]['first_name']
    for j in morph.parse(second_name):
        if 'Name' in j.tag:
            break
    if second_name == 'Милана':
        second_name = milan_pad[form]
    elif second_name == 'Александра':
        second_name = alex_pad[form]
    else:
        second_name = j.inflect({form}).word
    second_name = '@id' + str(i) + '(' + second_name.title() + ')'
    '''if f:
        second_name += f' в попытке {vs} Алексея'''''
    print(first_name, verb, second_name)
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=f'{first_name} {verb} {second_name}',
        random_id=random.randint(0, 2 ** 64))


def soso(event, vk, dop, verb):
    if verb == 'суицид':
        verb = 'совершить'
        dop = ' суицид' + dop
    verb = verb.replace('поделиться', 'делиться')
    morph = pymorphy2.MorphAnalyzer()
    if solo[verb][0]:
        form = set(solo[verb][0])
    else:
        form = {'pres', '3per'}
    if 'past' in form:
        if this < 0:
            first_name = 'Руна'
        else:
            response = vk.users.get(user_ids=this)
            first_name = response[0]['first_name']
        gender = morph.parse(first_name)[0].tag.gender
        form.add(gender)
    verb = morph.parse(verb)[0].inflect(form).word + dop
    if this < 0:
        first_name = 'Руна'
    else:
        response = vk.users.get(user_ids=this)
        first_name = response[0]['first_name']
    print(first_name, verb)
    vk.messages.send(
        peer_id=event.obj.message['peer_id'],
        message=f'{first_name} {verb}',
        random_id=random.randint(0, 2 ** 64))


def role(event, vk, t):
    global this, last
    if this != event.obj.message['from_id'] and event.obj.message['from_id'] > 0:
        last = this
        this = event.obj.message['from_id']
    if ' ' in t.lower():
        x = t.lower().split()
        verb = x[0].lower()
        dop = ' ' + ' '.join(x[1:])
    else:
        verb = t.lower()
        dop = ''
    if verb == 'сломать' and dop == ' щит':
        global chit
        chit = False
    if verb in solo:
        if verb in do:
            if 'reply_message' in event.obj.message:
                if verb == 'суицид' and random.randint(1, 20) == 1:
                    dazai_pashal(event, vk)
                elif verb == 'суицид' and random.randint(1, 5) == 1:
                    verb = 'двойное самоубийство с'
                    dodo(event, vk, dop, verb)
                else:
                    dodo(event, vk, dop, verb)
            else:
                soso(event, vk, dop, verb)
        else:
            soso(event, vk, dop, verb)
    elif verb in do:
        dodo(event, vk, dop, verb)
