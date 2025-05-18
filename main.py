import telebot
import keyboards

BOT_TOKEN = '7602951193:AAEgttnkv2Dn80xHR7lBnrqL3t-0PvhHpWM' 
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    if text == "Фото 🖼":
        bot.send_message(message.chat.id, "Напиши описание для фото", reply_markup=keyboards.back)
    elif text == "Текст 📝":
        bot.send_message(message.chat.id, "Начни общатся со мной в чате", reply_markup=keyboards.back)
    else:
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=keyboards.start)

bot.polling()
