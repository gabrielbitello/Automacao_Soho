import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pytz
import time
import random
import re
import pymysql.cursors          


conexao = pymysql.connect(host=config.host_Geral_Mysql,
                            user=config.user_Geral_Mysql,
                            password=config.password_Geral_Mysql,
                            database=config.database_Geral_Mysql,
                            cursorclass=pymysql.cursors.DictCursor)

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
    with conexao.cursor() as cursor:
        # Query SQL para buscar o número de ofertas ativas
        sql = "SELECT COUNT(*) AS total, pessoa, numero, nome_pessoa, nome_passou FROM soho_geral.ofertas_ativa WHERE ativa = 1 LIMIT 1"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        pessoa = resultado['pessoa']
        if pessoa == 1:
            return (1, resultado['numero'], resultado['nome_pessoa'], resultado['nome_passou'])
        else:
            return (0, resultado['total'])

def Mensagem_ofertas_ativas():
    with conexao.cursor() as cursor:
        # Query SQL para buscar o número de ofertas ativas
        sql = "SELECT mensagem FROM soho_geral.ofertas_ativa WHERE ativa = 1 LIMIT 1"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        mensagem_oferta = resultado['mensagem']
        return mensagem_oferta

def atualizar_h_termino():
    with conexao.cursor() as cursor:
        # Obtém o horário atual de São Paulo
        fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
        horario_atual_sp = datetime.now(fuso_horario_sp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Query SQL para atualizar o campo h_termino
        sql = "UPDATE soho_geral.ofertas_ativa SET ativa = 0, h_termino = %s WHERE ativa = 1 LIMIT 1"
        cursor.execute(sql, (horario_atual_sp,))
        
    # Confirma a transação
    conexao.commit()

    print("O horário de término foi atualizado com sucesso.")

def cadastrar_cliente(nome, nome_f, numero, numero_f, status, mensagem):
    with conexao.cursor() as cursor:
        # Data atual
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Query SQL para inserir os dados na tabela oferta_ativa_Clientes
        sql = """
        INSERT INTO soho_geral.oferta_ativa_Clientes (Nome, Nome_F, Numero, Numero_F, Status, Mensagem, Data, Retorno) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(sql, (nome, nome_f, numero, numero_f, status, mensagem, data_atual, 0))
        
    # Confirma a transação
    conexao.commit()

def verificar_numero_existente(numero):
    with conexao.cursor() as cursor:
        # Query SQL para verificar a existência do número e recuperar a data mais recente
        sql = "SELECT MAX(Data, Retorno) AS Data, Retorno FROM soho_geral.oferta_ativa_Clientes WHERE Numero = %s GROUP BY Numero"
        cursor.execute(sql, (numero,))
        resultado = cursor.fetchone()
        
        # Verifica se o número já existe
        if resultado is not None and resultado['Data'] is not None:
            ultima_data = resultado['Data']
            # Converte a data de string para datetime, assumindo que ultima_data é uma string no formato '%Y-%m-%d %H:%M:%S'
            ultima_data = datetime.strptime(ultima_data, '%Y-%m-%d %H:%M:%S')
            # Calcula a data 30 dias atrás a partir de hoje
            trinta_dias_atras = datetime.now() - timedelta(days=30)
            
            # Verifica se a última data registrada é menor que a data 30 dias atrás
            if ultima_data < trinta_dias_atras:
                if resultado['Retorno'] < 1:
                    return True  # O número existe, mas a última data registrada tem mais de 30 dias, e não esta bloquado o envio de mensagem
                else:
                    return False  # O número existe, mas a última data registrada tem mais de 30 dias, e esta bloquado o envio de mensagem
            else:
                return False  # O número existe e a última data registrada é recente (menos de 30 dias)
        else:
            return True  # O número não existe
