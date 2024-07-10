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


def contato_oferta_ativa(loop, mensagem_oferta, whatsapp, crmx):
    n_loop = loop
    # Inicia o processo de contato
    while n_loop > 0:

        time.sleep(2)

        crmx.find_element(By.XPATH, '//*[@id="info-cliente"]/div[2]/div/div[3]/div/div[1]/button').click()  # Atender cliente

        time.sleep(2)

        nome_cliente = crmx.find_element(By.XPATH, '//*[@id="oferta-ativa-body-content"]/p[3]/strong').text

        print(f"Contatando {nome_cliente}...")

        numero_cliente = crmx.find_element(By.XPATH, '//*[@id="oferta-ativa-body-content"]/p[4]').text

        print(f"Telefone: {numero_cliente}")

        # --------------------------------------------

        numero_formatado = funcoes.formatar_telefone(numero_cliente)

        print(f"Telefone: {numero_formatado}")

        primeiro_nome = nome_cliente.split(" ")[0]

        # --------------------------------------------

        if funcoes.verificar_numero_existente(numero_formatado):
            print("O número já existe na tabela de clientes.")
            opcao_select = "Pediu Informações"
        else:

            time.sleep(round(random.uniform(3, 5), 1))

            whatsapp.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div').click()  # Clica no ícone de nova mensagem

            time.sleep(round(random.uniform(2, 3), 1))

            xpath_novo_contato = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
            funcoes.clique_e_envie(whatsapp, xpath_novo_contato, numero_formatado, enter=False)

            try:

                mensagem = Mensagem.Mensagem(primeiro_nome, mensagem_oferta)

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

                opcao_select = "Pediu Informações"
                funcoes.cadastrar_cliente(nome_cliente, primeiro_nome, numero_cliente, numero_formatado, 1, mensagem)

            except NoSuchElementException:
                # Se o elemento não for encontrado, entra no except
                opcao_select = "Telefone Inválido"
                funcoes.cadastrar_cliente(nome_cliente, primeiro_nome, numero_cliente, numero_formatado, 0, mensagem)

            # --------------------------------------------

            status_contato = crmx.find_element(By.XPATH, '//*[@id="status"]')  # Corrige o status do contato select
            select = Select(status_contato)  # Seleciona o <select>
            select.select_by_visible_text(opcao_select)  # Seleciona a opção do select

            crmx.find_element(By.XPATH, '/html/body/div[13]/div[2]/div[2]/div[2]/form/div[2]/div/div[3]/div/div[1]/button').click()  # Salva o status do contato

        print("Executando a oferta ativa")
        n_loop -= 1