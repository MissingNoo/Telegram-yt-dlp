import os
import telebot
import telegram
#from random import seed
#from random import randint
import time
from subprocess import DEVNULL, STDOUT, check_call, CalledProcessError

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
res = bot.log_out()
print(res)