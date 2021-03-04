#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Dev: https://gitlab.com/4bolfazl

# Imports:
from pyrogram import Client, Filters, Message
from time import sleep
from datetime import datetime
import operator

# App Configuration:
api_id = 3097680
api_hash = '26658f497215034d610d255c0d0d17cf'
app = Client('tanin', api_id=api_id, api_hash=api_hash)

group_id = -1001472017560
ghofli = 1685600531
werewolves = [175844556, 198626752]
shekar_tags = r'#shekar|#شکارچی|#شکار|#شکارم|#shekarchi'
shekar = None
lynching = {}
start_lynch = None
vote_message = None

# Main:
@app.on_message(filters=Filters.chat(group_id) & Filters.user(werewolves) & Filters.regex(r'^یک بازی .*') & ~Filters.edited)
def join_game(client: Client, message: Message):
    game_code = message.click().split('start=')[-1]
    client.send_message(message.from_user.id, f'/start {game_code}')


@app.on_message(filters=Filters.chat(group_id) & Filters.regex(shekar_tags))
def find_shekar(client: Client, message: Message):
    global shekar
    shekar = message.from_user.id


@app.on_message(filters=Filters.user(werewolves) & Filters.private & Filters.regex(r'^کیو میخوای بخوری|^کیو میخوای امشب بکشی|^میخوای یه خونه دیگه'))
def kill_ghofli(client: Client, message: Message):
    if shekar == ghofli:
        return
    try:
        ghofli_info = client.get_chat_member(ghofli)
    except:
        sleep(25)
        ghofli_info = client.get_chat_member(ghofli)
    ghofli_name = ghofli_info.user.first_name + ' ' + ghofli_info.user.last_name
    if message.text.startswith('میخوای یه خونه دیگه'):
        try:
            message.click('جرقه')
        except:
            try:
                message.click(ghofli_name)
            except:
                message.click(0)
        return
    try:
        message.click(ghofli_name)
    except:
        pass


@app.on_message(filters=Filters.user(werewolves) & Filters.private & ~Filters.regex(r'^کیو میخوای بخوری|^کیو میخوای امشب بکشی|^میخوای یه خونه دیگه'))
def tell_role(client: Client, message: Message):
    sleep(3)
    if 'تو رمال هستی' in message:
        client.send_message(group_id, 'رمالم')
    elif 'چقد مستی تو' in message or 'الکلی بدبخت' in message:
        client.send_message(group_id, 'مستم')
    elif 'تو یه روستایی ساده' in message:
        client.send_message(group_id, 'روسم')
    elif 'تو ناظر هستی' in message:
        client.send_message(group_id, 'ناظرم')
    elif 'تو بچه وحشی هستی' in message:
        client.send_message(group_id, 'وحشیم')
    elif 'تو فراماسونی' in message:
        client.send_message(group_id, 'فرام')  
    elif 'تو کلانتر روستا' in message:
        client.send_message(group_id, 'کلانم')
    elif 'کدخدا دیگه اسمش' in message:
        client.send_message(group_id, 'کدخدام')
    elif 'تو شاهزاده' in message:
        client.send_message(group_id, 'شاهم')
    elif 'کلی الکل' in message:
        client.send_message(group_id, 'گیجم')
    elif 'تو گرگ نمایی' in message:
        client.send_message(group_id, 'نمام')
    elif 'پیشگوی نگاتیوی هستی' in message:
        client.send_message(group_id, 'نگاتیوم')
    elif 'تو صلح گرا هستی' in message:
        client.send_message(group_id, 'صلحم')
    elif 'تو ریش سفیدی' in message:
        client.send_message(group_id, 'ریشم')
    elif 'تو دردسرسازی' in message:
        client.send_message(group_id, 'دردسرم')
    elif 'تو یه شیمیدان هستی' in message:
        client.send_message(group_id, 'شیمیم')
    elif 'تو گورکن هستی' in message:
        client.send_message(group_id, 'گورکنم')
    else:
        return


@app.on_message(filters=Filters.chat(group_id) & Filters.user(werewolves) & Filters.regex('^خب دیگه شب شده'))
def reset_lynchings(client: Client, message: Message):
    global lynching
    lynching = {}
    global start_lynch
    start_lynch = datetime.utcfromtimestamp(message.date)


@app.on_message(filters=Filters.user(werewolves) & Filters.private & Filters.regex('^به کی رای میدی'))
def set_vote_message(client: Client, message: Message):
    global vote_message
    vote_message = message


@app.on_message(filters=Filters.chat(group_id) & Filters.user(werewolves) & Filters.regex(r'اعدام بشه'))
def votes(client: Client, message: Message):
    global lynching
    for i in message.entities:
        if i%2 == 0:
            lynching[message.entities[i].user.first_name + message.entities[i].user.last_name] = lynching.get(message.entities[i].user.first_name + message.entities[i].user.last_name, 0) + 1
    timesh = datetime.utcfromtimestamp(message.date)
    global start_lynch
    delta = timesh - start_lynch
    if delta.total_seconds() >= 85:
        dead = max(lynching.items(), key=operator.itemgetter(1))[0]
        vote_message.click(dead)


app.run()
