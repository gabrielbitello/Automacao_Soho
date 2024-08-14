import time
import subprocess
from selenium.common.exceptions import NoSuchWindowException
import funcoes

def executar_script(corretor_id, repeticoes, tipo, idoferta_ativa):
    comando = f'python Ofertas_ativas.py {corretor_id} {repeticoes} {tipo} {idoferta_ativa}'
    subprocess.run(comando, shell=True)

while True:
    try:
        resultado = funcoes.buscar_ofertas_ativas()
        if resultado[0] == 1:
            corretor_id = resultado[2]
            repeticoes = resultado[1]
            idoferta_ativa = resultado[4]
            print(f"Existem {repeticoes} ofertas ativas. Iniciando o processo com corretor {corretor_id}...")
            executar_script(corretor_id, repeticoes, 1, idoferta_ativa)
            funcoes.atualizar_h_termino()
        else:
            if resultado[0] == 2:
                corretor_id = resultado[4]
                repeticoes = resultado[1]
                idoferta_ativa = resultado[6]
                print(f"Iniciando processo específico com corretor {corretor_id}...")
                executar_script(corretor_id, repeticoes, 2, idoferta_ativa)
                funcoes.atualizar_h_termino()
            else:
                print("Não existem mensagens específicas ou ofertas ativas no momento.")
    except NoSuchWindowException:
        print("O processo foi encerrado durante a execução.")

    # Espera 1 minuto antes da próxima verificação
    time.sleep(60)
