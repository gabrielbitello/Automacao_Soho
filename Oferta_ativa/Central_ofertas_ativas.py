import time
from selenium.common.exceptions import NoSuchWindowException

import funcoes
import envio_de_mensagens
import envio_de_mensagem_expecifica
import Chromes



def verificar_navegador(navegador):
    try:
        navegador.current_url
        return True
    except:
        return False

def reiniciar_navegador(navegador, tipo):
    if tipo == 'whatsapp':
        return Chromes.iniciar_whatsapp()
    elif tipo == 'crmx':
        return Chromes.iniciar_crmx()
    return None






# Loop principal
while True:
    if not verificar_navegador(whatsapp):
        print("WhatsApp foi fechado. Reiniciando...")
        whatsapp = reiniciar_navegador(whatsapp, 'whatsapp')

    if not verificar_navegador(crmx):
        print("CRMX foi fechado. Reiniciando...")
        crmx = reiniciar_navegador(crmx, 'crmx')

    try:
        if funcoes.buscar_ofertas_ativas()[0] == 1:
            whatsapp = Chromes.iniciar_whatsapp(funcoes.buscar_ofertas_ativas()[2])
            crmx = Chromes.iniciar_crmx()
            print(f"Existem {funcoes.buscar_ofertas_ativas()[1]} ofertas ativas. Iniciando o processo de contato...")
            envio_de_mensagens.contato_oferta_ativa(funcoes.buscar_ofertas_ativas()[1], funcoes.Mensagem_ofertas_ativas(), whatsapp, crmx, deu_erro)
            funcoes.atualizar_h_termino()
        else:
            if funcoes.buscar_ofertas_ativas()[0] == 2:
                whatsapp = Chromes.iniciar_whatsapp(funcoes.buscar_ofertas_ativas()[4])
                crmx = Chromes.iniciar_crmx()
                envio_de_mensagem_expecifica.contato_mensagem(funcoes.buscar_ofertas_ativas()[1], funcoes.buscar_ofertas_ativas()[2], funcoes.buscar_ofertas_ativas()[3], funcoes.Mensagem_ofertas_ativas(), whatsapp)
                funcoes.atualizar_h_termino()
            else:
                print("Não existem mensagens específicas ativas no momento.")
            print("Não existem ofertas ativas no momento.")
    except NoSuchWindowException:
        print("Navegador foi fechado durante a execução. Reiniciando e continuando...")
        if not verificar_navegador(whatsapp):
            whatsapp = reiniciar_navegador(whatsapp, 'whatsapp')
            deu_erro = True
        if not verificar_navegador(crmx):
            crmx = reiniciar_navegador(crmx, 'crmx')

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)
