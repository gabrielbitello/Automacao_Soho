from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
#import MySql_E
#from MySql_E import insere_dados
import time
import random
import os
import re
import pyperclip
import pymysql.cursors

conexao = pymysql.connect(host='mysql.bitello.cloud',
                                user='soho_geral',
                                password='Soho2024!',
                                database='soho_geral',
                                cursorclass=pymysql.cursors.DictCursor)

email = "bia.souza@primesoho.com.br"
senha = "Vgsb20077002!"

#--------------------------------------------

def formatar_telefone(numero):
    # Passo 1: Remover caracteres não numéricos, exceto o sinal de mais (+) no início
    numero_limpo = re.sub(r'(?!^\+)\D', '', numero)
    
    # Passo 2: Verificar e adicionar "+55" se necessário
    if not numero_limpo.startswith('+55'):
        numero_limpo = '+55' + numero_limpo
    
    # Passo 3: Adicionar "41" como DDD padrão se faltar
    if len(numero_limpo) < 13:
        numero_limpo = numero_limpo[:3] + '41' + numero_limpo[3:]
    
    # Passo 4: Remover 9 extra após o DDD se necessário
    if len(numero_limpo) > 13:
        numero_limpo = numero_limpo[:5] + numero_limpo[6:]
    
    # Passo 5: Formatar o número
    numero_formatado = f'{numero_limpo[:3]} {numero_limpo[3:5]} {numero_limpo[5:9]} {numero_limpo[9:]}'
    
    return numero_formatado

def clique_e_envie(nav2, xpath, texto, enter=False, simular_shift_enter=False):
    try:
        elemento = WebDriverWait(nav2, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elemento.click()
        elemento.clear()
        for caractere in texto:
            elemento.send_keys(caractere)
            time.sleep(random.uniform(0.1, 0.5))  # Ajuste o intervalo de tempo conforme necessário
        if simular_shift_enter:
            elemento.send_keys(Keys.SHIFT + Keys.ENTER)  # Simula Shift+Enter
        if enter:
            elemento.send_keys(Keys.ENTER)  # Envia a mensagem
    except Exception as e:
        print(f"Erro ao interagir com o elemento: {e}")

def buscar_ofertas_ativas():
    try:
        with conexao.cursor() as cursor:
            # Query SQL para buscar o número de ofertas ativas
            sql = "SELECT COUNT(*) AS total FROM soho_geral.ofertas_ativa WHERE ativa = 1 LIMIT 1"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            numero_ofertas = resultado['total']
            return numero_ofertas
    finally:
        conexao.close()

def atualizar_h_termino():
    try:
        with conexao.cursor() as cursor:
            # Obtém o horário atual de São Paulo
            fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
            horario_atual_sp = datetime.now(fuso_horario_sp).strftime('%Y-%m-%d %H:%M:%S')
            
            # Query SQL para atualizar o campo h_termino
            sql = "UPDATE sua_tabela SET h_termino = %s WHERE status = 1 LIMIT 1"
            cursor.execute(sql, (horario_atual_sp))
        
        # Confirma a transação
        conexao.commit()
    finally:
        conexao.close()
def cadastrar_cliente(nome, nome_f, numero, numero_f, status, mensagem):
    try:
        with conexao.cursor() as cursor:
            # Data atual
            data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Query SQL para inserir os dados na tabela Clientes
            sql = """
            INSERT INTO soho_geral.Clientes (Nome, Nome_F, Numero, Numero_F, Status, Mensagem, Data) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, nome_f, numero, numero_f, status, mensagem, data_atual))
        
        # Confirma a transação
        conexao.commit()
    finally:
        conexao.close()

def verificar_numero_existente(numero):
    try:
        with conexao.cursor() as cursor:
            # Query SQL para verificar a existência do número
            sql = "SELECT COUNT(*) AS count FROM soho_geral.Clientes WHERE Numero = %s"
            cursor.execute(sql, (numero,))
            resultado = cursor.fetchone()
            
            # Verifica se o número já existe
            if resultado['count'] > 0:
                return True
            else:
                return False
    finally:
        conexao.close()

#--------------------------------------------

while True:
    n_ofertas_ativas = buscar_ofertas_ativas()
    if n_ofertas_ativas > 0:
        print(f"Existem {n_ofertas_ativas} ofertas ativas. Iniciando o processo de contato...")
        # Inicializa o navegador 1
        servico1 = Service(ChromeDriverManager().install())
        nav1 = webdriver.Chrome(service=servico1)

        time.sleep(5)

        nav1.get('https://crmx.novovista.com.br/')

        body = WebDriverWait(nav1, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        time.sleep(round(random.uniform(2, 4), 1))

        nav1.find_element(By.XPATH, '//*[@id="username"]').send_keys(email)

        time.sleep(round(random.uniform(1, 2), 1))

        nav1.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha) 

        time.sleep(round(random.uniform(1, 2), 1))

        nav1.find_element(By.XPATH, '//*[@id="submitLogin"]').click() 

        body = WebDriverWait(nav1, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))) 

        time.sleep(round(random.uniform(1, 2), 1))

        nav1.find_element(By.XPATH, '//*[@id="form_93R1295k8LZ341787"]/div/div[1]/button').click()  #fecha ad

        time.sleep(2)

        nav1.find_element(By.XPATH, '//*[@id="main"]/div/header/div[2]/div[7]/button').click() #abre lsita de leads

        time.sleep(2)

        nav1.find_element(By.XPATH, '//*[@id="lista-campanha"]/div/div/div[2]/ul[1]/li[1]/a').click() #seleciona a lsita de lead

        #inicia o navegador 2
        diretorio_atual = os.getcwd()
        perfil_usuario = os.path.join(diretorio_atual, 'perfil_usuario')

        chrome_options = Options()
        chrome_options.add_argument(f'user-data-dir={perfil_usuario}')

        servico2 = Service(ChromeDriverManager().install())
        nav2 = webdriver.Chrome(service=servico2, options=chrome_options)

        time.sleep(5)

        nav2.get('https://web.whatsapp.com/')

        body = WebDriverWait(nav2, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        time.sleep(8)

        

        #Inicia o processo de contato
        for i in range(n_ofertas_ativas):

            time.sleep(2)

            nav1.find_element(By.XPATH, '//*[@id="info-cliente"]/div[2]/div/div[3]/div/div[1]/button').click()  #atender cliente

            nome_cliente = nav1.find_element(By.XPATH, '//*[@id="oferta-ativa-body-content"]/p[3]/strong').text

            numero_cliente = nav1.find_element(By.XPATH, '//*[@id="oferta-ativa-body-content"]/p[4]').text

            #--------------------------------------------

            numero_formatado = formatar_telefone(numero_cliente)

            primeiro_nome = nome_cliente.split(" ")[0] 

            fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
            hora_atual_sp = datetime.now(fuso_horario_sp).hour

            if 6 <= hora_atual_sp < 12:
                saudacao = "Bom dia"
            elif 12 <= hora_atual_sp < 18:
                saudacao = "Boa tarde"
            else:
                saudacao = "Boa noite"

            texto_1_contato_neutro_p1 = "Meu nome é Gabriel e sou corretor de imóveis na Prime Soho. Recentemente, você forneceu suas informações de contato em resposta a um anúncio imobiliário."
            texto_1_contato_neutro_p2 = f"Então {primeiro_nome}, estou entrando em contato para saber se ainda está à procura de imóveis. Temos diversas opções disponíveis, tanto prontas quanto na planta, e acredito que podemos encontrar algo que atenda suas necessidades."
            texto_1_contato_neutro_p3 = "Caso tenha interesse, ficarei feliz em conversa para entender melhor o que está procurando e apresentar algumas opções. Estou à disposição para qualquer dúvida."

            msg_1_contato = f"{saudacao}, tudo bom {primeiro_nome}?\n\n{texto_1_contato_neutro_p1}\n\n{texto_1_contato_neutro_p2}\n\n{texto_1_contato_neutro_p3}\n\nAguardo seu retorno."

            #--------------------------------------------

            if verificar_numero_existente(numero_formatado):
                print("O número já existe na tabela de clientes.")
                opcao_select = "Pediu Informações"
            else:
                nav2.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div/span').click()  # Clica no ícone de nova mensagem

                time.sleep(round(random.uniform(2, 3), 1))

                xpath_novo_contato = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
                clique_e_envie(nav2, xpath_novo_contato, numero_formatado, enter=True)

                try:
                    pyperclip.copy(msg_1_contato)

                    # Encontra o campo de mensagem
                    campo_mensagem = nav2.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')

                    # Clica no campo de mensagem para garantir que ele está focado
                    campo_mensagem.click()

                    
                    time.sleep(round(random.uniform(3, 5), 1))

                    acoes = ActionChains(nav2)
                    acoes.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                    
                    time.sleep(round(random.uniform(2, 3), 1))

                    campo_mensagem.send_keys(Keys.ENTER)

                    time.sleep(3)

                    opcao_select = "Pediu Informações"
                    cadastrar_cliente(nome_cliente, primeiro_nome, numero_cliente, numero_formatado, 1, msg_1_contato, hora_atual_sp)

                except NoSuchElementException:
                    # Se o elemento não for encontrado, entra no except
                    opcao_select = "Telefone Inválido"
                    cadastrar_cliente(nome_cliente, primeiro_nome, numero_cliente, numero_formatado, 0, msg_1_contato, hora_atual_sp)

                #--------------------------------------------

                status_contato = nav1.find_element(By.XPATH, '//*[@id="status"]')  # Corrige o status do contato select
                select = Select(status_contato)  # Seleciona o <select>
                select.select_by_visible_text(opcao_select)  # Seleciona a opção do select

                nav1.find_element(By.XPATH, '//*[@id="form_kqq83Z9T29"]/div[2]/div/div[3]/div/div[1]/button').click() # Salva o status do contato
        atualizar_h_termino()
    else:
        print("Não há novas ofertas ativas no momento.")
        nav1.close()
        nav2.close()

            

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)


















