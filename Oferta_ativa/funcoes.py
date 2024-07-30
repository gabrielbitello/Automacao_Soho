import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pytz
import time
import random
import requests
import re
import logging
import pymysql.cursors       


logging.basicConfig(filename='app_errors.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def formatar_telefone(numero):
    # Passo 1: Remover caracteres não numéricos, exceto o sinal de mais (+) no início
    numero_limpo = re.sub(r'(?!^\+)\D', '', numero)
    
    # Passo 2: Verificar e adicionar "+55" se necessário, ajustando para não duplicar "55"
    if not numero_limpo.startswith('+'):
        if numero_limpo.startswith('55'):
            numero_limpo = '+' + numero_limpo
        else:
            numero_limpo = '+55' + numero_limpo
    
    # Passo 3: Adicionar "41" como DDD padrão se faltar
    if len(numero_limpo) < 13:
        numero_limpo = numero_limpo[:3] + '41' + numero_limpo[3:]
    
    # Passo 4: Remover um dígito '9' após o DDD se o número for de celular e tiver o dígito extra
    if len(numero_limpo) == 14 and numero_limpo[5] == '9':
        numero_limpo = numero_limpo[:5] + numero_limpo[6:]
    
    # Passo 5: Remover dois dígitos extras após o DDD se o número for muito longo e não seguir a regra anterior
    elif len(numero_limpo) > 13:
        numero_limpo = numero_limpo[:5] + numero_limpo[7:]
    
    # Passo 6: Formatar o número
    numero_formatado = f'{numero_limpo[:3]} {numero_limpo[3:5]} {numero_limpo[5:9]}-{numero_limpo[9:]}'
    
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
            time.sleep(2)
            elemento.send_keys(Keys.ENTER)  # Envia a mensagem
    except Exception as e:
        print(f"Erro ao interagir com o elemento: {e}")

def buscar_ofertas_ativas():
    try:
        response = requests.get('https://soho.bitello.cloud/API/buscar_oferta_ativa.php')
        if response.status_code == 200:
            resultado = response.json()
            return tuple(resultado)
        else:
            print(f"Erro ao buscar ofertas ativas: {response.status_code}")
            return (0, 0)
    except Exception as e:
        print(f"Erro ao buscar ofertas ativas: {e}")
        logging.error(f"Erro ao buscar ofertas ativas: {e}")
        return (0, 0)

def Mensagem_ofertas_ativas():
    try:
        response = requests.get('https://soho.bitello.cloud/API/mensagem_oferta_ativa.php')
        if response.status_code == 200:
            resultado = response.json()
            return resultado.get('mensagem', 'Nenhuma oferta ativa encontrada')
        else:
            print(f"Erro ao buscar mensagem de ofertas ativas: {response.status_code}")
            return 'Neutro'
    except Exception as e:
        print(f"Erro ao buscar mensagem de ofertas ativas: {e}")
        logging.error(f"Erro ao buscar mensagem de ofertas ativas: {e}")
        return 'Neutro'

def atualizar_h_termino():
    try:
        response = requests.get('https://soho.bitello.cloud/API/atualiza_h_termina.php')
        if response.status_code == 200:
            resultado = response.json()
            print(resultado.get('success', 'Erro ao atualizar o horário de término'))
        else:
            print(f"Erro ao atualizar o horário de término: {response.status_code}")
    except Exception as e:
        print(f"Erro ao atualizar o horário de término: {e}")
        logging.error(f"Erro ao atualizar o horário de término: {e}")

def cadastrar_cliente(nome_cliente, primeiro_nome, numero_cliente, numero_formatado, status, mensagem):
    url = 'https://soho.bitello.cloud/API/cadastrar_cliente.php'
    data = {
        'nome': nome_cliente,
        'nome_f': primeiro_nome,
        'numero': numero_cliente,
        'numero_f': numero_formatado,
        'status': status,
        'mensagem': mensagem
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            resultado = response.json()
            print(resultado.get('success', 'Erro ao cadastrar cliente'))
        else:
            print(f"Erro ao cadastrar cliente: {response.status_code}")
            logging.error(f"Erro ao cadastrar cliente: {response.status_code}")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
        logging.error(f"Erro ao cadastrar cliente: {e}")

def verificar_numero_existente(numero):
    url = 'https://soho.bitello.cloud/API/verificar_numero_existente.php'
    data = {'numero': numero}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            resultado = response.json()
            return resultado
        else:
            print(f"Erro ao verificar número: {response.status_code}")
            logging.error(f"Erro ao verificar número: {response.status_code}")
            return True
    except Exception as e:
        print(f"Erro ao verificar número: {e}")
        logging.error(f"Erro ao verificar número: {e}")
        return True

def remover_caracteres_nao_alfabeticos(nome):
    # Mantém apenas letras (com ou sem acentos)
    nome_limpo = re.sub(r'[^\wáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙäëïöüÄËÏÖÜãñõÃÑÕ]', '', nome)
    return nome_limpo

