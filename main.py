import telebot
import keyboards
import fsm
import ai
import loguru
import yaml 
import sys

logger = loguru.logger

try:
    with open("./config2.yaml", 'r')as file:
        cfg = yaml.safe_load(file)
        logger.info('Конфиг успешно загружен')
except Exception as e:
    logger.warning("Произошла ошибка при загрузке конфига []" ,  str(e))
    input()
    sys.exit(1)

BOT_TOKEN = cfg['telegram_token']
stater = fsm.FSM()
ai_service = ai.AI(cfg) 
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
        try:
            msg = bot.send_message(chat_id=message.chat.id, text = 'Генерирую...')
            image_url = ai_service.generate_image(message.text)
            bot.delete_message(chat_id=message.chat.id, message_id=msg.id)
            bot.send_photo(chat_id=message.chat.id, caption='Ваше фото', photo=image_url)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id, text=f'Произошла ошибка{str(e)}')

def handler_text_state(message):  
    if message.text == "◀️ В меню":
        ai_service.clear_dialog(message.chat.id)
        menu(message.chat.id)
    else: 
        msg = bot.send_message(message.chat.id, 'Думаю над запросом...')
        txt = ai_service.generate_text(message.text, message.chat.id)
        msg = bot.edit_message_text(text = txt, chat_id=message.chat.id, message_id=msg.id)



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    state = stater.get_state(message.chat.id)

    logger.info(
        "Пользователь [{}:{}] отправил сообщение '{}' в состоянии {}",
        message.chat.id,
        message.from_user.first_name,
        message.text,
        state
    )
    if state == fsm.DEFAULT_STATE :
        handler_def_state(message)
    elif state == fsm.IMAGE_STATE :
        handler_image_state(message)
    elif state == fsm.TEXT_STATE :
        handler_text_state(message)

bot.polling()
