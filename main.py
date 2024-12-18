import os
import telebot
from telebot import apihelper
import telegram
#from random import seed
#from random import randint
import time
from subprocess import DEVNULL, STDOUT, check_call, CalledProcessError

#region Start
global startreply
API_PORT = 8081
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
try:
    bot.log_out() #Logout from default api
except: #bot is already logged out from api
    print("")

#change to local api
apihelper.API_URL = 'http://0.0.0.0:' + str(API_PORT) + '/bot{0}/{1}'
apihelper.FILE_URL = 'http://0.0.0.0:' + str(API_PORT)
bot = telebot.TeleBot(BOT_TOKEN)
#endregion

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user = message.chat.username
    if message.chat.type == "supergroup":
        user = message.from_user.username
    text = message.text
    chatid = message.chat.id
    type = "video"
    custom_file = ""
    can_download = True
    if "|" in text:
        s = text.split("|")
        text = s[0]
        custom_file = s[1].replace(" ", "")
    if "youtu.be" in text or "youtube.com" in text or "reddit.com" in text or "@eduytdl_bot" in text or "instagram" in text or "x.com" in text:
        text = text.replace("@eduytdl_bot", "")
        if "/video" in text:
            type = "video"
            text = text.replace("/video", "")
        if "/audio" in text:
            type = "audio"
            text = text.replace("/audio", "")
        if "/live " not in text and "/live/" in text:
            can_download = False
        if "/live " in text:
            type = "live"
            text = text.replace("/live ", "")
        if "x.com" in text:
            type = "x"
            text = str.strip(text)
        
        text = text.replace(" ", "")
        if can_download:
            startreply = bot.reply_to(message, "Downloading")
            result = download_video(user, chatid, text, type, custom_file)
        else:
            result = [3]

        if result[0] == True:
            try:
                if type == "audio":
                    video = open(result[1] + result[3], 'rb')
                else:
                    os.system("mv " + result[1] + "* " + result[1] + "file")
                    print("A: mv " + result[1] + "* " + result[1] + "file")
                    video = open(result[1] + "file", 'rb')
            except:
                print("File not found!")
            
            bot.delete_message(startreply.chat.id, startreply.id)
            sendingreply = bot.reply_to(message, "Uploading")
            try:
                if type == "audio":
                    print("Sending audio")                    
                    bot.send_audio(chat_id = chatid, audio = video, timeout = 9999, reply_to_message_id = message.id)
                if type == "video" or type == "live" or type == "x":
                    print("Sending video")
                    bot.send_video(chat_id = chatid, video = video, timeout = 9999, supports_streaming = True, reply_to_message_id = message.id, )
                bot.delete_message(sendingreply.chat.id, sendingreply.id)
                if " " not in result[1] and "tmp" in result[1]:
                    os.system("rm " + result[1] + "file")
            except Exception as error:
                bot.reply_to(message, "Erro ao enviar o video.")
        elif result[0] != 3:
            bot.reply_to(message, result[1])

def download_video(user, chatid, link, type, custom_file):
    user = user.replace(" ", "")
    expath = ""
    value = int(time.time())
    os.system('mkdir -p /tmp/ytdl')
    extension = ".mp4"
    if type == "audio":
        extension = ".mp3"
    path = '/tmp/ytdl/' + user + '/'
    os.system('mkdir ' + path)
    #path = '/tmp/ytdl/' + user + '.' + str(value) + extension
    #path = '/tmp/ytdl/' + user + '.' + str(value) + extension
    if custom_file != "":
        expath = custom_file + extension
    result = 0
    print("Downloading video for " + user)
    try:
        downtries = 0
        while True:
            downtries += 1
            if type != "audio":
                result = os.system('./dl' + type + '.sh --no-playlist' +  ' -P ' + path + ' ' + "'" + link + "'")
            else:
                result = os.system('./dl' + type + '.sh --no-playlist' +  ' -P ' + path + ' -o ' + expath + " '" + link + "'")
            print("current try: " + str(downtries))
            if result == 0 or downtries > 30:
                break
        if type == "live":
            time.sleep(360)
    except CalledProcessError:
        print("yt-dlp error!")
    if result == 0:
        return [True, path, result, expath]
    elif result == 124:
        return [False, "Video muito longo"]
    else:
        return [False, "Erro ao baixar video"]
print("Bot started!")
bot.infinity_polling()
