import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

TOKEN = '7697533527:AAGGMctDz5BcPi1AkyvVdeHDB3cwBNJCaP8'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Бот работает и не спит!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне ссылку на video (Instagram, TikTok, Pinterest, YouTube), и я скачаю его в лучшем качестве 🚀")

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "Пожалуйста, отправь мне правильную ссылку на видео.")
        return

    status_msg = bot.reply_to(message, "⏳ Ищу видео в супер-качестве, начинаю скачивать...")

    ydl_opts = {
        'outtmpl': 'downloaded_video.%(ext)s', 
        'format': 'best',
        'max_filesize': 48 * 1024 * 1024,
        'quiet': True,
        'nocheckcertificate': True
    }
       
