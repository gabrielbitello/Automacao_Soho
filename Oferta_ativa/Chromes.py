import config
import random
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import funcoes

# Inicialização das bases (corrigido para chamar as funções)
deu_erro = False
canvas_xpath = '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas' 
simbolo_xpath = "/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/span/svg"






def iniciar_whatsapp(ID_corretor):
    pasta = (f"whatsapp_{ID_corretor}")
    corretor = funcoes.obter_corretor(ID_corretor)
    
    perfil_whatsapp = os.path.join(config.caminho, pasta)

    chrome_options = Options()
    chrome_options.add_argument(f'user-data-dir={perfil_whatsapp}')
    chrome_options.add_argument('--ignore-certificate-errors')  

    config_whatsapp = Service(ChromeDriverManager().install())
    whatsapp = webdriver.Chrome(service=config_whatsapp, options=chrome_options)

    time.sleep(5)

    whatsapp.get('https://web.whatsapp.com/')

    body = WebDriverWait(whatsapp, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    if deu_erro == False:
        time.sleep(8)
    
    time.sleep(4)

    return whatsapp

def iniciar_crmx(ID_corretor):
    pasta = (f"crmx {ID_corretor}")
    perfil_crmx = os.path.join(config.caminho, pasta)

    chrome_options2 = Options()
    chrome_options2.add_argument(f'user-data-dir={perfil_crmx}')
    chrome_options2.add_argument('--ignore-certificate-errors')  

    config_crmx = Service(ChromeDriverManager().install())
    crmx = webdriver.Chrome(service=config_crmx, options=chrome_options2)

    time.sleep(5)

    crmx.get('https://crmx.novovista.com.br/')

    body = WebDriverWait(crmx, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    time.sleep(round(random.uniform(2, 3), 1))

    time.sleep(round(random.uniform(2, 4), 1))

    crmx.find_element(By.XPATH, '//*[@id="username"]').send_keys(funcoes.obter_corretor(ID_corretor)[0]['EmailCRMX'])

    time.sleep(round(random.uniform(1, 2), 1))

    crmx.find_element(By.XPATH, '//*[@id="password"]').send_keys(funcoes.obter_corretor(ID_corretor)[0]['SenhaCRMX']) 

    time.sleep(round(random.uniform(1, 2), 1))

    crmx.find_element(By.XPATH, '//*[@id="submitLogin"]').click() 

    time.sleep(12) 

    crmx.find_element(By.XPATH, '//*[@id="main"]/div/header/div[2]/div[7]/button').click() #abre lista de leads

    time.sleep(2)

    crmx.find_element(By.XPATH, '//*[@id="lista-campanha"]/div/div/div[2]/ul[1]/li[1]/a').click() #seleciona a lista de lead

    return crmx