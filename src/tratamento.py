import nltk
import re
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options

#nltk.download('stopwords')
#nltk.download('vader_lexicon')


class Review:
    options = Options()
    options.add_argument("--headless")

    def retorna_intensidade(self, nome_filme):
        reviews_filmes = self._reviews(nome_filme)
        reviews_processadas = [self._pre_processamento(review) for review in reviews_filmes]
        reviews_sentimentos = [self._analise_sentimento(review) for review in reviews_processadas]
        media_intensidade = self._media_intensidade(reviews_sentimentos)

        return media_intensidade

    def _pre_processamento(self, texto):
        # Aqui eu pego somente o que é letra dentro do texto, tirando pontuações e outros sinais, e coloco tudo em minúsculo
        letras_min = re.findall(r'\b[A-zÀ-úü]+\b', texto.lower())

        # Aqui fica o tratamento com stopwords
        stopwords = nltk.corpus.stopwords.words('portuguese')
        sem_stopwords = [word for word in letras_min if word not in stopwords]

        texto_limpo = ' '.join(sem_stopwords)

        return texto_limpo

    def _analise_sentimento(self, texto_limpo):
        sentimento = SentimentIntensityAnalyzer()

        intensidade_sentimento = sentimento.polarity_scores(texto_limpo)

        return intensidade_sentimento['compound']

    def _media_intensidade(self, sentimentos):

        return np.round(np.mean(sentimentos), 2)

    def _reviews(self, filme):

        driver = None
        try:
            driver = webdriver.Chrome(options=self.options)

            # Exemplo de url do filme: https://www.rottentomatoes.com/m/kingdom_of_the_planet_of_the_apes/reviews
            # Os espaços nos nomes do filmes são preenchidos por _

            filme = filme.lower().replace(" ", "_")

            url = f"https://www.rottentomatoes.com/m/{filme}/reviews"

            driver.get(url)

            cont = 0
            while cont < 3:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "rt-button"))
                )

                button.click()
                cont += 1

                sleep(1)

            sleep(1)

            texts = [t.text for t in driver.find_elements(By.CLASS_NAME, "review-text")]

            return texts
        
        finally:
            if driver:
                driver.quit()