import os
import telebot
from telebot import apihelper
import telegram
#from random import seed
#from random import randint
import time
from subprocess import DEVNULL, STDOUT, check_call, CalledProcessError
apihelper.API_URL = 'http://0.0.0.0:8082/bot{0}/{1}'
apihelper.FILE_URL = 'http://0.0.0.0:8082'

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user = message.chat.username
    if message.chat.type == "supergroup":
        user = message.from_user.username
    text = message.text
    chatid = message.chat.id
    audio_only = False

    if "youtu.be" in text or "youtube" in text:
        startreply = bot.reply_to(message, "Downloading")
        if "/video" in text:
            text = text.replace("/video@eduytdl_bot ", "")
            text = text.replace("/video ", "")
        if "/audio" in text:
            audio_only = True
            text = text.replace("/audio@eduytdl_bot ", "")
            text = text.replace("/audio ", "")

        result = download_video(user, chatid, text, audio_only)

        if result[0]:
            video = open(result[1], 'rb')
            bot.delete_message(startreply.chat.id, startreply.id)
            sendingreply = bot.reply_to(message, "Uploading")
            try:
                if audio_only:
                    print("Sending audio")                    
                    bot.send_audio(chat_id = chatid, audio = video, timeout = 9999, reply_to_message_id = message.id)
                else:
                    print("Sending video")
                    bot.send_video(chat_id = chatid, video = video, timeout = 9999, supports_streaming = True, reply_to_message_id = message.id)
                bot.delete_message(sendingreply.chat.id, sendingreply.id)
                os.system("rm " + result[1])
            except Exception as error:
                bot.reply_to(message, "Erro ao enviar o video.")
        else:
            bot.reply_to(message, result[1])


def download_video(user, chatid, link, audio_only):
    value = int(time.time())
    os.system('mkdir -p /tmp/ytdl')
    extension = ".mp4"
    if audio_only:
        extension = ".mp3"
    path = '/tmp/ytdl/' + user + '.' + str(value) + extension
    result = 0
    print("Downloading video for " + user)
    try:
        if audio_only:
            result = os.system('./dla.sh --no-playlist' +  ' -o ' + path + ' ' + link + '')
        else:
            result = os.system('./dl.sh --no-playlist' +  ' -o ' + path + ' ' + link + ' > /dev/null 2>&1')
    except CalledProcessError:
        print("yt-dlp error!")
    if result == 0:
        return [True, path]
    else:
        return [False, "Erro ao baixar video"]
print("Bot started!")
bot.infinity_polling()
