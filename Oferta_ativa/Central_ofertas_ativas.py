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
caminho = r"C:\Users\ieubi\OneDrive\Documentos\Vg\drives\soho"

def iniciar_whatsapp():
    perfil_whatsapp = os.path.join(caminho, 'perfil_whatsapp')

    chrome_options = Options()
    chrome_options.add_argument(f'user-data-dir={perfil_whatsapp}')

    config_whatsapp = Service(ChromeDriverManager().install())
    whatsapp = webdriver.Chrome(service=config_whatsapp, options=chrome_options)

    time.sleep(5)

    whatsapp.get('https://web.whatsapp.com/')

    body = WebDriverWait(whatsapp, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    time.sleep(8)

    return whatsapp

def iniciar_crmx():
    perfil_crmx = os.path.join(caminho, 'perfil_crmx')

    chrome_options2 = Options()
    chrome_options2.add_argument(f'user-data-dir={perfil_crmx}')

    config_crmx = Service(ChromeDriverManager().install())
    crmx = webdriver.Chrome(service=config_crmx, options=chrome_options2)

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

    crmx.find_element(By.XPATH, '//*[@id="main"]/div/header/div[2]/div[7]/button').click() #abre lista de leads

    time.sleep(2)

    crmx.find_element(By.XPATH, '//*[@id="lista-campanha"]/div/div/div[2]/ul[1]/li[1]/a').click() #seleciona a lista de lead

    return crmx

def verificar_navegador(navegador):
    try:
        navegador.current_url
        return True
    except:
        return False

whatsapp = iniciar_whatsapp()
crmx = iniciar_crmx()

# Loop principal
while True:
    if not verificar_navegador(whatsapp):
        print("WhatsApp foi fechado. Reiniciando...")
        whatsapp = iniciar_whatsapp()

    if not verificar_navegador(crmx):
        print("CRMX foi fechado. Reiniciando...")
        crmx = iniciar_crmx()

    if funcoes.buscar_ofertas_ativas()[0] == 1:
        print(f"Existem {funcoes.buscar_ofertas_ativas()[1]} ofertas ativas. Iniciando o processo de contato...")
        envio_de_mensagens.contato_oferta_ativa(funcoes.buscar_ofertas_ativas()[1], funcoes.Mensagem_ofertas_ativas(), whatsapp, crmx)
        funcoes.atualizar_h_termino()
    else:
        if funcoes.buscar_ofertas_ativas()[0] == 2:
            envio_de_mensagem_expecifica.contato_mensagem(funcoes.buscar_ofertas_ativas()[1], funcoes.buscar_ofertas_ativas()[2], funcoes.buscar_ofertas_ativas()[3], funcoes.Mensagem_ofertas_ativas(), whatsapp)
            funcoes.atualizar_h_termino()
        else:
            print("Não existem mensagens específicas ativas no momento.")
        print("Não existem ofertas ativas no momento.")

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)
