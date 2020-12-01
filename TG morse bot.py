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

#function to translate english to morse
def toMorse(message):
    encrypted=""
    for char in message.lower(): 
         if char==" ":
             encrypted+="   "
         else:
              encrypted+=encryption[char]+" "
              
    return encrypted

#function to translate english to morse
def toEnglish(message):
    decrypted=""
    message=message.split(" ")

    for char in message: 
        #reverse search the dictionary
        for eng, mor in encryption.items():
            if char==mor:
                decrypted+=eng
    return decrypted

#handles /start and /help 
@bot.message_handler(commands=['start',"help"])
def send_welcome(message):
	bot.reply_to(message, "Welcome to morsey bot, send an english text here to convert to morse code!")

#handles /encrypt[english text]
@bot.message_handler(commands=["encrypt"])
def encrypt(message):
    if len(message.text)==8:
        #error message if no text after command
        bot.reply_to(message, "Please send your text after the commnad eg: /encrypt [text]")
    else:
        try:
            toReply = toMorse(message.text[9:])
            bot.reply_to(message,toReply)
        except:
            bot.reply_to(message, "Please try again, only english text")

#handles /decrypt[morse]
@bot.message_handler(commands=["decrypt"])
def decrypt(message):
    if len(message.text)==8:
        #error message if no text after command
        bot.reply_to(message, "Please send your text after the commnad eg: /decrypt [morse code]")
    else:
        try:
            toReply = toEnglish(message.text[9:])
            bot.reply_to(message,toReply)
        except:
            bot.reply_to(message, "Please try again, invalid morse code")


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