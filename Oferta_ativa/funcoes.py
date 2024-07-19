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
        sql = "SELECT total, pessoa, numero, nome_pessoa, nome_passou FROM soho_geral.ofertas_ativa WHERE ativa = 1 LIMIT 1"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        if resultado is None:
            return (0, 0)  # Ou qualquer outro valor que indique que nenhum resultado foi encontrado
        pessoa = resultado['pessoa']
        if pessoa == 1:
            return (2, resultado['numero'], resultado['nome_pessoa'], resultado['nome_passou'])
        else:
            if pessoa == 0:
                return (1, resultado['total'])
            else:
                return (0, 0)

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
        # Primeiro, buscar a data máxima
        sql_data = "SELECT MAX(Data) AS Data FROM soho_geral.oferta_ativa_Clientes WHERE Numero_F = %s"
        cursor.execute(sql_data, (numero,))
        resultado_data = cursor.fetchone()

        print(f"Resultado da busca da data: {resultado_data}")
        
        if resultado_data is not None and resultado_data['Data'] is not None:
            ultima_data = resultado_data['Data']
            # Debug: imprimir a última data obtida
            print(f"Última data obtida do banco de dados: {ultima_data}")
            try:
                # Converte a data de string para datetime
                ultima_data_f = datetime.strptime(ultima_data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                # Debug: em caso de erro na conversão, imprimir o erro
                print(f"Erro na conversão da data: {e}")
                return True  # Retorna True para evitar enviar a mensagem

            # Debug: imprimir a data convertida
            print(f"Última data convertida para datetime: {ultima_data_f}")
            
            # Calcula a data 30 dias atrás a partir de hoje
            trinta_dias_atras = datetime.now() - timedelta(days=30)
            # Debug: imprimir a data de 30 dias atrás
            print(f"Data de 30 dias atrás: {trinta_dias_atras}")
            
            # Verifica se a última data registrada é menor que a data 30 dias atrás
            if ultima_data_f < trinta_dias_atras:
                print("A última data registrada é menor que a data de 30 dias atrás.")
                sql_retorno = "SELECT MAX(Retorno) AS Retorno FROM soho_geral.oferta_ativa_Clientes WHERE Numero_F = %s"
                cursor.execute(sql_retorno, (numero,))
                resultado_retorno = cursor.fetchone()
                
                if resultado_retorno is not None and resultado_retorno['Retorno'] is not None:
                    # Debug: imprimir o valor do retorno
                    print(f"Valor do retorno: {resultado_retorno['Retorno']}")
                    if resultado_retorno['Retorno'] == 0:
                        print("Retorno é 0. Pode enviar mensagem.")
                        return False  # O número existe, e a última data registrada tem mais de 30 dias, e não está bloqueado o envio de mensagem
                    else:
                        print("Retorno é diferente de 0. Não pode enviar mensagem.")
                        return True  # O número existe, e a última data registrada tem mais de 30 dias, e está bloqueado o envio de mensagem
            else:
                return True  # O número existe, mas a última data registrada tem menos de 30 dias
        else:
            print("O número não existe.")
            return False  # O número não existe

def remover_caracteres_nao_alfabeticos(nome):
    # Mantém apenas letras (com ou sem acentos)
    nome_limpo = re.sub(r'[^\wáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙäëïöüÄËÏÖÜãñõÃÑÕ]', '', nome)
    return nome_limpo

