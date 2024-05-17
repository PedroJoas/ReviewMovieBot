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
        review_filme = review.retorna_intensidade(nome_filme)
        bot.send_message(mensagem.chat.id, f"{nome_filme} tem média de sentimentos de: {review_filme}")

    else:
        
        bot.send_message(mensagem.chat.id, "Digite o nome do filme!")

    

@bot.message_handler(commands=['elenco'])
def elenco(mensagem):
    nome_elenco = re.search(r"/elenco (.+)", mensagem.text).group(1)
    pass

@bot.message_handler(commands=['direcao'])
def direcao(mensagem):
    nome_direcao = re.search(r"/direcao (.+)", mensagem.text).group(1)
    pass

@bot.message_handler(commands=['help'])
def help(mensagem):
    info_help = '''/filme: mostra as informações base do filme. Exemplo de uso: /filme pixels
    /elenco: mostra o top 10 filmes mais bem avaliados com o ator/atriz pedido. Exemplo de uso: /elenco angelina jolie
    /direcao: mostra o top 10 filmes mais bem avaliados com o diretor(a) pedido. Exemplo de uso: /elenco george lucas
    '''
    bot.send_message(mensagem.chat.id, info_help)

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def resposta_padrao(mensagem):
    mensagem_padrao = '''
        Olá, seja bem vindo(a)!\n Me chamo Bex e estou aqui para falar de filmes!
o comando /help mostra os comandos utilizados para as informações.
    '''
    bot.reply_to(mensagem, mensagem_padrao)

bot.polling()