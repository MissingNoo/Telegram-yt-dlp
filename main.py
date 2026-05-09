import os
import time
import telebot
from telebot import apihelper
import telegram
#from random import seed
#from random import randint
import time
from subprocess import DEVNULL, STDOUT, check_call, CalledProcessError
import requests
import json
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

#region mongo
from pymongo import MongoClient
#try:
    

    # Query for a movie that has the title 'Back to the Future'
    #query = { "title": "Back to the Future" }
    #movie = movies.find_one(query)

    #print(movie)

    #client.close()

#except Exception as e:
#    raise Exception("Unable to find the document due to the following error: ", e)

#endregion

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user = message.chat.username
    if message.chat.type == "supergroup":
        user = message.from_user.username
    text = message.text
    chatid = message.chat.id
    type = "video"
    can_download = True
    if (("https" in text or "youtu.be" in text or "youtube.com" in text) and "channel" not in text) or "reddit.com" in text or "@eduytdl_bot" in text or "instagram" in text or "x.com" in text:
        text = text.replace("@eduytdl_bot", "").replace("channel", "asdasdkasdkaskdasd").replace(" ", "")
        if "&" in text:
            text = text.split("&")[0]
        if "/audio" in text:
            type = "audio"
            text = text.replace("/audio", "")
        if "/live " not in text and "/live/" in text:
            can_download = False
        if "list=" in text:
            text = text.split("?")[0]
        if "x.com" in text:
            type = "x"
            text = text.replace("x.com", "fxtwitter.com")
            #text = str.strip(text)

        if can_download:
            #if type != "x":
            startreply = bot.reply_to(message, "Downloading")
            result = download_video(user, chatid, text, type)
        #print(result)
        if result["sucess"]:
            try:
                uri = "mongodb://localhost:27017/"
                client = MongoClient(uri)
                database = client.get_database("ytdown")
                videos = database.get_collection("videos")
                videos.insert_one({"link" : text, "user" : user, "type" : type, "timestamp" : time.time()})
                client.close()                
            except Exception as e:
                print("Unable to find the document due to the following error: ", e)
            try:
                vv = result["path"]
                if os.path.exists(vv) == False:
                    vv = vv + ".webm"
                video = open(vv, 'rb')
                if type == "audio":
                    ff = os.system("ffmpeg -i " + result["path"] + " " + result["path"].replace(".mp4", ".mp3"))
                    if ff == 0:
                        video = open(result["path"].replace(".mp4", ".mp3"), 'rb')
                #else:
                #    #os.system("mv " + result[1] + "* " + result[1] + "file")
                #    #print("A: mv " + result[1] + "* " + result[1] + "file")
                #    video = open(result[1] + result[3], 'rb')
            except:
                print("File not found!")
            
            bot.delete_message(startreply.chat.id, startreply.id)
            #sendingreply = bot.reply_to(message, "Uploading")
            try:
                if type == "audio":
                    print("Sending audio")                    
                    bot.send_audio(chat_id = chatid, audio = video, timeout = 9999, reply_to_message_id = message.id)
                if type == "video" or type == "live" or type == "x":
                    print("Sending video")
                    bot.send_video(chat_id = chatid, video = video, timeout = 9999, supports_streaming = True, reply_to_message_id = message.id, )
                #bot.delete_message(sendingreply.chat.id, sendingreply.id)
                if " " not in result["basepath"] and "tmp" in result["basepath"]:
                    path = result["basepath"].replace(" ", "")
                    if "/ " not in path:
                        os.system("rm " + path + "*")
                    #os.system("rm " + result[1] + "file")
            except Exception as error:
                path = result["basepath"].replace(" ", "")
                if "/ " not in path:
                    os.system("rm " + path + "*")
                #bot.reply_to(message, "Erro ao enviar o video.")
                
        #elif result[0] != 3:
        #    bot.reply_to(message, result[1])

def download_video(user, chatid, link, type):
    user = user.replace(" ", "")
    expath = str(chatid)
    value = int(time.time())
    os.system('mkdir -p /tmp/ytdl')
    extension = ".mp4"
    #if type == "audio":
    #    extension = ".mp3"
    path = '/tmp/ytdl/' + user + '/'
    if "/ " not in path:
        os.system('rm -rf ' + path)
    os.system('mkdir ' + path)
    
    result = {}
    use_cobalt = True
    cobalt = 'https://cobalt.337494.xyz'
    myobj = json.loads("{}")
    myobj["url"] = link
    if type == "audio":
        myobj["downloadMode"] = "audio"
    os.system("clear")
    res1 = requests.post(cobalt, json = myobj, headers = {"Accept" : "application/json",  "Content-Type" : "application/json"})
    print("Downloading video for " + user)
    #print(myobj)
    #print(res1)
    if res1 == "<Response [404]>":
        use_cobalt = False
    try:
        res = res1.json()
    except:
        use_cobalt = False
    if use_cobalt:
        res = res1.json()
        if type == "audio" and expath == str(chatid):
            expath = res["filename"]
        if res["status"] == "redirect" or res["status"] == "tunnel":
            try:
                downtries = 0
                while True:
                    downtries += 1
                    if type != "audio":
                        extension += ".b"
                    result = os.system('aria2c' + ' -o "' + expath + extension + '" -d ' + path + " '" + res["url"] + "'")
                    if type != "audio":
                        result = os.system('ffmpeg -err_detect ignore_err -i ' + path + expath + extension + ' -c copy ' + path + expath + extension.replace(".b", ""))
                        extension = extension.replace(".b", "")
                    print("current try: " + str(downtries))
                    if result == 0 or downtries > 30:
                        break
            except CalledProcessError:
                print("yt-dlp error!")
            if result == 0:
                return {
                    "sucess": True,
                    "path" : path + expath + extension,
                    "basepath" : path
                }
            elif result == 124:
                return {
                    "sucess": False,
                    "message": "Video muito longo"
                }
            else:
                return {
                    "sucess": False,
                    "message": "Erro ao baixar video"
                }
        else:
            return {
                    "sucess": False,
                    "message": "Erro ao baixar video, " + str(res["error"])
                }        
    else:
        print("Cobalt error, using yt-dlp!")
        yt = os.system("./dlvideo.sh " + link + " -o " + path + expath + extension)
        print(yt)
        if yt == 0:
            return {
                "sucess": True,
                "path": path + expath + extension,
                "basepath" : path
            }
    return {
        "sucess": False,
        "message": "undefined"
    }
    
    

print("Bot started!")
bot.infinity_polling()
