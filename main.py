import os
from network import connect
from search import room
from modules import module

alias = input('username: ')
name = f'{alias}#iamthevoid030303'
icon = 'setton'
file_name = f'{name}.cookies'

bot = connect.Connect(name=name, icon=icon)
rooms = room.Search()
enter_room = module.Commands()

if not os.path.isfile(file_name):
    bot.login()
    bot.save_cookie(file_name=file_name)

rooms.load_cookie(file_name=file_name)
#rooms.search_room()
url_input_room = input("Enter Room Id: ")
url_room = 'https://drrr.com/room/?id={}'  .format(url_input_room)


# main
while 1:
    try:
        enter_room.load_cookie(file_name=file_name)
        e_room = enter_room.room_enter(url_room=url_room)
        is_leave = enter_room.room_update(room_text=e_room)

    except Exception as e:
        print(e)
