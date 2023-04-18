import openpyxl, csv, sqlite3, re, gender_guesser.detector as gender, pyautogui as gui, time
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from gett_gender import form, a_form, get_contact, cobrar_dev, cobrar_form, send_email_dev, send_email_form

def query_mluz_csv(response, cob_selec, codig, line_all):
    line_count = []
    whatsapp_sent = []
    email_sent = []

    if response == 'Cob_all'.casefold() or response == 'Cob_Whatsapp'.casefold():
        navegador = webdriver.Chrome()
        navegador.get("https://web.whatsapp.com/")
        while len(navegador.find_elements(By.ID, 'side')) < 1: 
            time.sleep(1)

    with open("C:/Users/João/Python and Projects/projects/Resume.atempts/agenda_GUI/Devedor.csv", "r", encoding="Latin-1") as file:  
                csv_reader = csv.reader(file, delimiter=';')  
                for devedor in csv_reader:
                        nome_dev = devedor[1]
                        try:
                            cobrador = int(devedor[24])
                        except:
                              ValueError
                              cobrador = devedor[24]
                        codigo = devedor[25]
                        obs_dev = devedor[29]
                        if cob_selec == cobrador:
                                if codig.casefold() == codigo.casefold():
                                        line_count.append(nome_dev)
                                        formando = form(obs_dev)
                                        formando_append = str(str(formando) + str(f' - {nome_dev}'))
                                        forms = a_form(formando)
                                        if forms == True:
                                            contatos = get_contact(obs_dev, forms)
                                            num_dev = contatos[0]
                                            num_form = contatos[1]
                                            email_dev = contatos[2]
                                            email_form = contatos[3]
                                            print(f"""
################################
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
                                            if response == 'Cob_all'.casefold() or response == 'Cob_Whatsapp'.casefold():
                                                    if num_dev == None:
                                                        pass
                                                    else:
                                                        cobrar_dev(nome_dev, num_dev, navegador, codig)
                                                        whatsapp_sent.append(nome_dev)
                                                        pass
                                                    if num_form == None:
                                                        pass
                                                    else:
                                                        cobrar_form(formando, nome_dev, num_form, navegador, codig)
                                                        whatsapp_sent.append(formando_append)
                                                        pass

                                            elif response == 'Cob_all'.casefold() or response == 'Cob_email'.casefold():
                                                if email_dev == None:
                                                    pass
                                                else:
                                                    send_email_dev(nome_dev, codig, email_dev)
                                                    email_sent.append(nome_dev)
                                                    pass
                                                if email_form == None:
                                                    pass
                                                else:
                                                    send_email_form(formando, nome_dev, codig, email_form)
                                                    email_sent.append(formando_append)
                                               
                                        elif forms == False:
                                            contato = get_contact(obs_dev, forms)
                                            numero = contato[0]
                                            email = contato[1]
                                            print(f"""
################################
nome = {nome_dev}
cob = {cobrador}
cod = {codigo}
formando = {formando}
numero: {numero}
email: {email}

Caso {len(line_count)}/{line_all}
################################""")
                                            if response == 'Cob_all'.casefold() or response == 'Cob_Whatsapp'.casefold():
                                                if numero == None:
                                                    pass
                                                else:
                                                    cobrar_dev(nome_dev, numero, navegador, codig)
                                                    whatsapp_sent.append(nome_dev)
                                                    pass
                                            elif response == 'Cob_all'.casefold() or response == 'Cob_email'.casefold():
                                                if email == None:
                                                        pass
                                                else:
                                                    send_email_dev(nome_dev, codig, email)
                                                    email_sent.append(nome_dev)
                                        
    print(f"A {len(line_count)} casos no setor {codig}, foram cobrados {int(len(whatsapp_sent) + len(email_sent))}, sendo {len(whatsapp_sent)} por whatsapp e {len(email_sent)} por email.")

def setor_count():
        codig = input("Qual codigo gostaria de cobrar? A, B, D ou M.  ").upper()
        cob_selec = int(input("Qual codigo do cobrador quer cobrar? "))
        line_count= 0
        with open("C:/Users/João/Python and Projects/projects/Resume.atempts/agenda_GUI/Devedor.csv", "r", encoding="Latin-1") as file:  
                csv_reader = csv.reader(file, delimiter=';')
                for devedor in csv_reader:
                    codigo = devedor[25]
                    try:
                        cobrador = int(devedor[24])
                    except:
                        ValueError
                        cobrador = devedor[24]
                    if cob_selec == cobrador:
                            if codig.casefold() == codigo.casefold():
                                    if line_count == 0:  
                                        line_count += 1   
                                    else:
                                        line_count += 1                       
        return [cob_selec, codig, line_count]  

if __name__ == "__main__":
    print("""

                           
░█████╗░░█████╗░██████╗░██████╗░░█████╗░██████╗░  ░██████╗███████╗████████╗░█████╗░██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
██║░░╚═╝██║░░██║██████╦╝██████╔╝███████║██████╔╝  ╚█████╗░█████╗░░░░░██║░░░██║░░██║██████╔╝
██║░░██╗██║░░██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ░╚═══██╗██╔══╝░░░░░██║░░░██║░░██║██╔══██╗
╚█████╔╝╚█████╔╝██████╦╝██║░░██║██║░░██║██║░░██║  ██████╔╝███████╗░░░██║░░░╚█████╔╝██║░░██║
░╚════╝░░╚════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░╚══════╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝



Commands:
Cob_all ; Cob_Whatsapp ; Cob_Email ; Help""")
    while True:
        response_command = input()
        if response_command in ("Cob_all".casefold(), "Cob_Whatsapp".casefold(), "Cob Email".casefold()):
            final_num = setor_count()
            cob_selec = final_num[0]
            codig = final_num[1]
            line_all = final_num[2]
            query_mluz_csv(response_command, cob_selec, codig, line_all)
            break
        elif response_command == 'Help'.casefold():
             print("NEED HELP? SEARCH THE INTERNET BITCH")
        else:
            print("Please Write a valid command!")
