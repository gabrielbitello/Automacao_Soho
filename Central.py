import time
from Oferta_ativa import funcoes
import os

def executar_OfertaAtiva(corretor_id, repeticoes, tipo, idoferta_ativa, Mensagem):
    comando = f'start cmd /k "python Oferta_ativa/Ofertas_ativas.py {corretor_id} {repeticoes} {tipo} {idoferta_ativa} {Mensagem}"'
    print(f"Executando Oferta")
    os.system(comando)

def executar_ConectarW(corretor_id, UID_pedido):
    comando = f'start cmd /k "python Oferta_ativa/ConectorW.py {corretor_id} {UID_pedido}"'
    print(f"Executando Oferta")
    os.system(comando)


while True:
    OfertaAtiva = funcoes.buscar_ofertas_ativas()
    Conector = funcoes.buscar_ConectorW()
    if OfertaAtiva[0] == 1 and int(OfertaAtiva[5]) == 0:
        funcoes.att_status()
        corretor_id = OfertaAtiva[2]
        repeticoes = OfertaAtiva[1]
        idoferta_ativa = OfertaAtiva[4]
        Mensagem = OfertaAtiva[6]
        print(f"Existem {repeticoes} ofertas ativas. Iniciando o processo com corretor {corretor_id}...")
        executar_OfertaAtiva(corretor_id, repeticoes, 1, idoferta_ativa, Mensagem)
    else:
        if OfertaAtiva[0] == 2 and OfertaAtiva[7] == 0:
            corretor_id = OfertaAtiva[4]
            repeticoes = OfertaAtiva[1]
            idoferta_ativa = OfertaAtiva[6]
            print(f"Iniciando processo específico com corretor {corretor_id}...")
            executar_OfertaAtiva(corretor_id, repeticoes, 2, idoferta_ativa, Mensagem)
            funcoes.atualizar_h_termino()
        else:
            print("Não existem mensagens específicas ou ofertas ativas no momento.")

    # Verifica se tem pedido de login whatsapp
    if Conector != [] and Conector[2] == 1:
        funcoes.att_StatusWhatsapp_cod(Conector[0], Conector[1])
        corretor_id = Conector[0]
        UID_cod = Conector[1]
        print(f"Corretor {corretor_id} precisa fazer login no WhatsApp.")
        executar_ConectarW(corretor_id, UID_cod)
        funcoes.att_status()


    time.sleep(30)
