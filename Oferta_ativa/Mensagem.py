import time

#poty_mensagem = (
#   "Aproveitando o contato, gostaria de apresentar um lançamento da Piemont, chamado Poty. "
#    "Será um condomínio de alto padrão contendo 2 torres: a primeira torre com um único apartamento por andar, "
#    "e a segunda torre com dois apartamentos por andar. Este empreendimento será o último prédio a ser construído em frente ao Clube Curitibano, "
#    "e contará com um supermercado Festival a apenas 400 metros de distância."
#)
#hike_mensagem = (
#    "Gostaria de apresentar o edifício Hike, que possui uma arquitetura moderna e está localizado próximo às vias de acesso "
#    "dos principais parques de Curitiba, no Bacacheri. O condomínio oferece uma excelente estrutura de clube e uma vantagem da era moderna: "
#    "uma garagem preparada para suportar o carregamento de carros elétricos. Com todas essas qualidades, o Hike tem plantas que variam de 64.9 a 181.6m²."
#)

def saudacao():
    if time.localtime().tm_hour < 12:
        saudacao = "Bom dia"
    elif 12 <= time.localtime().tm_hour < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    return saudacao

def Mensagem(primeiro_nome, mensagem_oferta, nome_passou, Nome_corretor, Genero):
    
    BaseM = f"Meu nome é {Nome_corretor} e sou Corretor imobiliário na Prime Soho. Recentemente, você forneceu suas informações de contato em resposta a um anúncio imobiliário."

    BaseF = f"Meu nome é {Nome_corretor} e sou Corretora imobiliária na Prime Soho. Recentemente, você forneceu suas informações de contato em resposta a um anúncio imobiliário."

    neutro_p1 = (
        f"Então {primeiro_nome}, estou entrando em contato para saber se ainda está à procura de imóveis. "
        "Temos diversas opções disponíveis, tanto prontas quanto na planta, e acredito que podemos encontrar algo que atenda suas necessidades."
    )
    neutro_p2 = (
        "Caso tenha interesse, ficarei feliz em conversar para entender melhor o que está procurando e apresentar algumas opções. "
        "Estou à disposição para qualquer dúvida."
    )

    if Genero == 1:
        mensagem = f"{saudacao()}, tudo bom {primeiro_nome}?\n\n{BaseM}\n\n{neutro_p1}\n\n{neutro_p2}\n\nAguardo seu retorno."
    elif Genero == 2:
        mensagem = f"{saudacao()}, tudo bom {primeiro_nome}?\n\n{BaseF}\n\n{neutro_p1}\n\n{neutro_p2}\n\nAguardo seu retorno."
    

    #print (f"Mensagem: {mensagem}")

    return (mensagem)