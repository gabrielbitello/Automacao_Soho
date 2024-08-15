import time
import sys
import os
from selenium.common.exceptions import NoSuchWindowException

import funcoes
import envio_de_mensagens
import envio_de_mensagem_expecifica
import Chromes




print ("Iniciando o processo de contato...")

def verificar_navegador(navegador):
    try:
        navegador.current_url
        return True
    except:
        return False

def reiniciar_navegador(navegador, tipo, tipo_mensagem, id):
    if tipo == 'whatsapp':
        if tipo_mensagem == 1:
            return Chromes.iniciar_whatsapp(id)
        elif tipo_mensagem == 2:
            return Chromes.iniciar_whatsapp(id)
    elif tipo == 'crmx':
        return Chromes.iniciar_crmx(id)
    return None

def verificar(id):
    if int(funcoes.verificar_oferta_ativa(id)[0]['restante']) > 0:
        return True
    else:
        return False
    

def start (id, Nloop, tipo, id_oferta_ativa):
    whatsapp = Chromes.iniciar_whatsapp(id)
    crmx = Chromes.iniciar_crmx(id)

    deu_erro = False
    while verificar(id_oferta_ativa):

        if not verificar_navegador(whatsapp):
            print("WhatsApp foi fechado. Reiniciando...")
            whatsapp = reiniciar_navegador(whatsapp, 'whatsapp', tipo, id)

        if not verificar_navegador(crmx):
            print("CRMX foi fechado. Reiniciando...")
            crmx = Chromes.iniciar_crmx(id)

        try:
            if tipo == 1:
                print(f"Existem {Nloop} ofertas ativas. Iniciando o processo de contato...")
                envio_de_mensagens.contato_oferta_ativa(Nloop, funcoes.Mensagem_ofertas_ativas(), whatsapp, crmx, deu_erro, id_oferta_ativa, id)
                funcoes.atualizar_h_termino()
            else:
                if tipo == 2:
                    envio_de_mensagem_expecifica.contato_mensagem(funcoes.buscar_ofertas_ativas()[1], funcoes.buscar_ofertas_ativas()[2], funcoes.buscar_ofertas_ativas()[3], funcoes.Mensagem_ofertas_ativas(), whatsapp)
                    funcoes.atualizar_h_termino()
                else:
                    print("Não existem mensagens específicas ativas no momento.")
                print("Não existem ofertas ativas no momento.")
        except NoSuchWindowException:
            print("Navegador foi fechado durante a execução. Reiniciando e continuando...")
            if not verificar_navegador(whatsapp):
                whatsapp = reiniciar_navegador(whatsapp, 'whatsapp', id)
                deu_erro = True
            if not verificar_navegador(crmx):
                crmx = reiniciar_navegador(crmx, 'crmx')

        time.sleep(60)



if __name__ == "__main__":
    corretor_id = sys.argv[1] 
    repeticoes = int(sys.argv[2]) 
    tipo = sys.argv[3] 
    idoferta_ativa = sys.argv[4]

    # Executando o processo com os dados recebidos
    start(int(corretor_id), int(repeticoes), int(tipo), int(idoferta_ativa))
    funcoes.atualizar_h_termino()
    sys.exit()
    time.sleep(6)
    os.system('taskkill /F /IM cmd.exe')