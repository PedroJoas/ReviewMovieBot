from chave_api import retorna_chave_api
CHAVE_API = retorna_chave_api()

import telebot
import re
from tratamento import Review


bot = telebot.TeleBot(CHAVE_API)
review = Review()

@bot.message_handler(commands=['filme'])
def pegar_nome_filme(mensagem):
    nome_filme = re.search(r"/filme (.+)", mensagem.text).group(1)
    bot.send_message(mensagem.chat.id, "Certo! Espere alguns segundos para o resultado!")
    
    review_filme = review.retorna_intensidade(nome_filme)
    bot.send_message(mensagem.chat.id, f"{nome_filme} tem média de sentimentos de: {review_filme}")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def resposta_padrao(mensagem):
    mensagem_padrao = '''
        Olá, bem vindo!
    Digite o nome do filme:
    '''
    bot.reply_to(mensagem, mensagem_padrao)

bot.polling()