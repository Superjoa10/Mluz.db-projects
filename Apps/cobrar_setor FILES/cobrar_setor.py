import csv, time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from gett_gender import form, a_form, get_contact, cobrar_dev, cobrar_form, send_email_dev, send_email_form, get_gender

def query_mluz_csv(response, cob_selec, codig, line_all, line_esp, skip__):
    line_count = []
    whatsapp_sent = []
    email_sent = []
    details = []
    start_ = time.perf_counter()   

    if response.casefold() == 'Cob_all'.casefold() or response.casefold() == 'Cob_Whatsapp'.casefold() or response.casefold() == 'continuar'.casefold():
        navegador = webdriver.Chrome()
        navegador.get("https://web.whatsapp.com/")
        while len(navegador.find_elements(By.ID, 'side')) < 1: 
            time.sleep(1)

    if response.casefold() == 'continuar'.casefold():
           Num_line = input(f'Aonde voce parou? Setor {codig} possui {line_all} casos ')  

    with open("Devedor.csv", "r", encoding="Latin-1") as file:
                csv_reader = csv.reader(file, delimiter=';')  
                for devedor in csv_reader:
                        id_dev = devedor[0]
                        nome_dev = devedor[1]
                        try:
                            cobrador = int(devedor[24])
                        except:
                              ValueError
                              cobrador = devedor[24]
                        codigo = devedor[25]
                        obs_dev = devedor[29]
                        cliente = devedor[23]
                        if cliente == '726' or cliente == '842' or cliente == '843' or cliente == '844' or cliente == '845' or cliente == '846':
                                if cob_selec == cobrador:
                                        if codig.casefold() == codigo.casefold():
                                                line_count.append(nome_dev)
                                                if response.casefold() == 'continuar'.casefold():
                                                        while int(len(line_count)) < int(Num_line):
                                                                break
                                                        else:
                                                               print(f' Estamos no caso {len(line_count)}')
                                                               response = input('Cob_whatsapp ; Cob_email ; Cob_all ?')
                                                               continue
                                                if skip__ == None:
                                                        cobs = True
                                                        pass
                                                else:
                                                        for skip_ in skip__:
                                                                while int(id_dev) != int(skip_):
                                                                        cobs = True
                                                                        break
                                                                else:
                                                                        cobs = False
                                                                        break

                                                formando = form(obs_dev)
                                                formando_append = str(str(formando) + str(f' - {nome_dev}'))
                                                forms = a_form(formando)
                                                if cobs == True:
                                                        if forms == True:
                                                                        nime_dev = nome_dev.split(" ")
                                                                        primeiro_nome_dev = nime_dev[0].capitalize()
                                                                        pronome_dev = get_gender(primeiro_nome_dev)

                                                                        nime_form = formando.split(" ")
                                                                        primeiro_nome_form = nime_form[0].capitalize()
                                                                        pronome_form = get_gender(primeiro_nome_form)

                                                                        contatos = get_contact(obs_dev, forms)
                                                                        num_dev = contatos[0]
                                                                        num_form = contatos[1]
                                                                        email_dev = contatos[2]
                                                                        email_form = contatos[3]
                                                                        print(f"""
                ################################
                id = {id_dev}
                nome = {nome_dev}
                cob = {cobrador}
                cod = {codigo}
                formando = {formando}
                numero dev: {num_dev}
                numero form: {num_form}
                email dev: {email_dev}
                email form: {email_form}

                Caso {len(line_count)}/{line_all}
                ################################""") 
                                                                        dict_withform = {'nome': nome_dev, 'forms': forms, 'num_dev': num_dev, 'num_form': num_form, 'email_dev': email_dev, 'email_form': email_form}
                                                                        if response.casefold() == 'Cob_all'.casefold():
                                                                                if num_dev == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_dev(nome_dev, num_dev, navegador, codig, pronome_dev)
                                                                                        whatsapp_sent.append(nome_dev)

                                                                                if num_form == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_form(formando, nome_dev, num_form, navegador, codig, pronome_dev, pronome_form)
                                                                                        whatsapp_sent.append(formando_append)

                                                                                if email_dev == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_dev(nome_dev, codig, email_dev, pronome_dev)
                                                                                        email_sent.append(nome_dev)

                                                                                if email_form == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_form(formando, nome_dev, codig, email_form, pronome_dev, pronome_form)
                                                                                        email_sent.append(formando_append)

                                                                                details.append(dict_withform)

                                                                        elif response.casefold() == 'Cob_whatsapp'.casefold():
                                                                                if num_dev == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_dev(nome_dev, num_dev, navegador, codig, pronome_dev)
                                                                                        whatsapp_sent.append(nome_dev)

                                                                                if num_form == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_form(formando, nome_dev, num_form, navegador, codig, pronome_dev, pronome_form)
                                                                                        whatsapp_sent.append(formando_append)

                                                                                details.append(dict_withform)

                                                                        elif response.casefold() == 'Cob_email'.casefold():
                                                                                if email_dev == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_dev(nome_dev, codig, email_dev, pronome_dev)
                                                                                        email_sent.append(nome_dev)

                                                                                if email_form == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_form(formando, nome_dev, codig, email_form, pronome_dev, pronome_form)
                                                                                        email_sent.append(formando_append)
                                                                                details.append(dict_withform)

                                                                        elif response.casefold() == 'Analise'.casefold():
                                                                                details.append(dict_withform)
                                                                                pass
                                                                
                                                        elif forms == False:
                                                                        nime = nome_dev.split(" ")
                                                                        primeiro_nome = nime[0].capitalize()
                                                                        pronome = get_gender(primeiro_nome)

                                                                        contato = get_contact(obs_dev, forms)
                                                                        numero = contato[0]
                                                                        email = contato[1]
                                                                        print(f"""
                ################################
                id = {id_dev}                                                        
                nome = {nome_dev}
                cob = {cobrador}
                cod = {codigo}
                formando = {formando}
                numero: {numero}
                email: {email}

                Caso {len(line_count)}/{line_all}
                ################################""")
                                                                        dict_noform = {'nome': nome_dev, 'forms': forms, 'num': numero, 'email': email}
                                                                        if response.casefold() == 'Cob_all'.casefold():
                                                                                if numero == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_dev(nome_dev, numero, navegador, codig, pronome)
                                                                                        whatsapp_sent.append(nome_dev)

                                                                                if email == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_dev(nome_dev, codig, email, pronome)
                                                                                        email_sent.append(nome_dev)
                                                                                details.append(dict_noform)

                                                                        elif response.casefold() == 'Cob_whatsapp'.casefold():
                                                                                if numero == None:
                                                                                        pass
                                                                                else:
                                                                                        cobrar_dev(nome_dev, numero, navegador, codig, pronome)
                                                                                        whatsapp_sent.append(nome_dev)
                                                                                details.append(dict_noform)
                                                                                
                                                                        elif response.casefold() == 'Cob_email'.casefold():
                                                                                if email == None:
                                                                                        pass
                                                                                else:
                                                                                        send_email_dev(nome_dev, codig, email, pronome)
                                                                                        email_sent.append(nome_dev)
                                                                                details.append(dict_noform)

                                                                        elif response.casefold() == 'Analise'.casefold():
                                                                                details.append(dict_noform)
                                                                                pass                                          
                                                elif cobs == False:
                                                        if forms == True:
                                                                        contatos = get_contact(obs_dev, forms)
                                                                        num_dev = contatos[0]
                                                                        num_form = contatos[1]
                                                                        email_dev = contatos[2]
                                                                        email_form = contatos[3]
                                                                        print(f"""
                ################################
                id = {id_dev}
                nome = {nome_dev}
                cob = {cobrador}
                cod = {codigo}
                formando = {formando}
                numero dev: {num_dev}
                numero form: {num_form}
                email dev: {email_dev}
                email form: {email_form}

                Caso {len(line_count)}/{line_all}
                ################################""")
                                                        elif forms == False:
                                                                        contato = get_contact(obs_dev, forms)
                                                                        numero = contato[0]
                                                                        email = contato[1]
                                                                        print(f"""
                ################################
                id = {id_dev}                                                        
                nome = {nome_dev}
                cob = {cobrador}
                cod = {codigo}
                formando = {formando}
                numero: {numero}
                email: {email}

                Caso {len(line_count)}/{line_all}
                ################################""")
                                                        input('Caso selecionado para não se cobrado, ok?')
                                                        continue


    finish_ = time.perf_counter()
    final_time = round(int(finish_- start_) / 60)
    if response.casefold() == 'Cob_all'.casefold():
        response_anal = input(f"A em total {line_esp + len(line_count)} casos, sendo {len(line_count)} casos da Millenium no setor {codig}, foram cobrados {int(len(whatsapp_sent) + len(email_sent))}, sendo {len(whatsapp_sent)} por whatsapp e {len(email_sent)} por email. Levou {final_time} minutos. Escreva \"ANALISE\" para ver os casos que não foram cobrados e porque!")
    if response.casefold() == 'Cob_Whatsapp'.casefold():
        response_anal = input(f"A em total {line_esp + len(line_count)} casos, sendo {len(line_count)} casos da Millenium no setor {codig}, foram cobrados {int(len(whatsapp_sent))} por whatsapp. Levou {final_time} minutos. Escreva \"ANALISE\" para ver os casos que não foram cobrados e porque! ")      
    if response.casefold() == 'Cob_email'.casefold():                  
        response_anal = input(f"A em total {line_esp + len(line_count)} casos, sendo {len(line_count)} casos da Millenium no setor {codig}, foram {len(email_sent)} email enviados. Levou {final_time} minutos. Escreva \"ANALISE\" para ver os casos que não foram cobrados e porque! ")
    if response.casefold() == 'Analise'.casefold():                  
        response_anal = input(f"A em total {line_esp + len(line_count)} casos, sendo {len(line_count)} casos da Millenium no setor {codig}, todos analisados. Levou {final_time} minutos. Escreva \"ANALISE\" para ver os casos que não foram cobrados e porque! ")

    if response_anal.casefold() == 'ANALISE'.casefold():
        for detail in details:
                missing_components = []
                forms_ = detail['forms']
                if forms_ == True:
                        if detail['num_dev'] == None:
                                if codig.casefold() == 'M'.casefold():
                                        pass
                                else:
                                        missing_components.append('#Numero do devedor')
                        if detail['num_form'] == None:
                                if codig.casefold() == 'M'.casefold():
                                        pass
                                else:
                                        missing_components.append('#Numero do formando')
                        if detail['email_dev'] == None:
                                        missing_components.append('#Email do devedor')
                        if detail['email_form'] == None:
                                        missing_components.append('#Email do formando')

                        if not missing_components:
                                        pass
                        else:
                              miss_comp = [_ for _ in missing_components]
                              print(f"Caso {detail['nome']}, não possui: {miss_comp} ")

                elif forms_ == False:
                        if detail['num'] == None:
                                if codig.casefold() == 'M'.casefold():
                                        pass
                                else:
                                        missing_components.append('#Numero')
                        if detail['email'] == None:
                                        missing_components.append('#Email')

                        if not missing_components:
                              pass
                        else:
                              miss_comp = [_ for _ in missing_components]
                              print(f"Caso {detail['nome']}, não possui: {miss_comp} ")
        
        
        """
        MAKE A EXCEL FILE
        response__ = input('''-------------------------------
Would you like the response on an Excel file?''')
    else:
        pass
        """   

def setor_count():
        codig = input("Qual codigo gostaria de cobrar? A, B, D ou M.  ").upper()
        cob_selec = int(input("Qual codigo do cobrador quer cobrar? "))
        line_count = 0
        line_count_all = 0
        with open("Devedor.csv", "r", encoding="Latin-1") as file:  
                csv_reader = csv.reader(file, delimiter=';')
                for devedor in csv_reader:
                    codigo = devedor[25]
                    try:
                        cobrador = int(devedor[24])
                    except:
                        ValueError
                        cobrador = devedor[24]
                    cliente = devedor[23]
                    if cliente == '726' or cliente == '842' or cliente == '843' or cliente == '844' or cliente == '845' or cliente == '846':
                        if cob_selec == cobrador:
                            if codig.casefold() == codigo.casefold():
                                    if line_count == 0:  
                                        line_count += 1   
                                    else:
                                        line_count += 1
                    else:
                        if cob_selec == cobrador:
                            if codig.casefold() == codigo.casefold():
                                if line_count_all == 0:  
                                        line_count_all += 1   
                                else:
                                        line_count_all += 1                  
        return [cob_selec, codig, line_count, line_count_all]  

def test():
        nome =  'João Victor Santos Luz'
        dev = 'Cleber Valdo Clebinho'
        setor_ = 'd'.casefold()
        while True:
                response_test_ = input('Test What?: Whatsapp; Email; All. ')
                if response_test_.casefold() in ("Whatsapp".casefold(), "Email".casefold(), "All".casefold()):
                                
                                if response_test_.casefold() == "All".casefold() or response_test_.casefold() == "Whatsapp".casefold():
                                        navegador__ = webdriver.Chrome()
                                        navegador__.get("https://web.whatsapp.com/")
                                        while len(navegador__.find_elements(By.ID, 'side')) < 1: 
                                                time.sleep(1)
                                        pass

                                if response_test_.casefold() == "All".casefold():
                                        numero_ = input('insert valid phone number with country code: ')
                                        email_receiver = input('insert valid email: ')
                                        cobrar_dev(nome, numero_, navegador__, setor_)
                                        cobrar_form(nome, dev, numero_, navegador__, setor_)
                                        send_email_dev(nome, setor_, email_receiver)
                                        send_email_form(nome, dev, setor_, email_receiver)
                                        break
                                if response_test_.casefold() == "Whatsapp".casefold():
                                        numero_ = input('insert valid phone number: ')
                                        cobrar_dev(nome, numero_, navegador__, setor_)
                                        cobrar_form(nome, dev, numero_, navegador__, setor_)
                                        break
                                if response_test_.casefold() == "email".casefold():
                                        email_receiver = input('insert valid email')
                                        send_email_dev(nome, setor_, email_receiver)
                                        send_email_form(nome, dev, setor_, email_receiver)
                                        break

                else:
                        print("Please Write a valid command!")

def skip():
       #maybe make a view to make sure its the right one
        ids_skip = []
        while True:
                response_skip = int(input('Por favor informe o id do caso que gostaria de pular. N: '))
                with open("Devedor.csv", "r", encoding="Latin-1") as file:  
                        csv_reader = csv.reader(file, delimiter=';')
                        for devedor in csv_reader:
                                try:
                                   id = int(devedor[0])
                                except ValueError:
                                   id = devedor[0]
                               
                                nome_dev = devedor[1]
                                obs = devedor[29]
                                if id == response_skip:
                                      print(f"""
id = {id}
nome = {nome_dev}""")
                                      sure = input("Seria esse o caso? S ou N ")
                                      if sure == 'S'.casefold():
                                             ids_skip.append(response_skip)
                                      elif sure == 'N'.casefold():
                                             pass
                                else:
                                      pass
                response_bruh = input('Mais algum? S ou N? ')
                if response_bruh == 'S'.casefold():
                        pass
                if response_bruh.casefold() == 'N'.casefold():
                        break
        
        print(ids_skip)
        return ids_skip
       
if __name__ == "__main__":
    print("""

                           
░█████╗░░█████╗░██████╗░██████╗░░█████╗░██████╗░  ░██████╗███████╗████████╗░█████╗░██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
██║░░╚═╝██║░░██║██████╦╝██████╔╝███████║██████╔╝  ╚█████╗░█████╗░░░░░██║░░░██║░░██║██████╔╝
██║░░██╗██║░░██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ░╚═══██╗██╔══╝░░░░░██║░░░██║░░██║██╔══██╗
╚█████╔╝╚█████╔╝██████╦╝██║░░██║██║░░██║██║░░██║  ██████╔╝███████╗░░░██║░░░╚█████╔╝██║░░██║
░╚════╝░░╚════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░╚══════╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝



Comandos:
Cob_all ; Cob_Whatsapp ; Cob_Email ; Continuar ; Analise ; Test_Func ; Ajuda.""")
    while True:
        response_command = input()
        if response_command.casefold() in ("Cob_all".casefold(), "Cob_Whatsapp".casefold(), "Cob_Email".casefold(), "Analise".casefold(), "continuar".casefold()):
                response_skip = input('Gostaria de pular algum caso? Sim ou Não ')
                if response_skip.casefold() == 'sim'.casefold():
                        skip_func = skip()
                elif response_skip.casefold() == 'não'.casefold() or response_skip == 'nao'.casefold():
                        skip_func = None
                final_num = setor_count()
                cob_selec = final_num[0]
                codig = final_num[1]
                line_all = final_num[2]
                line_esp = final_num[3]
                query_mluz_csv(response_command, cob_selec, codig, line_all, line_esp, skip_func)
                break
        elif response_command.casefold() == 'Ajuda'.casefold():
                clear = lambda: os.system('cls')
                clear()
                print("""O programa tem o intuito de cobrar os setores especificos do banco de dados da M-luz no formato CSV, 
especializando a forma que gostaria que fosse cobrado, tal como whatsapp ou email.
**Local do DB: "C:/Users/João/Desktop/agenda_files/Devedor.csv"**
____________________________________________________________________________________________________________

Funções e suas utilidades:

Cob_all:
Cobra de ambas formas, whatsapp e email. Pede o login do whatsapp antes de iniciar.

Cob_Whatsapp:
Cobra somente via whatsapp. Pede o login do whatsapp antes de iniciar.

Cob_email:
Cobra somente via Email, dependendo da forma que for adquirido o programa nescessita do
email que for enviar e uma chave especial.

Continuar:
Tem o intuito de continuar de onde parou em algum dos setores por via do numero fornecido.
Pede o login do whatsapp indepente, e assim que atinge o numero da linha solicitado o programa
pergunta quais metodos gostaria de usar para cobrar.

Analise:
Pula toda cobrança automatica para testar as funções profundas de analise,
passando pelo setor selecionado inteiro , e vendo quais casos não possuem quais tipos de contato.

Test_func:
Testa a mensagem automatica gerada, o sistema advinhador de genero e tanto o
Selenium (para whatsapp) e o Email. dependendo de como adquirir o programa nescessita da
chave do e-mail e de colocar um numero e e-mail que gostaria de enviar o teste.
____________________________________________________________________________________________________________
*Escreva alguma função*
Esse programa foi feito por Superjoa10 GITHUB: https://github.com/Superjoa10""")

        elif response_command.casefold() == 'test_func'.casefold():
                test()
                break
        else:
            print("Please Write a valid command!")
