from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

import funcoes
import config
import envio_de_mensagens
import envio_de_mensagem_expecifica

# Inicialização das bases (corrigido para chamar as funções)
diretorio_atual = os.getcwd()
perfil_usuario = os.path.join(diretorio_atual, 'perfil_usuario')

chrome_options = Options()
chrome_options.add_argument(f'user-data-dir={perfil_usuario}')

servico2 = Service(ChromeDriverManager().install())
whatsapp = webdriver.Chrome(service=servico2, options=chrome_options)

time.sleep(5)

whatsapp.get('https://web.whatsapp.com/')

body = WebDriverWait(whatsapp, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

time.sleep(8)




# Inicialização da base do CRMX
diretorio_atual = os.getcwd()
perfil_usuario = os.path.join(diretorio_atual, 'perfil_usuario1')

chrome_options1 = Options()
chrome_options1.add_argument(f'user-data-dir={perfil_usuario}')

servico1 = Service(ChromeDriverManager().install())
crmx = webdriver.Chrome(service=servico1, options=chrome_options1)

time.sleep(5)

crmx.get('https://crmx.novovista.com.br/')

body = WebDriverWait(crmx, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

time.sleep(round(random.uniform(2, 3), 1))

time.sleep(round(random.uniform(2, 4), 1))

crmx.find_element(By.XPATH, '//*[@id="username"]').send_keys(config.email_CRMX)

time.sleep(round(random.uniform(1, 2), 1))

crmx.find_element(By.XPATH, '//*[@id="password"]').send_keys(config.senha_CRMX) 

time.sleep(round(random.uniform(1, 2), 1))

crmx.find_element(By.XPATH, '//*[@id="submitLogin"]').click() 

time.sleep(12) 

crmx.find_element(By.XPATH, '//*[@id="main"]/div/header/div[2]/div[7]/button').click() #abre lsita de leads

time.sleep(2)

crmx.find_element(By.XPATH, '//*[@id="lista-campanha"]/div/div/div[2]/ul[1]/li[1]/a').click() #seleciona a lista de lead


# Loop principal
while True:

    if funcoes.buscar_ofertas_ativas()[0] == 1:
        print(f"Existem {funcoes.buscar_ofertas_ativas()[1]} ofertas ativas. Iniciando o processo de contato...")
        envio_de_mensagens.contato_oferta_ativa(funcoes.buscar_ofertas_ativas()[1], funcoes.Mensagem_ofertas_ativas(), whatsapp, crmx)
        funcoes.atualizar_h_termino()
    else:
        if funcoes.buscar_ofertas_ativas()[0] == 2:
            envio_de_mensagem_expecifica.contato_mensagem(funcoes.buscar_ofertas_ativas()[1], funcoes.buscar_ofertas_ativas()[2], funcoes.buscar_ofertas_ativas()[3], funcoes.
            Mensagem_ofertas_ativas(), whatsapp)
            funcoes.atualizar_h_termino()
        else:
            print("Não existem mensagens expecificas ativas no momento.")
        print("Não existem ofertas ativas no momento.")

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)