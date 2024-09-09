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
    type = "video"
    text = text.replace("@eduytdl_bot", "")
    custom_file = ""
    if "|" in text:
        s = text.split("|")
        text = s[0]
        custom_file = s[1].replace(" ", "")
    if "youtu.be" in text or "youtube.com" in text or "reddit.com" in text:
        startreply = bot.reply_to(message, "Downloading")
        if "/video" in text:
            type = "video"
            text = text.replace("/video", "")
        if "/audio" in text:
            type = "audio"
            text = text.replace("/audio", "")
        if "/live" in text:
            type = "live"
            text = text.replace("/live", "")
        text = text.replace(" ", "")
        result = download_video(user, chatid, text, type, custom_file)

        if result[0]:
            try:
                video = open(result[1], 'rb')
            except:
                print("File not found!")
            
            bot.delete_message(startreply.chat.id, startreply.id)
            sendingreply = bot.reply_to(message, "Uploading")
            try:
                if type == "audio":
                    print("Sending audio")                    
                    bot.send_audio(chat_id = chatid, audio = video, timeout = 9999, reply_to_message_id = message.id)
                if type == "video" or type == "live":
                    print("Sending video")
                    bot.send_video(chat_id = chatid, video = video, timeout = 9999, supports_streaming = True, reply_to_message_id = message.id)
                bot.delete_message(sendingreply.chat.id, sendingreply.id)
                os.system("rm " + result[1])
            except Exception as error:
                bot.reply_to(message, "Erro ao enviar o video.")
        else:
            bot.reply_to(message, result[1])

def download_video(user, chatid, link, type, custom_file):
    value = int(time.time())
    os.system('mkdir -p /tmp/ytdl')
    extension = ".mp4"
    if type == "audio":
        extension = ".mp3"
    path = '/tmp/ytdl/' + user + '.' + str(value) + extension
    if custom_file != "":
        path = '/tmp/ytdl/' + custom_file + extension
    result = 0
    print("Downloading video for " + user)
    try: 
        result = os.system('./dl' + type + '.sh --no-playlist' +  ' -o ' + path + ' ' + link)
        if type == "live":
            time.sleep(360)
    except CalledProcessError:
        print("yt-dlp error!")
    if result == 0:
        return [True, path, result]
    elif result == 124:
        return [False, "Video muito longo"]
    else:
        return [False, "Erro ao baixar video"]
print("Bot started!")
bot.infinity_polling()
