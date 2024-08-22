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
    resultado = funcoes.buscar_ofertas_ativas()
    if resultado[0] == 1 and int(resultado[5]) == 0:
        funcoes.att_status()
        corretor_id = resultado[2]
        repeticoes = resultado[1]
        idoferta_ativa = resultado[4]
        Mensagem = resultado[6]
        print(f"Existem {repeticoes} ofertas ativas. Iniciando o processo com corretor {corretor_id}...")
        executar_OfertaAtiva(corretor_id, repeticoes, 1, idoferta_ativa, Mensagem)
    else:
        if resultado[0] == 2 and resultado[7] == 0:
            corretor_id = resultado[4]
            repeticoes = resultado[1]
            idoferta_ativa = resultado[6]
            print(f"Iniciando processo específico com corretor {corretor_id}...")
            executar_OfertaAtiva(corretor_id, repeticoes, 2, idoferta_ativa, Mensagem)
            funcoes.atualizar_h_termino()
        else:
            print("Não existem mensagens específicas ou ofertas ativas no momento.")

    # Verifica se tem pedido de login whatsapp
    if funcoes.buscar_ConectorW() != []:
        corretor_id = funcoes.buscar_ConectorW()[0]
        UID_cod = funcoes.buscar_ConectorW()[1]
        print(f"Corretor {corretor_id} precisa fazer login no WhatsApp.")
        executar_ConectarW(corretor_id, UID_cod)
        funcoes.att_status()


    time.sleep(30)
