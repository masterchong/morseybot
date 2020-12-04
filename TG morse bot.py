import telebot as tb
from flask import Flask,request
import os

Token = 'TOKEN'
bot = tb.TeleBot(Token)
server = Flask(__name__)

encryption={
"a":".-",
"b":"-...",
"c":"-.-.",
"d":"-..",
"e":".",
"f":"..-.",
"g":"--.",
"h":"....",
"i":"..",
"j":".---",
"k":"-.-",
"l":".-..",
"m":"--",
"n":"-.",
"o":"---",
"p":".--.",
"q":"--.-",
"r":".-.",
"s":"...",
"t":"-",
"u":"..-",
"v":"...-",
"w":".--",
"x":"-..-",
"y":"-.--",
"z":"--..",
"1":".----",
"2":"..---",
"3":"...--",
"4":"....-",
"5":".....",
"6":"-....",
"7":"--...",
"8":"---..",
"9":"----.",
"0":"-----",
}


#handles /start and /help 
@bot.message_handler(commands=['start',"help"])
def send_welcome(message):
	bot.reply_to(message, "Welcome to morsey bot, use /encrypt to translate any english text to morse code and use /decrypt to translate any morse code to english!")

#handles /encrypt[english text]
@bot.message_handler(commands=["encrypt"])
def encrypt(message):
    #error message if no text after command
    msg = bot.reply_to(message, "What would you like to encrypt?")
    bot.register_next_step_handler(msg, toMorse)

def toMorse(message):
    encrypted=""
    try:   
        for char in message.text.lower(): 
            if char==" ":
                encrypted+="   "
            else:
                encrypted+=encryption[char]+" "
                
        bot.reply_to(message,encrypted)

    except:
        bot.reply_to(message,"Unable to encrypt this, please send only pure english text")

#handles /decrypt[morse]
@bot.message_handler(commands=["decrypt"])
def decrypt(message):
    msg = bot.reply_to(message, """\
    What would you like to decrypt? 
(use a space to separate every morse character)
    """)
    bot.register_next_step_handler(msg, toEnglish)

def toEnglish(message):
    decrypted=""
    morse=message.text.split(" ")

    try: 
        for char in morse: 
            #reverse search the dictionary
            for eng, mor in encryption.items():
                if char==mor:
                    decrypted+=eng

        bot.reply_to(message, decrypted)
    except:
        bot.reply_to(message,"Unable to encrypt this, please send only dots, dashes with a space between each morse character.")

@server.route("/"+ Token, methods=['POST'])
def getMessage():
    bot.process_new_updates([tb.types.Update.de_json(request.stream.read().decode("utf-8"))]) 
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://<APPNAME>.herokuapp.com/"+ Token)
    return "!", 200

if __name__=="__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT',5000)))
