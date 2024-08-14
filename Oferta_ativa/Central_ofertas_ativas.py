import time
import funcoes
import os

def executar_script(corretor_id, repeticoes, tipo, idoferta_ativa):
    comando = f'start cmd /k "python Ofertas_ativas.py {corretor_id} {repeticoes} {tipo} {idoferta_ativa}"'
    print(f"Executando comando: {comando}")
    os.system(comando)


while True:
    resultado = funcoes.buscar_ofertas_ativas()
    if resultado[0] == 1 and int(resultado[5]) == 0:
        funcoes.att_status()
        corretor_id = resultado[2]
        repeticoes = resultado[1]
        idoferta_ativa = resultado[4]
        print(f"Existem {repeticoes} ofertas ativas. Iniciando o processo com corretor {corretor_id}...")
        executar_script(corretor_id, repeticoes, 1, idoferta_ativa)
    else:
        if resultado[0] == 2 and resultado[7] == 0:
            corretor_id = resultado[4]
            repeticoes = resultado[1]
            idoferta_ativa = resultado[6]
            print(f"Iniciando processo específico com corretor {corretor_id}...")
            executar_script(corretor_id, repeticoes, 2, idoferta_ativa)
            funcoes.atualizar_h_termino()
        else:
            print("Não existem mensagens específicas ou ofertas ativas no momento.")

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)
