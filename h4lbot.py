#!/usr/bin/env python
import sys
import time
import pprint
import telepot
import random
import datetime
import json

from tinydb import TinyDB, Query
from daemonize import Daemonize

class commands:
    addmovie, addmusic, addtorrent, unknown= range(4)

def show_wishlist(chat_id, media_type):
    bot.sendMessage(chat_id, "This is the " + media_type + " wishlist:")
    wishlist = Query()
    rows = db.search(wishlist.type == media_type)
    message = ""
    for row in rows:
        message += row['name'] + "\n"
    bot.sendMessage(chat_id, message)

def add_to_wishlist(chat_id, media_type, values):
    for value in values.split("\n"):
        db.insert({'type': media_type, 'name': value})
    bot.sendMessage(chat_id, media_type + " succesfully added.")

def handle(msg):
    global current_command
    global db 
    chat_id = msg['chat']['id']
    text    = msg['text']
    if text == '/addmovie':
        bot.sendMessage(chat_id, "Send me a movie you want to add to the wishlist")
        current_command = commands.addmovie
    elif text == '/addmusic':
        bot.sendMessage(chat_id, "Send me some music you want to add to the wishlist")
        current_command = commands.addmusic
    elif text == '/addtorrent':
        bot.sendMessage(chat_id, "Send me a torrent you want to add to the download queue")
        current_command = commands.addtorrent
    elif text == '/showmusic':
        show_wishlist(chat_id, 'music')
    elif text == '/showmovies':
        show_wishlist(chat_id, 'movie')
    elif current_command != commands.unknown: 
        if current_command == commands.addmovie:
            add_to_wishlist(chat_id, 'movie', text)
        if current_command == commands.addmusic:
            add_to_wishlist(chat_id, 'music', text)
        current_command = commands.unknown
# Getting the token from command-line is better than embedding it in code,
# because tokens are supposed to be kept secret.
TOKEN 	= sys.argv[1]
DB_PATH = sys.argv[2]

db = TinyDB(DB_PATH + '/db.json')

current_command = commands.unknown
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')


# Keep the program running.
def main():
    while True:
       time.sleep(10)

daemon = Daemonize(app="h4lbot", pid="/tmp/h4lbot.pid", action=main)
daemon.start()
