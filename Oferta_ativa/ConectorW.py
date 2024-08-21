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
import sys
import os

deu_erro = False
canvas_xpath = '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas' 

def Conectar_WhatsApp(ID_corretor):
    pasta = (f"whatsapp_{ID_corretor}")
    corretor = funcoes.obter_corretor(ID_corretor)
    
    perfil_whatsapp = os.path.join(config.caminho, pasta)

    chrome_options = Options()
    chrome_options.add_argument(f'user-data-dir={perfil_whatsapp}')

    config_whatsapp = Service(ChromeDriverManager().install())
    whatsapp = webdriver.Chrome(service=config_whatsapp, options=chrome_options)

    time.sleep(5)

    whatsapp.get('https://web.whatsapp.com/')

    body = WebDriverWait(whatsapp, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    if deu_erro == False:
        time.sleep(8)
    
    time.sleep(4)

    if len(whatsapp.find_elements(By.XPATH, canvas_xpath)) > 0:
        whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[3]/div/span').click()
        time.sleep(1.5)
        whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/form/input').click()
        time.sleep(1.5)
        pyperclip.copy(corretor[0]['Numero'])
        acoes = ActionChains(whatsapp)
        acoes.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        print("Número: ", corretor[0]['Numero'])
        time.sleep(1)
        whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/button').click()
        time.sleep(1.5)
        a = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[1]/span').text
        b = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/span').text
        c = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[3]/span').text
        d = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[4]/span').text
        e = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[5]/span').text
        f = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[6]/span').text
        g = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[7]/span').text
        h = whatsapp.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[8]/span').text
        # 3 a 4m para mudar
        cod = a + b + c + d + e + f + g + h
        funcoes.atualizar_cod_corretor(ID_corretor, cod)
        while funcoes.elemento_existe(whatsapp, '/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[8]/span') == True:
            time.sleep(5)
        funcoes.att_StatusWhatsapp(ID_corretor)
    return whatsapp

if __name__ == "__main__":
    corretor_id = sys.argv[1] 
    UID_pedido = sys.argv[2] 


    # Executando o processo com os dados recebidos
    Conectar_WhatsApp(int(corretor_id), UID_pedido)
    funcoes.atualizar_h_termino()
    time.sleep(6)
    os.system('taskkill /F /IM cmd.exe')