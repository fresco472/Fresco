import telebot
import keyboards
import fsm

BOT_TOKEN = '7602951193:AAEgttnkv2Dn80xHR7lBnrqL3t-0PvhHpWM'
stater = fsm.FSM() 
bot = telebot.TeleBot(BOT_TOKEN)

def menu(chat_id):
    stater.set_state(chat_id, fsm.DEFAULT_STATE)
    bot.send_message(chat_id, text='Главное меню', reply_markup=keyboards.start)         

def handler_def_state(message):
    if message.text == "Фото 🖼":
        stater.set_state(message.chat.id, fsm.IMAGE_STATE)
        bot.send_message(message.chat.id, text='Напиши описание фото', reply_markup=keyboards.back)
    elif message.text == "Текст 📝":
        stater.set_state(message.chat.id, fsm.TEXT_STATE)
        bot.send_message(message.chat.id, text='Напиши то, о чем ты хочешь у меня поинтересоваться', reply_markup=keyboards.back) 
    else: 
        bot.send_message(message.chat.id, text='Ниче не понял', reply_markup=keyboards.start) 

def handler_image_state(message):
    if message.text == "◀️ В меню":
        menu(message.chat.id)
    else: 
        bot.send_message(message.chat.id, text='Начинаю генерировать фото')

def handler_text_state(message):  
    if message.text == "◀️ В меню":
        menu(message.chat.id)
    else: 
        bot.send_message(message.chat.id, text='Начинаю генерировать текст') 



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    state = stater.get_state(message.chat.id)

    if state == fsm.DEFAULT_STATE :
        handler_def_state(message)
    elif state == fsm.IMAGE_STATE :
        handler_image_state(message)
    elif state == fsm.TEXT_STATE :
        handler_text_state(message)

bot.polling()
