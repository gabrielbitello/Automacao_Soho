from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import pyperclip         


import funcoes
import Mensagem


def contato_mensagem(numero, nome, nome_passou, mensagem_oferta, whatsapp):

    nome_cliente = nome

    numero_formatado = numero

    print(f"Contatando {nome_cliente}...")
    print(f"Telefone: {numero_formatado}")

    # --------------------------------------------

    time.sleep(round(random.uniform(3, 5), 1))

    whatsapp.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div/span').click()  # Clica no ícone de nova mensagem

    time.sleep(round(random.uniform(2, 3), 1))

    xpath_novo_contato = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
    funcoes.clique_e_envie(whatsapp, xpath_novo_contato, numero_formatado, enter=False)


    mensagem = Mensagem.Mensagem(nome_cliente, mensagem_oferta, nome_passou)

    time.sleep(round(random.uniform(3, 5), 1))

    whatsapp.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div').click()

    time.sleep(round(random.uniform(3, 5), 1))

    pyperclip.copy(mensagem)

    # Encontra o campo de mensagem
    campo_mensagem = whatsapp.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')

    # Clica no campo de mensagem para garantir que ele está focado
    campo_mensagem.click()

    time.sleep(round(random.uniform(3, 5), 1))

    acoes = ActionChains(whatsapp)
    acoes.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    time.sleep(round(random.uniform(2, 3), 1))

    campo_mensagem.send_keys(Keys.ENTER)

    time.sleep(3)

    funcoes.cadastrar_cliente(nome_cliente, nome_cliente, numero_formatado, numero_formatado, 1, mensagem)

    # --------------------------------------------

    print("Executando a oferta ativa")
