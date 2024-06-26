from chave_api import retorna_chave_api
CHAVE_API = retorna_chave_api()

import telebot
import re
from tratamento import Review


bot = telebot.TeleBot(CHAVE_API)
review = Review()


@bot.message_handler(commands=['filme'])
def avaliacao_filme(mensagem):
    nome_filme = re.search(r"/filme (.+)", mensagem.text).group(1)
    if(nome_filme != ''):

        bot.send_message(mensagem.chat.id, "Certo! Espere alguns segundos para o resultado!")
        sinopse = review.retonar_sinopse(nome_filme)
        review_filme = review.retorna_intensidade(nome_filme)

        bot.send_message(mensagem.chat.id, f"Sinopse do filme {nome_filme}:\n\n{sinopse}")
        bot.send_message(mensagem.chat.id, f"{review_filme}% das reviews são positivas sobre o filme {nome_filme}")

    else:

        bot.send_message(mensagem.chat.id, "Digite o nome do filme!")

    

@bot.message_handler(commands=['elenco'])
def elenco(mensagem):
    nome_elenco = re.search(r"/elenco (.+)", mensagem.text).group(1)
    if(nome_elenco != ''):

        bot.send_message(mensagem.chat.id, "Certo! Espere alguns segundos para o resultado!")

        filmes = review.retonar_elenco(nome_elenco)
        bot.send_message(mensagem.chat.id, filmes)
    else:
        bot.send_message(mensagem.chat.id, "Digite o nome da celebridade!")


@bot.message_handler(commands=['help'])
def help(mensagem):
    
    bot.send_message(mensagem.chat.id, 
    '/filme: mostra as informações base do filme.\n' + 
    'Exemplo de uso: /filme pixels\n'+
    '/elenco: mostra o top 10 filmes mais bem avaliados com o ator/atriz ou diretor(a) pedido.'+
    'Exemplo de uso: /elenco angelina jolie')



def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def resposta_padrao(mensagem):


    bot.reply_to(mensagem, 'Olá, seja bem vindo(a)!\n Me chamo Bex e estou aqui para falar de filmes!\n'+
                 'O comando /help mostra os comandos utilizados para as informações.')

bot.polling()