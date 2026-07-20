import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = "7697533527:AAFWJCg-BzfA6NC9JTu-2rFRg1rVQ2-p8fI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა Привет, пиблик! 💕

Я уже в полном ожидании твоей ссылки!

Отправь её, и через пару секунд твоё видео будет готово к скачиванию. 🐾"""
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    url = message.text.strip()
    
    if "youtube.com" not in url and "youtu.be" not in url and "tiktok.com" not in url:
        error_text = "૮₍ ˃̵м˂̵ ₎ა Ой, кажется, эта ссылка мне не подходит или указана неверно! 💔\n\nПроверь её и попробуй отправить ещё раз. 🐾"
        bot.send_animation(
            message.chat.id,
            open('pibblie_error.mp4', 'rb'),
            caption=error_text
        )
        return

    status_msg = bot.send_message(message.chat.id, "⏳ Ищу видео, подожди секунду...")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'max_filesize': 50 * 1024 * 1024,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open('video.mp4', 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)
            
        bot.delete_message(message.chat.id, status_msg.message_id)
        os.remove('video.mp4')
        
    except Exception as e:
        bot.delete_message(message.chat.id, status_msg.message_id)
        error_text = "૮₍ ˃̵м˂̵ ₎ა Ой, кажется, ссылка указана неверно или видео недоступно! 💔\n\nПроверь её и попробуй отправить ещё раз. 🐾"
        bot.send_animation(
            message.chat.id,
            open('pibblie_error.mp4', 'rb'),
            caption=error_text
        )
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

bot.infinity_polling()
