from chatterbot import ChatBot
from datetime import date
from datetime import datetime

now = datetime.now()
bot = ChatBot("Crux",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
         }])

while True:
    yo = input("Dialogo")
    charla_log = []
    respuesta = bot.get_response(yo)
    usuario_respuesta = str("{} {}:{}:{} {} : {}"
                .format(date.today(),now.hour,now.minute,now.second,"Nombre",yo))
    charla_log.append(usuario_respuesta)

    bot_respuesta = str("{} {}:{}:{} {} : {}"
                .format(date.today(),now.hour,now.minute,now.second,"Nombre",respuesta))
    print(bot_respuesta)
    charla_log.append(bot_respuesta)
    log = open("log.txt","w")
    for dialogo in charla_log:
        log.write(dialogo+"\n")
print(charla_log)
