import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# Подключаем токен из секретных настроек Render
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Настраиваем веб-сервер, чтобы Render не выключал бота
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა Привет, пиблик! 💕

Я уже в полном ожидании твоей ссылки!

Отправь её, и через пару секунд твоё видео будет готово к скачиванию. 🐾""")

# Обработка ссылок и скачивание
@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    
    if not url.startswith("http"):
        bot.reply_to(message, "Пожалуйста, отправь мне правильную ссылку на видео.")
        return

    status_msg = bot.reply_to(message, "⏳ Ищу видео в супер-качестве, начинаю скачивать...")

    # Настройки для скачивания видео
    ydl_opts = {
        'outtmpl': 'downloaded_video.%(ext)s',
        'format': 'best',
        'max_filesize': 48 * 1024 * 1024,
        'quiet': True,
        'nocheckcertificate': True
    }

    try:
        # Скачиваем видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info)

        # Отправляем видео в Телеграм
        with open(video_filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        # Удаляем сообщение "Ищу видео..." и сам файл с сервера, чтобы не засорять память
        bot.delete_message(message.chat.id, status_msg.message_id)
        os.remove(video_filename)
        
    except Exception as e:
        error_text = """૮₍ ˃̵м˂̵ ₎ა Ой, кажется, ссылка указана неверно или видео недоступно! 💔
        Проверь её и попробуй отправить ещё раз. 🐾"""
        bot.send_animation(
            message.chat.id,
            open('pibble_error.mp4', 'rb'),
            caption=error_text
        )

# Главная команда запуска
if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
