from chatterbot import ChatBot
from datetime import date
from datetime import datetime


bot = ChatBot("Crux",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
         }])
log = open("log.txt","w")
def registro_log (dialogo,usuario):
    now = datetime.now()
    dialogo_log = str("{} {}:{}:{} {} : {}"
                .format(date.today(),now.hour,now.minute,now.second,usuario,dialogo))
    log.write(dialogo_log+"\n")
while True:
    yo = input("Dialogo")
    registro_log(yo,"Enzo")
    respuesta = bot.get_response(yo)
    registro_log(respuesta,"Crux")
    break


        