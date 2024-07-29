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





diretorio_atual = os.getcwd()
perfil_usuario = os.path.join(diretorio_atual, 'perfil_usuario_Instagram')

chrome_options = Options()
chrome_options.add_argument(f'user-data-dir={perfil_usuario}')

servico = Service(ChromeDriverManager().install())
Instagram = webdriver.Chrome(service=servico, options=chrome_options)

time.sleep(5)

Instagram.get('chrome-extension://hndnabgpcmhdmaejoapophbidipmgnpb/dash/dash.html?match=j8imoveis&extract=follower&max=100000&interval=6&www_claim=hmac.AR2hFbdEiq0ypG5zYYDqfX9TGcp-UB4zs2Wja_UJrhgbXuvz&v=2&me=gabriel_bitello&profile=true&h=1&hc=0&')

body = WebDriverWait(Instagram, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

time.sleep(32)

nr = 10
ne = 0

while ne == nr:

    ne = ne + 1

    for i in range(1, 6):  

        #Linha 1

        User_name = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[2]/span').text
        Nome = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[3]/span').text
        Numero = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[9]/span').text
        Email = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[6]/span').text
        Cidade = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[10]/span').text
        Biography = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[1]/td[11]/span').text



        #Linha 2

        User_name2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[2]/span').text
        Nome2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[3]/span').text
        Numero2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[9]/span').text
        Email2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[6]/span').text
        Cidade2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[10]/span').text
        Biography2 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[2]/td[11]/span').text



        #Linha 3

        User_name3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[2]/span').text
        Nome3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[3]/span').text
        Numero3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[9]/span').text
        Email3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[6]/span').text
        Cidade3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[10]/span').text
        Biography3 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[3]/td[11]/span').text



        #Linha 4
        User_name4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[2]/span').text
        Nome4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[3]/span').text
        Numero4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[9]/span').text
        Email4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[6]/span').text
        Cidade4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[10]/span').text
        Biography4 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[4]/td[11]/span').text



        #Linha 5

        User_name5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[2]/span').text
        Nome5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[3]/span').text
        Numero5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[9]/span').text
        Email5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[6]/span').text
        Cidade5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[10]/span').text
        Biography5 = Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div/div[3]/table/tbody/tr[5]/td[11]/span').text


        time.sleep(random.uniform(4, 6))

    



    Instagram.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div[2]/div/div/div[4]/div[2]/a[2]').click()

