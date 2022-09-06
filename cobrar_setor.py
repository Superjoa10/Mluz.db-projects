import openpyxl, csv, sqlite3, re, gender_guesser.detector as gender, pyautogui as gui, time
from gett_gender import get_gender, form, a_form, get_time, dev_num
#if want to add excel go after bitch
#------------------------------------------------------------------------------------------------------------
#descide which method to store contact number
#by the dev_num() takes obs and forms
with open("C:/Users/João/Desktop/Access/Devedor.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0 
            for devedor in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    horario = get_time() 
                    nome = devedor[1]
                    prim_nome = nome.split(' ')[0]
                    cobrador = devedor[24]
                    obs = devedor[29]
                    codigo = devedor[25]
                    #check for cliente
                    if cobrador == "6":
                        codig = input("Qual codigo gostaria de cobrar? A, B, D ou M").upper()
                        if codigo == codig:
                            if codig == "D":
                                formando = form(obs)
                                forms = a_form(formando)
                                if forms == True:
                                    #true é form é o mesmo
                                    # cheak for if numero == None better
                                    numero = dev_num(obs, forms)
                                    print(numero)
                                    if numero == None:
                                        break
                                    pass
                                if forms == False:
                                    numero = dev_num(obs, forms)
                                    print(numero[0], numero[1])
                                    num_dev = numero[0]
                                    if num_dev == None:
                                        continue
                                    num_form = numero[1]
                                    if num_form == None:
                                        break
                                    pass
                            if codig == "B":
                                if forms == True:
                                    #form é o mesmo
                                    pass
                                if forms == False:
                                    pass
                            if codig == "A":
                                if forms == True:
                                    #form é o mesmo
                                    pass
                                if forms == False:
                                    pass
                            if codig == "M":
                                if forms == True:
                                    #form é o mesmo
                                    pass
                                if forms == False:
                                    pass

                        pronomes_dev = get_gender(prim_nome)
                        print("--------------------------------------------------------")
                        formando = form(obs)
                        print(f"Nome:{nome}, cod cobrador:{cobrador}, formando: {formando}")
                        #NEED TO CLEAN  FORMANDO INSITE OBS, TAKE ANY BULSHIT
                        forms = a_form(formando)
                        if forms == True:
                            pronomes_form = get_gender(formando)
                            text =f"""{horario} {pronomes_form[0]}, é o Vitor, referente ao seu album de formatura em aberto com a Millenium no nome {pronomes_dev[1]} {pronomes_dev[0]}{nome}. Estamos com condição especial para quitação *SEM JUROS*.
                            Caso haja interesse em negociar para limpar o nome {pronomes_dev[1]} {prim_nome}, me retorne para que eu te passe as condições."""
                            print(f"THIS IS ITTTTTTTTTTTTTTT {text}")
                        elif forms == False:
                            text =f"""{horario} {pronomes_dev[0]} {nome}, é o Vitor, referente ao seu album de formatura em aberto com a Millenium. Estamos com condição especial para quitação *SEM JUROS*.
                            Caso haja interesse em negociar para limpar seu nome, me retorne para que eu te passe as condições."""
                            print(text)
                            
                    line_count += 1
            print(f"Total Rows: {line_count}")



