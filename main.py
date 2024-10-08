#это дз 16 тут я продолжила бот с прошлой домашки
import telebot
import os
import sqlite3

TOKEN = os.getenv('YOUR_BOT_TOKEN')
bot = telebot.TeleBot('7613639105:AAGz-03wZ-VKCJB9YRvm_39WyfSA1jo_DnQ')

user_data = {}

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY, name TEXT, phone TEXT)''')
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пожалуйста, введите ваше имя.")
    user_data[message.from_user.id] = {}

@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
def set_name(message):
    user_data[message.from_user.id]['name'] = message.text
    bot.reply_to(message, f"Спасибо, {message.text}! Теперь отправьте мне свой номер телефона.", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(telebot.types.KeyboardButton("Отправить номер", request_contact=True)))

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_data[message.from_user.id]['phone'] = message.contact.phone_number
    bot.reply_to(message, f"Ваш номер: {message.contact.phone_number}. Теперь отправьте вашу локацию.", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(telebot.types.KeyboardButton("Отправить локацию", request_location=True)))

@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_data[message.from_user.id]['location'] = {'lat': message.location.latitude, 'lon': message.location.longitude}
    name = user_data[message.from_user.id]['name']
    phone = user_data[message.from_user.id]['phone']
    cursor.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)", (message.from_user.id, name, phone))
    conn.commit()
    bot.reply_to(message, f"Спасибо, {name}! Ваша локация получена. Данные сохранены. Приятного использования бота!")

try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
